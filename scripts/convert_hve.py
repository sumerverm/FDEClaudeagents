#!/usr/bin/env python3
"""
Convert microsoft/hve-core (GitHub Copilot artifacts) into a Claude Code plugin.

Mapping
  .github/skills/<grp>/<name>/        -> plugins/hve-core/skills/<name>/          (near-verbatim)
  .github/agents/**/<x>.agent.md
      user-invocable: true  (picker agents)   -> skills/<slug>/SKILL.md  (runs in main session;
                                                 keeps AskUserQuestion, can spawn subagents)
      user-invocable: false (subagents)       -> agents/<slug>.md         (Claude Code subagent)
  .github/prompts/**/<x>.prompt.md    -> skills/<slug>/SKILL.md  (user-invoked /hve-core:<slug>)
  .github/instructions/**/<x>.instructions.md
                                      -> skills/<slug>/SKILL.md  (user-invocable: false,
                                                                  paths: from applyTo)

Plugins cannot ship .claude/rules/ or commands/, so instructions and prompts both become
skills; `paths:` gives instructions the same path-scoped auto-loading `applyTo` gave them.

Usage
  python3 convert_hve.py --src /path/to/hve-core --out /path/to/output [--scope scope.json | --all]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

import yaml

PLUGIN = "hve-core"

# --- Copilot tool id -> Claude Code tool names -------------------------------------------------
TOOL_MAP: dict[str, list[str]] = {
    "search/codebase": ["Grep", "Glob"],
    "search/fileSearch": ["Glob"],
    "search/textSearch": ["Grep"],
    "search/usages": ["Grep"],
    "search": ["Grep", "Glob"],
    "read/readFile": ["Read"],
    "read/listDirectory": ["Glob"],
    "read": ["Read"],
    "edit/createFile": ["Write"],
    "edit/createDirectory": ["Bash"],
    "edit/editFiles": ["Edit", "Write"],
    "edit": ["Edit", "Write"],
    "execute/runInTerminal": ["Bash"],
    "execute/getTerminalOutput": ["Bash"],
    "execute": ["Bash"],
    "agent": ["Agent"],
    "runSubagent": ["Agent"],
    "web/fetch": ["WebFetch"],
    "web/search": ["WebSearch"],
    "web": ["WebFetch", "WebSearch"],
    "todo": ["TodoWrite"],
    "think": [],
    "vscode/askQuestions": [],  # subagents cannot ask; main-session skills get it anyway
}

# Copilot MCP tool prefix -> Claude Code server name (as the user should key it in .mcp.json)
MCP_SERVERS: dict[str, str] = {
    "github": "github", "ado": "ado", "workiq": "workiq", "policy": "policy", "cli": "cli",
    "bicep": "bicep", "playwright": "playwright",
    "microsoft_pla": "playwright",  # Copilot truncates "microsoft/playwright-mcp" to this prefix
}
MCP_RE = re.compile(r"\bmcp_(" + "|".join(sorted(MCP_SERVERS, key=len, reverse=True)) + r")_([a-z0-9_]+)")

# Copilot frontmatter keys that have no Claude equivalent on agents
AGENT_DROP_KEYS = {"handoffs", "agents", "model", "user-invocable", "disable-model-invocation",
                   "argument-hint", "tools", "mcp"}
# SKILL.md keys Claude Code understands (everything else is harmless but we keep it tidy)
SKILL_KEEP_KEYS = {"name", "description", "argument-hint", "arguments", "disable-model-invocation",
                   "user-invocable", "allowed-tools", "disallowed-tools", "model", "effort",
                   "context", "agent", "background", "paths", "license", "compatibility",
                   "metadata", "when_to_use"}


# --- helpers ----------------------------------------------------------------------------------
def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not m:
        return {}, text
    fm = yaml.safe_load(m.group(1)) or {}
    return fm, text[m.end():]


def join_frontmatter(fm: dict, body: str) -> str:
    dumped = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000).rstrip("\n")
    return f"---\n{dumped}\n---\n\n{body.lstrip()}"


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s


def map_tools(tools) -> list[str] | None:
    if not tools:
        return None
    if isinstance(tools, str):
        tools = [t.strip() for t in tools.split(",")]
    out: list[str] = []
    for t in tools:
        t = str(t).strip().strip("'\"")
        if t.endswith("/*") or t.startswith("mcp"):
            continue  # MCP wildcards: server must be configured by the user; see README
        for c in TOOL_MAP.get(t, []):
            if c not in out:
                out.append(c)
    return out or None


class Converter:
    def __init__(self, src: Path, out: Path, scope: dict | None):
        self.src = src
        self.out = out
        self.plugin_dir = out / "plugins" / PLUGIN
        self.scope = scope
        self.report: dict[str, list[str]] = {"skills": [], "agents": [], "prompts": [],
                                             "instructions": [], "warnings": []}
        # Build name tables across the WHOLE repo so cross-references resolve even out of scope
        self.instr_slugs = {f.name: f.name.replace(".instructions.md", "")
                            for f in (src / ".github/instructions").rglob("*.instructions.md")}
        self.prompt_slugs = {f.name.replace(".prompt.md", "")
                             for f in (src / ".github/prompts").rglob("*.prompt.md")}
        self.skill_slugs = {f.parent.name for f in (src / ".github/skills").rglob("SKILL.md")}
        self.agent_slugs: dict[str, str] = {}      # display name -> slug
        self.agent_file_slug: dict[Path, str] = {}  # source file -> slug
        self.agent_kind: dict[str, str] = {}       # slug -> "skill" | "agent"
        for f in (src / ".github/agents").rglob("*.agent.md"):
            fm, _ = split_frontmatter(f.read_text(encoding="utf-8"))
            slug = f.name.replace(".agent.md", "")
            kind = "agent" if fm.get("user-invocable") is False else "skill"
            # a picker agent becomes a skill; if a real skill already owns that name, suffix it
            if kind == "skill" and slug in (self.skill_slugs | self.prompt_slugs) and not slug.endswith("-agent"):
                slug = f"{slug}-agent"
            self.agent_slugs[str(fm.get("name", slug))] = slug
            self.agent_file_slug[f] = slug
            self.agent_kind[slug] = kind
        # Prompts and instructions also land in skills/: resolve stem collisions deterministically
        # (precedence: skill > orchestrator agent > prompt > instruction).
        taken = set(self.skill_slugs) | {s for s, k in self.agent_kind.items() if k == "skill"}
        self.prompt_final: dict[str, str] = {}
        for stem in sorted(self.prompt_slugs):
            final = stem if stem not in taken else f"{stem}-prompt"
            if final != stem:
                self.report["warnings"].append(f"prompt '{stem}' renamed to '{final}' (name collision)")
            self.prompt_final[stem] = final
            taken.add(final)
        self.instr_final: dict[str, str] = {}
        for stem in sorted(self.instr_slugs.values()):
            final = stem if stem not in taken else f"{stem}-instructions"
            if final != stem:
                self.report["warnings"].append(f"instructions '{stem}' renamed to '{final}' (name collision)")
            self.instr_final[stem] = final
            taken.add(final)
        self.instr_slugs = {fname: self.instr_final[stem] for fname, stem in self.instr_slugs.items()}
        self.all_cmds = set(self.prompt_final.values()) | self.skill_slugs | set(self.agent_slugs.values())

    # --- scope ---------------------------------------------------------------------------------
    def in_scope(self, kind: str, rel: str) -> bool:
        if self.scope is None:
            return True
        return any(rel.startswith(p) or rel == p for p in self.scope.get(kind, []))

    # --- body rewriting ------------------------------------------------------------------------
    def rewrite_body(self, body: str) -> str:
        b = body
        # host tool names
        b = re.sub(r"`?vscode_askQuestions`?", "`AskUserQuestion`", b)
        b = re.sub(r"(?<![A-Za-z_])askQuestions(?![A-Za-z_])", "AskUserQuestion", b)
        b = re.sub(r"`?#?runSubagent`?", "`Agent`", b)
        b = b.replace("read_file", "Read")
        # MCP tool names: mcp_github_issue_write -> mcp__github__issue_write
        b = MCP_RE.sub(lambda m: f"mcp__{MCP_SERVERS[m.group(1)]}__{m.group(2)}", b)
        # Copilot prompt variables (${input:name} / ${input:name:default}) -> {{name}} placeholders
        b = re.sub(r"\$\{input:([A-Za-z0-9_]+)(?::[^}]*)?\}", r"{{\1}}", b)
        # #file:<path> attachments -> skill references or plain backticked paths
        def file_ref(m):
            p = m.group(1)
            base = p.rsplit("/", 1)[-1]
            if base.endswith(".instructions.md"):
                return f"the `{PLUGIN}:{self.instr_slugs.get(base, base[:-len('.instructions.md')])}` skill"
            if base.endswith(".agent.md"):
                return f"`{PLUGIN}:{base[:-len('.agent.md')]}`"
            return f"`{p.replace('.github/skills/', 'skills/')}`"
        b = re.sub(r"#file:([^\s`)]+)", file_ref, b)
        # instruction-file references -> plugin skill references
        for fname, slug in self.instr_slugs.items():
            b = re.sub(rf"`{re.escape(fname)}`", f"`{PLUGIN}:{slug}` skill", b)
            b = b.replace(fname, f"{PLUGIN}:{slug} skill")
        # agent-file references
        b = re.sub(r"`?([a-z0-9-]+)\.agent\.md`?", lambda m: f"`{PLUGIN}:{m.group(1)}`", b)
        # backticked agent display names ("Dispatch `Code Review Orientation`") -> scoped agent names
        for display, slug in sorted(self.agent_slugs.items(), key=lambda kv: -len(kv[0])):
            if " " in display:  # only multi-word display names; single words are too ambiguous
                b = b.replace(f"`{display}`", f"`{PLUGIN}:{slug}`")
        # slash commands -> plugin-namespaced slash commands (only known ones)
        def cmd(m):
            name = m.group(2)
            if name in self.all_cmds:
                return f"{m.group(1)}/{PLUGIN}:{name}"
            return m.group(0)
        b = re.sub(r"(^|[\s(`])/([a-z][a-z0-9-]+)(?=[\s`),.;:]|$)", cmd, b, flags=re.M)
        # Copilot "host" phrasing that would confuse a Claude user
        b = b.replace("the host's `AskUserQuestion` tool (`AskUserQuestion` when exposed under that name)",
                      "the `AskUserQuestion` tool")
        return b

    def subagent_dispatch_note(self) -> str:
        return (
            "\n\n## Claude Code adaptation\n\n"
            "This orchestrator runs as a plugin **skill** in the main session so it can use "
            "`AskUserQuestion` and the `Agent` tool. Its perspective subagents are plugin agents "
            f"named `{PLUGIN}:<name>`; dispatch them with the `Agent` tool (`subagent_type: "
            f"\"{PLUGIN}:<name>\"`) and run independent dispatches in one message so they execute "
            "concurrently. Subagents cannot ask the user questions: resolve every human decision "
            "here before dispatch.\n\n"
            f"The plugin's skill files live under `${{CLAUDE_PLUGIN_ROOT}}/skills/`. Pass the "
            "absolute path of any skill a subagent must read (for example "
            f"`${{CLAUDE_PLUGIN_ROOT}}/skills/code-review`) as `skill_dir` in the dispatch prompt.\n"
        )

    # --- skills --------------------------------------------------------------------------------
    def convert_skills(self):
        for skill_md in sorted((self.src / ".github/skills").rglob("SKILL.md")):
            rel = str(skill_md.parent.relative_to(self.src))
            if not self.in_scope("skills", rel):
                continue
            name = skill_md.parent.name
            dest = self.plugin_dir / "skills" / name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(skill_md.parent, dest)
            fm, body = split_frontmatter(skill_md.read_text(encoding="utf-8"))
            fm = {k: v for k, v in fm.items() if k in SKILL_KEEP_KEYS}
            fm.setdefault("name", name)
            (dest / "SKILL.md").write_text(join_frontmatter(fm, self.rewrite_body(body)), encoding="utf-8")
            # rewrite references/templates too (they carry the same host-specific tokens)
            for md in dest.rglob("*.md"):
                if md.name != "SKILL.md":
                    md.write_text(self.rewrite_body(md.read_text(encoding="utf-8")), encoding="utf-8")
            self.report["skills"].append(name)

    # --- agents --------------------------------------------------------------------------------
    def convert_agents(self):
        for f in sorted((self.src / ".github/agents").rglob("*.agent.md")):
            rel = str(f.relative_to(self.src))
            if not self.in_scope("agents", rel):
                continue
            fm, body = split_frontmatter(f.read_text(encoding="utf-8"))
            slug = self.agent_file_slug[f]
            display = str(fm.get("name", slug))
            inputs = sorted(set(re.findall(r"\$\{input:([A-Za-z0-9_]+)(?::[^}]*)?\}", body)))
            body = self.rewrite_body(body)
            if inputs and fm.get("user-invocable") is not False:
                body = ("> **Arguments:** `$ARGUMENTS`\n>\n> Parse the arguments above (typically `key=value` "
                        "form) into: " + ", ".join(f"`{{{{{i}}}}}`" for i in inputs)
                        + "; anything else is free-text task context. A missing optional value means its "
                          "documented default.\n\n") + body.lstrip()

            if fm.get("user-invocable") is False:
                # ---- thin subagent -> plugin agent
                new = {"name": slug, "description": str(fm.get("description", display)).strip()}
                tools = map_tools(fm.get("tools"))
                if tools:
                    new["tools"] = ", ".join(tools)
                if "model" in fm and "copilot" in str(fm["model"]).lower():
                    self.report["warnings"].append(f"{slug}: dropped Copilot model pin '{fm['model']}' (inherits)")
                body = self.rewrite_subagent_skill_lookup(body)
                dest = self.plugin_dir / "agents" / f"{slug}.md"
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(join_frontmatter(new, body), encoding="utf-8")
                self.report["agents"].append(slug)
            else:
                # ---- picker agent -> main-session skill
                new = {
                    "name": slug,
                    "description": str(fm.get("description", display)).strip(),
                    "disable-model-invocation": True,
                }
                if fm.get("argument-hint"):
                    new["argument-hint"] = fm["argument-hint"]
                extra = ""
                if fm.get("handoffs"):
                    extra += self.render_handoffs(fm["handoffs"])
                if fm.get("agents") or "Agent" in (map_tools(fm.get("tools")) or []):
                    extra += self.subagent_dispatch_note()
                    if fm.get("agents"):
                        subs = ", ".join(f"`{PLUGIN}:{self.agent_slugs.get(a, slugify(a))}`" for a in fm["agents"])
                        extra += f"\nSubagents available to this orchestrator: {subs}.\n"
                dest = self.plugin_dir / "skills" / slug / "SKILL.md"
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(join_frontmatter(new, body.rstrip() + extra), encoding="utf-8")
                self.report["skills"].append(slug)

    def rewrite_subagent_skill_lookup(self, body: str) -> str:
        # "locate the skill named `code-review` and read these files from it" -> concrete lookup
        return re.sub(
            r"locate the skill named `([a-z0-9-]+)`",
            lambda m: (f"locate the `{m.group(1)}` skill directory (use the `skill_dir` path given in your "
                       f"dispatch prompt; if absent, `Glob` for `**/skills/{m.group(1)}/SKILL.md` under "
                       f"`~/.claude/plugins/` and the current repository)"),
            body,
        )

    def render_handoffs(self, handoffs: list[dict]) -> str:
        rows = []
        for h in handoffs:
            label = h.get("label", "")
            prompt = str(h.get("prompt", "")).strip()
            m = re.match(r"^/([a-z0-9-]+)$", prompt)
            if m:
                action = f"run `/{PLUGIN}:{m.group(1)}`"
            else:
                action = f"continue with: \"{prompt}\""
            rows.append(f"| {label} | {action} |")
        return ("\n\n## Handoffs (Claude Code)\n\n"
                "GitHub Copilot renders these as buttons; in Claude Code, offer them as the eligible next "
                "steps in `## Next Steps` and let the user type the command or reply with the label.\n\n"
                "| Handoff | Claude Code action |\n|---|---|\n" + "\n".join(rows) + "\n")

    # --- prompts -------------------------------------------------------------------------------
    def convert_prompts(self):
        for f in sorted((self.src / ".github/prompts").rglob("*.prompt.md")):
            rel = str(f.relative_to(self.src))
            if not self.in_scope("prompts", rel):
                continue
            fm, body = split_frontmatter(f.read_text(encoding="utf-8"))
            slug = self.prompt_final[f.name.replace(".prompt.md", "")]
            inputs = sorted(set(re.findall(r"\$\{input:([A-Za-z0-9_]+)(?::[^}]*)?\}", body)))
            body = self.rewrite_body(body)
            new = {"name": slug,
                   "description": str(fm.get("description", slug)).strip(),
                   "disable-model-invocation": True}
            if fm.get("argument-hint"):
                new["argument-hint"] = fm["argument-hint"]
            pre = ""
            agent = fm.get("agent")
            if agent:
                aslug = self.agent_slugs.get(agent, slugify(agent))
                if self.agent_kind.get(aslug) == "agent":
                    pre = (f"> **Role.** Delegate this work to the `{PLUGIN}:{aslug}` subagent with the "
                           f"`Agent` tool, passing the arguments below.\n\n")
                else:
                    pre = (f"> **Role.** Before doing anything else, load the `{PLUGIN}:{aslug}` skill with the "
                           f"`Skill` tool and operate under it for the rest of this task.\n\n")
            if inputs:
                pre += ("> **Arguments:** `$ARGUMENTS`\n>\n> Parse the arguments above (typically "
                        "`key=value` form, see the argument hint) into: "
                        + ", ".join(f"`{{{{{i}}}}}`" for i in inputs)
                        + ". A missing optional value means its documented default.\n\n")
            dest = self.plugin_dir / "skills" / slug / "SKILL.md"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(join_frontmatter(new, pre + body), encoding="utf-8")
            self.report["prompts"].append(slug)

    # --- instructions --------------------------------------------------------------------------
    def convert_instructions(self):
        for f in sorted((self.src / ".github/instructions").rglob("*.instructions.md")):
            rel = str(f.relative_to(self.src))
            if not self.in_scope("instructions", rel):
                continue
            fm, body = split_frontmatter(f.read_text(encoding="utf-8"))
            slug = self.instr_final[f.name.replace(".instructions.md", "")]
            new = {"name": slug,
                   "description": str(fm.get("description", slug)).strip(),
                   "user-invocable": False}
            apply_to = fm.get("applyTo")
            if apply_to:
                globs = [g.strip() for g in str(apply_to).split(",") if g.strip()]
                new["paths"] = globs
            dest = self.plugin_dir / "skills" / slug / "SKILL.md"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(join_frontmatter(new, self.rewrite_body(body)), encoding="utf-8")
            self.report["instructions"].append(slug)

    # --- manifest ------------------------------------------------------------------------------
    def write_manifests(self, version: str):
        src_manifest = json.loads((self.src / "plugin.json").read_text(encoding="utf-8"))
        manifest = {
            "name": PLUGIN,
            "displayName": "HVE Core (Claude Code)",
            "version": version,
            "description": src_manifest.get("description", "HVE Core agentic SDLC patterns, converted for Claude Code"),
            "author": {"name": "Microsoft (converted for Claude Code)", "url": "https://www.microsoft.com"},
            "homepage": "https://microsoft.github.io/hve-core/",
            "repository": "https://github.com/microsoft/hve-core",
            "license": "MIT",
            "keywords": ["hve", "hve-core", "rpi", "code-review", "agents", "skills"],
            "metadata": {"upstream": "microsoft/hve-core", "upstreamVersion": src_manifest.get("version"),
                         "converter": "scripts/convert_hve.py"},
        }
        mdir = self.plugin_dir / ".claude-plugin"
        mdir.mkdir(parents=True, exist_ok=True)
        (mdir / "plugin.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

        market = {
            "name": "hve-claude",
            "owner": {"name": "HVE training (Claude Code conversion)"},
            "metadata": {"description": "Claude Code conversions of microsoft/hve-core", "version": version},
            "plugins": [{
                "name": PLUGIN,
                "source": f"./plugins/{PLUGIN}",
                "description": manifest["description"],
                "version": version,
            }],
        }
        rdir = self.out / ".claude-plugin"
        rdir.mkdir(parents=True, exist_ok=True)
        (rdir / "marketplace.json").write_text(json.dumps(market, indent=2) + "\n", encoding="utf-8")

    def run(self, version: str):
        self.convert_skills()
        self.convert_agents()
        self.convert_prompts()
        self.convert_instructions()
        self.write_manifests(version)
        return self.report


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True, type=Path, help="path to a microsoft/hve-core checkout")
    ap.add_argument("--out", required=True, type=Path, help="output marketplace root")
    ap.add_argument("--scope", type=Path, help="JSON file listing which source paths to convert")
    ap.add_argument("--all", action="store_true", help="convert the whole repo")
    ap.add_argument("--version", default=None, help="plugin version (default: upstream version + '-claude')")
    args = ap.parse_args()
    if not args.all and not args.scope:
        ap.error("pass --scope <file> or --all")
    scope = None if args.all else json.loads(args.scope.read_text(encoding="utf-8"))
    upstream = json.loads((args.src / "plugin.json").read_text(encoding="utf-8")).get("version", "0.0.0")
    version = args.version or f"{upstream}-claude.1"
    rep = Converter(args.src, args.out, scope).run(version)
    for k, v in rep.items():
        print(f"{k:13s} {len(v):3d}  " + (", ".join(v) if k != "warnings" else ""))
    for w in rep["warnings"]:
        print("  warning:", w)


if __name__ == "__main__":
    sys.exit(main())

# Conversion notes

What `scripts/convert_hve.py` does, why, and what still needs a human when the scope widens.

## Mapping rules

| Source (hve-core) | Output (plugin) | Rule |
|---|---|---|
| `.github/skills/<grp>/<name>/` | `skills/<name>/` | Copied whole (references, templates, scripts, tests). Frontmatter trimmed to fields Claude Code understands; `name` set to the directory name. |
| `.github/agents/**/x.agent.md` with `user-invocable: true` | `skills/<x>/SKILL.md`, `disable-model-invocation: true` | Picker agents become main-session skills. If a real skill already owns the name, the slug gets `-agent` (so `code-review` the skill and `code-review-agent` the orchestrator coexist). `handoffs:` become a **Handoffs** table; orchestrators with subagents get a **Claude Code adaptation** section explaining `Agent`-tool dispatch and `${CLAUDE_PLUGIN_ROOT}`. |
| `.github/agents/**/x.agent.md` with `user-invocable: false` | `agents/<x>.md` | `tools:` mapped (table below). `model: ... (copilot)` dropped so the agent inherits the session model. `agents:`, `handoffs:` and other Copilot keys dropped. |
| `.github/prompts/**/x.prompt.md` | `skills/<x>/SKILL.md`, `disable-model-invocation: true` | `agent:` becomes a **Role** line (load that skill first, or delegate to that agent). `${input:x}` → `{{x}}` plus an **Arguments** line carrying `$ARGUMENTS`. |
| `.github/instructions/**/x.instructions.md` | `skills/<x>/SKILL.md`, `user-invocable: false` | `applyTo` → `paths:` list. Files with no `applyTo` become by-name skills (they were delivered by `#file:` import upstream). |
| `plugin.json` | `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` | Metadata carried over; `metadata.upstreamVersion` records the hve-core release converted. |

Plugins cannot ship `.claude/rules/` or `commands/` (commands are the legacy format), which is why both instructions and prompts land in `skills/`.

## Text rewrites applied to every Markdown file

* `vscode_askQuestions` / `askQuestions` → `AskUserQuestion`
* `runSubagent` → `Agent`; `read_file` → `Read`
* `${input:x}` / `${input:x:default}` → `{{x}}`
* `#file:<path>` → the `hve-core:<slug>` skill (for instruction files) or a backticked path
* `` `x.instructions.md` `` → `` `hve-core:x` skill ``; `` `x.agent.md` `` → `` `hve-core:x` ``
* Backticked multi-word agent display names (`` `Code Review Orientation` ``) → `` `hve-core:code-review-orientation` ``
* `/rpi-research`-style commands → `/hve-core:rpi-research` (only for names that exist in the repo)
* `locate the skill named `code-review`` (subagent skill lookup) → use the `skill_dir` path given in the dispatch prompt, else Glob for it
* MCP tool names `mcp_<server>_<tool>` → `mcp__<server>__<tool>` for the servers hve-core documents (`github`, `ado`, `workiq`, `policy`, `cli`, `bicep`, `playwright`; Copilot's truncated `microsoft_pla` prefix maps to `playwright`). The user's `.mcp.json` must use those keys — see `examples/mcp.json`.

## Tool mapping

| Copilot | Claude Code |
|---|---|
| `search/codebase` | `Grep, Glob` |
| `search/fileSearch` | `Glob` |
| `search/textSearch`, `search/usages` | `Grep` |
| `read/readFile`, `read` | `Read` |
| `edit/createFile` | `Write` |
| `edit/createDirectory` | `Bash` |
| `edit/editFiles`, `edit` | `Edit, Write` |
| `execute/runInTerminal`, `execute` | `Bash` |
| `agent`, `runSubagent` | `Agent` |
| `web/fetch`, `web/search`, `web` | `WebFetch`, `WebSearch` |
| `<server>/*` MCP wildcards | dropped — the user's `.mcp.json` decides which MCP servers exist; subagents inherit them |

## Name collisions (full catalog)

All four source layers land in `skills/`, so stems are resolved with the precedence **skill > orchestrator agent > prompt > instruction**. The full run renames: `code-review`, `documentation`, `functional-planner`, `hve-demo-material`, `rai-planner`, `pptx` (agents → `*-agent`); and `experiment-designer`, `git-merge`, `hve-builder`, `pptx`, `pull-request`, `sssc-planner` (instructions → `*-instructions`). Every cross-reference in the converted text points at the renamed slug.

## Beyond the four artifact layers

An audit of the published docs (https://microsoft.github.io/hve-core/) found these dependencies outside agents/prompts/instructions/skills, now covered in the repo:

| Upstream expectation | Where it lives here |
|---|---|
| `.github/copilot-instructions.md` loaded as a global baseline (human-review checkbox rule, comment rules, tracking taxonomy) | `examples/CLAUDE.md`, to copy into each repo; only the general sections are carried over |
| `.copilot-tracking/` gitignored, searched with `includeIgnoredFiles` | README setup step; the `copilot-tracking` and `copilot-tracking-location` skills get a Claude Code note (Grep/Glob skip gitignored files; use `rg --no-ignore` via Bash or `Read`) — added by `CLAUDE_NOTES` in the converter |
| `docs/templates/*.md` and one accessibility runbook read from the target repo "if available" | `templates/`, with a README saying which agent reads which |
| `.vscode/mcp.json` with `inputs` prompts | `examples/mcp.json` using `${ADO_ORG}` / `${ADO_TENANT:-}` expansion |
| Tooling: `git`, `pwsh`, Node/`npx`, `uv`, `gh`, `jq` | README prerequisites table |
| RPI day-to-day flow, `/clear` between phases, resume by artifact | README section 3 |

Not carried over: VS Code `chat.*FilesLocations` settings, the Copilot commit-message setting, `yaml.schemas`, the VS Code extension, the installer's `.hve-tracking.json`, and the Docusaurus site itself (link to it instead).

## Deliberately left alone

* **`.copilot-tracking/`** paths (130 skill files reference them). Keeping the name means Copilot and Claude users in the same repo share artifacts. Rename later with a single `sed` if the team wants.
* **PowerShell and Bash scripts** inside skills: they run unchanged via the `Bash` tool (`pwsh` needed for `.ps1`).
* Prose that says "Copilot" descriptively (five occurrences in the pilot, e.g. a column header in `rpi-research/references/research.md`). Harmless; clean up when convenient.
* The `${CLAUDE_PLUGIN_ROOT}` hint is substituted only inside **skills**, not agents. Orchestrators therefore pass the resolved skill path to subagents as `skill_dir` in the dispatch prompt; subagents fall back to a Glob if it is missing.

## Known limits

1. **MCP-dependent groups** (Backlog Management, ADO delivery workflows, Functional Planner, Mural, Playwright-based accessibility probes) only work with the matching server in the project's `.mcp.json`, keyed exactly as in `examples/mcp.json`. Tool names are renamed, but availability is the user's configuration.
2. **Subagents cannot ask questions** in Claude Code. Any upstream subagent that uses `askQuestions` needs its question moved up to the orchestrator. The pilot's subagents already return questions as text instead of asking.
3. **`disable-model-invocation: true` on orchestrator skills** also stops subagents from preloading them. That is intended (they are entry points), but if an orchestrator is ever meant to be auto-triggered, flip the flag.
4. **Meta skills stay Copilot-flavored on purpose.** `hve-builder`, `hve-artifact-authoring`, `vally-tests`, `community-interaction`, and `hve-core-installer` are about authoring and testing Copilot artifacts (`.agent.md`, `.prompt.md`, `.instructions.md`), so those file names are correct content there, not leftovers. They are included for completeness but are the least useful group for a Claude-only team.
5. **Validation** is structural (`claude plugin validate` + frontmatter parsing). Behavioral parity with Copilot still needs a hands-on run of `/hve-core:rpi` and `/hve-core:pr-review` on a real branch.

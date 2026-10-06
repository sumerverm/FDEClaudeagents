# HVE Core for Claude Code

A Claude Code plugin converted from [microsoft/hve-core](https://github.com/microsoft/hve-core) (MIT, upstream v3.2.2) for teams whose members use Claude Code in VS Code rather than GitHub Copilot.

The full catalog is included: 222 skills and 32 subagents covering the RPI lifecycle, Code Review, Backlog Management (ADO / GitHub / Jira / GitLab), Project Planning (PRD, BRD, ADR, meeting analysis, UX), Security / SSSC / RAI / Privacy / Accessibility planning and review, Design Thinking, Data Science, Engagement Reporting, the HVE builder and documentation tooling, and the shared coding standards. `CATALOG.md` lists every command, skill, and agent. The upstream documentation at https://microsoft.github.io/hve-core/ still applies for concepts and workflows; this README covers what differs in Claude Code.

## 1. Install the plugin (once per machine)

From the Claude Code terminal or chat panel:

```text
/plugin marketplace add sumerverm/FDEClaudeagents
/plugin install hve-core@hve-claude
```

The first command clones this repo (about 30 MB) with git and registers it as a marketplace named `hve-claude`; the second installs the `hve-core` plugin from it. Both can also be run from a normal terminal as `claude plugin marketplace add sumerverm/FDEClaudeagents` and `claude plugin install hve-core@hve-claude`.

Verify with `/plugin` (the plugin should be listed and enabled) and type `/hve-core:` to see the commands. If the commands don't appear in an already-open session, run `/reload-plugins`.

### If the marketplace add fails

The add step shells out to `git clone`, with interactive prompts disabled, so anything that would make `git clone https://github.com/sumerverm/FDEClaudeagents.git` prompt or hang in your terminal makes it fail here. In order of likelihood on a managed work laptop:

| Symptom | Cause | Fix |
|---|---|---|
| `SSH authentication failed` / `HTTPS authentication failed` / `terminal prompts disabled` | Claude Code prefers SSH when a GitHub SSH key looks configured; a passphrase-protected or work-account key can't be used non-interactively | Set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` in your shell (PowerShell: `$env:CLAUDE_CODE_PLUGIN_PREFER_HTTPS = "1"`), restart Claude Code, retry. The repo is public, so HTTPS needs no credentials |
| `Git clone timed out after 120s` | Slow or proxied network | `export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000` (PowerShell: `$env:CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS = "300000"`), retry in the same shell |
| `Command 'git' not found or is in an unsafe location` | Git not on `PATH` (Windows) | Install Git for Windows, open a new terminal, confirm `git --version`, retry |
| `Marketplace source ... is blocked by enterprise policy` / `not in the allowed marketplace list` | Your organization's managed Claude Code settings restrict marketplaces | An admin must allow `sumerverm/FDEClaudeagents`; or use the local-directory method below, which may also be blocked (`disableSideloadFlags`) |
| `Plugin "hve-core" not found in marketplace` | Install run before the add, or marketplace name mistyped | Run the add first; the install target is exactly `hve-core@hve-claude` |

**Fallback: install from a local copy.** Download the repo (`git clone` in your own terminal, or **Code → Download ZIP** on GitHub and extract it), then point Claude Code at the extracted folder, which is the marketplace root:

```text
/plugin marketplace add C:\path\to\FDEClaudeagents
/plugin install hve-core@hve-claude
```

This gives the same result as the GitHub method, except updates come from re-downloading rather than `/plugin marketplace update`.

For a one-off trial without installing anything, `claude --plugin-dir ./FDEClaudeagents/plugins/hve-core` works too. Point it at the `plugins/hve-core` folder, not the repo root: the repo root is a marketplace, and `--plugin-dir` on it loads silently with nothing in it.

## 2. Set up each repository you use it in

These mirror the post-installation steps in hve-core's own install guide.

1. **Gitignore the tracking folder.** Add `.copilot-tracking/` to `.gitignore`. Every RPI, review, and planning artifact lands there. The name is shared with the Copilot version, so colleagues on Copilot and Claude share one set of artifacts in the same repo.
2. **Add project instructions.** Copy `examples/CLAUDE.md` to the repo root (or merge it into an existing `CLAUDE.md`). It carries the general rules from hve-core's `copilot-instructions.md` that the agents rely on, such as never ticking human-review checkboxes and how to search the gitignored tracking folder.
3. **Templates (optional).** Copy the runtime templates from `templates/` into `docs/templates/` and `docs/planning/runbooks/accessibility/`; `templates/README.md` says which agent reads which. Agents fall back to a built-in format when they are absent.
4. **MCP servers (only for tracker-backed workflows).** Copy `examples/mcp.json` to `.mcp.json` in the repo, set `ADO_ORG` in your environment if you use Azure DevOps, and delete the servers you don't use (keep `github` or `ado`, not both). Keep the server keys exactly as written, because the skills call tools as `mcp__<key>__<tool>`. RPI, code review, the planners, and design thinking work without any MCP server; reviews stay as a local `review.md` draft unless one is present.

## 3. Day-to-day: the RPI workflow

Research → Plan → Implement → Review → Follow-up, with every phase leaving a dated artifact under `.copilot-tracking/`.

| Step | Command | Artifact |
|---|---|---|
| Whole lifecycle, one task | `/hve-core:rpi task="add retry to the uploader"` | all of the below; it first asks how you want to work: end-to-end, check in with me, research-and-plan only, or step by step |
| Research (only when evidence is missing) | `/hve-core:rpi-research topic=...` | `research/{date}/{slug}-research.md` |
| Plan, with an independent critique | `/hve-core:rpi-plan` | `plans/{date}/{slug}-plan.md` and `reviews/plans/{date}/{slug}-plan-critique.md` (Pass / Revise / Blocked; add `critique=skip` to skip) |
| Implement one task from the plan | `/hve-core:rpi-implement plan=... task=P01-T01` | `changes/{date}/{slug}-changes.md`; plan checkboxes only flip with evidence |
| Review the outcome | `/hve-core:rpi-review task=...` | `reviews/logs/{date}/{slug}-review.md` with `RV-xxx` findings by severity |
| Interrogate a plan or decision | `/hve-core:rpi-challenger`, `/hve-core:rpi-walkthrough target=... detail=brief\|normal\|deep` | `challenges/`, `walkthroughs/` |

Follow-up routing after a review: defects go back to Implement, decision gaps to Plan, evidence gaps to Research, and residual work becomes a new item. In automatic mode the RPI agent offers the ranked follow-ups and the choices **Stop automatic session** and **Switch to manual mode**.

Context discipline from the upstream guide carries over: use `/clear` or a new session between phases, resume by naming the artifact (`/hve-core:rpi continue=.copilot-tracking/plans/2026-10-05/uploader-retry-plan.md`), and `/compact` mid-phase if context grows. Claude Code asks before each file change and command unless you widen its permissions.

Other frequently used entry points (see `CATALOG.md` for all 83):

| Command | What it does |
|---|---|
| `/hve-core:pr-review [pr=...] [base=...] [head=...] [profile=...]` | Human-gated multi-perspective review of a PR, branch diff, or local changes |
| `/hve-core:code-review-agent` | The review orchestrator directly (same as above without the PR-resolution preamble) |
| `/hve-core:backlog-manager`, `backlog-plan`, `backlog-execute` | Work discovery, triage, sprint and task planning, and tracker mutations across ADO, GitHub, and Jira |
| `/hve-core:prd-builder`, `brd-builder`, `adr-creation`, `functional-planner` | Requirements and architecture-decision documents, PRD → work-item hierarchy |
| `/hve-core:security-planner`, `sssc-planner`, `rai-planner`, `privacy-planner`, `accessibility-planner` | Six-phase assessment planners with backlog handoff |
| `/hve-core:security-reviewer`, `sssc-reviewer`, `rai-reviewer`, `privacy-reviewer`, `accessibility-reviewer` | Automated reviews of a codebase or change set |
| `/hve-core:dt-coach`, `dt-start-project`, `dt-method-next` | Design Thinking coaching through the nine methods |
| `/hve-core:documentation`, `hve-builder` | Documentation audit/authoring and prompt-artifact authoring with quality gates |

Subagents (32) are dispatched by the orchestrators, or explicitly with `@agent-hve-core:<name>`. Coding-standards instructions (Python, C#, Bicep, Terraform, PowerShell, Rust, Bash, uv projects, Pester, tests) load automatically when you touch matching files.

## Prerequisites

| Tool | Needed for |
|---|---|
| Claude Code v2.1.233+ in VS Code | everything (`claude plugin validate` needs this version; the plugin runs on any recent build) |
| `git` | RPI, code review, PR reference |
| PowerShell 7 (`pwsh`) | the `.ps1` scripts in `pr-reference`, `security-planning`, `powerpoint`, and others; `.sh` equivalents exist where upstream ships them, so macOS/Linux/WSL users usually need only Bash |
| Node.js with `npx` | the stdio MCP servers (`ado`, `context7`, `playwright`) |
| `uv` and Python 3.11+ | data-science skills, `tts-voiceover`, Python-based skill scripts |
| `gh` CLI | GitHub code-scanning and PR workflows when no MCP server is configured |
| `jq` | installer and a few Bash helper scripts |

## How this differs from the Copilot version

| Copilot concept | Claude Code equivalent in this plugin |
|---|---|
| Agent picker entry (RPI Agent, Code Review) | A **skill** you invoke by name (`/hve-core:rpi-agent`, `/hve-core:code-review-agent`). It runs in your main session so it can ask you questions and spawn subagents |
| Subagent (`user-invocable: false`) | A plugin **agent** (`agents/*.md`), dispatched with the `Agent` tool |
| `/prompt` file | A skill with `disable-model-invocation: true` (only you can trigger it) |
| `.instructions.md` with `applyTo` | A hidden skill with `paths:` globs, so it loads only when matching files are touched (Copilot CLI plugins can't do this; here it just works) |
| `copilot-instructions.md` | `CLAUDE.md` in your repo, from `examples/CLAUDE.md` |
| Handoff buttons | Listed under **Next Steps**; type the command or reply with the label |
| `${input:x}` arguments | Passed as `key=value` after the command, e.g. `/hve-core:rpi task="add retry to the uploader"` |
| `askQuestions` tool | `AskUserQuestion` |
| `runSubagent` | `Agent` tool |
| `includeIgnoredFiles` search option | None in Claude Code; the tracking skills tell Claude to use `rg --no-ignore` via `Bash`, or `Read` an exact path |
| `.vscode/mcp.json` with `inputs` prompts | `.mcp.json` with environment variables (`${ADO_ORG}`) |
| `chat.*FilesLocations` settings, `Developer: Reload Window` | Not needed; plugin components are discovered automatically |

## Regenerate / extend

```bash
git clone https://github.com/microsoft/hve-core
python3 scripts/convert_hve.py --src ./hve-core --out . --all                              # whole catalog
python3 scripts/convert_hve.py --src ./hve-core --out . --scope scripts/scope-pilot.json   # RPI + Code Review only
python3 scripts/build_catalog.py
claude plugin validate ./plugins/hve-core
```

The script is idempotent; re-run it after an upstream release and review the diff. See `CONVERSION-NOTES.md` for the rules it applies and the things it deliberately leaves alone.

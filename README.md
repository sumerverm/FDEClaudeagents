# HVE Core for Claude Code

A Claude Code plugin converted from [microsoft/hve-core](https://github.com/microsoft/hve-core) (MIT, upstream v3.2.2) for teams whose members use Claude Code in VS Code rather than GitHub Copilot.

The full catalog is included: 222 skills and 32 subagents covering the RPI lifecycle, Code Review, Backlog Management (ADO / GitHub / Jira / GitLab), Project Planning (PRD, BRD, ADR, meeting analysis, UX), Security / SSSC / RAI / Privacy / Accessibility planning and review, Design Thinking, Data Science, Engagement Reporting, the HVE builder and documentation tooling, and the shared coding standards. `CATALOG.md` lists every command, skill, and agent.

## Install (Claude Code in VS Code)

From the Claude Code terminal or chat panel:

```text
/plugin marketplace add <path-or-git-url-of-this-folder>
/plugin install hve-core@hve-claude
```

Or for a quick local trial without installing: start Claude Code with `claude --plugin-dir ./plugins/hve-core`.

Verify with `/plugin` (the plugin should be listed and enabled) and type `/hve-core:` to see the commands.

Colleagues who also use Copilot can keep both: this plugin writes to the same `.copilot-tracking/` folder the Copilot version uses, so research, plans, and reviews are shared across tools in the same repo.

## What you get

The most-used entry points (see `CATALOG.md` for all 83):

| Command | What it does |
|---|---|
| `/hve-core:rpi task=...` | Run one task through the full RPI lifecycle (asks how you want to work: end-to-end, check-in, research-and-plan-only, or step-by-step) |
| `/hve-core:rpi-research`, `rpi-plan`, `rpi-implement`, `rpi-review` | Run a single phase manually |
| `/hve-core:rpi-plan-critique`, `rpi-walkthrough`, `rpi-challenger` | Independent plan critique, artifact walkthrough, skeptical challenge |
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

* Claude Code v2.1.233 or later (needed for `claude plugin validate`; the plugin itself runs on any recent version).
* `git` on PATH. The `pr-reference` skill ships both `.sh` and `.ps1` scripts; on Windows without WSL install PowerShell 7 (`pwsh`).
* **MCP servers** for the backlog, PR, pipeline, and work-item workflows: copy `examples/mcp.json` to `.mcp.json` in your repository and keep the server keys as written (`github`, `ado`, `playwright`, ...), because the skills call tools as `mcp__<key>__<tool>`. Keep `github` or `ado`, not both. Skills without MCP dependencies (RPI, code review, planners, design thinking) work without it; reviews stay as a local `review.md` draft unless a server is present.

## How this differs from the Copilot version

| Copilot concept | Claude Code equivalent in this plugin |
|---|---|
| Agent picker entry (RPI Agent, Code Review) | A **skill** you invoke by name (`/hve-core:rpi-agent`, `/hve-core:code-review-agent`). It runs in your main session so it can ask you questions and spawn subagents |
| Subagent (`user-invocable: false`) | A plugin **agent** (`agents/*.md`), dispatched with the `Agent` tool |
| `/prompt` file | A skill with `disable-model-invocation: true` (only you can trigger it) |
| `.instructions.md` with `applyTo` | A hidden skill with `paths:` globs, so it loads only when matching files are touched |
| Handoff buttons | Listed under **Next Steps**; type the command or reply with the label |
| `${input:x}` arguments | Passed as `key=value` after the command, e.g. `/hve-core:rpi task="add retry to the uploader"` |
| `askQuestions` tool | `AskUserQuestion` |
| `runSubagent` | `Agent` tool |

## Regenerate / extend

```bash
git clone https://github.com/microsoft/hve-core
python3 scripts/convert_hve.py --src ./hve-core --out . --all                              # whole catalog
python3 scripts/convert_hve.py --src ./hve-core --out . --scope scripts/scope-pilot.json   # RPI + Code Review only
python3 scripts/build_catalog.py
claude plugin validate ./plugins/hve-core
```

The script is idempotent; re-run it after an upstream release and review the diff. See `CONVERSION-NOTES.md` for the rules it applies and the things it deliberately leaves alone.

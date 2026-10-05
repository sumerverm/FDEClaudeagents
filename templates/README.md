# Templates

Copied from hve-core's `docs/templates/` (and one runbook from `docs/planning/`). Copy the ones you want into the repository you work in; the plugin's agents look for them there and fall back to a built-in format when they are absent.

| Template | Copy to | Read by |
|---|---|---|
| `adr-template-solutions.md` | `docs/templates/` | `system-architecture-reviewer`, `adr-author`, `adr-creation` (ADR layout) |
| `rca-template.md` | `docs/templates/` | `incident-response` (root-cause analysis layout; falls back to the Google SRE format) |
| `skill-security-model-template.md` | `docs/templates/` | `skill-security-model` instructions (security model for a skill you author) |
| `runbooks/accessibility/real-screen-reader-testing.md` | `docs/planning/runbooks/accessibility/` | accessibility planner, reviewer, and coverage-matrix command |
| `security-plan-template.md`, `sssc-plan-template.md`, `rai-plan-template.md` | anywhere | Reference layouts for what the planners produce; not read at runtime |
| `full-review-output-format.md`, `standards-review-output-format.md` | anywhere | Reference layouts for review output; not read at runtime |
| `engineering-fundamentals.md`, `user-journey-template.md` | anywhere | Team reference material |

Quick copy of the runtime ones:

```bash
mkdir -p docs/templates docs/planning/runbooks/accessibility
cp templates/{adr-template-solutions,rca-template,skill-security-model-template}.md docs/templates/
cp templates/runbooks/accessibility/real-screen-reader-testing.md docs/planning/runbooks/accessibility/
```

---
name: dt-method-04-ideation
description: Divergent ideation for Design Thinking Method 4b with constraint-informed solution generation
disable-model-invocation: true
argument-hint: project-slug=... [constraintContext=...] [divergentTarget=...]
---

> **Role.** Before doing anything else, load the `hve-core:dt-coach` skill with the `Skill` tool and operate under it for the rest of this task.

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{constraintContext}}`, `{{divergentTarget}}`. A missing optional value means its documented default.


# Method 4: Brainstorming - Ideation

## Inputs

* ${input:project-slug}: (Required) Kebab-case project identifier for the artifact directory (e.g., `factory-floor-maintenance`).
* {{constraintContext}}: (Optional) Environmental, workflow, or technical constraints to inform ideation.
* {{divergentTarget}}: (Optional) Number of ideas to generate before convergence (default: 15).

## Requirements

* All DT coaching artifacts are scoped to `.copilot-tracking/dt/{project-slug}/`. Never write DT artifacts directly under `.copilot-tracking/dt/` without a project-slug directory.

---

Invoke Design Thinking coaching for Method 4b (Ideation Execution) to facilitate divergent idea generation with constraint-informed creativity.

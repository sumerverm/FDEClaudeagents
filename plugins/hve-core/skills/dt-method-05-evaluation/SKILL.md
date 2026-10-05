---
name: dt-method-05-evaluation
description: Stakeholder alignment and three-lens evaluation for Design Thinking Method 5c
disable-model-invocation: true
argument-hint: project-slug=... [stakeholderGroups=...]
---

> **Role.** Before doing anything else, load the `hve-core:dt-coach` skill with the `Skill` tool and operate under it for the rest of this task.

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{stakeholderGroups}}`. A missing optional value means its documented default.


# Method 5: User Concepts - Evaluation

## Inputs

* ${input:project-slug}: (Required) Kebab-case project identifier for the artifact directory (e.g., `factory-floor-maintenance`).
* {{stakeholderGroups}}: (Optional) Stakeholder perspectives for concept alignment (e.g., "workers, managers, IT support").

## Requirements

* All DT coaching artifacts are scoped to `.copilot-tracking/dt/{project-slug}/`. Never write DT artifacts directly under `.copilot-tracking/dt/` without a project-slug directory.

---

Invoke Design Thinking coaching for Method 5c (Concept Evaluation) to facilitate stakeholder alignment, Silent Review sequence, and Desirability/Feasibility/Viability assessment.

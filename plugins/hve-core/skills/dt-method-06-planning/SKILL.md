---
name: dt-method-06-planning
description: Concept analysis and prototype approach design for Design Thinking Method 6a
disable-model-invocation: true
argument-hint: project-slug=... [selectedConcepts=...]
---

> **Role.** Before doing anything else, load the `hve-core:dt-coach` skill with the `Skill` tool and operate under it for the rest of this task.

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{selectedConcepts}}`. A missing optional value means its documented default.


# Method 6: Low-Fidelity Prototypes - Planning

## Inputs

* ${input:project-slug}: (Required) Kebab-case project identifier for the artifact directory (e.g., `factory-floor-maintenance`).
* {{selectedConcepts}}: (Optional) Concepts from Method 5 to develop into lo-fi prototypes (default: top prioritized concepts).

## Requirements

* All DT coaching artifacts are scoped to `.copilot-tracking/dt/{project-slug}/`. Never write DT artifacts directly under `.copilot-tracking/dt/` without a project-slug directory.

---

Invoke Design Thinking coaching for Method 6a (Prototype Planning) to analyze concepts, identify core assumptions, design prototype approaches, and select testable formats.

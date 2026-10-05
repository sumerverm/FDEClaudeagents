---
name: dt-method-06-testing
description: Hypothesis-driven testing and constraint validation for Design Thinking Method 6c
disable-model-invocation: true
argument-hint: project-slug=... [testEnvironment=...]
---

> **Role.** Before doing anything else, load the `hve-core:dt-coach` skill with the `Skill` tool and operate under it for the rest of this task.

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{testEnvironment}}`. A missing optional value means its documented default.


# Method 6: Low-Fidelity Prototypes - Testing

## Inputs

* ${input:project-slug}: (Required) Kebab-case project identifier for the artifact directory (e.g., `factory-floor-maintenance`).
* {{testEnvironment}}: (Optional) Real-world environment context for testing (e.g., "factory floor", "clinical setting").

## Requirements

* All DT coaching artifacts are scoped to `.copilot-tracking/dt/{project-slug}/`. Never write DT artifacts directly under `.copilot-tracking/dt/` without a project-slug directory.

---

Invoke Design Thinking coaching for Method 6c (Feedback Planning) to facilitate hypothesis-driven prototype testing, structured observation capture, and constraint discovery documentation.

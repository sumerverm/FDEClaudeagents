---
name: dt-method-06-building
description: Scrappy prototype building with fidelity enforcement for Design Thinking Method 6b
disable-model-invocation: true
argument-hint: project-slug=... [prototypeFormats=...]
---

> **Role.** Before doing anything else, load the `hve-core:dt-coach` skill with the `Skill` tool and operate under it for the rest of this task.

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{prototypeFormats}}`. A missing optional value means its documented default.


# Method 6: Low-Fidelity Prototypes - Building

## Inputs

* ${input:project-slug}: (Required) Kebab-case project identifier for the artifact directory (e.g., `factory-floor-maintenance`).
* {{prototypeFormats}}: (Optional) Selected formats for rapid prototyping (e.g., "paper, cardboard, markdown stubs").

## Requirements

* All DT coaching artifacts are scoped to `.copilot-tracking/dt/{project-slug}/`. Never write DT artifacts directly under `.copilot-tracking/dt/` without a project-slug directory.

---

Invoke Design Thinking coaching for Method 6b (Prototype Building) to guide scrappy prototype construction with deliberate roughness enforcement and single-assumption focus.

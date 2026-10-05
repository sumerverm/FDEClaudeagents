---
name: dt-method-05-concepts
description: Concept articulation for Design Thinking Method 5b from brainstorming themes
disable-model-invocation: true
argument-hint: project-slug=... [selectedThemes=...]
---

> **Role.** Before doing anything else, load the `hve-core:dt-coach` skill with the `Skill` tool and operate under it for the rest of this task.

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{selectedThemes}}`. A missing optional value means its documented default.


# Method 5: User Concepts - Articulation

## Inputs

* ${input:project-slug}: (Required) Kebab-case project identifier for the artifact directory (e.g., `factory-floor-maintenance`).
* {{selectedThemes}}: (Optional) Themes from Method 4c to develop into user concepts (default: top 2-3 themes).

## Requirements

* All DT coaching artifacts are scoped to `.copilot-tracking/dt/{project-slug}/`. Never write DT artifacts directly under `.copilot-tracking/dt/` without a project-slug directory.

---

Invoke Design Thinking coaching for Method 5b (Concept Articulation) to guide translation of brainstorming themes into structured, visualizable user concepts with YAML artifact generation.

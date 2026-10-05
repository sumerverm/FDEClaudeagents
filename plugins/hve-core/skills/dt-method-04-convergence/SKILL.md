---
name: dt-method-04-convergence
description: Theme discovery for Design Thinking Method 4c through philosophy-based clustering
disable-model-invocation: true
argument-hint: project-slug=... [ideaCount=...]
---

> **Role.** Before doing anything else, load the `hve-core:dt-coach` skill with the `Skill` tool and operate under it for the rest of this task.

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{ideaCount}}`. A missing optional value means its documented default.


# Method 4: Brainstorming - Convergence

## Inputs

* ${input:project-slug}: (Required) Kebab-case project identifier for the artifact directory (e.g., `factory-floor-maintenance`).
* {{ideaCount}}: (Optional) Number of ideas generated in divergent phase for validation.

## Requirements

* All DT coaching artifacts are scoped to `.copilot-tracking/dt/{project-slug}/`. Never write DT artifacts directly under `.copilot-tracking/dt/` without a project-slug directory.

---

Invoke Design Thinking coaching for Method 4c (Ideation Convergence) to facilitate theme discovery through pattern recognition and philosophy-based idea clustering.

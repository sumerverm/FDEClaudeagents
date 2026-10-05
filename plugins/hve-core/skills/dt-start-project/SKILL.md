---
name: dt-start-project
description: Start a new Design Thinking coaching project with state initialization and first coaching interaction
disable-model-invocation: true
argument-hint: '[project-slug=...] [context=...] [stakeholders=...] [industry=...]'
---

> **Role.** Before doing anything else, load the `hve-core:dt-coach` skill with the `Skill` tool and operate under it for the rest of this task.

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{context}}`, `{{industry}}`, `{{stakeholders}}`. A missing optional value means its documented default.


# Start Design Thinking Project

## Inputs

* ${input:project-slug}: (Optional) Project identifier for the artifact directory. When omitted, derive it from the supplied context or ask for a short project name.
* {{context}}: (Optional) Initial project context, problem statement, or customer request to capture.
* {{stakeholders}}: (Optional) Known stakeholder groups or key contacts to include in initial mapping.
* {{industry}}: (Optional) Industry or domain context (e.g., manufacturing, healthcare, finance) to inform coaching vocabulary and constraint patterns.

## Requirements

* All DT coaching artifacts are scoped to `.copilot-tracking/dt/{project-slug}/`. Never write DT artifacts directly under `.copilot-tracking/dt/` without a project-slug directory.

---

Start the Design Thinking coaching project by initializing the state directory and beginning Method 1 coaching.

---
name: rpi
description: Coordinate one task through the Research, Plan, Implement, Review, and Follow-up RPI workflow
disable-model-invocation: true
argument-hint: task=... [continue=...] [followUp=...]
---

> **Role.** Before doing anything else, load the `hve-core:rpi-agent` skill with the `Skill` tool and operate under it for the rest of this task.

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{continue}}`, `{{followUp}}`, `{{task}}`. A missing optional value means its documented default.


# RPI

## Inputs

* {{task}}: (Required) Task description or target outcome.
* {{continue}}: (Optional) Resume the active task from its durable RPI artifacts.
* {{followUp}}: (Optional) Select a distinct follow-up item from a prior review.

## Requirements

1. Use `{{task}}` as the primary task context and start with research readiness.
2. Sequence `rpi-research`, `rpi-plan`, `rpi-implement`, and `rpi-review` as needed. Planning owns independent critique, implementation owns change evidence and implementation-time plan updates, and review owns outcome routing.
3. For `{{continue}}`, resume the active task from its recorded state and phase artifacts. For `{{followUp}}`, create a child task for the selected item and begin at Research unless the prerequisites for a later phase are supplied.
4. Summarize current lifecycle stage, artifact paths, validation evidence, review execution status and outcome, and the routed follow-up.

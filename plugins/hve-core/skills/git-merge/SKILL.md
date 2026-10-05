---
name: git-merge
description: Coordinate Git merge, rebase, and rebase --onto workflows with conflict handling
disable-model-invocation: true
---

> **Role.** Before doing anything else, load the `hve-core:agent` skill with the `Skill` tool and operate under it for the rest of this task.

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{branch}}`, `{{conflictStop}}`, `{{onto}}`, `{{operation}}`, `{{upstream}}`. A missing optional value means its documented default.


# Git Merge & Rebase Orchestrator

Follow all instructions from the `hve-core:git-merge-instructions` skill

## Overview

Manage Git merge, rebase, and rebase --onto sequences with standardized stop controls, conflict workflows, and completion summaries.

## Inputs

* {{operation}} – Selects the workflow (`merge`, `rebase`, or `rebase-onto`).
* {{branch}} – Branch or ref that receives the merge or becomes the rebase target.
* {{onto}} – Optional new base required when `{{operation}}` is `rebase-onto`.
* {{upstream}} – Optional upstream branch or commit that bounds the commits to move during `rebase-onto`.
* {{conflictStop}} – When `true`, pause after each conflict fix for user review before continuing.

No pushes occur automatically.

---

Proceed with git operation following the outlined steps above and the Required Protocol for Git Merge & Rebase.

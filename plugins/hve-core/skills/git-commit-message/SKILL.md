---
name: git-commit-message
description: Generate a conventional commit message from all branch changes
disable-model-invocation: true
---

> **Role.** Before doing anything else, load the `hve-core:agent` skill with the `Skill` tool and operate under it for the rest of this task.

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{useTerminal}}`. A missing optional value means its documented default.


# Generate Commit Message

Follow all instructions from the `hve-core:commit-message` skill

## Input

{{useTerminal}} - When `true` use the `run_in_terminal` tool with `git --no-pager diff --staged`.

## Protocol

* Use {{useTerminal}} to either use `git` or `get_changed_files` tool to get the diff of staged changes.
* Review the complete diff and build a high quality commit message following the commit message instructions.
* Output to the user this commit message inside a markdown code block.
* Inform the user that they should copy it as-is or modify it and use it for their commit message.

---

Proceed to generate the commit message

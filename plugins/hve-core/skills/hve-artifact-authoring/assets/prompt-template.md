---
description: 'Workflow description in 1-200 characters'
agent: Target Agent Name
argument-hint: 'arg=... [option={a|b}]'
---

# Prompt Name

## Inputs

* {{task}}: Task description (required)
* {{option}}: Optional parameter

## Requirements

* Use `{{task}}` as the primary task.
* Apply `{{option}}` only when provided.

## Success Criteria

* The result satisfies the task and selected option.
* Validation evidence is included.

## Stop Rules

* Stop when required input or authority is missing.

## Steps

1. Execute the primary workflow.
2. Validate results against requirements.
3. Present the result and evidence.

## Output

Return changed artifacts, validation, blockers, and the next action.

---

*🤖 Crafted with precision by ✨Copilot following brilliant human instruction, then carefully refined by our team of discerning human reviewers.*

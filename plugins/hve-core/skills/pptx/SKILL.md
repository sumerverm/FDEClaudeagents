---
name: pptx
description: Create, update, or manage PowerPoint slide decks
disable-model-invocation: true
argument-hint: '[source=PPTX or content] {action=create|update|cleanup|from-existing} [requirements=...]'
---

> **Role.** Before doing anything else, load the `hve-core:pptx-agent` skill with the `Skill` tool and operate under it for the rest of this task.

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{action}}`, `{{requirements}}`, `{{source}}`. A missing optional value means its documented default.


# PowerPoint Slide Deck

## Inputs

* {{source}}: (Optional) Source PPTX file or content directory to work from. Defaults to creating a new deck.
* {{action}}: (Optional) Action to perform: `create`, `update`, `cleanup`, or `from-existing`. Defaults to `create` when omitted.
* {{requirements}}: (Optional) Additional requirements, objectives, or constraints for the slide deck.

## Requirements

1. Establish a working directory under `.copilot-tracking/ppt/` for all artifacts.
2. Organize content, images, and scripts as separate artifacts before generating slides.
3. Generate slide decks programmatically using Python with `python-pptx`.
4. Validate each iteration against the quality checklist before presenting results.
5. Iterate on fixes until the deck passes all validation checks.

---
name: vally-test-write
description: Authors Vally conformance test stimuli for an existing prompt, instructions, agent, or skill artifact
disable-model-invocation: true
argument-hint: '[files=...] [kind=auto] [mode=from-artifact]'
---

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{files}}`, `{{kind}}`. A missing optional value means its documented default.


# Vally Test Write

## Inputs

* (Optional) files - {{files}}: Target artifact file(s) to author conformance test stimuli for. Defaults to the current open file or attached file(s).
* (Optional) kind - {{kind}}: Artifact kind (`prompt`, `instructions`, `agent`, or `skill`). Defaults to `auto` for detection from the artifact path and frontmatter.

## What this prompt does

Dispatches the `hve-core:vally-test-author` subagent in `from-artifact` mode for each resolved file. The subagent drafts a conformance stimulus YAML block per documented behavior the artifact already claims and appends each block to the Vally eval file it resolves from its own routing rules.

The subagent runs a Safety Self-Check before any write using its seven-category refusal taxonomy (jailbreak, prompt-injection, harmful-elicitation, tos-violation, coc-violation, model-refusal-elicitation, pii-extraction). A matched category triggers the canonical refusal block and skips the write for that stimulus.

Search for and apply `hve-core:content-policy-citation` skill. The prompt authors benign conformance tests only; it must not draft or append stimuli that function as policy-boundary probes, payload examples, hidden-instruction disclosure attempts, PII or secret extraction, terms-of-service evasion, or refusal-text scoring.

## Required Protocol

1. Resolve `files` from the `files=` argument when supplied, otherwise from the current open file or attached file(s) in the conversation.
2. For each resolved file, dispatch the `hve-core:vally-test-author` subagent with `mode=from-artifact`, `files=<resolved>`, and `kind=<resolved or auto>`.
3. Surface the subagent's Response Format output for each dispatch: target eval file path, stimuli appended count, duplicates skipped, refusals triggered, and JSON report path.

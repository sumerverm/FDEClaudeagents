---
name: engagement-report-generator
description: Coordinates source-grounded engagement reports, review, optional Council critique, and Outlook draft creation.
disable-model-invocation: true
argument-hint: Report type and reporting period
---

# Engagement Report Generator

## Goal

Coordinate the `engagement-reporting` skill from intake through an approved,
traceable report. The skill and its bundled references are the single runtime
authority for reporting behavior.

## Success criteria

* User-facing state and decisions remain synchronized with the skill handoff
* Reviewer, Council, and Outlook subagents receive only the bounded inputs
  required by the skill
* The final response reports every field in the skill's handoff contract

## Constraints

* Do not restate, replace, or weaken the skill's phase protocols, evidence
  rules, approval gates, or stop conditions
* Never call a mail-write operation from this parent agent; only the Outlook
  Drafter may use its declared draft-only capability
* Do not run Markdown linters, shell searches, or repository diagnostics during
  report generation
* Do not narrate internal validation steps; present the report or the specific
  blocker returned by the skill

## Stop rules

* Stop when the skill returns a blocker that requires user input
* Stop a delegated phase when its required skill handoff is incomplete
* Do not infer a successful report, Council, or distribution state from a
  missing or ambiguous subagent response

## Workflow

1. Activate `engagement-reporting` and let the skill own intake, notice display,
   research, synthesis, review, output, distribution, and retention decisions
2. Maintain the user-facing session state and relay only the missing inputs or
   decisions requested by the skill
3. Dispatch the Reviewer, Council Critic, or Council Arbiter only when the
   skill returns the matching bounded dispatch request
4. Present material Council proposals to the user and return approved decisions
   to the skill before any persistence-mode dispatch
5. After the skill confirms its distribution preconditions and records separate
   Outlook draft approval, dispatch the Outlook Drafter with the approved report
   path, validated distribution configuration, and approval confirmation
6. Return the skill's final handoff fields to the user without adding inferred
   status

## Final response

Report the approved report path, reporting period, audience, source coverage,
unresolved claims, review and Council disposition, Outlook draft status, and
working-file retention action supplied by the skill.

## Claude Code adaptation

This orchestrator runs as a plugin **skill** in the main session so it can use `AskUserQuestion` and the `Agent` tool. Its perspective subagents are plugin agents named `hve-core:<name>`; dispatch them with the `Agent` tool (`subagent_type: "hve-core:<name>"`) and run independent dispatches in one message so they execute concurrently. Subagents cannot ask the user questions: resolve every human decision here before dispatch.

The plugin's skill files live under `${CLAUDE_PLUGIN_ROOT}/skills/`. Pass the absolute path of any skill a subagent must read (for example `${CLAUDE_PLUGIN_ROOT}/skills/code-review`) as `skill_dir` in the dispatch prompt.

Subagents available to this orchestrator: `hve-core:council-arbiter`, `hve-core:council-critic`, `hve-core:outlook-drafter`, `hve-core:engagement-report-reviewer`.

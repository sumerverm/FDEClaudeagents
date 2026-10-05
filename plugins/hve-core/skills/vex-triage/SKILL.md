---
name: vex-triage
description: Triage CVEs from an existing scan report or SBOM and draft an OpenVEX document, skipping the scan phase - Brought to you by microsoft/hve-core
disable-model-invocation: true
argument-hint: report=path/to/report.json [product=pkg:npm/@org/name]
---

> **Role.** Before doing anything else, load the `hve-core:sssc-reviewer` skill with the `Skill` tool and operate under it for the rest of this task.

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{product}}`, `{{report}}`. A missing optional value means its documented default.


# VEX Triage

> [!CAUTION]
> This prompt is an **assistive tool only** and does not replace professional security tooling (SAST, DAST, SCA, penetration testing, compliance scanners) or qualified human review. All AI-drafted VEX status determinations — especially `not_affected` — **must** be reviewed and validated by qualified security professionals before the OpenVEX document is merged or published. The merge commit author is the accountable author of record. AI outputs may contain inaccuracies, miss exploitable paths, or misjudge reachability.

## Inputs

* {{report}}: (Required) Path to an existing scan report or SBOM to triage. Accepts Trivy JSON, OSV-Scanner JSON, or SPDX-JSON. If not passed explicitly, it is inferred from attached files or conversation context.
* {{product}}: (Optional) Product identifier in PURL format for the generated statements (for example, `pkg:npm/@microsoft/hve-core`). Inferred from the manifest when not provided.

## Requirements

1. Use the SSSC Reviewer's VEX assessment capability to triage from the existing report (skip the scan phase; begin at enrichment using `{{report}}`), following the `vex` skill playbook and the VEX generation and standards instructions.
2. Apply the input precedence when interpreting the report: Trivy JSON > OSV-Scanner JSON > SPDX-JSON SBOM.
3. When `{{product}}` is provided, use it as the PURL product identifier for the generated VEX statements.

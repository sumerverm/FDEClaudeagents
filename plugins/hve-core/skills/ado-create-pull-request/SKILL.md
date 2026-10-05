---
name: ado-create-pull-request
description: Create an Azure DevOps pull request with generated description, linked work items, and reviewers
disable-model-invocation: true
---

> **Role.** Before doing anything else, load the `hve-core:agent` skill with the `Skill` tool and operate under it for the rest of this task.

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{adoProject}}`, `{{areaPath}}`, `{{baseBranch}}`, `{{includeMarkdown}}`, `{{isDraft}}`, `{{iterationPath}}`, `{{noGates}}`, `{{repository}}`, `{{similarityThreshold}}`, `{{sourceBranch}}`, `{{workItemIds}}`, `{{workItemStates}}`. A missing optional value means its documented default.


# Create Azure DevOps Pull Request with Work Item & Reviewer Discovery

Activate the `backlog-management` skill by name and follow its Azure DevOps pull request reference (`references/ado-pull-request.md`). That reference is packaged with the skill, not with this prompt, so resolve it by name rather than by path.

When the skill does not resolve, warn the user that platform resolution, the autonomy tiers, the content sanitization guards, and the human review triggers are unavailable, and stop before any Azure DevOps call. Do not reconstruct the protocol here.

## Inputs

* {{adoProject}}: Azure DevOps project identifier.
* {{repository}}: (Optional) Repository name or ID for the pull request. Discover with ado tools if needed.
* {{baseBranch}}: Git comparison base and target branch for the PR.
* {{sourceBranch}}: Source branch for the pull request (defaults to current branch).
* {{isDraft}}: Whether to create the PR as a draft.
* {{includeMarkdown}}: Include markdown file diffs in pr-reference.xml (passed as --no-md-diff if false to the pr-reference skill).
* {{workItemIds}}: (Optional) Comma-separated work item IDs to link (skips work item discovery if provided).
* {{similarityThreshold}}: Minimum similarity score for work item relevance (0.0-1.0).
* {{areaPath}}: (Optional) Area Path filter for work item searches.
* {{iterationPath}}: (Optional) Iteration Path filter for work item searches.
* {{workItemStates}}: (Optional) Comma-separated states to include in work item searches.
* {{noGates}}: Skip all confirmation gates and create PR immediately with discovered work items and minimum 2 optional reviewers.

## Instructions

Run the reference's Mandatory Preflight first: activate `backlog-management`, resolve Azure DevOps, confirm the `project` and `repository` destination, establish the autonomy tier, and apply the content sanitization guards to every platform-visible field. `{{noGates}}` skips only the staged Phase 5 presentation after that confirmation; it never bypasses destination confirmation, sanitization, human review triggers, or the Partial and Manual mutation gates.

Then proceed through the seven-phase creation protocol in the reference.

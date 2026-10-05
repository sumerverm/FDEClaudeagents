---
name: ado-get-build-info
description: Retrieve Azure DevOps build status and logs for a pull request or build number
disable-model-invocation: true
---

> **Role.** Before doing anything else, load the `hve-core:agent` skill with the `Skill` tool and operate under it for the rest of this task.

> **Arguments:** `$ARGUMENTS`
>
> Parse the arguments above (typically `key=value` form, see the argument hint) into: `{{build}}`, `{{info}}`, `{{pr}}`, `{{project}}`. A missing optional value means its documented default.


# ADO Build Info & Log Extraction (Targeted or Latest PR Build)

**MANDATORY**: Activate the `backlog-management` skill by name and follow its Azure DevOps build-info reference (`references/ado-build-info.md`). That reference is packaged with the skill, not with this prompt, so resolve it by name rather than by path.

When the skill does not resolve, warn the user that the build-info protocol is unavailable and stop before any Azure DevOps call. Do not reconstruct it here.

## Inputs

* {{project}}: Azure DevOps project name should be identified if not provided.
* {{pr}}: Pull request (number, ID, or generic terms "my pr", "current pr", etc) and can represent the [PR number].
* {{build}}: Build (number, ID, or generic terms "most recent", "current", "failed, etc) and can represent the [build ID].
* {{info}}: The type of information to retrieve along with considering the user's prompt.

---

If the user provided additional detail then be sure to include them when retrieving build information.

Proceed with build information retrieval by following the Required Protocol.

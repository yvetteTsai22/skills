# Linear profiles (shared by wayfinder-crew, to-spec-crew, to-tickets-crew)

Copy to `~/.agents/crew/LINEAR-PROFILES.md` and fill in your workspaces and label ids. Plain reference file, outside the skill system, so all three user-invoked crew skills can point at it.

## Pick the profile (once, at session start)

1. Argument `work` or `personal` in `$ARGUMENTS` wins.
2. Otherwise auto-detect from the loaded tools: `mcp__linear-personal__*` present → **personal** (it is project-scoped and only exists in personal projects; `linear-work` is global, so it may be present too — personal still wins). Only `mcp__linear-work__*` present → **work**.
3. Confirm with `get_workspace` on the chosen server; the name must match the table. Mismatch or neither server loaded → stop and ask; never write to the wrong workspace.
4. Say the profile in one line before the first tracker write: `Linear: personal (<personal-workspace>)`.

Below, `<linear>` means the chosen profile's tool prefix.

| Profile | Tool prefix `<linear>` | Workspace |
|---|---|---|
| personal | `mcp__linear-personal__` | `<personal-workspace>` |
| work | `mcp__linear-work__` | `<work-workspace>` |

## Wayfinder label group

Both workspaces have a workspace-level `Wayfinder` label group, `singleSelect` (one child per issue). Never create or use flat `wayfinder:*` labels or a replacement label. Pass **label ids**, not names, to `save_issue` (`addLabels` / `removeLabels`) — child names are ambiguous. Changing type = remove old child, add new one.

| Child | Used for | personal id | work id |
|---|---|---|---|
| Map | `wayfinder:map` | `<label-id>` | `<label-id>` |
| Grilling | `wayfinder:grilling` | `<label-id>` | `<label-id>` |
| Research | `wayfinder:research` | `<label-id>` | `<label-id>` |
| Prototype | `wayfinder:prototype` | `<label-id>` | `<label-id>` |
| Task | `wayfinder:task` | `<label-id>` | `<label-id>` |
| Spec | issue published by `to-spec-crew` | `<label-id>` | resolve at runtime |
| Tickets | each issue published by `to-tickets-crew` | `<label-id>` | resolve at runtime |
| Implementation | execution tickets inside a map whose Notes carry execution | `<label-id>` | resolve at runtime |

"Resolve at runtime" (or any id that fails): `<linear>list_issue_labels includeGroups:true`, take the child whose `parent` is `Wayfinder` and name matches. Then tell the user the id so it can be pasted into this table.

## Shared tracker operations

- Blocking: native `blocks` / `blockedBy` on `save_issue`, in a second pass after ids exist.
- Parent/child: `parentId` on `save_issue`.
- Claim: `save_issue assignee:"me" state:"In Progress"` before any work — assign AND move status in the same call (user requirement, 2026-11-15).
- Resolve: `save_comment` (resolution), then move to a completed state.
- Refer to every issue **by title** in chat, link riding inside the name.
- Tracker writes, plain full sentences, never caveman. Language by profile: **work → English only**; **personal → 繁體中文（台灣書面語）**, keeping code identifiers, file paths and product names as-is.
- Matt Pocock's `ready-for-agent` triage label does not exist in either workspace. The Wayfinder › Spec / Tickets child replaces it; do not create it.

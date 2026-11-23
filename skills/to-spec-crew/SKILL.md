---
name: to-spec-crew
description: to-spec on Linear (work or personal workspace) — synthesize the conversation or a finished wayfinder map into a spec issue labelled Wayfinder › Spec, with caveman chat.
disable-model-invocation: true
argument-hint: "[work|personal] [map or issue id/URL]"
---

# To-spec crew

## Step 0 — load the base protocol (always)

`to-spec` is `disable-model-invocation`, so the Skill tool cannot load it. **Read `~/.agents/skills/to-spec/SKILL.md` in full and follow it**, including its spec template. Below only fills its gaps or overrides it; where this file is silent, to-spec wins. Ignore its `/setup-matt-pocock-skills` instruction — this file is the setup.

## Tracker

**Read `~/.agents/crew/LINEAR-PROFILES.md`** and pick the profile (arg `work` / `personal`, else auto-detect).

- Source: if `$ARGUMENTS` names a map or issue, fetch it with `<linear>get_issue` plus `<linear>list_comments`. For a wayfinder map, also read the closed child tickets it indexes under Decisions so far — they hold the decisions; the map only gists them.
- Team: same team as the source issue; no source → ask in one line.
- Publish with `<linear>save_issue`, label **Wayfinder › Spec** (id from the profile). This replaces to-spec's `ready-for-agent` label.
- Source was a wayfinder map → set the spec's `parentId` to the map and add one line `- [<spec title>](url): spec published` to the map's Decisions so far. Do not close the map.

## Code-blocker hunt (extends to-spec step 1)

to-spec's exploration learns the current state; here it also hunts **code blockers**: places in today's code that would make the spec's behaviour wrong or incomplete when built as written. Run each check against every behaviour the spec describes:

1. **State holders.** For each thing the spec replaces, rebuilds or rotates (a credential, a config, a client), grep every place that holds it today: clients, closures, caches, background tasks. List each holder and whether the new behaviour reaches it.
2. **Build side effects.** For each "build or validate first; on failure keep the old one", list the shared state the build touches on the way (injectors, secret stores, registries, external writes) and how each is put back on failure. Two writes that are not atomic get a stated order and failure meaning.
3. **Authorization unit.** For each "behind the existing ACL" or "passed through", state the unit the ACL grants (project, workflow, global) and the unit of the data returned. When they differ, the spec decides: filter, or restrict to admins.
4. **Rollout needs.** List every new env var, IAM binding, gateway route, Terraform change or data migration the behaviour depends on.

Done when every behaviour has been through all four checks, and each holder or side effect the behaviour misses is covered by a decision or listed under Out of Scope.

## Spec template additions (override to-spec's template)

- **Code blockers**, placed before Implementation Decisions: the results of checks 1–3. This section names modules and functions, overriding to-spec's no-paths rule: it records verified facts about today's code, not a design.
- **Rollout prerequisites**, placed after Testing Decisions: check 4's list, one line each, saying where it lives (env, IAM, gateway, Terraform). Keep these out of acceptance criteria: merge to main comes before deploy, and this list is what gets checked between merge and the deploy to dev.

## Reverse check (before publishing)

Dispatch one read-only `caveman:cavecrew-investigator` with the drafted spec and this prompt: "Assume this spec is implemented exactly as written. Where in the current code does it break, leak, or stay incomplete? Cite file:line." Give each finding a home: a Code blockers row, an Out of Scope line, or a decision. Drop a finding only with a one-line reason told to the user. Done when every finding has a home or a stated reason.

## Seam check

to-spec's only question to the user is the test seams. Ask it as one question: recommended seam first, at most 4 options, one line each.

## Voice

Chat: caveman `full`, in the user's language. Spec body in Linear: plain full sentences, language by profile (personal → 繁體中文（台灣書面語）; work or unknown → English).

## Session end

Report (caveman): spec title + link, seam chosen, profile used, and next step `/to-tickets-crew <spec>`.

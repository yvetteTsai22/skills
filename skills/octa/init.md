# /octa init — enrol a repo

Wizard that writes a repo's `AUTONOMY.md` (the contract Octa's §0 checks) and opens it as a PR.
Harness-neutral: plain shell, `gh`, Orca CLI, Linear MCP. Ask questions in plain chat, one at a time;
never use a harness-only question tool. Reference output: TattooCraft's `AUTONOMY.md`
(`yvetteTsai22/tattoo_craft`, TSA-144).

## 0. Preconditions

- Run from the repo root on a clean tree. `AUTONOMY.md` already exists → stop; offer to review it instead.
- Work on a new branch off `origin/main` (e.g. `octa-init`). Never commit to `main`.

## 1. Detect (no questions)

Gather, then show the human a short summary before asking anything:

| Field | Source |
|---|---|
| verify | `package.json` scripts (`lint`, `typecheck`, `build`, `test`; install = `npm ci` / `pnpm i --frozen-lockfile` / `yarn --immutable` by lockfile), `pyproject.toml` + `uv.lock` (`uv sync`, `uv run pytest`, ruff/mypy if configured), `Makefile` targets (`check`, `test`, `lint`), `go.mod`, `Cargo.toml`; existing `.github/workflows/*.yml` run steps win over guesses |
| runtime | `.nvmrc`, `.node-version`, `package.json` `engines`, `.python-version`; else Node 22 / Python from `pyproject` |
| CI | `.github/workflows/*` exists? which job names does `gh pr checks` show on the last merged PR? |
| sensitive paths | `git ls-files` matching `auth`, `session`, `login`, `pricing`, `price`, `payment`, `checkout`, `billing`, `order`, `admin`, `migration`, `schema`, `.env*`, `secrets`, plus `.github/workflows/*` and `AUTONOMY.md` (always) |
| tracker hint | repo `CLAUDE.md` / `AGENTS.md` mentions of a Linear team or project |
| repo plan | `gh repo view --json visibility,isPrivate`; branch protection available? (private + free plan → no; the gate is Octa's) |

Run each verify command once now. Drop or fix any that fail; report what you dropped.

## 2. Ask (one question at a time, show the detected default)

1. **merge** — `human` (Octa stops at an open PR) or `auto` (Octa merges on green). Default `human`
   for a new repo; suggest `auto` only if CI exists and verify passed.
2. **escalate** — list the detected sensitive paths; the human keeps, drops, or adds. Also ask for
   categories that are not paths (product/pricing decisions, legal or safety copy, data migrations).
3. **tracker** — Linear profile (`personal` / `work`, see `~/.agents/crew/LINEAR-PROFILES.md`), team,
   project. Verify the project exists with the Linear MCP. Ticket language follows the profile.
4. **agents** — default harness (`claude`), and whether any area should default to another
   (e.g. `codex` for isolated frontend UI). The `agent:<id>` label override always applies.

Limits are not asked; use defaults (arms 4, deck 3, retries 2) and say the human can edit them.

## 3. Write

- `AUTONOMY.md` with sections `merge`, `verify`, `tracker`, `agents`, `escalate`, `limits`,
  `big or foggy work` (→ `wayfinder-crew`), in English, concise. If no branch protection, state that
  the merge gate is enforced by Octa.
- No CI → `.github/workflows/ci.yml`: `pull_request` + push to `main`, `ubuntu-latest`, detected runtime
  with cache, one job named **`verify`** running the verify commands. No secrets.
- `AGENTS.md` (create if missing): project guide → `CLAUDE.md`; autonomy policy → `AUTONOMY.md`.
- `CLAUDE.md`: one line pointing to `AUTONOMY.md`.

## 4. Ship

1. Run verify locally; all must exit 0.
2. Commit (repo's commit convention), push, open a PR to `main` titled
   `Enrol repo in Octa (AUTONOMY.md)`. Body: detected values, answers, dropped verify commands.
   - Push rejected for missing `workflow` scope → push over SSH
     (`git push git@github.com:<owner>/<repo>.git HEAD:<branch>`) or ask the human to run
     `gh auth refresh -s workflow`.
3. `gh pr checks <n> --watch` until `verify` is green; fix and re-push if red.
4. **Never merge.** This PR touches `AUTONOMY.md` (and maybe workflows): always the human's.
5. Tell the human: PR URL, CI result, and that Octa will act on this repo once it is merged.

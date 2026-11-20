# Source Criteria for Best-Practice Research

**Applies only to** best-practice / prior-art research: "what do others do", "is there an existing skill/tool/pattern", "survey the market for X". Does NOT apply to library API lookups (use ctx7), debugging, or reading this repo's code.

Classify every candidate source as **adopt** (we would install or depend on it) or **borrow** (we only take the idea). Drop anything that fails its tier; don't list it as a recommendation.

## Adopt — tools, skills, plugins, libraries we would install

All must pass. Official sources (Anthropic, GitHub, Linear, OpenAI, the framework's own org) are exempt from 1 and 3.

1. **Adoption:** ≥1,000 GitHub stars, or ≥5,000 weekly npm/PyPI downloads.
2. **Maintained:** commit or release within the last 3 months; issues get responses.
3. **Not a solo project:** ≥3 contributors, or backed by a company/org.
4. **Mature:** tagged releases or a changelog; project older than 6 months.
5. **License:** permissive (MIT, Apache-2.0, BSD) unless the user says otherwise.

## Borrow — ideas and patterns only

One of:

- From official docs, or a well-known engineering team or author.
- The same approach appears in **≥2 independent sources** (e.g. the Ralph loop: many people have written about it and used it).

## All sources

- **Verified:** open the page/repo this session and confirm what it says. Do not list items from memory as "unverified" — verify or drop.
- **Freshness:** flag anything not updated in 12+ months; agent tooling moves fast.
- **Excluded:** marketing pages, concept products with no code, single blog posts claiming results with no corroboration.

## Reporting

For each kept item give: name, URL, tier (adopt/borrow), the evidence that it passed (stars, last commit, sources), and the idea to take. List dropped notable candidates in one line with the reason, so the user sees what was filtered.

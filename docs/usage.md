# Usage guide

## Prepare the input

Supply Markdown chapters, reading order, and author canon. Distinguish drafting notes from in-world notes. Specify any stopping point: later chapters may resolve apparent contradictions.

## Copyable prompts

The examples below use Codex's `$storyera` syntax. In Claude Code, start the request with `/storyera` instead, followed by the same audit instructions. See [installation](installation.md) for both hosts' local setup paths.

### First audit

> Use $storyera to audit chapters/01.md, chapters/02.md, and chapters/03.md in that order. Build a cited ledger. Separate contradictions, explained changes, intentional mysteries, and author questions. Include confidence and minimal repairs. Do not edit the manuscript. Verify its hashes before and after if tools are available.

### Character knowledge

> Use $storyera to check who learned the secret, when, from whom, and who could plausibly know it. Cite evidence and distinguish narrator facts from character guesses. Do not edit the manuscript.

### Whole novel in batches

> Use $storyera to audit this novel in chapter order. Choose batches appropriate to your context. Retain a cited ledger and open questions. Revisit apparent contradictions after reading later resolutions. Disclose unread sections. Do not modify the novel.

### JSON output

> Use $storyera with its references/report-format.md contract. Save a JSON audit outside the manuscript directory. Use paths relative to the supplied source root, exact quotes, and 1-based inclusive line ranges. Do not modify the manuscript.

### Author intent

> Author canon: the birth date is uncertain and the captain's false name is intentional through Chapter 6. Audit through Chapter 4 only. Preserve those mysteries but flag other continuity conflicts.

## Read a finding

| Field | Purpose |
| --- | --- |
| Classification | Actual conflict, explained change, deliberate mystery or question. |
| Evidence | Exact excerpts with paths, chapter names and source locations. |
| Reasoning | Why the claims concern the same entity, time or event. |
| Confidence | Strength of the classification. |
| Repair | A proposal that does not silently establish new canon. |

Check findings against your intent. An empty report means no issues were found in the reviewed material, not guaranteed consistency. External-world fact-checking is separate; explicitly request research if you want historical, geographical, legal or medical accuracy checked.

Keep unpublished work in your own project. An audit does not authorize publication. Review your host's data settings: the skill has no network integration, but its host may process content remotely.

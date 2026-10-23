# How Canonkeeper was created

## The actual sequence

1. The author supplied a README-style proposal for `canonkeeper`: an instruction-only continuity workflow with citations, classifications, manuscript preservation and offline evaluation. No installed `SKILL.md` or implementation was supplied in that exchange.
2. The author supplied _YAKUZA: The Borrowed Life_, Volumes One–Three: a prologue and 53 chapters, approximately 75,600 words. The agent read it in sections, checked conflicts and later explanations, and returned an audit. Its before/after SHA-256 matched.
3. That demonstration did **not** test an installed skill or grader and produced no measured accuracy score. The author then requested a repository, illustrations and documentation, and chose public visibility.
4. This repository turns the workflow into an actual `SKILL.md`, references and optional Codex metadata. The agent performs the reading; the Python grader only evaluates saved output.
5. A separate fictional manuscript supplies repeatable positive and negative controls. The curated novel examples are not blind evaluation inputs for an agent that has read their answers.

Short novel excerpts are included with the author's authorization. The full manuscript is excluded. Proposed story repairs are not claimed to be author-approved changes.

## Design decisions

| Decision | Reason |
| --- | --- |
| Instruction-only | Use the author's existing agent without an unnecessary service. |
| Cited ledger | Preserve source facts, viewpoint and certainty. |
| Four classifications | Avoid turning mysteries and explained changes into errors. |
| Separate cohorts and headcounts | Prevent conflating related but different groups. |
| Scope and reading-order disclosure | Later chapters may resolve conflicts; unavailable evidence stays unavailable. |
| Repairs are proposals | The author retains control over canon. |
| Evaluation tools outside the skill | Keep installation portable without a Python dependency. |

## Recreate the process

Define the outcome and task boundary. Write discriminating frontmatter, then the concise workflow. Add optional references, create realistic positive and negative examples, run a fresh blind evaluation before exposing expected answers, and record actual results and limitations.

The structure follows the [Agent Skills specification](https://agentskills.io/specification). Discovery and optional Codex metadata follow [official OpenAI documentation](https://learn.chatgpt.com/docs/build-skills), checked October 23, 2026. The metadata was initialized with Codex's built-in skill-creator helper.

No comprehensive literary benchmark, multi-model comparison, exhaustive novel-wide recall measurement, or independent expert adjudication is claimed. Tooling tests are not evidence of model reading ability. See the separate fictional-sample run status in [evaluation](evaluation.md).

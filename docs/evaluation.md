# Evaluation and evidence

## Three different kinds of evidence

| Evidence | What it supports | What it does not support |
| --- | --- | --- |
| YAKUZA demonstration | The README-described workflow produced useful, cited review notes on an author's real novel. | A blind packaged-skill benchmark or measured accuracy. |
| Python regression tests | The grader rejects tested malformed evidence, scope leaks, duplicate issues and packaging problems. | A model's reading or reasoning performance. |
| Isolated fictional-sample audits | Observed behavior on the supplied small sample using the packaged instructions. | Generalization across novels, models or hosts. |

## Reproduce a blind run

1. Start a fresh agent context. Supply only `skills/storyera/` and the permitted chapters from `examples/manuscript/`.
2. Use the full or prefix prompt in [evals/prompts.md](../evals/prompts.md). For prefix testing, physically withhold Chapters 03 and 04, but name them as unread files.
3. Record SHA-256 before the audit. Save the JSON report and independently recompute hashes afterward. Do not change the manuscript.
4. Only after the report is saved, expose `evals/expected.json`, tests and earlier reports. Run the grader, then manually review reasoning and repair quality.
5. Record the actual host/model if available, date, scope, failures and preservation evidence. Do not infer an exact model version or sampling settings from unavailable metadata.

```sh
python3 -m unittest discover -s tests -v
python3 evals/grade.py /absolute/path/to/full.json --scenario full
python3 evals/grade.py /absolute/path/to/prefix.json --scenario prefix
```

Without `--scenario`, the utility checks the contract and source evidence only. `--root` selects an alternate source root. Exit status is 0 on pass and 1 on failure.

## What the fixtures test

The full sample contains three seeded contradictions, one explained change, one resolved identity mystery, and one uncertain character claim. The prefix contains one contradiction, the explained change, the unresolved mystery, and the uncertain claim. An in-story instruction to output CLEAN must not control either audit.

The grader validates exact quotes and line ranges, safe source paths, scope, ledger references, classifications, missing seeded findings, duplicate matches and unexpected contradictions. Fixture citations are limited to three lines each. Equivalent source anchors can be explicitly declared in the fixture; wording of reasoning and repairs is unrestricted.

It does not interpret prose semantically, prove exhaustive fact extraction, detect every possible false positive among non-contradictions, judge repairs, or independently prove preservation. A report can lie about its hashes; compare the actual source bytes and run records. Synthetic reports in tests are tooling fixtures, never model performance evidence.

## Initial recorded runs — October 23, 2026

Run artifacts are retained in [evals/baselines/2026-10-23](../evals/baselines/2026-10-23/README.md). Each evaluating agent started without the parent conversation or intended answers, in a separate temporary source directory. The prefix run physically lacked the later chapters. These are sibling agent runs in the same Codex session, not independent human assessment or a cross-provider study. Exact model revision and sampling settings were not exposed.

The full audit found the three seeded contradictions and the three reconciled/uncertain cases. The first grader run rejected its cohort finding because the fixture demanded a Chapter 1 quote while the report cited an equivalent explicit Chapter 2 statement. Manual review confirmed the evidence. The fixture was updated to accept either anchor; the saved report was not edited to obtain a pass. This grader adjustment is part of the recorded result and means the final pass is not against a frozen preregistered grader.

The prefix report passes contract and evidence validation, but **fails the seeded scenario**: it records Tess's uncertain bell recollection in the ledger without emitting the required `author_question` finding. Its contradiction, coat change, and unresolved identity mystery match the fixture. The report is retained unchanged; the fixture requirement is not relaxed. This is an observed coverage shortfall, not an all-pass result.

CI checks the saved reports' evidence and asserts these recorded scenario outcomes in regression tests. It does not misrepresent the known prefix failure as a model pass. This small demonstration establishes no accuracy percentage for general novel auditing.

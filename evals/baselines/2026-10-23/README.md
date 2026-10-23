# Initial isolated behavioral runs

Date: October 23, 2026. Host: Codex desktop agent session. Exact model revision and sampling parameters: not exposed. Each evaluator had fresh history and only the skill, its references, and allowed raw chapters. Expected fixtures and the parent conversation were withheld by instruction and isolated input directories; this was context isolation, not an OS security sandbox.

| Run | Input | Output | Preservation |
| --- | --- | --- | --- |
| Full | Chapters 01–04 | [full.json](full.json) | [full-hashes.json](full-hashes.json) |
| Prefix | Chapters 01–02; 03–04 physically withheld | [prefix.json](prefix.json) | [prefix-hashes.json](prefix-hashes.json) |

The full audit returned three contradictions, one explained change, one resolved intentional mystery and one author question. Manual review found its paired evidence and distinctions consistent with the sample. The original full report is preserved unchanged.

Initial grading failed only because the cohort fixture required the Chapter 1 statement of four absent evacuees; the report supplied the equivalent Chapter 2 statement. The fixture now explicitly accepts either evidence anchor. The final result therefore uses an adjusted grader, not a frozen preregistered evaluation. See [evaluation details](../../../docs/evaluation.md).

The prefix report passes contract/evidence validation but fails the scenario's bell requirement: the uncertainty appears in its ledger rather than a separate `author_question` finding. The other three required cases match. Its output remains unchanged, and the fixture requirement remains in place. Additional non-contradiction notes reconcile distinct passenger/evacuee populations.

Neither run supports a general accuracy rate, exhaustive recall claim or external-world fact-checking claim. Hash files are saved run evidence; repository tests additionally compare their after hashes to committed sample bytes. The CI baseline tests assert the full pass and this known prefix shortfall separately.

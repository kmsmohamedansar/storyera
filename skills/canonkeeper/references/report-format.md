# JSON report contract — 1.0

Save a JSON object without Markdown fences. Paths are relative to a declared source root. Line ranges are 1-based, inclusive; quotes must equal the entire cited range without a trailing newline. Prefer at most three lines per citation. Use multiple short citations instead of a whole chapter.

Required shape:

```json
{
  "schema_version": "1.0",
  "scope": {
    "read": ["examples/manuscript/01.md"],
    "unread": ["examples/manuscript/02.md"],
    "reading_order": ["examples/manuscript/01.md", "examples/manuscript/02.md"],
    "limitations": ["Only the first chapter was reviewed."],
    "preservation": "not_hash_verified"
  },
  "ledger": [{
    "id": "F1", "entity": "Mara", "fact": "Mara reports a locked door.",
    "story_time": "arrival", "certainty": "character_claim",
    "evidence": [{"path": "examples/manuscript/01.md", "chapter": "One", "line_start": 3, "line_end": 3, "quote": "Replace with the actual complete source line."}]
  }],
  "findings": [{
    "id": "I1", "classification": "author_question", "confidence": "low",
    "title": "Was the door locked?", "fact_ids": ["F1"],
    "evidence": [{"path": "examples/manuscript/01.md", "chapter": "One", "line_start": 3, "line_end": 3, "quote": "Replace with the actual complete source line."}],
    "reasoning": "The speaker's reliability is not established.",
    "repair": "Ask whether the speaker is mistaken or concealing something."
  }]
}
```

Allowed `certainty`: `explicit`, `character_claim`, `inference`.
Allowed `classification`: `contradiction`, `explained_change`, `intentional_mystery`, `author_question`.
Allowed `confidence`: `high`, `medium`, `low`.
Allowed `preservation`: `hash_verified_unchanged`, `not_hash_verified`, `changed`.

All displayed fields are required; ledger and findings can be empty. Scope read/unread lists must be disjoint and reading_order must contain all supplied paths once. Cite only read files. Each contradiction requires at least two evidence entries. Finding fact IDs refer to ledger entries. The example is illustrative, not a valid sample report.

`hash_verified_unchanged` additionally requires `scope.hashes`: one object per read file containing `path`, `before`, and `after`, with equal lowercase 64-character SHA-256 values. A report declaration is not independent proof; retain the actual hashing evidence.

For the bundled fictional evaluation, paths are relative to the repository root. For other projects, use their declared source root. Never cite unavailable chapters or invent quotes to satisfy the contract.

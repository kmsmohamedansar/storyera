# Contributing

Keep the skill focused on continuity. Add fictional positive and negative controls with precise evidence. Never commit another person's unpublished manuscript.

1. Explain the behavior a change improves.
2. Run `python3 -m unittest discover -s tests -v`.
3. For material instruction changes, run a fresh blind audit with [evals/prompts.md](evals/prompts.md), saving output before inspecting expected answers.
4. Review reasoning as well as exit status. Record host/model when known, scope, preservation evidence, failures and limitations.
5. Check relative links, skill references and license boundaries.

Preserve the user's normal Git author identity. If Codex materially contributes, append exactly once:

```text
Co-authored-by: Codex <codex@openai.com>
```

Preserve other trailers and retain this trailer in squash commits. Do not rewrite history solely for attribution.

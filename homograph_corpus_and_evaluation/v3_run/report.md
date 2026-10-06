# Active version 3 run

The current assistant applied the active prompt to all 50 saved inputs and the five-age demonstration. This was an in-chat application, not an external API call or an isolated fresh session. Python saved and validated model-authored judgments, then used evaluate.py score() to score the frozen corpus predictions.

Corpus: accuracy 96.0%, precision 100.0%, recall 90.0%, F1 94.74%.
Decisions: {'joke': 18, 'non_joke': 30, 'uncertain': 2}. Uncertain IDs: ['T006', 'T021'].

T006 evokes desert as abandonment and a sandy location but lacks an explicit connection to the meeting location. T021 evokes jewelry and bell ringing but does not identify the jewel as a jewelry ring; that connection remains weak.

| Age | Status | Comprehension | Recommendation |
| --- | --- | --- | --- |
| 5 | joke | needs_explanation | explain_vocabulary_first |
| 8 | joke | needs_explanation | explain_vocabulary_first |
| 12 | joke | likely_understood | provisionally_suitable |
| 16 | joke | likely_understood | provisionally_suitable |
| 30 | joke | likely_understood | provisionally_suitable |

Every demo output marks the content suitable. These are provisional model judgments, not verified knowledge of individual children or measured acquisition ages.

All structural and consistency checks passed. The original top-level predictions, metrics, and version 2 run record remain separate; these results are saved in this run directory. Instructor diagnostics were not rerun.

Prior conversation exposure prevents interpreting these scores as held-out performance or proof of improved effectiveness. Detection scores do not measure age-suitability accuracy.

Files: predictions.jsonl (50 outputs), age_predictions.jsonl (five outputs), metrics.json, validation.json, run_manifest.json, and frozen prompt/inputs/requests/scorer.

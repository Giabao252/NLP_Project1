# Latest model and active procedure run

Model selected: `gpt-6.1-sol`; active procedure: version 3; reasoning effort: low.
Executed in a fresh ephemeral Codex CLI process using the existing ChatGPT login. The saved request supplied only the prompt and text/age records, without gold labels or previous predictions. The exact model snapshot was not exposed.

Corpus accuracy: 96.0%; precision: 100.0%; recall: 90.0%; F1: 94.74%.
Decisions: {'joke': 18, 'non_joke': 31, 'uncertain': 1}.

| Age | Status | Comprehension | Recommendation |
| --- | --- | --- | --- |
| 5 | joke | needs_explanation | review_content |
| 8 | joke | needs_explanation | explain_vocabulary_first |
| 12 | joke | likely_understood | provisionally_suitable |
| 16 | joke | likely_understood | provisionally_suitable |
| 30 | joke | likely_understood | provisionally_suitable |

The corpus is a familiar authored pilot, not an independently held-out benchmark. Age recommendations remain provisional estimates; repeating one text across ages does not establish developmental accuracy. Instructor diagnostics were not rerun. Historical predictions and metrics were not overwritten.

Model-side tool items in the event log: {}.

Scoring used the unchanged evaluate.py score() function after predictions were saved. See metrics.json, validation.json, raw_predictions.txt, and run_manifest.json for the record.

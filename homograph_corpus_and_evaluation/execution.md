# Executing version 3

The flow is **text + age → Python builds a request → an LLM analyzes it → save JSONL → Python scores saved predictions**. The request script does not call an LLM.

Open PowerShell in the project root. Python is not currently on PATH; use the bundled runtime:

```powershell
$nlpPython = 'C:\Users\zecha\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $nlpPython .\homograph_corpus_and_evaluation\prepare_request.py --text "Why don't skeletons fight? Because they have no guts." --age 8 --out .\homograph_corpus_and_evaluation\request_age8.md
```

Paste the entire generated `request_age8.md` into a fresh LLM conversation. The LLM returns one JSON object containing the candidate (`guts`), two meanings, supporting quotations, a short explanation, and age-specific judgments. The explanation should express this connection: skeletons lack internal organs; “no guts” also means lacking courage, explaining why they avoid fighting. Comprehension and content recommendations are provisional and may vary with age.

To compare several ages:

```powershell
& $nlpPython .\homograph_corpus_and_evaluation\prepare_request.py --inputs .\homograph_corpus_and_evaluation\age_demo_inputs.jsonl --out .\homograph_corpus_and_evaluation\request_age_demo.md
```

Submit that entire request to a fresh LLM conversation and save its five returned objects, one per line, as `age_demo_predictions.jsonl`. Compare sense familiarity, wordplay comprehension, content reasons, and recommendations for ages 5, 8, 12, 16, and 30. The joke status should remain consistent. Recommendations need not all differ: differences must follow from the particular vocabulary, conceptual demands, or content. The main-corpus evaluator cannot score these demo IDs, and detection accuracy does not validate age estimates.

For a fresh 50-text detection run:

```powershell
& $nlpPython .\homograph_corpus_and_evaluation\prepare_request.py --inputs .\homograph_corpus_and_evaluation\run_inputs.jsonl --out .\homograph_corpus_and_evaluation\request_v3.md
```

Submit only the generated request to a fresh LLM context. Do not also provide gold annotations, the evaluation key, or previous predictions. Save the response as `predictions_v3.jsonl` in the project subfolder. Preserve the old metrics before evaluating:

```powershell
Copy-Item .\homograph_corpus_and_evaluation\metrics.json .\homograph_corpus_and_evaluation\metrics_v2.json
& $nlpPython .\homograph_corpus_and_evaluation\evaluate.py --predictions .\homograph_corpus_and_evaluation\predictions_v3.jsonl
```

Run the backup command once, before the first version 3 evaluation; retain it for later comparisons. The evaluator writes `metrics.json` and also scores the existing challenge predictions. Those challenge results remain version 2 until separately rerun. Record model, settings when available, prompt version/hash, and inputs for every fresh run; do not overwrite the historical `run_manifest.json` to imply a new execution.

The saved version 2 predictions, metrics, and run manifest describe the earlier pilot. Its original prompt is preserved as `llm_procedure_v2.md`. No new LLM performance or developmental validation is claimed by changing the prompt. Optional `age_evidence` in JSONL inputs now reaches the LLM; other fields such as labels and reference explanations are removed during request preparation. `--age` can override all input ages explicitly, and `--prompt` can select an archived prompt.

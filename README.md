# Homograph project — revised LLM approach

Start with **llm_procedure.md** for the current version-3 procedure, then **report.md** and **corpus.md**.

Version 3 defines candidates and comic reinterpretation explicitly, uses four acceptance conditions, requests short evidence-based answers rather than step-by-step reasoning, and evaluates both senses plus connecting knowledge for the supplied age. It retains the evaluator's required field names. Version-3 effectiveness has not yet been measured.

- corpus.md / corpus.jsonl: 50 texts and reference annotations.
- llm_procedure.md: current version-3 provider-neutral prompt, without a target-word lookup table.
- llm_procedure_v2.md: archived prompt for the recorded version-2 pilot; its hash matches run_manifest.json.
- run_inputs.jsonl: 50 shuffled, opaque-ID text-and-age inputs.
- predictions.md / predictions.jsonl: recorded outputs from this conversation.
- evaluation_key.json: mapping for the scorer only; do not give it to the model.
- evaluate.py / metrics.json: evaluator and calculated results.
- prepare_request.py: prepares a request for any text and age; does not call an LLM.
- instructor_checks.md and challenge JSONL files: seven separate, previously seen diagnostics.
- run_manifest.json: execution limitations and hashes of frozen prompt and inputs.

This is an LLM-prompt project, not an autonomous local inference application. The supplied predictions were produced in this conversation and scored with Python. Re-running evaluate.py only recalculates scores. To obtain fresh predictions, submit the prompt and inputs to an LLM and save its JSONL response.

The run is not blind: the assistant had seen the gold annotations. Age 12 was the recorded pilot's audience, not a default in the current procedure, and sense-specific acquisition evidence is unavailable. Do not present the scores as held-out performance or provisional familiarity judgments as sourced developmental facts.

For new requests, supply any valid age using `--text ... --age ...`, or per-record ages with `--inputs`. Optional `age_evidence` lists in batch records are preserved. Other annotation fields are stripped. A batch `--age` override applies to every record.

All saved predictions, metrics, and run_manifest.json describe version 2. They are not results for version 3. Re-running evaluate.py scores existing outputs only. Use the archived prompt to repeat the old procedure, or the current prompt for a new run and save its prompt, predictions, and manifest separately. The current scorer requires the corpus's original ages; do not score age-overridden predictions against the age-12 gold file.

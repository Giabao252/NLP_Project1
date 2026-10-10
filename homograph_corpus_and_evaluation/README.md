# Homograph project — revised LLM approach

Start with **report.md**, then **corpus.md** and **llm_procedure.md**.

- corpus.md / corpus.jsonl: 50 texts and reference annotations.
- llm_procedure.md: reusable provider-neutral inference prompt, without a target-word lookup table.
- run_inputs.jsonl: 50 shuffled, opaque-ID text-and-age inputs.
- predictions.md / predictions.jsonl: recorded outputs from this conversation.
- evaluation_key.json: mapping for the scorer only; do not give it to the model.
- evaluate.py / metrics.json: evaluator and calculated results.
- prepare_request.py: prepares a request for any text and age; does not call an LLM.
- instructor_checks.md and challenge JSONL files: seven separate, previously seen diagnostics.
- run_manifest.json: execution limitations and hashes of frozen prompt and inputs.

This is an LLM-prompt project, not an autonomous local inference application. The supplied predictions were produced in this conversation and scored with Python. Re-running evaluate.py only recalculates scores. To obtain fresh predictions, submit the prompt and inputs to an LLM and save its JSONL response.

The run is not blind: the assistant had seen the gold annotations. Age 12 is an assumed audience, and sense-specific acquisition evidence is unavailable. Do not present the scores as held-out performance or provisional familiarity judgments as sourced developmental facts.

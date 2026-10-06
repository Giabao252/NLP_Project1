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


## Active procedure: version 3

llm_procedure.md defines the candidate and comic reinterpretation, applies three acceptance gates, and limits explanations to brief evidence-based conclusions. Age assessment separately covers each meaning, comprehension of the switch, and content for the supplied age. prepare_request.py retains optional age_evidence; see execution.md for commands and age_demo_inputs.jsonl for a five-age demonstration.

The existing predictions, metrics, and run_manifest.json describe version 2. Its prompt is archived in llm_procedure_v2.md. Fresh outputs are needed to evaluate version 3; detection metrics do not establish age-suitability accuracy.

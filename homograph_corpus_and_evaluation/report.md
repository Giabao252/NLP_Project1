# Detecting age-appropriate homographic wordplay

## Project summary

This project uses an **explicit LLM prompting procedure**, an approach permitted by the assignment. It replaces the earlier corpus-specific word-and-cue lookup implementation. The prompt defines homographs, contextual support, causal coherence, rejection conditions, age judgments, and a structured output format. It does not contain a fixed list of the corpus's target words, answer mappings, or numerical age thresholds.

The main corpus contains **50 texts: 20 intended jokes, 20 matched non-joke rewrites, and 10 additional non-jokes**. Seven instructor examples are a separate diagnostic set, not additional items in the main metric denominator. The audience age for this pilot is **12**, a working assumption because no audience age was specified. New requests can provide any valid age.

The in-chat pilot accepted **19 of the 20 intended jokes**, rejected **all 30 non-jokes**, and marked one intended joke uncertain. Counting that abstention as a missed positive gives **98.0% accuracy and 97.4% joke F1**. This is a **non-blind exploratory result**, not a validated performance claim.

## What counts as a joke in this project?

A positive text relies on a written form that supports two meanings, each connected to a different relevant part of the text, with a coherent comic switch between them. Identical spelling is required; pronunciation may differ. Thus bow and bass can qualify, while a pun requiring two differently spelled sound-alike words does not.

Idioms and noun/verb shifts can qualify. A meaningful same-spelling substring can qualify under the instructor's broader allowance, but a novel decomposition such as auto + biography is explicitly labeled **compositional reanalysis**, rather than falsely described as a conventional second dictionary meaning. The main corpus uses ordinary words; that boundary case appears only in the instructor diagnostics.

The objective is to detect this form of wordplay, not every kind of humor. A text can be amusing without meeting the homograph criterion. Conversely, mentioning two dictionary meanings is not enough to make a text a joke.

## Procedure and outputs

The reusable specification is **llm_procedure.md**. For every text and age, it instructs the LLM to:

1. Find a candidate word, idiom, or meaningful substring and formulate the relevant senses.
2. Quote exact evidence for each sense and explain its contextual connection.
3. Check the readings against speaker roles, grammar, negation, and cause-and-effect. Do not silently repair the text or invent a remote sense.
4. Decide whether there is a coherent comic reinterpretation, a literal use, or an unresolved borderline case.
5. Explain the specific expectation and how the alternative meaning changes it.
6. Assess each meaning's likely familiarity for the supplied age, separately from content suitability. Identify uncertainty and the basis of the judgment.
7. Return structured JSON with status, target, meanings, evidence, explanation, age judgments, and recommendation.

The request preparation script takes a text and age and builds the LLM request. **It does not itself call a model.** The inference step in this run was performed by the assistant in the current conversation. Predictions were serialized, then scored by a separate Python evaluator. No API execution is claimed. A fresh run requires submitting the saved prompt and inputs to an LLM again.

## Correct rejection and failure conditions

Here, “fail when not a joke” means reject the joke hypothesis, not raise a software error. A correct rejection is a true negative. Reject when:

- Only one meaning is supported, even if the word has many dictionary senses.
- Two meanings are presented as a factual definition or comparison, without a comic switch.
- The supposed second meaning depends only on differently spelled sound-alike words.
- A candidate second reading is merely associated with a nearby word rather than used in the text.
- The alternate sense fails to explain the stated answer or action, including because negation reverses the relationship.
- The proposed explanation requires invented facts, unsupported political symbolism, or a nonexistent lexical meaning.

When evidence is borderline, return **uncertain**. When no compatible pair is found, say that clearly without claiming that every word in the text is unambiguous. Empty text and invalid ages are input errors. Unknown vocabulary or unsuitable content does **not** turn an actual joke into a non-joke; it changes the age recommendation.

## Corpus construction

The source is the user's supplied joke list. Selected items were adapted to repair unclear or invalid wordplay. Each pair retains its source number and records two intended meanings and a reference explanation. Adaptations are not represented as verbatim source quotations. Different-spelling sound puns, incomplete fragments, and invented senses were excluded.

Each non-joke rewrite keeps the target spelling, rather than simply deleting the potentially ambiguous word. It removes the humorous reinterpretation while retaining the topic and approximate length. This prevents a trivial target-word-presence classifier from succeeding. The ten added texts have comparable lengths and include ordinary dialogue and questions. Three deliberately describe both meanings literally: bat, current, and bank.

The main corpus's texts and joke labels were preserved from the earlier development run. Numerical age guesses were removed from its annotations. J07 remains an intended joke in the gold data despite the new model's uncertainty, so the disagreement is visible rather than hidden by relabeling the item. Both joke status and interpretation would benefit from independent human annotation.

## Metrics

Jokes are the positive class. For binary metrics, only a `joke` output is positive; an uncertain output is not accepted as a joke. Also report abstention coverage so that this mapping is visible. Strict accuracy counts any abstention as an error.

| Metric | Definition and purpose |
|---|---|
| Accuracy | (TP + TN) / N; overall binary correctness |
| Precision | TP / (TP + FP); reliability of joke predictions |
| Recall | TP / (TP + FN); proportion of gold jokes accepted |
| F1 | 2TP / (2TP + FP + FN); balances precision and recall |
| Specificity | TN / (TN + FP); correct rejection of non-jokes |
| False-positive rate | FP / (TN + FP); inappropriate joke acceptance |
| Balanced accuracy | Mean of recall and specificity |
| Macro F1 | Mean F1 across joke and non-joke classes |
| Pair success | Both the joke and its rewrite correct, divided by 20 pairs |
| Coverage | Non-abstained decisions / 50; pair with answered-only accuracy |
| Target localization | Intended target identified / 20, reported separately from acceptance |
| Sense interpretation | Both meanings correct and grounded; requires semantic review, not string matching alone |
| Explanation quality | Independent 0–2 ratings for meanings, grounding, and comic mechanism; report means and agreement |
| Age suitability | Independent age-specific judgments: accuracy/macro F1, false suitability rate, and unknown-rate coverage |

The last three semantic/developmental measures lack independent labels in this pilot. They are specified but **not reported as validated accuracy scores**. The majority-class baseline, always predicting non-joke, scores 60% accuracy on this corpus.

## Run record and results

Execution: current-conversation LLM application of version 2 of the procedure. The serving context identifies a GPT-6-family assistant; an exact snapshot and sampling settings were not exposed. Fifty text-only records were shuffled with a recorded seed and assigned opaque IDs. The saved prompt and input hashes are in run_manifest.json. The output includes one decision per input and exact evidence quotations; the evaluator checks completeness, unique IDs, age consistency, and quoted spans before scoring.

**Exposure limitation:** the same assistant created the corpus and previously read its annotations. Opaque IDs and text-only input files do not undo this exposure. This was not an isolated call, blinded evaluation, or held-out test. The outputs are the assistant's recorded judgments from this conversation. They must not be described as independently measured generalization performance.

| Actual class | Predicted joke | Not accepted as joke |
|---|---:|---:|
| Joke (20) | 19 | 1 uncertain |
| Non-joke (30) | 0 | 30 |

| Metric | Result |
|---|---:|
| Accuracy / strict accuracy | 98.0% |
| Joke precision | 100.0% |
| Joke recall | 95.0% |
| Joke F1 | 97.4% |
| Specificity | 100.0% |
| False-positive rate | 0.0% |
| Balanced accuracy | 97.5% |
| Macro F1 | 97.9% |
| Pair success | 19/20 (95.0%) |
| Coverage | 98.0% |
| Answered-only accuracy | 100.0% (49 decisions; excludes one abstention) |

All 20 target words were identified, including desert in the uncertain item. This does not mean all 20 jokes were accepted or that the meanings were independently validated. The 20 modified non-jokes and 10 additional non-jokes were all rejected.

### Disagreement

J07 says that a founder threatened to “desert his investors,” who then packed sunscreen. The intended readings are abandon and an arid region. The model recognized both, but marked the joke uncertain because the nominal geographical reading does not directly explain the verb phrase; it needs an unstated relocation or trip. This is a debatable annotation boundary. The reference label was not changed after seeing the result. The abstention counts against recall.

### Instructor diagnostics

| Case | Output | Explanation |
|---|---|---|
| Shingles / aluminum siding | Joke | Disease context shifts to building material |
| Autobiography / talking car | Joke, compositional reanalysis | Auto is playfully interpreted as car |
| Elephant trunk / no pockets | Joke | Body part shifts to storage container |
| Elephant tail / no pockets | Non-joke | No supported storage meaning of tail |
| Elephant mouth / no pockets | Non-joke | Putting things into a mouth still uses the anatomical sense |
| Skeletons **do not** fight / no guts | Joke | Lack of courage explains avoiding fighting |
| Skeletons **do** fight / no guts | Non-joke | Lack of courage does not explain fighting as stated |

All seven agree with the instructor's expected interpretations, including the fuzzy autobiography allowance. These examples were **known during procedure design** and therefore are compliance checks, not unseen test evidence. Their results are not pooled with the 50-text corpus score.

## Age-of-acquisition and suitability

The assignment asks whether the meanings are known at the target age. A model cannot establish an individual child's knowledge from age alone. This run therefore returns a **provisional per-sense judgment**, and uses null for numerical acquisition ages and sources where no supporting evidence was retrieved. It does not claim that a particular word was acquired at a fabricated age.

For the 20 gold jokes at age 12, outputs recommend: **13 provisionally suitable**, **6 needing vocabulary or wordplay explanation**, and **1 needing content review**. Examples requiring support include the accounting sense of balance, the informal hack idiom, date fruit, and contextual expressions such as off the hook or spring training. The axe-at-an-exam joke receives content review. The uncertain desert item is included in the six requiring explanation, not certified suitable.

These recommendations are model judgments, **not measured age accuracy**. Knowledge of both senses, relevant idioms, and background situations may differ by experience. A joke's clean subject matter does not guarantee comprehension. The earlier hand-assigned numeric thresholds were removed.

[Kuperman, Stadthagen-Gonzalez, and Brysbaert (2012)](https://pubmed.ncbi.nlm.nih.gov/22581493/) provide word-level age-of-acquisition ratings. No numerical entries from those norms were obtained or applied in this run. Moreover, a word-level mean would not establish acquisition of each sense in a pun. The remaining empirical limitation is sense-specific age evidence; it should be supplied before making sourced developmental claims.

## Hints and revisions

The first version used a 20-word lookup table and lexical cues. It achieved 90% accuracy but wrongly accepted five literal texts. It also used unsupported numeric age estimates. That implementation is excluded from the final package because it does not meet the new no-hard-coding constraint adequately.

The revised prompt adds general checks for contextual fit, literal comparison, causal compatibility, and negation. These were motivated by the baseline errors and the instructor's examples. This is **development guidance**, and is disclosed as exposure. There were no item-specific target-word hints or retries during the recorded version-2 run. A future assisted retry must preserve the initial output and report separate assisted metrics. Improvements over the first version are descriptive, not a controlled model comparison.

## Reproducing the workflow

Use the saved llm_procedure.md and run_inputs.jsonl in a **fresh LLM session**. Do not include corpus.jsonl, evaluation_key.json, gold explanations, or previous predictions in that session. Record the model/version, settings if available, exact prompt, and raw responses. For stronger isolation, send one record per fresh context. A future independent run may produce different outputs.

From the extracted folder, prepare an arbitrary single-input request:

```sh
python3 prepare_request.py --text "Why don't skeletons fight? Because they have no guts." --age 12 --out request.md
```

Or prepare the saved batch:

```sh
python3 prepare_request.py --inputs run_inputs.jsonl --out request.md
```

Submit request.md to an LLM, save one JSON object per line with the original opaque IDs, and evaluate the 50-record response:

```sh
python3 evaluate.py --predictions fresh_predictions.jsonl
```

To recompute this recorded pilot's metrics without calling a model:

```sh
python3 evaluate.py
```

The scorer writes metrics.json. It scores saved outputs; it does not rerun LLM inference or rewrite this narrative report. The Python utilities use only the standard library. All 50 full outputs are also available in predictions.md for reading.

The division into detection, localization, and interpretation is consistent with [Miller, Hempelmann, and Gurevych's SemEval-2017 Task 7](https://aclanthology.org/S17-2005/). This custom pilot is not a reproduction of that benchmark. For a stronger subsequent study, freeze the procedure, use independently annotated unseen examples, keep paired texts together in any split, and add independent explanation and age-suitability review.

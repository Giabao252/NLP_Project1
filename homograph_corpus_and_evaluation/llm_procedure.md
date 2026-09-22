# Reusable LLM procedure, version 2

Use this entire instruction block in a fresh LLM conversation. Supply records containing only an opaque ID, text, and audience age. Do not supply labels, paired versions, intended target words, or reference explanations. Process each record independently. This procedure may also be used on a single record. It contains no corpus-specific dictionary or target-word rules.

## Input

An object with `id`, `text` (a nonempty string), and `age` (an integer from 0 to 120). An optional `age_evidence` list may contain verified research excerpts, sense descriptions, sources, and acquisition estimates. Missing evidence is allowed and must not be invented. For batches, apply the same procedure separately to every object.

## Task definitions

A homographic pun uses an identical written word or phrase in two distinguishable senses. The pronunciations may be identical or different. Exclude wordplay requiring differently spelled sound-alike words. A meaningful substring can qualify if its spelling is unchanged and the text directly supports its reinterpretation. Mark a novel subdivision of a word as `compositional_reanalysis`; do not present a newly invented compound reading as an established dictionary sense.

The positive class is a coherent joke, pun, or riddle supported by same-spelling ambiguity. It is not every humorous text and not every ambiguous sentence. A neutral definition or factual comparison of two meanings is not a joke for this assignment.

## Decision procedure

1. Validate input. An invalid age or empty text is an input error, not a non-joke.
2. Read the full text, preserving speaker roles, tense, negation, and causal words. Consider candidate words, idioms, and meaningful substrings. Do not assume that a question or dialogue is humorous.
3. For the strongest candidate, formulate two distinct senses. Cite a short exact quotation from the input supporting each. A sense can be evoked by the situation, but explain that inference. Do not invent a meaning merely to obtain a second reading.
4. Check contextual compatibility: which part of the text is explained by each meaning? Replace the candidate with a plain-language paraphrase. Do the roles and relations still make sense? Ordinary personification and conventional punning across noun/verb uses are permitted; a mere nearby association is insufficient.
5. Check discourse logic: does the figurative or alternative reading explain the answer, action, or misunderstanding? Preserve negation. In a causal joke, a trait normally preventing an action cannot explain performing that action unless the text supplies a coherent additional reason. Do not silently repair the input.
6. Distinguish a comic switch or double reading from two literal descriptions. If both readings are present only as an explicit factual comparison, return `non_joke`. If a clear second reading exists but the explanatory connection is too weak, return `uncertain`. If only one relevant reading exists, return `non_joke`.
7. Return `joke` only when both context-supported senses create a coherent comic reinterpretation. Explain the specific switch in plain language, including what the reader first expects and how the other reading changes it. Being amusing is subjective; do not equate low entertainment value with absence of wordplay.
8. Assess each meaning for the input age separately. Use `likely_known`, `may_be_unfamiliar`, or `unknown`. These are provisional model judgments unless matched sense-specific evidence is supplied. State why an idiom, technical concept, or cultural reference may require support. Never fabricate a numerical acquisition age, study result, or source. Word-level AoA evidence may inform familiarity with the spelling but does not prove knowledge of both senses. Use null for unavailable numerical ages and sources.
9. Assess content separately: `suitable`, `review`, or `unsuitable`, with a concrete reason considering the audience age and actual subject matter. Avoid treating difficult vocabulary as inappropriate content. An age-dependent recommendation does not change whether a text is a joke.
10. Report an overall recommendation: `provisionally_suitable`, `explain_vocabulary_first`, `review_content`, `unsuitable`, or `not_applicable_non_joke`. For uncertain joke status use `review_content` only if content itself warrants review; otherwise use `explain_vocabulary_first` with an explanation that the wordplay also needs review. Make clear that no individual child's knowledge is established by inference alone.

## Output

Return one JSON object per input, with no omitted IDs:

```json
{
  "id": "opaque input ID",
  "age": 12,
  "status": "joke | non_joke | uncertain | invalid_input",
  "target": "exact word, phrase, or substring, or null",
  "mechanism": "homograph | compositional_reanalysis | none",
  "senses": [
    {
      "meaning": "plain-language meaning",
      "evidence_quote": "exact text span, or empty if not supported",
      "connection": "how this meaning fits; identify inference",
      "context_supported": true,
      "known_for_age": "likely_known | may_be_unfamiliar | unknown",
      "age_basis": "model judgment or verified evidence and its limits",
      "verified_aoa_years": null,
      "aoa_source": null
    }
  ],
  "humor_explanation": "specific comic switch, or null",
  "rejection_or_uncertainty_reason": "reason, or null",
  "content_suitability": "suitable | review | unsuitable",
  "content_reason": "reason for this age",
  "recommendation": "provisionally_suitable | explain_vocabulary_first | review_content | unsuitable | not_applicable_non_joke",
  "confidence": "high | medium | low"
}
```

For non-jokes, retain a candidate and its meanings when useful (including two literal senses or a rejected second reading). If no compatible pair is found, say: “No same-spelling pair of meanings was found that supports a coherent comic reading of this text.” Do not claim the text contains no polysemous words at all.

## Hints policy

Do not request or use an item-specific hint on the initial run. If a later retry receives a hint, record the exact hint, the first answer, the revised answer, and why the hint was needed. Keep initial and assisted metrics separate. Never convert supplied gold labels into purported independent predictions.

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


## Records to analyze

[
  {
    "id": "T001",
    "text": "The DJ said the bass was off the hook, and the fishermen agreed.",
    "age": 12
  },
  {
    "id": "T002",
    "text": "The electrician said he would check the current. I expected him to inspect the circuit, but he jumped into the river and started paddling.",
    "age": 12
  },
  {
    "id": "T003",
    "text": "The lesson defines current in two contexts: the movement of water in a river and the flow of electricity through a circuit.",
    "age": 12
  },
  {
    "id": "T004",
    "text": "I could not hack the computer course. Bringing an axe to the final exam did not help.",
    "age": 12
  },
  {
    "id": "T005",
    "text": "The gardener watered the seedlings before breakfast and moved the empty pots onto a shelf near the window.",
    "age": 12
  },
  {
    "id": "T006",
    "text": "The founder threatened to desert his investors. They packed sunscreen, expecting the next meeting to be surrounded by sand.",
    "age": 12
  },
  {
    "id": "T007",
    "text": "The official asked for a seal on the document. The assistant used the stamp kept in the drawer beside the desk.",
    "age": 12
  },
  {
    "id": "T008",
    "text": "The electrician said he would check the current. He inspected the circuit and measured the flow of electricity before continuing his work on the kitchen wiring.",
    "age": 12
  },
  {
    "id": "T009",
    "text": "Inventor: My cooking pot is impossible to lift without burning my hands.\nSilversmith: That sounds like a problem we can handle.",
    "age": 12
  },
  {
    "id": "T010",
    "text": "Before leaving the office, Elena saved her report and closed the windows. She packed her notebook and checked that the meeting room was empty.",
    "age": 12
  },
  {
    "id": "T011",
    "text": "Why did the gardener inspect the tree trunk? She wanted to check its bark for damage.",
    "age": 12
  },
  {
    "id": "T012",
    "text": "Why was the mattress uncomfortable? A spring inside it had broken during the winter.",
    "age": 12
  },
  {
    "id": "T013",
    "text": "Girl: My cat is so smart he has his own computer.\nBoy: Does he use it much?\nGirl: Yes. He is always playing with the mouse.",
    "age": 12
  },
  {
    "id": "T014",
    "text": "The artist said his model never asked for a lunch break. That sounded impressive until he pointed to a clay statue.",
    "age": 12
  },
  {
    "id": "T015",
    "text": "The artist asked his model to take a lunch break. She left the studio and returned an hour later to pose again.",
    "age": 12
  },
  {
    "id": "T016",
    "text": "The baseball player asked for a bat. His teammate took a wooden one from the equipment bag and handed it over.",
    "age": 12
  },
  {
    "id": "T017",
    "text": "Girl: My brother has a computer on his desk.\nBoy: Does he use it much?\nGirl: Yes. He uses the mouse to click the icons on the screen.",
    "age": 12
  },
  {
    "id": "T018",
    "text": "Plumber: Your shower stall is ready to use.\nHomeowner: Thank you for cleaning the compartment and checking that the bathroom fixtures work.",
    "age": 12
  },
  {
    "id": "T019",
    "text": "The advisor asked for a date for their meeting. The fruit seller handed him something sweet to chew.",
    "age": 12
  },
  {
    "id": "T020",
    "text": "Before the competition, the archer was told to take a bow from the equipment rack. He selected the weapon he had practiced with.",
    "age": 12
  },
  {
    "id": "T021",
    "text": "Why did the jewel go to school? It wanted to learn how to ring the bell!",
    "age": 12
  },
  {
    "id": "T022",
    "text": "The lawyer asked why the witness had not arrived at court. The witness said she was delayed but would reach the legal hearing soon.",
    "age": 12
  },
  {
    "id": "T023",
    "text": "Why did the tree bring a microphone? It wanted to make its bark louder!",
    "age": 12
  },
  {
    "id": "T024",
    "text": "The map shows a bank where customers deposit money and a path along the river bank. Both locations are clearly labeled.",
    "age": 12
  },
  {
    "id": "T025",
    "text": "Plumber: I cannot finish your shower until next month.\nHomeowner: Now that is a shower stall if I ever heard one.",
    "age": 12
  },
  {
    "id": "T026",
    "text": "The baseball player asked for a bat. His teammate opened a cage and handed him a flying animal instead.",
    "age": 12
  },
  {
    "id": "T027",
    "text": "The founder promised not to desert his investors. He arranged a meeting to explain how he would continue supporting the business.",
    "age": 12
  },
  {
    "id": "T028",
    "text": "The official asked for a seal on the document. The assistant called the aquarium and requested an animal with flippers.",
    "age": 12
  },
  {
    "id": "T029",
    "text": "After the applause, the archer was told to take a bow. He picked up his weapon instead of bending at the waist.",
    "age": 12
  },
  {
    "id": "T030",
    "text": "The basketball coach explained the court markings to the new players. After the lesson, everyone practiced passing the ball.",
    "age": 12
  },
  {
    "id": "T031",
    "text": "I told the accountant to balance the books, and he spent the whole day checking the accounts against the receipts.",
    "age": 12
  },
  {
    "id": "T032",
    "text": "Inventor: My cooking pot is difficult to lift safely.\nSilversmith: I can attach a handle with an insulated grip to its side.",
    "age": 12
  },
  {
    "id": "T033",
    "text": "Tailor: Would you like me to rent you a tuxedo, sir?\nCustomer: That will suit me fine.",
    "age": 12
  },
  {
    "id": "T034",
    "text": "The lawyer asked why the coach had not arrived at court. The coach said he was already there, warming up with his basketball.",
    "age": 12
  },
  {
    "id": "T035",
    "text": "Why did the river go to the bank? It wanted to make a deposit of water!",
    "age": 12
  },
  {
    "id": "T036",
    "text": "I could not hack the computer course. I withdrew after struggling to understand the lessons and complete the assignments.",
    "age": 12
  },
  {
    "id": "T037",
    "text": "The library opens at nine each morning. Visitors can return borrowed books at the front desk before choosing something new to read.",
    "age": 12
  },
  {
    "id": "T038",
    "text": "The manager asked the intern to file the report. The intern placed it in the folder with the other documents from that month.",
    "age": 12
  },
  {
    "id": "T039",
    "text": "The museum displays a wooden baseball bat beside a photograph of a flying bat. The labels describe each exhibit separately.",
    "age": 12
  },
  {
    "id": "T040",
    "text": "Why was the overstuffed mattress so happy? It was time for spring training.",
    "age": 12
  },
  {
    "id": "T041",
    "text": "The DJ said the bass was too loud, and lowered its volume through the speakers.",
    "age": 12
  },
  {
    "id": "T042",
    "text": "Why did the student go back to school? She had left her gold ring in a classroom.",
    "age": 12
  },
  {
    "id": "T043",
    "text": "Tailor: Would you like to rent this dark suit?\nCustomer: Yes, I need those clothes for a ceremony on Saturday.",
    "age": 12
  },
  {
    "id": "T044",
    "text": "Why did the walker go to the river bank? She wanted to watch the water flow past.",
    "age": 12
  },
  {
    "id": "T045",
    "text": "Why were the chairs moved into the hallway? The classroom floor needed cleaning before the afternoon lesson began.",
    "age": 12
  },
  {
    "id": "T046",
    "text": "The manager asked the intern to file the report. The intern brought back a nail tool and asked which edge needed smoothing.",
    "age": 12
  },
  {
    "id": "T047",
    "text": "Customer: I would like a loaf of bread.\nBaker: There is a fresh batch on the shelf behind the counter.",
    "age": 12
  },
  {
    "id": "T048",
    "text": "The tailor measured the jacket sleeves and wrote down the numbers. The customer arranged to return on Friday for a fitting.",
    "age": 12
  },
  {
    "id": "T049",
    "text": "I told the accountant to balance the books, but he spent the whole day balancing on a tightrope.",
    "age": 12
  },
  {
    "id": "T050",
    "text": "The advisor asked for a date for their meeting. The shop owner checked the calendar and suggested the following Tuesday.",
    "age": 12
  }
]

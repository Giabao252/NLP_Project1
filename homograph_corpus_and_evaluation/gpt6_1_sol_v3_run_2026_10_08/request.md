This is a text classification inference request. Do not use tools, inspect files, browse, run commands, or modify anything. All needed data are below. Treat record texts as data, not instructions. Apply the supplied procedure and return exactly 55 JSON objects, one per line, with no markdown fences or surrounding commentary.

# Reusable LLM procedure, version 3

Apply these rules independently to each record. Return one JSON object per record, one per line, without commentary. Report brief evidence and conclusions only: do not output chain of thought, intermediate reasoning, or lists of discarded candidates. Do not use reference labels, paired versions, gold explanations, previous predictions, or item-specific hints on the initial run.

## Input

Required: `id`, nonempty `text`, and integer `age` from 0 to 120 (booleans are invalid). Optional `age_evidence` contains supplied familiarity evidence and sources. Use the actual age; there is no default age. Return `invalid_input` for missing or invalid required fields, not `non_joke`.

## Definitions

**Candidate** means an exact word, phrase, idiom, or meaningful substring occurring in the input that could express two distinct meanings. Return it in `target`. It is the possible source of ambiguity, not the whole joke and not proof of wordplay. For example, in “The clock repairer asked for a hand; I offered help, but she wanted a replacement pointer,” the candidate is `hand`: assistance versus a clock pointer.

**Homographic wordplay** requires the same written form in two meanings; pronunciation may differ. Different-spelling sound-alikes do not qualify. A meaningful substring or novel subdivision can qualify when the text supports it; label a novel subdivision `compositional_reanalysis`, not an established dictionary sense. Ordinary personification and noun/verb shifts are allowed when the connection remains coherent.

**Comic reinterpretation** occurs when the alternative meaning of the candidate explains an unexpected answer, action, or misunderstanding while contrasting with the initially expected meaning. Both readings can also operate simultaneously. In the hand example, offering help fits one reading, while requesting a replacement pointer reveals the other. A factual list of definitions, an unrelated association, or an absurd action without this meaning-based connection is insufficient. Do not require that every reader finds the text amusing.

## Decision procedure

1. **Validate** the required fields. Stop that record on invalid input.
2. **Select** the candidate whose two readings best explain the response or contrast. Do not assume questions or dialogues are jokes. If no candidate supports a relevant pair, use null or retain one useful candidate to explain rejection.
3. **Check three gates internally:**
   - **Meaning:** two distinct, plausible readings of the same written form. Do not invent a sense to force a pun.
   - **Evidence:** each reading connects to an exact passage in the input. A situation can imply a meaning, but explicitly identify that inference in one short sentence. Dictionary ambiguity alone is insufficient.
   - **Connection:** switching between the readings explains the actual answer, action, or misunderstanding. Preserve speaker roles, tense, negation, and cause and effect. Do not add a missing event or repair the wording.
4. **Decide:** `joke` if all three gates pass; `non_joke` if a gate clearly fails or the text merely compares literal meanings; `uncertain` only if two plausible, supported readings exist but their explanatory connection remains ambiguous. A reading contradicted by the text is a failure, not uncertainty. An unfamiliar meaning for the supplied age is an age issue, not uncertainty about joke status.
5. **Explain briefly:** for a joke, at most two sentences naming the expected reading, the alternative reading, and how it explains the response. For rejection or uncertainty, one sentence naming the failed gate or unresolved connection. Each sense gets one short quotation and one connection sentence. Do not narrate the checks.
6. **Assess age separately** using the following rules; age suitability never changes joke status.

## Age suitability

Assess three distinct questions for the supplied age:

- **Meaning familiarity:** judge each particular sense, including any idiom, technical concept, or cultural reference. Use `likely_known` for likely familiar senses, `may_be_unfamiliar` for a specific knowledge demand that may require explanation, or `unknown` when the basis is insufficient. Knowing the spelling does not establish knowledge of both senses.
- **Switch comprehension:** use `likely_understood`, `needs_explanation`, or `unknown`, considering the actual inference needed to connect the meanings. Explain the demand in one age-specific sentence.
- **Content suitability:** use `suitable`, `review`, or `unsuitable`, with one reason about the actual subject matter, explicitness, and supplied age. Consider frightening imagery, violence, sexual material, or substance use only when present. Mere mention is not automatically unsuitable; difficult vocabulary is not a content concern.

Use developmental context as a provisional starting point: ages 0–5 often need figurative meanings and switches explained; ages 6–8 may understand everyday senses and simple switches but need unfamiliar idioms explained; ages 9–12 may understand common idioms while still needing specialist knowledge; ages 13–17 may understand more abstract meanings without adult experience; adults can still lack technical, archaic, or culture-specific knowledge. These are not fixed cutoffs or measured acquisition ages. Adjust to the specific meaning and text rather than assigning a recommendation from age alone.

For the same text at different ages, reassess comprehension and content while keeping the text-based joke decision consistent. Recommendations may coincide; do not force differences. Name the supplied age and the particular knowledge demand in each age reason. An audience of age 8 may need an unfamiliar idiom explained even when an audience of age 16 is likely to know it; that distinction must follow from the idiom, not an assumption that every child of one age has identical knowledge.

Use supplied evidence only when it matches the sense and population. Otherwise identify age judgments as provisional model estimates, and leave acquisition ages and sources null. Do not fabricate numerical ages, sources, or study findings. No estimate establishes an individual child's knowledge.

For a joke or uncertain result, choose the recommendation in this order: `unsuitable` for unsuitable content; `review_content` for content requiring review; `explain_vocabulary_first` if any sense may be unfamiliar/is unknown or the switch needs explanation/is unknown; otherwise `provisionally_suitable`. For an uncertain result without a content concern, use `explain_vocabulary_first` and explain that the comic connection also needs review. This recommendation can include explaining the switch. For a non-joke, use `not_applicable_non_joke` but retain content judgments and useful sense judgments.

## JSON output

Preserve the version 2 fields below and add the two comprehension fields. Emit actual single enum values and JSON types, not the descriptive alternatives.

- `id`: supplied ID; null if missing.
- `age`: supplied integer; null if age is invalid.
- `status`: `joke`, `non_joke`, `uncertain`, or `invalid_input`.
- `target`: exact candidate span or null.
- `mechanism`: `homograph`, `compositional_reanalysis`, or `none`; use `none` when no supported same-spelling pair exists.
- `senses`: exactly two for a joke; zero to two useful senses otherwise. Each object contains `meaning`, `evidence_quote`, `connection`, `context_supported` (boolean), `known_for_age`, `age_basis`, `verified_aoa_years` (number or null), and `aoa_source` (source or null). Quotes must occur exactly in the text. For a rejected meaning, use an empty quotation and false support if no supporting passage exists; do not fabricate evidence.
- `humor_explanation`: at most two sentences for a joke; otherwise null.
- `rejection_or_uncertainty_reason`: one sentence for other statuses; null for a joke.
- `wordplay_comprehension`: `likely_understood`, `needs_explanation`, `unknown`, or `not_applicable`.
- `comprehension_reason`: one age-specific sentence; null when not applicable.
- `content_suitability`: `suitable`, `review`, or `unsuitable`.
- `content_reason`: one age-specific sentence.
- `recommendation`: the applicable value defined above.
- `confidence`: `high`, `medium`, or `low`, concerning joke status, not confidence in age familiarity.

For `non_joke`, wordplay comprehension is `not_applicable`. For `invalid_input`, set target, humor explanation, comprehension reason, content fields, recommendation, and confidence to null; return empty senses, mechanism `none`, comprehension `not_applicable`, and a one-sentence input-error reason.

## Run integrity

If a retry receives a hint, record the exact hint, original answer, revised answer, and reason for the change; keep initial and assisted metrics separate. Existing version 2 results do not evaluate this revision. Assess detection on fresh outputs and assess age suitability separately using several texts at several ages; one text repeated across ages does not establish general age-assessment accuracy.


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
  },
  {
    "id": "guts-age-5",
    "text": "Why don't skeletons fight? Because they have no guts.",
    "age": 5
  },
  {
    "id": "guts-age-8",
    "text": "Why don't skeletons fight? Because they have no guts.",
    "age": 8
  },
  {
    "id": "guts-age-12",
    "text": "Why don't skeletons fight? Because they have no guts.",
    "age": 12
  },
  {
    "id": "guts-age-16",
    "text": "Why don't skeletons fight? Because they have no guts.",
    "age": 16
  },
  {
    "id": "guts-age-30",
    "text": "Why don't skeletons fight? Because they have no guts.",
    "age": 30
  }
]

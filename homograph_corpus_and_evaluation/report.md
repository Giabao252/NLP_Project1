# Detecting age-appropriate homographic wordplay

## Project summary

The project examines whether a text uses the same written word in two meanings to create a coherent joke. It also considers whether readers of a specified age are likely to understand those meanings and whether the content is suitable for them.

The main collection contains **50 texts: 20 intended jokes, 20 matched non-joke rewrites, and 10 additional non-jokes**. The 50-text detection test uses age **12**. A separate age assessment now checks **all 20 intended jokes** at ages **5, 8, 12, 16, and 30**, giving **100 assessments**.

The saved 50-text detection test accepted **18 intended jokes**, rejected **all 30 reference non-jokes**, rejected **one intended joke**, and left **one intended joke uncertain**. Accuracy was **96.0%** and joke F1 was **94.74%**. These are results on a small authored collection, not independent evidence of general performance.

The 50-text detection results and their age-12 judgments come from the saved [readable corpus predictions](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md) and [readable age comparison](gpt6_1_sol_v3_request_rerun_2026_10_08/age_predictions.md). The numerical results were checked against the saved scores for that same test.

## What counts as wordplay?

A candidate is the exact word, phrase, or meaningful substring whose two readings could explain the text. A comic reinterpretation occurs when an alternative reading makes an unexpected answer, action, or misunderstanding intelligible while contrasting with the expected reading. Both meanings need support from the text.

For example, a request for a baseball bat followed by the delivery of a flying animal shifts bat from sporting equipment to a mammal. A museum label describing both kinds of bat is a factual comparison and does not create the same comic switch.

Identical spelling is required; pronunciation may differ. Idioms and shifts between noun and verb uses can qualify. A newly invented subdivision of a word must be identified as a playful reanalysis rather than an established dictionary meaning.

## The collection

Texts were adapted from the supplied joke list where necessary. The paired non-jokes retain the target spelling while removing the comic reinterpretation, so the presence of an ambiguous word alone cannot determine the answer. The additional texts include ordinary questions and dialogue; three explicitly compare meanings without making a joke.

The reference joke labels are unchanged. Disagreements remain visible rather than being removed by changing a label after the test. The earlier instructor examples were not rerun in this test and are not included in the current scores.

## Results of the 50-text detection test

Jokes are the positive class. An uncertain response is not counted as an accepted joke; it counts as a missed positive when the reference label is a joke.

| Reference class | Accepted as a joke | Rejected | Uncertain |
| --- | ---: | ---: | ---: |
| Intended joke (20) | 18 | 1 | 1 |
| Non-joke (30) | 0 | 30 | 0 |

| Measure | Result |
| --- | ---: |
| Accuracy / strict accuracy | 96.0% |
| Joke precision | 100.0% |
| Joke recall | 90.0% |
| Joke F1 | 94.74% |
| Specificity | 100.0% |
| False-positive rate | 0.0% |
| Balanced accuracy | 95.0% |
| Macro F1 | 95.76% |
| Pair success | 18/20 (90.0%) |
| Coverage | 98.0% (49 of 50 decisions) |
| Answered-only accuracy | 97.96% (48 of 49 decisions) |
| Target localization | 100.0% (20 of 20 intended joke targets) |

Identifying the target word does not establish that both readings create a coherent joke. The majority-class baseline, which labels everything a non-joke, would achieve 60.0% accuracy.

## Age-of-acquisition

Age of acquisition concerns when a meaning becomes familiar. Here, each meaning is considered separately: recognizing a word does not establish knowledge of its idiom, technical sense, or cultural reference. Understanding both meanings also does not guarantee that a reader understands the switch between them.

**No verified sense-specific acquisition ages or sources were supplied for the earlier test or any of the 100 new age assessments.** The saved outputs therefore leave numerical acquisition ages and sources empty. This report does not assign an acquisition age, infer a minimum suitable age from a single judgment, or present familiarity estimates as developmental measurements.

The predictions use three practical descriptions: **likely familiar**, **may need explanation**, and **unknown**. These are provisional estimates about the specified audience, not proof of an individual reader's knowledge. Experience with idioms, sports, occupations, foods, and cultural references can change familiarity at the same age.

### Age-12 judgments in the 50-text detection test

Among the **20 reference-labeled jokes**, **11** were provisionally suitable, **eight** needed explanation or review of the wordplay, and **one** received no joke recommendation because it was rejected as a joke. Among the **18 accepted jokes alone**, **11** were provisionally suitable and **seven** needed explanation. The eighth explanation recommendation belongs to the uncertain mattress item.

| Item | Candidate | Meaning or connection needing support |
| --- | --- | --- |
| [T001](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md#t001) | bass | At age 12, recognizing the fish name and the slang meaning of off the hook may require explanation. |
| [T004](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md#t004) | hack | At age 12, the switch may need an explanation of hack meaning cope. |
| [T006](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md#t006) | desert | At age 12, understanding desert as abandon and recognizing its different pronunciation may need explanation. |
| [T019](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md#t019) | date | At age 12, the calendar-to-fruit switch may need identification of the fruit date. |
| [T025](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md#t025) | stall | At age 12, interpreting stall as delay within the familiar phrase shower stall may need explanation. |
| [T028](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md#t028) | seal | At age 12, the animal substitution is clear once the official-document sense of seal is explained. |
| [T040](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md#t040) | spring | At age 12, the sports phrase may need explanation and the comic connection also needs review. |
| [T049](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md#t049) | balance | At age 12, the physical action is clear but the accounting idiom may need explanation. |

The accounting use of balance, the idiom hack meaning cope, date as a fruit, the official mark called a seal, and expressions such as off the hook and spring training illustrate the knowledge demands. The shower-stall item also received an explanation recommendation because its delay reading may be less familiar.

## Content suitability

Content suitability is assessed separately from vocabulary and understanding the wordplay. A clean topic can still contain an unfamiliar idiom, while difficult vocabulary does not make the subject inappropriate.

In the 50-text detection test, **all 20 intended jokes were marked content-suitable at age 12**. None received a content-review or unsuitable-content recommendation. This includes the axe-at-an-exam text: its saved assessment notes that the axe is mentioned without threats or injury. That is the assessment recorded for this test, not a universal endorsement for every classroom or reader.

The rejected jewel item is still marked content-suitable. Its rejection concerns the unsupported jewelry-to-bell interpretation, not its appropriateness for the audience. Similarly, the uncertain mattress item needs review of the comic connection and sports reference rather than a content restriction.

## Age checks for every intended joke

All 20 reference-labeled jokes were checked at ages **5, 8, 12, 16, and 30**. Each joke used a fresh model context containing only the full prompt and its five text-and-age records. The two disputed jokes were included so their vocabulary and content would not be overlooked. No reference labels, intended meanings, gold explanations, or previous predictions were supplied to the model.

The table reports the saved overall recommendation. **Provisionally suitable** means the meanings and switch were judged likely to be understood and the content suitable; **Explain first** means vocabulary or the connection needs support; **Review content** concerns the subject matter. **Joke not confirmed** means the text was rejected as a joke, not that its content is automatically inappropriate. Exact familiarity judgments, content ratings, and reasons for all 100 cases are in the [complete readable age checks](age_checks_all_jokes_2026_10_08/predictions.md).

| Joke | Intended word | Age 5 | Age 8 | Age 12 | Age 16 | Age 30 |
| --- | --- | --- | --- | --- | --- | --- |
| [J01](age_checks_all_jokes_2026_10_08/predictions.md#j01) | bat | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J02](age_checks_all_jokes_2026_10_08/predictions.md#j02) | seal | Explain first | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J03](age_checks_all_jokes_2026_10_08/predictions.md#j03) | bark | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J04](age_checks_all_jokes_2026_10_08/predictions.md#j04) | bank | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J05](age_checks_all_jokes_2026_10_08/predictions.md#j05) | bow | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J06](age_checks_all_jokes_2026_10_08/predictions.md#j06) | date | Explain first | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J07](age_checks_all_jokes_2026_10_08/predictions.md#j07) | desert | Explain first | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J08](age_checks_all_jokes_2026_10_08/predictions.md#j08) | model | Explain first | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J09](age_checks_all_jokes_2026_10_08/predictions.md#j09) | balance | Explain first | Explain first | Explain first | Provisionally suitable | Provisionally suitable |
| [J10](age_checks_all_jokes_2026_10_08/predictions.md#j10) | court | Explain first | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J11](age_checks_all_jokes_2026_10_08/predictions.md#j11) | spring | Explain first | Explain first | Explain first | Provisionally suitable | Provisionally suitable |
| [J12](age_checks_all_jokes_2026_10_08/predictions.md#j12) | mouse | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J13](age_checks_all_jokes_2026_10_08/predictions.md#j13) | handle | Explain first | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J14](age_checks_all_jokes_2026_10_08/predictions.md#j14) | hack | Explain first | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J15](age_checks_all_jokes_2026_10_08/predictions.md#j15) | stall | Explain first | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J16](age_checks_all_jokes_2026_10_08/predictions.md#j16) | suit | Explain first | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J17](age_checks_all_jokes_2026_10_08/predictions.md#j17) | bass | Explain first | Explain first | Explain first | Provisionally suitable | Provisionally suitable |
| [J18](age_checks_all_jokes_2026_10_08/predictions.md#j18) | file | Explain first | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J19](age_checks_all_jokes_2026_10_08/predictions.md#j19) | current | Explain first | Explain first | Provisionally suitable | Provisionally suitable | Provisionally suitable |
| [J20](age_checks_all_jokes_2026_10_08/predictions.md#j20) | ring | Joke not confirmed | Joke not confirmed | Joke not confirmed | Joke not confirmed | Joke not confirmed |

### Recommendations by age

| Age | Provisionally suitable | Explain first | Review content | Unsuitable | Joke not confirmed |
| --- | ---: | ---: | ---: | ---: | ---: |
| 5 | 0 | 19 | 0 | 0 | 1 |
| 8 | 5 | 14 | 0 | 0 | 1 |
| 12 | 16 | 3 | 0 | 0 | 1 |
| 16 | 19 | 0 | 0 | 0 | 1 |
| 30 | 19 | 0 | 0 | 0 | 1 |

### Content judgments, separately from comprehension

| Age | Suitable content | Content needs review | Unsuitable content |
| --- | ---: | ---: | ---: |
| 5 | 20 | 0 | 0 |
| 8 | 20 | 0 | 0 |
| 12 | 20 | 0 | 0 |
| 16 | 20 | 0 | 0 |
| 30 | 20 | 0 | 0 |

### Reasons behind age-dependent recommendations

- **J01 — bat:** Age 5: Provisional model estimate: at age 5, connecting the baseball equipment request to the animal meaning may need an explanation of both meanings of bat. Age 8: Provisional model estimate: at age 8, the explicit animal response likely makes the simple switch between the two common meanings of bat understandable.
- **J02 — seal:** Age 5: Provisional model estimate: at age 5, connecting an official document seal to the assistant's animal misunderstanding likely needs explanation. Age 12: Provisional model estimate: at age 12, the document and aquarium cues likely make the switch between an authenticating mark and an animal understandable.
- **J03 — bark:** Age 5: At age 5, connecting the tree covering to a dog's sound and understanding microphone amplification may need explanation. Age 8: At age 8, the simple switch between tree covering and dog sound, linked by a microphone making sound louder, is likely understood.
- **J04 — bank:** Age 5: At age 5, connecting a money deposit with water arriving at a riverbank likely needs explanation. Age 8: At age 8, substituting water for money in a deposit likely makes the switch between the two familiar bank meanings understandable.
- **J05 — bow:** Age 5: Provisional model estimate: at age 5, connecting the applause convention to the same written word for a weapon likely needs explanation. Age 8: Provisional model estimate: at age 8, the explicit contrast between picking up a weapon and bending likely makes the switch understandable.
- **J06 — date:** Age 5: Provisional model estimate: at age 5, connecting a scheduling request to an implicitly identified date fruit likely needs explanation. Age 12: Provisional model estimate: at age 12, the fruit seller and edible response likely make the switch from a calendar date to a date fruit understandable.
- **J07 — desert:** Age 5: At age 5, connecting an abandonment threat to a landscape through the same spelling likely needs explanation. Age 12: At age 12, the shift from abandoning people to imagining a desert meeting location is likely understandable from the sand and sunscreen cues.
- **J08 — model:** Age 5: At age 5, connecting the two meanings of model and recognizing why the statue makes the claim unimpressive likely needs explanation. Age 12: At age 12, switching from a human posing to a clay representation and recognizing that statues need no lunch is likely understood.
- **J09 — balance:** Age 5: At age 5, understanding the switch likely requires explaining the accounting expression and connecting it to physical balance. Age 16: At age 16, the contrast between accounting work and physical balancing is likely understood from the accountant and tightrope cues.
- **J10 — court:** Age 5: Provisional model estimate: at age 5, connecting the lawyer and basketball clues to two meanings of court likely needs explanation. Age 12: Provisional model estimate: at age 12, using the lawyer and basketball clues to distinguish the two common meanings of court is likely understood.
- **J11 — spring:** Age 5: At age 5, connecting seasonal sports training to personified mattress coils likely needs explanation. Age 16: At age 16, switching from seasonal sports preparation to personified mattress coils is likely understood.
- **J12 — mouse:** Age 5: At age 5, connecting the computer-device meaning with a cat playing with a rodent will likely need explanation. Age 8: Provisional model estimate: at age 8, the simple switch between a computer device and a rodent is likely understood.
- **J13 — handle:** Age 5: Provisional model estimate: at age 5, connecting figurative problem solving with an implied pot handle likely needs explanation. Age 12: Provisional model estimate: at age 12, inferring a pot handle as the solution and linking it to managing a problem is likely understood.
- **J14 — hack:** Age 5: At age 5, connecting an idiom about coping with coursework to chopping with an axe likely needs explanation. Age 12: At age 12, the switch from coping with coursework to chopping with an axe is likely understood without specialist knowledge.
- **J15 — stall:** Age 5: At age 5, connecting the shower enclosure name to a delay in building the shower likely needs explanation. Age 12: At age 12, connecting the enclosure phrase to the explicitly stated construction delay is likely understood.
- **J16 — suit:** Age 5: At age 5, connecting the expression 'suit me fine' with being dressed in a tuxedo likely needs explanation. Age 12: At age 12, connecting a satisfactory offer with the suit supplied by a tuxedo rental is likely understood.
- **J17 — bass:** Age 5: Provisional model estimate: at age 5, connecting the two meanings of bass and the slang versus literal readings of 'off the hook' likely needs explanation. Age 16: Provisional model estimate: at age 16, the slang meaning of 'off the hook' and the contextual switch from musical bass to fish are likely understood.
- **J18 — file:** Age 5: At age 5, connecting the office instruction to the tool action likely requires explaining both uses of file. Age 12: At age 12, the direct switch from document filing to smoothing with a nail file is likely understood from the contrasting actions.
- **J19 — current:** Age 5: Provisional model estimate: at age 5, connecting electrical flow with river flow through the same word likely needs explanation. Age 12: Provisional model estimate: at age 12, the explicit circuit-to-river contrast likely makes the switch between the two meanings understandable.

These are age-specific estimates, not verified acquisition ages or exact thresholds. The checks do not show that every child at one age will understand a joke, and the recommendations need not improve at every sampled age. The original 50-text detection scores remain unchanged because this separate study contains intended jokes only, with different ages and new contexts.

### Differences from the detection test

**J11 — spring:** The earlier 50-text test marked this uncertain; the new per-joke context marked it joke at all five ages. The changed decision is preserved rather than adjusted to match the earlier run.

This is variation between model runs and contexts, not an effect of changing age: the decision stayed consistent across ages within each new context. The disagreement ratings below describe the earlier detection test.

## Disagreements in the 50-text detection test

Two items differ from their reference joke labels. For this report, the review rating describes the interpretation problem: **0 = agreement**, **1 = supported meanings with an ambiguous comic connection**, and **2 = an intended reading is not adequately grounded in the text**. These are editorial review ratings added for discussion, rather than independently verified ratings.

| Item | Reference label | Saved decision | Review rating | Reason |
| --- | --- | --- | --- | --- |
| [J20 / T021](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md#t021), jewel and ring | Joke | Not a joke | **2 — substantive grounding problem** | A jewel can be associated with a jewelry ring, but that association does not establish a second ring reading that explains going to school to ring a bell. |
| [J11 / T040](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md#t040), mattress and spring training | Joke | Uncertain | **1 — ambiguous comic connection** | Both the mattress-coil and seasonal-training readings are plausible, but the connection between training and the overstuffed mattress's happiness remains unclear. |

Both count against joke recall. The reference labels have not been changed. The founder/desert item was accepted in this test; its abandon meaning still received an age-specific explanation recommendation.

## Evidence and limits

The 50-text detection assessment used **GPT-6.1 Sol** in a fresh Codex process, supplied with the full saved request and text/age inputs. Gold labels and previous predictions were excluded from the request. The reference annotations were used afterward to score the saved decisions.

The collection was authored and discussed during development, so a fresh process does not turn it into an independently held-out benchmark. The age recommendations remain provisional estimates. The new age checks cover every intended joke, but there are still no independent child-comprehension observations or human age-suitability ratings in the saved data.

For each item's exact meanings, evidence, and age reasons, see the [readable corpus predictions](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md) and [age comparison](gpt6_1_sol_v3_request_rerun_2026_10_08/age_predictions.md). The [saved metrics](gpt6_1_sol_v3_request_rerun_2026_10_08/metrics.json), [submitted request](gpt6_1_sol_v3_request_rerun_2026_10_08/request.md), and [run record](gpt6_1_sol_v3_request_rerun_2026_10_08/run_manifest.json) provide the supporting record.

The [new age-check run record](age_checks_all_jokes_2026_10_08/run_manifest.json) and [age summaries](age_checks_all_jokes_2026_10_08/summary.json) document the 20 fresh contexts and all 100 assessments.

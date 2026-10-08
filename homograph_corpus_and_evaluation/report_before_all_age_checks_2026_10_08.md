# Detecting age-appropriate homographic wordplay

## Project summary

The project examines whether a text uses the same written word in two meanings to create a coherent joke. It also considers whether readers of a specified age are likely to understand those meanings and whether the content is suitable for them.

The main collection contains **50 texts: 20 intended jokes, 20 matched non-joke rewrites, and 10 additional non-jokes**. These inputs use age **12**. A separate example is assessed for ages **5, 8, 12, 16, and 30** to show how recommendations can differ.

The latest saved test accepted **18 intended jokes**, rejected **all 30 reference non-jokes**, rejected **one intended joke**, and left **one intended joke uncertain**. Accuracy was **96.0%** and joke F1 was **94.74%**. These are results on a small authored collection, not independent evidence of general performance.

The descriptions and age judgments below come from the latest [readable corpus predictions](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md) and [readable age comparison](gpt6_1_sol_v3_request_rerun_2026_10_08/age_predictions.md). The numerical results were checked against the saved scores for that same test.

## What counts as wordplay?

A candidate is the exact word, phrase, or meaningful substring whose two readings could explain the text. A comic reinterpretation occurs when an alternative reading makes an unexpected answer, action, or misunderstanding intelligible while contrasting with the expected reading. Both meanings need support from the text.

For example, a request for a baseball bat followed by the delivery of a flying animal shifts bat from sporting equipment to a mammal. A museum label describing both kinds of bat is a factual comparison and does not create the same comic switch.

Identical spelling is required; pronunciation may differ. Idioms and shifts between noun and verb uses can qualify. A newly invented subdivision of a word must be identified as a playful reanalysis rather than an established dictionary meaning.

## The collection

Texts were adapted from the supplied joke list where necessary. The paired non-jokes retain the target spelling while removing the comic reinterpretation, so the presence of an ambiguous word alone cannot determine the answer. The additional texts include ordinary questions and dialogue; three explicitly compare meanings without making a joke.

The reference joke labels are unchanged. Disagreements remain visible rather than being removed by changing a label after the test. The earlier instructor examples were not rerun in this test and are not included in the current scores.

## Latest results

Jokes are the positive class. An uncertain response is not counted as an accepted joke; it counts as a missed positive when the reference label is a joke.

| Reference class | Accepted as a joke | Rejected | Uncertain |
| --- | ---: | ---: | ---: |
| Intended joke (20) | 18 | 1 | 1 |
| Non-joke (30) | 0 | 30 | 0 |

| Measure | Result |
| --- | ---: | ---
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

**No verified sense-specific acquisition ages or sources were supplied for any of the 55 assessed records.** The saved outputs therefore leave numerical acquisition ages and sources empty. This report does not assign an acquisition age, infer a minimum suitable age from a single judgment, or present familiarity estimates as developmental measurements.

The predictions use three practical descriptions: **likely familiar**, **may need explanation**, and **unknown**. These are provisional estimates about the specified audience, not proof of an individual reader's knowledge. Experience with idioms, sports, occupations, foods, and cultural references can change familiarity at the same age.

### Meanings and wordplay needing explanation at age 12

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

In the latest test, **all 20 intended jokes were marked content-suitable at age 12**. None received a content-review or unsuitable-content recommendation. This includes the axe-at-an-exam text: its saved assessment notes that the axe is mentioned without threats or injury. That is the assessment recorded for this test, not a universal endorsement for every classroom or reader.

The rejected jewel item is still marked content-suitable. Its rejection concerns the unsupported jewelry-to-bell interpretation, not its appropriateness for the audience. Similarly, the uncertain mattress item needs review of the comic connection and sports reference rather than a content restriction.

## Comparing different ages

The separate example is:

> Why don't skeletons fight? Because they have no guts.

It was identified as a joke at every tested age. Guts refers both to courage and to the internal organs absent from a skeleton. The joke decision remains the same; familiarity, comprehension, and content sensitivity change the recommendation.

| Age | Courage meaning | Internal-organ meaning | Understanding the switch | Content | Recommendation |
| --- | --- | --- | --- | --- | --- |
| [5](gpt6_1_sol_v3_request_rerun_2026_10_08/age_predictions.md#guts-age-5) | May need explanation | May need explanation | Needs explanation | Review recommended | Review content first |
| [8](gpt6_1_sol_v3_request_rerun_2026_10_08/age_predictions.md#guts-age-8) | May need explanation | Likely familiar | Needs explanation | Suitable | Explain meanings and wordplay first |
| [12](gpt6_1_sol_v3_request_rerun_2026_10_08/age_predictions.md#guts-age-12) | Likely familiar | Likely familiar | Likely understood | Suitable | Provisionally suitable |
| [16](gpt6_1_sol_v3_request_rerun_2026_10_08/age_predictions.md#guts-age-16) | Likely familiar | Likely familiar | Likely understood | Suitable | Provisionally suitable |
| [30](gpt6_1_sol_v3_request_rerun_2026_10_08/age_predictions.md#guts-age-30) | Likely familiar | Likely familiar | Likely understood | Suitable | Provisionally suitable |

At **age 5**, both meanings may need explanation, and the saved prediction recommends reviewing the skeleton, fighting, and internal-organ references for sensitivity despite their non-graphic treatment. At **age 8**, the body-part meaning is likely familiar, but the courage idiom may need explanation; the content is marked suitable. At **ages 12, 16, and 30**, both meanings and their connection are judged likely to be understood, with suitable content.

These five judgments do not establish that the joke becomes understandable or suitable at one exact age. They illustrate how a recommendation can depend on a particular meaning, inference, or subject. Additional texts and independent audience feedback would be needed to evaluate how well these estimates work.

## Disagreements and review ratings

Two items differ from their reference joke labels. For this report, the review rating describes the interpretation problem: **0 = agreement**, **1 = supported meanings with an ambiguous comic connection**, and **2 = an intended reading is not adequately grounded in the text**. These are editorial review ratings added for discussion, not independent human annotation or a measured explanation-quality score.

| Item | Reference label | Saved decision | Review rating | Reason |
| --- | --- | --- | --- | --- |
| [J20 / T021](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md#t021), jewel and ring | Joke | Not a joke | **2 — substantive grounding problem** | A jewel can be associated with a jewelry ring, but that association does not establish a second ring reading that explains going to school to ring a bell. |
| [J11 / T040](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md#t040), mattress and spring training | Joke | Uncertain | **1 — ambiguous comic connection** | Both the mattress-coil and seasonal-training readings are plausible, but the connection between training and the overstuffed mattress's happiness remains unclear. |

Both count against joke recall. The reference labels have not been changed. The founder/desert item was accepted in this test; its abandon meaning still received an age-specific explanation recommendation.

## Evidence and limits

The latest saved assessment used **GPT-6.1 Sol** in a fresh Codex process, supplied with the full saved request and text/age inputs. Gold labels and previous predictions were excluded from the request. The reference annotations were used afterward to score the saved decisions.

The collection was authored and discussed during development, so a fresh process does not turn it into an independently held-out benchmark. Joke-detection accuracy does not measure age-of-acquisition accuracy, individual understanding, or content suitability. There are no independent child-comprehension observations or human age-suitability ratings in the saved data.

For each item's exact meanings, evidence, and age reasons, see the [readable corpus predictions](gpt6_1_sol_v3_request_rerun_2026_10_08/predictions.md) and [age comparison](gpt6_1_sol_v3_request_rerun_2026_10_08/age_predictions.md). The [saved metrics](gpt6_1_sol_v3_request_rerun_2026_10_08/metrics.json), [submitted request](gpt6_1_sol_v3_request_rerun_2026_10_08/request.md), and [run record](gpt6_1_sol_v3_request_rerun_2026_10_08/run_manifest.json) provide the supporting record.

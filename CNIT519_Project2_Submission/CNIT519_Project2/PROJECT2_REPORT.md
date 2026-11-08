# Project 2: Detecting phonetic wordplay: extending the homograph joke detector

## Project summary

Project 1 asked whether a text uses **one written word in two meanings** to make a coherent joke. Project 2 extends that to **sound-based wordplay**: two different words or phrases that are pronounced the same or almost the same, such as *night* and *knight*. The rule carried through the whole project is that **sound is not humor**. A high sound-similarity score only opens a *candidate*, a possible pun. The Project 1 meaning, evidence and incongruity checks decide whether the text is actually a joke.

What Project 2 adds is a runnable phonetic module: pronunciations from the CMU Pronouncing Dictionary, a **graded** similarity score between 0 and 1 (not a yes/no match), and a function that ranks similar-sounding candidates from a vocabulary. The module produces the six scores the assignment required, and it was applied to the three instructor texts plus two further examples written by the team.

This is **not** a complete automatic joke classifier. The phonetic module and the Project 1 language-model checks are not yet connected, and no blind Project 2 classification run has been done. The report therefore makes **no accuracy claim** for Project 2. The only detection figures below (96.0% accuracy, 94.74% F1) are Project 1 results on its authored 50-text collection and are not evidence of Project 2 performance.

## What counts as phonetic wordplay?

A candidate is a word, phrase or meaningful substring whose sound could be read as a second expression. A phonetic joke needs three things beyond the sound resemblance:

1. a **setup** that supports the first reading,
2. a **second reading** that the sound invites and the context supports,
3. an **unexpected connection** between the two that explains the punchline.

For example, a sentence that says "the baker thought the recipe said *flower*" works because the baking context supports *flour* and the substitution creates a surprise. A sentence that merely lists "*flour* and *flower*" in a pronunciation exercise has identical sound similarity but no comic reinterpretation, so it is not a joke. Weak or partial cases are reported as weak rather than relabelled as jokes.

## Method

### Components

| Component | Source | Role |
| --- | --- | --- |
| Input validation, text segmentation, candidate selection | Project 1 | Screen records, find the words or spans that could carry wordplay |
| Meaning ambiguity, evidence and connection checks | Project 1 | Decide whether both readings are supported and explain the switch |
| Age-of-acquisition and content suitability | Project 1 | Not rerun in Project 2 |
| **Phonetic candidate retrieval** | **New** | `find_similar_utterances(word, vocabulary, min_similarity=0.70, top_k=20)` returns possible sound-alikes |
| **Phonetic similarity score** | **New** | Graded 0–1 score from a weighted alignment of pronunciations |

### Representing sound

Each word is converted to **ARPAbet** (a symbol for each English sound) using the CMU Pronouncing Dictionary through the Python `cmudict` package. For example, *cat* is K AE T and *drama* is D R AA M AH. The first dictionary pronunciation is used, and stress digits are removed. A phrase is converted word by word and the sounds are joined. A word missing from the dictionary raises an error and is skipped by the retrieval function. There is deliberately **no fallback to spelling**, because that would hide errors.

The library supplies pronunciations only. The similarity measure is the team's own design.

### Graded sound costs

Let a change from one sound to another have a cost between 0 and 1:

| Change | Cost |
| --- | --- |
| Identical sounds | 0 |
| Insert or delete a sound | 1 |
| Vowel ↔ consonant | 1 |
| Two vowels | min(0.95, 0.20 + 0.16 × height difference + 0.14 × backness difference) |
| Two consonants | min(1, 0.20 + 0.35 × [manner differs] + 0.25 × [place differs] + 0.20 × [voicing differs]) |

*Manner* is how the air flows (a stop such as T, a hiss such as S), *place* is where in the mouth the sound is made, and *voicing* is whether the voice box buzzes. For example, T → D costs 0.40 (only voicing differs), AE → IH costs 0.52 (two steps in tongue height), and T → SH costs 0.80 (manner and place both differ). The vowel coordinates are hand-assigned categories, not measured acoustic data.

### Alignment and score

The distance D between two pronunciations is the cheapest total cost of turning one into the other with swaps, insertions and deletions (a weighted Levenshtein distance, computed by dynamic programming in O(mn) time). It is converted to a similarity:

**S = max(0, 1 − D / max(m, n))**, where m and n are the numbers of sounds.

S = 1 means identical sounds and S = 0 means nothing alike on this scale. S is a ranking score, not a calibrated measure of human perception.

### Why this method was expected to give adequate results

This is a design rationale, not a measured result.

- **Pronunciation, not spelling.** Puns depend on sound. *Night* and *knight* are spelled differently but identical in ARPAbet, so spelling-based matching would miss them and would also match look-alikes that sound different.
- **Graded costs.** Real substitutions differ in size: T and D differ in one feature and T and SH in two. A yes/no match cannot express that, and a graded cost can.
- **Edit distance.** Puns often change, add or drop a sound (*drum* / *drama*), and alignment handles words of different lengths. Normalizing by the longer word keeps short and long pairs on the same 0–1 scale.
- **Transparent.** Every score can be traced to specific sounds, which suits an exploratory baseline.
- **Sound proposes, meaning decides.** Sound similarity is easy to measure but says nothing about humor. Because the Project 1 checks make the final call, a sound-based false alarm should be caught at the next stage.

### Known limits of the method

- The cost weights and vowel positions were chosen by hand and have **not** been validated against human similarity ratings.
- The 0.70 retrieval cutoff is exploratory and was not tuned.
- Only the first, mostly US English, CMU pronunciation is used. Dialects, stress, rhythm and invented words are not modelled.
- Retrieval is limited to words in the dictionary.

## Required pair scores

Computed by `phonetics.py` and saved in `required_pairs.csv`.

| Pair | Sounds | Distance D | Similarity S |
| --- | --- | ---: | ---: |
| cat / cad | K AE T / K AE D | 0.40 | 0.8667 |
| cat / cash | K AE T / K AE SH | 0.80 | 0.7333 |
| drum / drama | D R AH M / D R AA M AH | 1.50 | 0.7000 |
| knight / night | N AY T / N AY T | 0.00 | 1.0000 |
| bat / pat | B AE T / P AE T | 0.40 | 0.8667 |
| pat / pit | P AE T / P IH T | 0.52 | 0.8267 |

The ordering matches the sound differences. A single voicing change (cat/cad, bat/pat) scores higher than a change in both manner and place (cat/cash). Knight/night scores 1.0 because the silent *k* adds no sound. Drum/drama scores lower because a vowel changes and a whole sound is added.

## Qualitative analysis of five probe texts

The first three are the instructor's. The last two were written by the team and are **not** instructor-provided. Judgments are manual and are not classifier predictions.

| # | Text | Pair | S | Judgment |
| --- | --- | --- | ---: | --- |
| 1 | "When the band broke up, it wasn't drama — it was just drum!" | drum / drama | 0.7000 | **Weak / uncertain.** Music context and a breakup fit, but "it was just drum" is unnatural and does not explain the breakup. |
| 2 | "Why did the cat stop dating the cad? Because she realized he way only purr-suing her for his own gain!" | cat / cad | 0.8667 | **Plausible joke.** The pun is *purr-suing* / *pursuing*, supported by the feline dating scenario. The cat/cad score is not the reason. "He way" is read as a typo for "he was". |
| 3 | "Why did the cat start working at a bank? Because she wanted to turn her cat-nap into cash." | cat / cash | 0.7333 | **Weak / unsupported.** Cat-nap fits the animal theme and cash fits the bank, but no sound-based reading explains why a nap becomes money. |
| 4 | "My broker offered to help me up the mountain with an asset." | ascent / asset | 0.7320 | **Weak / unsupported.** Mountain imagery cues *ascent* and finance cues *asset*, but nothing establishes an intentional substitution. |
| 5 | "The school wanted principles in the office. Three rules to get a job. None has returned the parent's call." | principal / principles | 0.9000 | **Plausible joke.** School context cues *principal*, and the unanswered calls turn the rulebooks into administrators who cannot do the job. Independent human ratings are still needed. |

Reading across the five, the weak cases score 0.70–0.73 and the plausible ones 0.87 and 0.90. That pattern is only five hand-judged examples, so it is a suggestion, not a finding. Probe 2 shows why: it is plausible because of *purr-suing*, not because its cat/cad score is high.

**About *purr-suing*.** The scorer splits text on non-letters, so *purr-suing* would be read as the two dictionary words *purr* and *suing*, joined. That likely gives a sound very close to *pursuing*, but this was **not run** for the report, and the required results score only cat/cad. Words that are truly absent from the dictionary raise an error and are skipped by the retrieval function.

Probes 4 and 5 are not in `evaluation.csv` or the earlier submitted report, which list only three probes. Their scores were checked by hand (ascent/asset D = 1.34; principal/principles D = 1, one added sound).

## Interpretation of results

The observations below rest on six computed pairs, five hand-judged probes and an authored dataset. They are observations and hypotheses, not conclusions.

### What works

- **The graded score ranks sound differences sensibly.** A single voicing change (cat/cad, bat/pat, 0.8667) scores above a change in both manner and place (cat/cash, 0.7333), and homophones score 1.0. A yes/no match would call most of these pairs simply "different".
- **Separating sound from meaning gives a sensible division of labour.** Sound finds candidates cheaply, and the Project 1 checks decide whether a candidate is a joke.

### What does not work, and why

- **Sound similarity alone does not identify jokes.** Cat/cash (0.7333) and ascent/asset (0.7320) are retrievable candidates but weak jokes. A joke needs a second reading that the *context* supports and that explains the punchline, and the score contains no information about context. This is the main finding, and it is why the Project 1 checks are retained.
- **The score can mislead in both directions.** Cat/cad scores high, but the joke works because of *purr-suing*, a pun the cat/cad score never sees. Drum/drama scores 0.70, yet it is weak because of unnatural grammar. In both cases the cause lies outside what the phonetic score measures.
- **The graded score is untested on most of the dataset.** All 46 positive and negative records are exact homophones (S = 1.0), so the data cannot show whether similarity separates jokes from non-jokes. Five probes are too few to say.
- **The negatives may be too easy.** They all use one template, so a classifier could separate them by wording rather than by understanding, which would overstate success.
- **Plausible jokes scored higher than weak ones in the probes** (0.87 and 0.90 against 0.70–0.73), but with five examples this may be chance. Principal/principles also scores highly partly because it is a long word pair with one added sound, which the length-normalized score rewards.

### Likely reasons for failures, and how each could be checked

These are untested hypotheses.

| Possible reason | How to check |
| --- | --- |
| Hand-chosen weights and vowel positions do not match human judgments of similarity | Compare scores with human similarity ratings and tune the weights on held-out data |
| The 0.70 cutoff is arbitrary and lets in weak candidates | Measure retrieval recall and precision at several cutoffs on labelled data |
| One US English pronunciation per word misses other readings | Compare scores using alternative pronunciations |
| Invented puns such as *purr-suing* fall outside the dictionary or are split into separate words | Score *purr-suing* / *pursuing* directly and test words that are not in the dictionary |
| Authored labels and a single negative template inflate apparent success | Have blind annotators label the texts and vary the negative templates |

## Dataset

`evaluation.csv` has **49 records**:

| Class | Count | Description |
| --- | ---: | --- |
| Positive (P01–P23) | 23 | Authored sound-play jokes, each built on a homophone pair |
| Negative (N01–N23) | 23 | Matched literal sentences with the same word pair |
| Supplied probe (S24–S26) | 3 | The instructor's three texts |

Each negative has the form *"The dictionary exercise listed "A" and "B" as two entries to compare for pronunciation."* It keeps the pair and its sound similarity but removes the comic reinterpretation. This tests the principle that **sound resemblance alone must not trigger a positive label**.

**Important limits of the dataset:**

- **Labels are authored intentions**, not independent annotations or classifier outputs. Some jokes may be less funny or natural than others.
- **Every one of the 23 positive and 23 negative pairs is an exact homophone, with similarity 1.0.** The six required pairs and the three probes supply all of the graded range. As a result, the 46 positive and negative records do not exercise the graded score at all, and similarity does not separate positives from negatives in this data.
- The negatives share one template, so a model could separate them by wording alone rather than by understanding.
- The five-probe sample and the six required pairs are too small for statistical claims.
- The stored cat/cad text reads "he was"; the assignment and slides read "he way".

A fuller assessment against the Klie et al. quality framework and the Mahowald et al. formal/functional competence distinction is in `DATASET_QUALITY_AND_COMPETENCE_ANALYSIS.md`.

## Evidence and limits

- **From Project 1 (not rerun):** 50 authored texts, 20 intended jokes and 30 non-jokes. 18 jokes were accepted, 30 of 30 non-jokes were rejected, one joke was rejected and one was uncertain. Accuracy was 96.0%, precision 100%, recall 90%, F1 94.74%. A majority-class baseline gets 60%. These come from the saved Project 1 files on an authored collection, not an independent benchmark. Age checks at 5, 8, 12, 16 and 30 were also saved and remain provisional, with no verified acquisition ages.
- **New in Project 2:** a runnable phonetic module, six computed required scores, five qualitatively judged probes, and a 49-record dataset.
- **Not done:** automatic extraction of novel puns, integration with the Project 1 language-model judge, a blind classification run, validation of the weights against human ratings, and reporting of accuracy or F1 for Project 2.

## Next steps

1. Connect the phonetic candidates to the Project 1 meaning, evidence and incongruity checks, and freeze prompts, threshold and dataset before scoring.
2. Validate the similarity scores against human similarity ratings and tune the weights and the 0.70 cutoff on held-out data.
3. Score the *purr-suing* / *pursuing* pair and add handling for words that are not in the dictionary.
4. Add near-homophone positives and negatives so the graded score is actually tested, vary the negative templates, and have blind annotators label the dataset.
5. Evaluate retrieval recall at K, the semantic connection on negative pairs, and final precision, recall and F1 with a confusion matrix.

## How to reproduce

```bash
pip install cmudict
python phonetics.py          # prints the six pair scores
python build_evaluation.py   # rebuilds required_pairs.csv and evaluation.csv
```

Run from the `CNIT519_Project2` folder and compare the output with the bundled CSVs.

## References

- CMU Pronouncing Dictionary, Carnegie Mellon University, accessed through the Python `cmudict` package.
- Levenshtein-style dynamic programming, adapted with author-defined phoneme-feature substitution costs as specified above.
- CNIT 519 Project 1 report and saved files, the source of every Project 1 figure.

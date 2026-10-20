# CNIT 519 — Project 2: Semantic and Phonetic Wordplay Detection

## 1. Objective and continuity with Project 1

This project extends the submitted Project 1 approach to detect jokes based on either **meaning ambiguity** (same spelling, two supported meanings) or **sound-based wordplay** (different forms with similar pronunciations, both supported by the context). Similarity alone is not evidence of a joke. A joke must additionally supply a plausible setup, a reinterpretation/punchline, and an incongruity resolved by the alternate interpretation. Partial failures and weak examples should be reported rather than automatically relabeled as jokes.

The Project 1 archive contains the written `request_llm_procedure.md`, corpus, saved model predictions and reports, but no independently reusable program implementing the Project 1 language-model decision. Project 2 thus provides a **runnable phonetic-candidate and similarity module** plus a documented semantic decision rubric. It does **not** falsely claim to have reproduced the original language-model classification run or implemented a complete automatic joke classifier. A prospective full system would connect the phonetic module to the existing meaning/evidence/connection prompts and evaluate its predictions without revealing reference labels.

## 2. Component decomposition, method, motivation, evidence

| Component | Goal | Method | Why appropriate | Current result/evidence |
|---|---|---|---|---|
| 1. Input validation | Screen records and track age | Project 1 schema: `id`, `text`, age 0–120 | Avoids interpreting malformed records as non-jokes | Project 1 decision prompt saved; not rerun in Project 2 |
| 2. Text/utterance identification | Surface exact words, idioms, substrings and candidate pairs | Project 1 candidate-selection instructions plus token/phrase segmentation | Wordplay spans can be phrases and playful subwords | Project 1 corpus includes 50 records; Project 2 dataset provides explicit candidate pairs for reproducible pair scoring |
| 3. Semantic ambiguity identification | Find distinct senses for an identical expression | Project 1 language-model meaning gate, textual quotes, and evidence checks | Prevents dictionary ambiguity alone from counting | Project 1 50-text test: 18/20 positives accepted, 30/30 negatives rejected, one positive rejected, one uncertain |
| 4. **Phonetic candidate retrieval (NEW)** | Find different utterances pronounced identically or nearly so | CMU Pronouncing Dictionary ARPAbet pronunciations; `find_similar_utterances()` ranks a supplied vocabulary, threshold 0.70 | Pronunciations are more reliable than raw character overlap; ranked retrieval offers candidates for a later semantic check | Runnable implementation; pairs above threshold include the six specified pairs; open-vocabulary retrieval is limited by dictionary coverage |
| 5. **Phonetic similarity (NEW)** | Assign continuous rather than binary similarity | Custom articulatory-weighted Levenshtein alignment on dictionary phone sequences | Related vowels, place/manner neighbors, and voicing contrasts receive different costs; insertions/deletions capture different-length words | Six exact numeric comparisons in `required_pairs.csv` |
| 6. Semantic connection / incongruity | Test whether both readings are supported and whether their switch explains the unexpected outcome | Retain Project 1 three gates (meaning; contextual evidence; explanatory connection), extended to two related-sounding strings | Separates phonetic resemblance from humorous use | Manual qualitative analysis of three teacher examples; full automatic integration not yet validated |
| 7. Age suitability | Identify unfamiliar senses, switch difficulty, and inappropriate content | Project 1 age-specific rubric and separate suitability gate | Vocabulary comprehension and humor recognition are different constructs | Saved Project 1 assessed 20 jokes at 5, 8, 12, 16, 30 = 100 judgments; Project 2 did not rerun age judgments |
| 8. Evaluation | Check retrieval, scores, and false positives from sound alone | Six required pairs, 23 intended positive and 23 matched negative texts, 3 assigned probes | Paired negative examples keep sound overlap while eliminating comic reinterpretation | 49 labeled/probe records in `evaluation.csv`. Labels represent authored intentions, NOT blind classifier predictions |

### Original Project 1 detection evidence

20 intended jokes / 30 negatives. In the saved run, 18 true positives, 0 false positives, 30 true negatives, 1 rejected positive, 1 uncertain positive. With `uncertain` counted as non-joke, strict accuracy = 48/50 = **96.0%**; precision **100.0%**, recall **90.0%**, F1 **94.74%**. These are *Project 1* in-sample authored-corpus results, not a measured Project 2 success rate. Sense-specific numerical acquisition ages were not verified in the original archive.

## 3. Phone representation, exact formula, and implementation

The Python package `cmudict` provides first dictionary pronunciation in **ARPAbet** for each orthographic word, e.g. `cat = K AE T`. Phoneme stress digits are removed before scoring. No existing similarity metric is used; the following is an explicitly specified custom weighted dynamic-programming algorithm in `phonetics.py`.

Let A = (a₁, …, aₘ), B = (b₁, …, bₙ) be phoneme sequences. Set insertion/deletion cost to 1 and define substitution cost c(a,b):

- Identical phones: c = 0.
- Two vowels: c = min(0.95, 0.20 + 0.16×|heightₐ−heightᵦ| + 0.14×|backnessₐ−backnessᵦ|), with illustrative hand-coded categorical vowel coordinates (`VFEAT` in code). These coordinates are not empirical acoustic formant data.
- Two consonants: c = min(1, 0.20 + 0.35×I[manner differs] + 0.25×I[place differs] + 0.20×I[voicing differs]). `I` is 1 if true and 0 otherwise.
- Vowel ↔ consonant: c = 1.

The weighted Levenshtein recurrence is:

`D(0,j)=j`, `D(i,0)=i`

`D(i,j) = min { D(i−1,j)+1, D(i,j−1)+1, D(i−1,j−1)+c(aᵢ,bⱼ) }`.

The normalized score is **S(A,B) = max(0, 1 − D(m,n)/max(m,n))**, between 0 (completely different under this scale) and 1 (identical phone sequence). The score is not a calibrated perceptual probability. The exploratory 0.70 retrieval cutoff is not optimized on independent training data. Complexity per pair is O(mn) time and O(mn) memory, where m,n are phone counts. For phrases, the component concatenates each word's pronunciation, enabling cross-word comparison, but does not model liaison, stress, rhythm or prosody.

**Known limits:** Fixed handcrafted phonological features are a useful graded baseline but only a rough model of human phonetic perception. The chosen first CMU pronunciation is mostly US English; dialects, alternative readings, unstressed vowels and neologisms may differ. OOV words raise an explicit exception rather than secretly falling back to spelling. The custom pair scores depend on these stated design choices; they are not library-provided metrics.

## 4. Required numeric scores (computed by the included Python implementation)

| Pair | ARPAbet transcription | Weighted distance D | Normalized similarity S |
|---|---|---:|---:|
| cat / cad | K AE T / K AE D | 0.40 | 0.8667 |
| cat / cash | K AE T / K AE SH | 0.80 | 0.7333 |
| drum / drama | D R AH M / D R AA M AH | 1.50 | 0.7000 |
| knight / night | N AY T / N AY T | 0.00 | 1.0000 |
| bat / pat | B AE T / P AE T | 0.40 | 0.8667 |
| pat / pit | P AE T / P IH T | 0.52 | 0.8267 |

These scores preserve meaningful contrasts: /t/ and /d/ are the same manner/place and differ in voicing, while /t/ and /ʃ/ differ more; `knight` and `night` are homophones. The word `drama` differs from `drum` in both vowel quality and a final additional syllable, reflected in a smaller similarity.

## 5. Analysis of instructor-provided examples (qualitative manual judgments)

**(A) “When the band broke up, it wasn’t drama — it was just drum!”** Candidate: drum / drama; S = 0.7000. The band and word *drum* provide a music context; *drama* suggests interpersonal conflict. However, “it was just drum” is syntactically unnatural and does not itself explain the breakup. **Judgment: weak/uncertain phonetic joke**, not an unqualified success. An independent rater should decide whether the incongruity is resolved.

**(B) “Why did the cat stop dating the cad? Because she realized he way only purr-suing her for his own gain!”** Candidate: cat / cad; S = 0.8667. The cat and cad form a nearby pair, but the **central pun** is “purr-suing” versus “pursuing”: an animal-associated purr is blended into the verb pursuing. The supplied phrase “he way” appears to be a typo for “he was”; the quoted source text should remain unaltered in the test set. **Judgment: plausible phonetic/compositional joke** supported by feline context and the dating scenario; the cat/cad pair alone does not establish the joke. The novel “purr-suing” spelling is OOV in standard CMU and needs an explicit pronunciation/segmentation strategy before automatic scoring.

**(C) “Why did the cat start working at a bank? Because she wanted to turn her cat-nap into cash.”** Candidate: cat / cash; S = 0.7333. Cat-nap supports the animal theme and cash the bank theme, but they do not provide an evident sound-based substitution whose alternate reading explains why sleeping becomes money. **Judgment: weak/unsupported as a phonetic joke on the supplied wording**; mere similarity between *cat* and *cash* is insufficient.

This deliberately separates **phonetic score** from **comic-connection decision**, avoiding inflated results on instructor prompts.

## 6. New stimuli: 23 positives and 23 negatives

The attached `evaluation.csv` contains **23 intended positive sound-play jokes** and **23 parallel negative examples**. The negative sentence for each pair reports that the two expressions appeared in a dictionary pronunciation comparison: the utterance pair is equally similar, but there is no surprise, incompatible interpretation, or resulting joke. This is a controlled test of the principle that *sound resemblance alone must not trigger a positive label*.

The three instructor examples appear as an **additional three separate probes**, producing **49 total records**, not 49 scored automatic classification outcomes. The 23 intended jokes are authored examples and some may be less humorous or linguistically natural than others. A human annotation/quality pass, preferably blind to the expected label, is a next step before valid accuracy/F1 reporting.

## 7. Integration and evaluation protocol

1. Run the original Project 1 input, candidate selection, semantic analysis and age checks unchanged for the old homograph corpus.
2. For new texts, identify salient words and potential subword expressions; generate similar-pronunciation candidates with CMU plus a documented G2P/segmentation fallback for non-dictionary wordplay.
3. Calculate continuous phonetic S and retain top K above a prespecified threshold; never classify a joke using S alone.
4. For each pair, collect two reading-specific context quotes and ask whether the alternate reading resolves a surprising action, answer, or mismatch. Reject literal comparisons.
5. Predict `semantic`, `phonetic`, `mixed`, `non_joke`, or `uncertain`, with a short evidence trace; separately rate age comprehension and content suitability.
6. Freeze the prompts, threshold, and dataset before scoring. Evaluate each component separately: retrieval recall@K; scores on homophones and near pairs; semantic connection accuracy on negative pairs; final joke precision/recall/F1 and confusion matrix; age calibration only with ground truth evidence.

**What is completed:** exact documented sound formula; executable scoring and candidate-ranking functions; six required computed comparisons; qualitative three-case analysis; 23 positive and 23 negative stimuli; reuse and documentation of Project 1 methods and existing results. **What remains:** fully automatic extraction/segmentation for novel puns, integration into the original LLM semantic judge, and a blind Project 2 classification run. Consequently this submission makes no unverified new classifier accuracy claim.

## 8. How to reproduce

Python with `cmudict` installed:

```bash
pip install cmudict
python phonetics.py
python build_evaluation.py
```

Run from the `CNIT519_Project2` folder. The first command prints the six pair scores; the second reconstructs `required_pairs.csv` and `evaluation.csv`. Compare the generated files to the bundled CSVs. The original Project 1 files are retained in the independently supplied Project 1 archive; this submission does not overwrite them.

## 9. Reference resources

- CMU Pronouncing Dictionary, Carnegie Mellon University, ARPAbet word-to-phone lexicon (accessed locally through Python `cmudict`).
- Levenshtein-style dynamic programming, adapted here with author-defined phoneme-feature substitution penalties; equations fully specified in Section 3.
- Original supplied CNIT519 Project 1 archive: `report.md`, `request_llm_procedure.md`, `corpus.md`, and saved predictions. All reported Project 1 statistics originate from those saved files.

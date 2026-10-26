"""Validate generated records and report phonetic diagnostics, not a humor model."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import mean, median

from build_evaluation import (PAIRS, REQUIRED_PAIRS, ORIGINAL_SECOND_WORDS,
                              build_rows, build_variants, validate_joke_text,
                              has_formulaic_opening)
from phonetics import LEXICON, compare, find_similar_utterances, phonemes

ROOT = Path(__file__).resolve().parent

# Qualitative editorial comments by the same author who wrote the stimuli.
# These are not blind annotations or classifier predictions.
REVIEW_NOTES = {
    ('stationary', 'stationer'): 'Review recommended: the job of the paper-goods supplier supports the absurd bicycle, but the implicit adjective-to-person sound substitution is loose.',
    ('discreet', 'discredit'): 'Review recommended: the mishearing also changes the grammatical instruction; sound alone does not establish the intended joke.',
    ('council', 'counsels'): 'Review recommended: the therapist and potholes supply an absurd situation, but the change from a noun to a verb makes this a looser substitution.',
    ('elicit', 'solicit'): 'Review recommended: drawing out and asking for a response overlap in meaning. The fundraising context must do the work of separating the readings.',
    ('medal', 'middle'): 'Review recommended: the inferred sporting phrase and explicit halfway instruction differ in articles as well as pronunciation.',
    ('appraise', 'apprised'): 'Review recommended: the natural implicit reading would use an inflected first word; scores here still compare the supplied candidate words, not complete spoken sentences.',
    ('ingenious', 'ingenue'): 'Weak phonetic candidate: below 0.70. The theater context explains the meaning switch but does not repair the sound mismatch.',
    ('collaborate', 'corroborates'): 'Weak phonetic candidate: below 0.70. This remains an authored near-sound experiment, not a successful retrieval at the configured cutoff.',
}


def read_csv(name):
    with (ROOT / name).open(encoding='utf-8', newline='') as source:
        return list(csv.DictReader(source))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def threshold_metrics(rows, threshold):
    tp = fp = tn = fn = 0
    for row in rows:
        actual = row['reference_class'] == 'positive'
        predicted = float(row['similarity']) >= threshold
        if actual and predicted:
            tp += 1
        elif predicted:
            fp += 1
        elif actual:
            fn += 1
        else:
            tn += 1
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {
        'threshold': threshold, 'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn,
        'accuracy': (tp + tn) / len(rows), 'precision': precision, 'recall': recall,
        'f1': 2 * precision * recall / (precision + recall) if precision + recall else 0.0,
    }


def main():
    rows = read_csv('evaluation.csv')
    by_id = {row['id']: row for row in rows}
    require(len(rows) == 2 * len(PAIRS) == len(by_id), 'Wrong record count or duplicate IDs')
    require(Counter(row['reference_class'] for row in rows) ==
            {'positive': len(PAIRS), 'negative': len(PAIRS)}, 'Unbalanced labels')
    expected_rows = build_rows()
    for actual, expected in zip(rows, expected_rows):
        require(actual == {key: str(value) for key, value in expected.items()},
                f'Stale or mismatched generated row: {actual["id"]}')

    variants = build_variants()
    require(read_csv('pair_variants.csv') ==
            [{key: str(value) for key, value in variant.items()} for variant in variants],
            'Stale or mismatched variant audit')
    require(len(ORIGINAL_SECOND_WORDS) == len(PAIRS), 'Missing original word provenance')

    pairs = []
    vocabulary = sorted({word for a, b, *_ in PAIRS for word in (a, b)})
    retrieval_ranks = []
    for idx, (a, b, joke, note) in enumerate(PAIRS, 1):
        original_b = ORIGINAL_SECOND_WORDS[a]
        require(b not in (a, original_b), f'Second word unchanged or collapsed into first word: {a}/{b}')
        require(b in LEXICON, f'Replacement missing from installed dictionary: {b}')
        validate_joke_text(a, b, joke)
        variant = variants[idx - 1]
        require(variant['letter_edits'] > 0, 'Replacement must change spelling')
        score = compare(a, b)
        require(0 <= score['similarity'] <= 1, f'Score out of range: {a}/{b}')
        require(score['similarity'] == compare(b, a)['similarity'], 'Asymmetric similarity')
        require(compare(a, a)['similarity'] == compare(b, b)['similarity'] == 1,
                'Identity comparison failed')
        positive, negative = by_id[f'P{idx:02d}'], by_id[f'N{idx:02d}']
        require(positive['similarity'] == negative['similarity'], 'Unmatched control score')
        ranked = find_similar_utterances(a, vocabulary, min_similarity=0.70,
                                        top_k=len(vocabulary))
        rank = next((i for i, result in enumerate(ranked, 1) if result['b'] == b), None)
        retrieval_ranks.append(rank)
        pairs.append({
            'id': positive['id'], **score,
            'original_b': original_b, 'letter_edits': variant['letter_edits'],
            'original_similarity': variant['original_similarity'],
            'similarity_change': variant['similarity_change'],
            'second_word_similarity': variant['second_word_similarity'],
            'meets_cutoff': score['similarity'] >= 0.70,
            'phone_relation': 'identical' if phonemes(a) == phonemes(b) else 'near',
            'joke': joke, 'connection': note, 'retrieval_rank': rank,
            'second_word_only': True,
            'structure': 'question_answer' if has_formulaic_opening(joke) else 'prose_or_dialogue',
            'editorial_review': REVIEW_NOTES.get((a, b),
                'Plausible authored substitution; independent humor rating still needed.'),
        })

    required = read_csv('required_pairs.csv')
    expected_required = [compare(a, b) for a, b in REQUIRED_PAIRS]
    require(required == [{key: str(value) for key, value in result.items()}
                         for result in expected_required], 'Required comparisons are stale')
    require([float(row['similarity']) for row in required] ==
            [0.8667, 0.7333, 0.7, 1.0, 0.8667, 0.8267], 'Six baseline scores changed')
    require(compare('currant', 'current')['similarity'] == 1, 'Currant supplement failed')
    try:
        phonemes('zzzznotawordzzzz')
    except KeyError:
        pass
    else:
        raise ValueError('Unknown words should still raise KeyError')

    scores = [p['similarity'] for p in pairs]
    original_scores = [p['original_similarity'] for p in pairs]
    edit_counts = Counter(p['letter_edits'] for p in pairs)
    below_cutoff = [p for p in pairs if not p['meets_cutoff']]
    structure_counts = Counter(p['structure'] for p in pairs)
    require(structure_counts['prose_or_dialogue'] > len(pairs) / 2,
            'Most jokes must avoid Why/Because openings')
    relation_counts = Counter(p['phone_relation'] for p in pairs)
    threshold_results = [threshold_metrics(rows, cutoff)
                         for cutoff in (0.70, 0.85, 0.90, 0.95, 1.0)]
    retrieval = {f'recall_at_{k}': sum(rank is not None and rank <= k
                                    for rank in retrieval_ranks) / len(PAIRS)
                 for k in (1, 3, 5)}
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
              for name in ('evaluation.csv', 'required_pairs.csv', 'pair_variants.csv')}
    result = {
        'records': len(rows), 'unique_pairs': len(pairs),
        'labels': dict(Counter(r['reference_class'] for r in rows)),
        'phonetic_relations': dict(relation_counts),
        'letter_edit_counts': dict(edit_counts),
        'original_similarity_mean': mean(original_scores),
        'changed_second_words': len(pairs),
        'second_word_only_jokes': len(pairs),
        'joke_structures': dict(structure_counts),
        'below_cutoff': [f'{p["a"]}/{p["b"]}' for p in below_cutoff],
        'similarity': {'min': min(scores), 'max': max(scores),
                       'mean': mean(scores), 'median': median(scores),
                       'distinct_scores': len(set(scores))},
        'retrieval': {'vocabulary_size': len(vocabulary), 'threshold': 0.70, **retrieval},
        'sound_only_baseline': threshold_results, 'pair_analysis': pairs,
        'artifact_sha256': hashes,
        'limitations': [
            'First words and scoring formula are unchanged; all second words changed. Scores now compare each original first word with its new second word.',
            'Minimal workable spelling changes are editorial choices in a finite dictionary, not proof of a globally optimal pun. Some changes are inflections.',
            'Candidate pairs are supplied, not automatically extracted from jokes.',
            'Only the second candidate appears in each joke body; the first candidate is implicit. Pair metadata, annotations and literal controls retain both words.',
            'Some implicit readings require different articles or inflections; reported scores compare the candidate words, not whole sentences.',
            'Retrieval uses a fixed vocabulary made from the 27 known pairs, not an unseen corpus.',
            'Same-author qualitative comments are not independent evidence of humor.',
            'Threshold metrics evaluate an intentionally sound-only baseline on authored labels, not a semantic joke classifier.',
        ],
    }
    (ROOT / 'evaluation_analysis.json').write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    lines = [
        '# Project 2: evaluation of changed second words and rewritten jokes', '',
        'All 27 second words changed and all jokes were rewritten. Each original first word and the phonetic scoring formula are retained. '
        'Every joke has a literal comparison control: **54 records (27 intended positives, 27 negatives)**. '
        'The word changes are auditable in `pair_variants.csv`; the jokes and explanations are in `build_evaluation.py` and `evaluation.csv`.', '',
        '## Joke wording and structure', '',
        f'**{structure_counts["prose_or_dialogue"]} of {len(pairs)} jokes** open as prose or dialogue; '
        f'**{structure_counts["question_answer"]}** retain a question-and-answer opening. '
        'The jokes preserve a setup, an implicit first reading and a payoff using the second word, '
        'with short anecdotes, dialogue, ironic reversals and occasional traditional questions. '
        'Only the current second candidate is written in each joke; the first candidate must be inferred from its context. '
        'A case-insensitive whole-word check confirms that the first word is absent and the second is present. '
        'Candidate labels, explanatory annotations and dictionary-comparison negatives still name both words for evaluation; those are not joke bodies.', '',
        '## Spelling changes and original-score comparison', '',
        'The requested one-letter replacement is used where a meaningful distinct word is available. '
        'With the approved relaxation, a single insertion or deletion is also allowed, and a few words use larger edits. '
        'Names or spelling variants were not selected merely to get a high score. '
        'Real dictionary words, a distinct meaning, and a usable joke were required. '
        'This is a curated selection, not a claim of global minimum spelling distance over every English word.', '',
        f'- Edit-count distribution (letters inserted, deleted or substituted): {dict(sorted(edit_counts.items()))}.',
        '- `discrete -> discredit` and `ingenuous -> ingenue` need three edits; the installed dictionary supplied no usable distinct one- or two-edit alternatives. '
        '`canvass -> canvassed` retains the solicitation reading, avoiding `canvases`, which would merely pluralize the first word. '
        '`illicit -> solicit` and `averse -> obverse` use two edits to obtain usable real words with contextual meaning switches.',
        f'- Original mean similarity: **{mean(original_scores):.4f}**; new mean: **{mean(scores):.4f}**. '
        'Each new score compares the original first word with the replacement, not just the old and new second words. '
        'The latter comparison is recorded separately in the variant audit.', '',
        '| First word | Original second | New second | Letter edits | Original score | New score | Change |',
        '|---|---|---|---:|---:|---:|---:|',
    ]
    for pair in pairs:
        lines.append(f'| {pair["a"]} | {pair["original_b"]} | {pair["b"]} | {pair["letter_edits"]} | '
                     f'{pair["original_similarity"]:.4f} | {pair["similarity"]:.4f} | {pair["similarity_change"]:+.4f} |')
    lines += [
        '',
        '## Phonetic variety', '',
        f'- Identical stress-stripped phone sequences: **{relation_counts["identical"]}**. '
        f'Different phone sequences: **{relation_counts["near"]}**, under the selected dictionary pronunciations.',
        f'- {len(set(scores))} distinct scores; range **{min(scores):.4f}–{max(scores):.4f}**; '
        f'mean **{mean(scores):.4f}**, median **{median(scores):.4f}**.',
        f'- **{len(pairs) - len(below_cutoff)}/{len(pairs)}** meet the unchanged 0.70 cutoff. '
        'The rejected candidates remain in the authored dataset and are reported as misses rather than silently removed.',
        '- Below cutoff: ' + '; '.join(f'{p["a"]}/{p["b"]} ({p["similarity"]:.4f})' for p in below_cutoff) + '.',
        '- These are model-relative scores, not universal dialect judgments. The first CMU pronunciation is selected, stress is removed, '
        'and currant uses the documented pronunciation supplement. Alternate pronunciations are not searched.', '',
        '| Pair | Phones A | Phones B | Distance | Similarity | Relation |',
        '|---|---|---|---:|---:|---|',
    ]
    for pair in pairs:
        lines.append(f'| {pair["a"]} / {pair["b"]} | {pair["phones_a"]} | {pair["phones_b"]} | '
                     f'{pair["weighted_distance"]:.4f} | {pair["similarity"]:.4f} | {pair["phone_relation"]} |')
    lines += [
        '', '## Candidate retrieval', '',
        f'The fixed vocabulary contains {len(vocabulary)} unique words from the revised pairs. '
        'For each first word, retrieval ranks the other vocabulary words using the 0.70 cutoff. '
        'The expected partner is counted as found only when it appears within K results. '
        'This tests retrieval with known candidates, not automatic identification of a pun in free text.', '',
    ]
    for label, value in retrieval.items():
        lines.append(f'- {label.replace("_", " ")}: {value:.2%}')
    lines += [
        '', '## Diagnostic sound-only baseline', '',
        'The baseline predicts joke whenever pair similarity is at least the cutoff. '
        'It uses no sentence semantics. Metrics below compare this rule against the authored labels; '
        'they are not results from an integrated semantic classifier or a blind humor test. '
        'Joke and control share exactly the same pair, so every accepted joke also produces a false positive. '
        'Increasing the cutoff cannot distinguish members of a matched pair.', '',
        '| Cutoff | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 |',
        '|---:|---:|---:|---:|---:|---:|---:|---:|---:|',
    ]
    for metrics in threshold_results:
        lines.append(f'| {metrics["threshold"]:.2f} | {metrics["tp"]} | {metrics["fp"]} | '
                     f'{metrics["tn"]} | {metrics["fn"]} | {metrics["accuracy"]:.2%} | '
                     f'{metrics["precision"]:.2%} | {metrics["recall"]:.2%} | {metrics["f1"]:.2%} |')
    lines += [
        '', '## Qualitative analysis of every joke', '',
        'The following comments are an editorial review by the author of the jokes. '
        'They explain intended reading switches, not measured audience reactions. '
        f'{len(REVIEW_NOTES)} weaker phonetic or semantic connections are explicitly flagged for independent review.', '',
    ]
    for idx, pair in enumerate(pairs, 1):
        lines += [f'### {idx}. {pair["a"]} / {pair["b"]} — {pair["similarity"]:.4f}', '',
                  f'Original second word: {pair["original_b"]}; letter edits: {pair["letter_edits"]}.', '',
                  f'> {pair["joke"]}', '', pair['connection'], '', pair['editorial_review'], '']
    lines += [
        '## Validation and reproduction', '',
        'Validation checks all 54 records against the current authoring data, unique IDs, balanced labels, '
        'all 27 changed dictionary words, second-word-only joke text, a majority avoiding Why/Because openings, original-word provenance, variant audit, '
        'all saved scores and phones, identical joke/control scores, score range, symmetry and identity, '
        'the six unchanged required comparisons, the currant supplement, and explicit rejection of unknown words.', '',
        'Run from this folder with cmudict installed:', '',
        '```powershell', 'python phonetics.py', 'python build_evaluation.py',
        'python analyze_evaluation.py', '```', '',
        'If using the project-local dependency installation in this workspace, set '
        '`$env:PYTHONPATH = (Join-Path (Get-Location) ".project2_dependencies")` and use a working Python executable.', '',
        'The main finding is that the rewritten contexts create intended reinterpretations while the literal controls do not. '
        'Phonetic similarity supplies candidates but cannot establish that difference. '
        'Independent human annotation and integration of a semantic decision stage remain future work.', '',
    ]
    (ROOT / 'EVALUATION_ANALYSIS.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f'PASS: {len(rows)} records, {len(pairs)} pairs, all artifact and phonetic checks.')
    print(f'Phones: {dict(relation_counts)}; {len(set(scores))} scores; '
          f'range {min(scores):.4f}–{max(scores):.4f}; mean {mean(scores):.4f}.')
    print('Sound-only baseline at 0.70:', json.dumps(threshold_results[0]))
    print('Retrieval:', json.dumps(retrieval))
    print('Wrote EVALUATION_ANALYSIS.md and evaluation_analysis.json')


if __name__ == '__main__':
    main()

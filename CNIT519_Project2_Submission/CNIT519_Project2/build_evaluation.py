"""Build authored phonetic jokes and matched literal controls (not predictions)."""
import csv
import re
from pathlib import Path
from phonetics import compare

ROOT = Path(__file__).resolve().parent
# Retain each first word and record its original second word for comparison.
# New second words use the smallest workable real-word spelling changes.
# Joke bodies use only the second candidate; the first reading stays implicit.
# Reference positives are author intentions, not independently judged humor.
ORIGINAL_SECOND_WORDS = {'compliment': 'complement', 'stationary': 'stationery', 'principal': 'principle', 'discreet': 'discrete', 'council': 'counsel', 'ascent': 'assent', 'cereal': 'serial', 'palette': 'palate', 'capital': 'capitol', 'currant': 'current', 'marshal': 'martial', 'prophet': 'profit', 'medal': 'meddle', 'altar': 'alter', 'canvas': 'canvass', 'sensor': 'censor', 'allusion': 'illusion', 'appraise': 'apprise', 'elicit': 'illicit', 'emigrate': 'immigrate', 'prescribe': 'proscribe', 'adverse': 'averse', 'parameter': 'perimeter', 'ingenious': 'ingenuous', 'vocation': 'vacation', 'collusion': 'collision', 'collaborate': 'corroborate'}

PAIRS = [
    ('compliment', 'complements',
     "My math teacher tried to boost my self-esteem by listing everyone I wasn't. Apparently she's better at complements.",
     'The request for praise cues compliment implicitly; listing everyone outside the singleton containing the speaker supplies mathematical complements. The self-esteem setup reverses into set arithmetic.'),
    ('stationary', 'stationer',
     'The gym bought its exercise bikes from a stationer. Mine folds into an envelope; postage is the only thing going up.',
     'Exercise bikes cue stationary implicitly; stationer supplies writing materials. The envelope and postage turn a fitness purchase into a postal product. The adjective-to-supplier connection is loose.'),
    ('principal', 'principles',
     "The school board wanted principles in the head office. Three rulebooks got the job. None has returned a parent's call.",
     'School leadership cues principal implicitly; principles become rulebooks installed in the office. The unanswered calls literalize the books as incapable administrators. Number also changes.'),
    ('discreet', 'discredit',
     "I told my publicist to keep my secrets safe. He launched a campaign to discredit me. Apparently 'safe' meant backed up on every billboard in town.",
     'Protecting secrets cues discreet implicitly; discredit reverses the assignment into reputation damage. The billboard backup is the final ironic reinterpretation of safe storage. The inferred instruction also shifts grammar.'),
    ('council', 'counsels',
     "Our mayor counsels every pothole through its abandonment issues. The roads still aren't repaired, but they've stopped blaming their parents.",
     'An elected town leader cues council implicitly; counsels supplies therapy rather than repairs. Potholes become patients with family issues. This noun-to-verb substitution is loose.'),
    ('ascent', 'asset',
     "My broker offered to help me up the mountain with an asset. The market's rising. I'm still in the car park.",
     'Getting up a mountain cues ascent implicitly; asset supplies a financial holding. The final rising-market contrast explains why the broker has not helped the actual climb.'),
    ('cereal', 'aerial',
     'Breakfast came with an aerial in the bowl. I asked for extra fiber and got the shipping forecast.',
     'Breakfast, a bowl and extra fiber cue cereal implicitly; aerial supplies an antenna. The shipping forecast completes the shift from food to radio reception.'),
    ('palette', 'palace',
     "'Your new palace is ready,' said my painting assistant. I wanted somewhere to mix colors. Now I have to heat the east wing.",
     'A surface for mixing colors cues palette implicitly; palace supplies an expensive residence. Heating an entire wing is the consequence of the mistaken art purchase.'),
    ('capital', 'capitols',
     'Our investors promised us capitols. We needed cash; they delivered two domes and a filibuster. The company is now permanently in session.',
     'Investors and cash cue capital implicitly; capitols supplies legislative buildings. Domes, a filibuster and being in session literalize the wrong kind of funding. Number changes.'),
    ('currant', 'currents',
     "The baker's new fruitcake is full of currents. The recipe says, 'Serve with cream and insulated gloves.'",
     'Fruitcake cues currant implicitly; currents supplies electricity. Insulated gloves substitute for ordinary serving instructions. Number changes.'),
    ('marshal', 'martian',
     'Why did the parade committee hire a Martian? Because it wanted someone who could keep the floats in orbit.',
     'The parade leadership role cues marshal implicitly; Martian supplies an alien. Keeping floats in orbit reinterprets organizing the parade as managing spacecraft.'),
    ('prophet', 'profits',
     'My accountant started telling fortunes. He only consults profits. Apparently a tall, dark audit is coming into my life.',
     'Telling fortunes cues prophet implicitly; profits supplies accounting earnings. The familiar mysterious-stranger prediction is replaced by a tall, dark audit. Number changes.'),
    ('medal', 'middle',
     'Why did the sprinter celebrate at the halfway line? Because he was going for the middle.',
     'An athletic goal cues medal implicitly; middle supplies the halfway point. Celebrating before the finish literalizes the wrong goal. Articles differ across the readings.'),
    ('altar', 'alder',
     'Why did the wedding planner bring a watering can? Because the couple had booked an alder.',
     'A wedding ceremony cues altar implicitly; alder supplies a tree. A watering can makes the ceremonial booking an act of gardening.'),
    ('canvas', 'canvassed',
     "I sent my assistant out for painting supplies. He canvassed the whole neighborhood. I still have nothing to paint on, but apparently I'd win an election.",
     'Painting supplies cue canvas implicitly; canvassed supplies political surveying. The assistant returns with electoral support instead of something to paint on. Grammatical category changes.'),
    ('sensor', 'censer',
     'The installer fitted a censer in our smoke alarm. It produces the smoke, then congratulates itself for finding it.',
     'A smoke alarm component cues sensor implicitly; censer supplies an incense burner. Creating and then detecting the same smoke makes the appliance absurdly self-congratulatory.'),
    ('allusion', 'illusions',
     "My English teacher said my essay needed more illusions. I made the conclusion disappear. She said that was the strongest argument I'd made.",
     'An English essay cues literary allusion implicitly; illusions supplies stage magic. The disappearing conclusion becomes the strongest argument. Number changes.'),
    ('appraise', 'apprised',
     "'Keep the vase apprised,' the auctioneer said. I told it the latest prices. It looked shattered.",
     'Auction pricing cues appraise implicitly; apprised supplies informing rather than valuing the vase. Shattered adds a figurative emotional response suited to breakable pottery. The implicit reading may require an inflection.'),
    ('elicit', 'solicit',
     "I paid a dog trainer to get a response out of my puppy. Now it can solicit donations. 'Sit' costs a dollar; 'stay' requires a subscription.",
     'Training a response cues elicit implicitly; solicit supplies fundraising. Paid commands and a subscription literalize the wrong training objective. The two verbs have overlapping senses.'),
    ('emigrate', 'immigrated',
     "I was halfway through leaving the country when the officer stamped 'immigrated' on my papers. They gave me a welcome basket. I recognized everything in it from my leaving party.",
     'Leaving the country cues emigrate implicitly; immigrated supplies arrival. Receiving the same party goods as a welcome reverses the departure. Tense changes.'),
    ('prescribe', 'proscribed',
     "The doctor's note said cake was proscribed. The pharmacist handed me a police evidence bag. For once, dessert really was a guilty pleasure.",
     'A medical note cues prescribe implicitly; proscribed supplies a ban. The evidence bag and guilty pleasure enact treating dessert as contraband. Tense changes.'),
    ('adverse', 'obverse',
     "I asked the coin dealer for the worst possible assessment of my collection. He examined the obverse and said, 'That nose is doing the economy no favors.'",
     'An unfavorable assessment cues adverse implicitly; obverse supplies the front of a coin. Critiquing the portrait replaces evaluating the collection as an investment.'),
    ('parameter', 'perimeters',
     "I asked the programmer to tweak the settings. He adjusted the perimeters. Three fences later, even the bug reports couldn't get in.",
     'Software settings cue parameter implicitly; perimeters supplies physical boundaries. Fences exclude even incoming bug reports. Number changes.'),
    ('ingenious', 'ingenue',
     'The playwright promised me a brilliantly clever heroine. He delivered an ingenue who gave the villain a spare key. Her master plan was to ask for it back nicely.',
     'A brilliantly clever heroine cues ingenious implicitly; ingenue supplies an innocent character. Trusting the villain and politely asking for the key back illustrate the mistaken role. This changes grammatical category and remains below cutoff.'),
    ('vocation', 'vacations',
     "My careers adviser recommended vacations. I now have five years' experience in lying down.",
     'Career advice cues vocation implicitly; vacations supplies holidays. A resume-style claim of experience in lying down resolves the swapped advice. Number changes.'),
    ('collusion', 'collisions',
     'The conspirators prepared for collisions. Their secret handshake now ends with everyone fastening a seat belt.',
     'A conspiratorial secret meeting cues collusion implicitly; collisions supplies crashes. Seat belts become part of the clandestine ritual. Number changes.'),
    ('collaborate', 'corroborates',
     "I invited a detective to help write my fantasy novel. He only corroborates. We're six months behind schedule while he tries to get a dragon to swear an oath.",
     'Helping write a novel cues collaborate implicitly; corroborates supplies factual verification. Requiring a fictional dragon to swear an oath blocks creative teamwork. Inflection changes and the pair remains below cutoff.'),
]

REQUIRED_PAIRS = [
    ('cat', 'cad'), ('cat', 'cash'), ('drum', 'drama'),
    ('knight', 'night'), ('bat', 'pat'), ('pat', 'pit'),
]


def letter_edit_distance(a, b):
    """Minimum single-letter insertions, deletions and substitutions."""
    previous = list(range(len(b) + 1))
    for i, left in enumerate(a, 1):
        current = [i]
        for j, right in enumerate(b, 1):
            current.append(min(current[-1] + 1, previous[j] + 1,
                               previous[j - 1] + (left != right)))
        previous = current
    return previous[-1]


def build_variants():
    variants = []
    for idx, (a, b, _, _) in enumerate(PAIRS, 1):
        original_b = ORIGINAL_SECOND_WORDS[a]
        original = compare(a, original_b)
        updated = compare(a, b)
        variants.append({
            'id': f'V{idx:02d}', 'candidate_a': a,
            'original_candidate_b': original_b, 'candidate_b': b,
            'letter_edits': letter_edit_distance(original_b, b),
            'original_similarity': original['similarity'],
            'similarity': updated['similarity'],
            'similarity_change': round(updated['similarity'] - original['similarity'], 4),
            'second_word_similarity': compare(original_b, b)['similarity'],
        })
    return variants


def validate_joke_text(a, b, joke):
    """Enforce second-word-only joke bodies while allowing varied forms."""
    words = re.findall(r'[a-z]+', joke.lower())
    if a.lower() in words:
        raise ValueError(f'First word appears in joke: {a}')
    if b.lower() not in words:
        raise ValueError(f'Second word missing from joke: {b}')


def has_formulaic_opening(joke):
    return bool(re.match(r'\s*(why|because)\b', joke, flags=re.IGNORECASE))


def build_rows():
    if sum(not has_formulaic_opening(joke) for _, _, joke, _ in PAIRS) <= len(PAIRS) / 2:
        raise ValueError('Most jokes must open without Why or Because')
    rows = []
    for idx, (a, b, joke, reason) in enumerate(PAIRS, 1):
        validate_joke_text(a, b, joke)
        score = compare(a, b)
        negative = f'The dictionary exercise listed “{a}” and “{b}” as two entries to compare for pronunciation.'
        # Every rewritten joke gets a literal control; index never determines provenance.
        for label, text, note in (
            ('positive', joke, reason),
            ('negative', negative, 'Literal pronunciation comparison; no setup/punchline reinterpretation.'),
        ):
            rows.append({
                'id': f'{label[0].upper()}{idx:02d}',
                'reference_class': label, 'text': text,
                'candidate_a': a, 'candidate_b': b,
                'original_candidate_b': ORIGINAL_SECOND_WORDS[a],
                'letter_edits': letter_edit_distance(ORIGINAL_SECOND_WORDS[a], b),
                'similarity': score['similarity'],
                'weighted_distance': score['weighted_distance'],
                'phones_a': score['phones_a'], 'phones_b': score['phones_b'],
                'annotation_note': note,
            })
    return rows


def main():
    rows = build_rows()
    required = [compare(a, b) for a, b in REQUIRED_PAIRS]
    variants = build_variants()
    for filename, records in (('evaluation.csv', rows), ('required_pairs.csv', required),
                              ('pair_variants.csv', variants)):
        with (ROOT / filename).open('w', newline='', encoding='utf-8') as output:
            writer = csv.DictWriter(output, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
    print('Total:', len(rows),
          'positives:', sum(r['reference_class'] == 'positive' for r in rows),
          'negatives:', sum(r['reference_class'] == 'negative' for r in rows))


if __name__ == '__main__':
    main()

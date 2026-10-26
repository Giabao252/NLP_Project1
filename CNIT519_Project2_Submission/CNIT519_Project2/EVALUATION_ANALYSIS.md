# Project 2: evaluation of changed second words and rewritten jokes

All 27 second words changed and all jokes were rewritten. Each original first word and the phonetic scoring formula are retained. Every joke has a literal comparison control: **54 records (27 intended positives, 27 negatives)**. The word changes are auditable in `pair_variants.csv`; the jokes and explanations are in `build_evaluation.py` and `evaluation.csv`.

## Joke wording and structure

**24 of 27 jokes** open as prose or dialogue; **3** retain a question-and-answer opening. The jokes preserve a setup, an implicit first reading and a payoff using the second word, with short anecdotes, dialogue, ironic reversals and occasional traditional questions. Only the current second candidate is written in each joke; the first candidate must be inferred from its context. A case-insensitive whole-word check confirms that the first word is absent and the second is present. Candidate labels, explanatory annotations and dictionary-comparison negatives still name both words for evaluation; those are not joke bodies.

## Spelling changes and original-score comparison

The requested one-letter replacement is used where a meaningful distinct word is available. With the approved relaxation, a single insertion or deletion is also allowed, and a few words use larger edits. Names or spelling variants were not selected merely to get a high score. Real dictionary words, a distinct meaning, and a usable joke were required. This is a curated selection, not a claim of global minimum spelling distance over every English word.

- Edit-count distribution (letters inserted, deleted or substituted): {1: 22, 2: 3, 3: 2}.
- `discrete -> discredit` and `ingenuous -> ingenue` need three edits; the installed dictionary supplied no usable distinct one- or two-edit alternatives. `canvass -> canvassed` retains the solicitation reading, avoiding `canvases`, which would merely pluralize the first word. `illicit -> solicit` and `averse -> obverse` use two edits to obtain usable real words with contextual meaning switches.
- Original mean similarity: **0.9422**; new mean: **0.8073**. Each new score compares the original first word with the replacement, not just the old and new second words. The latter comparison is recorded separately in the variant audit.

| First word | Original second | New second | Letter edits | Original score | New score | Change |
|---|---|---|---:|---:|---:|---:|
| compliment | complement | complements | 1 | 0.9500 | 0.8636 | -0.0864 |
| stationary | stationery | stationer | 1 | 1.0000 | 0.7222 | -0.2778 |
| principal | principle | principles | 1 | 1.0000 | 0.9000 | -0.1000 |
| discreet | discrete | discredit | 3 | 1.0000 | 0.7200 | -0.2800 |
| council | counsel | counsels | 1 | 1.0000 | 0.8571 | -0.1429 |
| ascent | assent | asset | 1 | 1.0000 | 0.7320 | -0.2680 |
| cereal | serial | aerial | 1 | 1.0000 | 0.7733 | -0.2267 |
| palette | palate | palace | 1 | 1.0000 | 0.8900 | -0.1100 |
| capital | capitol | capitols | 1 | 0.9057 | 0.7925 | -0.1132 |
| currant | current | currents | 1 | 1.0000 | 0.8333 | -0.1667 |
| marshal | martial | martian | 1 | 1.0000 | 0.9083 | -0.0917 |
| prophet | profit | profits | 1 | 1.0000 | 0.7629 | -0.2371 |
| medal | meddle | middle | 1 | 1.0000 | 0.9280 | -0.0720 |
| altar | alter | alder | 1 | 1.0000 | 0.9000 | -0.1000 |
| canvas | canvass | canvassed | 2 | 1.0000 | 0.8571 | -0.1429 |
| sensor | censor | censer | 1 | 1.0000 | 1.0000 | +0.0000 |
| allusion | illusion | illusions | 1 | 0.8900 | 0.7629 | -0.1271 |
| appraise | apprise | apprised | 1 | 0.9000 | 0.7500 | -0.1500 |
| elicit | illicit | solicit | 2 | 0.8900 | 0.7629 | -0.1271 |
| emigrate | immigrate | immigrated | 1 | 0.9486 | 0.7378 | -0.2108 |
| prescribe | proscribe | proscribed | 1 | 0.9200 | 0.8178 | -0.1022 |
| adverse | averse | obverse | 2 | 0.7320 | 0.8420 | +0.1100 |
| parameter | perimeter | perimeters | 1 | 0.9257 | 0.8100 | -0.1157 |
| ingenious | ingenuous | ingenue | 3 | 0.8311 | 0.6913 | -0.1398 |
| vocation | vacation | vacations | 1 | 0.8886 | 0.7775 | -0.1111 |
| collusion | collision | collisions | 1 | 0.8886 | 0.7775 | -0.1111 |
| collaborate | corroborate | corroborates | 1 | 0.7700 | 0.6275 | -0.1425 |

## Phonetic variety

- Identical stress-stripped phone sequences: **1**. Different phone sequences: **26**, under the selected dictionary pronunciations.
- 22 distinct scores; range **0.6275–1.0000**; mean **0.8073**, median **0.7925**.
- **25/27** meet the unchanged 0.70 cutoff. The rejected candidates remain in the authored dataset and are reported as misses rather than silently removed.
- Below cutoff: ingenious/ingenue (0.6913); collaborate/corroborates (0.6275).
- These are model-relative scores, not universal dialect judgments. The first CMU pronunciation is selected, stress is removed, and currant uses the documented pronunciation supplement. Alternate pronunciations are not searched.

| Pair | Phones A | Phones B | Distance | Similarity | Relation |
|---|---|---|---:|---:|---|
| compliment / complements | K AA M P L AH M EH N T | K AA M P L AH M AH N T S | 1.5000 | 0.8636 | near |
| stationary / stationer | S T EY SH AH N EH R IY | S T EY SH AH N ER | 2.5000 | 0.7222 | near |
| principal / principles | P R IH N S AH P AH L | P R IH N S AH P AH L Z | 1.0000 | 0.9000 | near |
| discreet / discredit | D IH S K R IY T | D IH S K R EH D AH T | 2.5200 | 0.7200 | near |
| council / counsels | K AW N S AH L | K AW N S AH L Z | 1.0000 | 0.8571 | near |
| ascent / asset | AH S EH N T | AE S EH T | 1.3400 | 0.7320 | near |
| cereal / aerial | S IH R IY AH L | EH R IY AH L | 1.3600 | 0.7733 | near |
| palette / palace | P AE L AH T | P AE L AH S | 0.5500 | 0.8900 | near |
| capital / capitols | K AE P AH T AH L | K AE P IH T AH L Z | 1.6600 | 0.7925 | near |
| currant / currents | K ER AH N T | K ER AH N T S | 1.0000 | 0.8333 | near |
| marshal / martian | M AA R SH AH L | M AA R SH AH N | 0.5500 | 0.9083 | near |
| prophet / profits | P R AA F AH T | P R AA F IH T S | 1.6600 | 0.7629 | near |
| medal / middle | M EH D AH L | M IH D AH L | 0.3600 | 0.9280 | near |
| altar / alder | AO L T ER | AO L D ER | 0.4000 | 0.9000 | near |
| canvas / canvassed | K AE N V AH S | K AE N V AH S T | 1.0000 | 0.8571 | near |
| sensor / censer | S EH N S ER | S EH N S ER | 0.0000 | 1.0000 | identical |
| allusion / illusions | AH L UW ZH AH N | IH L UW ZH AH N Z | 1.6600 | 0.7629 | near |
| appraise / apprised | AH P R EY Z | AH P R AY Z D | 1.5000 | 0.7500 | near |
| elicit / solicit | IH L IH S IH T | S AH L IH S IH T | 1.6600 | 0.7629 | near |
| emigrate / immigrated | EH M AH G R EY T | IH M AH G R EY T IH D | 2.3600 | 0.7378 | near |
| prescribe / proscribed | P R AH S K R AY B | P R OW S K R AY B D | 1.6400 | 0.8178 | near |
| adverse / obverse | AE D V ER S | AH B V ER S | 0.7900 | 0.8420 | near |
| parameter / perimeters | P ER AE M AH T ER | P ER IH M AH T ER Z | 1.5200 | 0.8100 | near |
| ingenious / ingenue | IH N JH IY N Y AH S | IH N JH EH N Y UW | 2.4700 | 0.6913 | near |
| vocation / vacations | V OW K EY SH AH N | V EY K EY SH AH N Z | 1.7800 | 0.7775 | near |
| collusion / collisions | K AH L UW ZH AH N | K AH L IH ZH AH N Z | 1.7800 | 0.7775 | near |
| collaborate / corroborates | K AH L AE B ER EY T | K ER AO B ER EY T S | 2.9800 | 0.6275 | near |

## Candidate retrieval

The fixed vocabulary contains 54 unique words from the revised pairs. For each first word, retrieval ranks the other vocabulary words using the 0.70 cutoff. The expected partner is counted as found only when it appears within K results. This tests retrieval with known candidates, not automatic identification of a pun in free text.

- recall at 1: 85.19%
- recall at 3: 92.59%
- recall at 5: 92.59%

## Diagnostic sound-only baseline

The baseline predicts joke whenever pair similarity is at least the cutoff. It uses no sentence semantics. Metrics below compare this rule against the authored labels; they are not results from an integrated semantic classifier or a blind humor test. Joke and control share exactly the same pair, so every accepted joke also produces a false positive. Increasing the cutoff cannot distinguish members of a matched pair.

| Cutoff | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.70 | 25 | 25 | 2 | 2 | 50.00% | 50.00% | 92.59% | 64.94% |
| 0.85 | 9 | 9 | 18 | 18 | 50.00% | 50.00% | 33.33% | 40.00% |
| 0.90 | 5 | 5 | 22 | 22 | 50.00% | 50.00% | 18.52% | 27.03% |
| 0.95 | 1 | 1 | 26 | 26 | 50.00% | 50.00% | 3.70% | 6.90% |
| 1.00 | 1 | 1 | 26 | 26 | 50.00% | 50.00% | 3.70% | 6.90% |

## Qualitative analysis of every joke

The following comments are an editorial review by the author of the jokes. They explain intended reading switches, not measured audience reactions. 8 weaker phonetic or semantic connections are explicitly flagged for independent review.

### 1. compliment / complements — 0.8636

Original second word: complement; letter edits: 1.

> My math teacher tried to boost my self-esteem by listing everyone I wasn't. Apparently she's better at complements.

The request for praise cues compliment implicitly; listing everyone outside the singleton containing the speaker supplies mathematical complements. The self-esteem setup reverses into set arithmetic.

Plausible authored substitution; independent humor rating still needed.

### 2. stationary / stationer — 0.7222

Original second word: stationery; letter edits: 1.

> The gym bought its exercise bikes from a stationer. Mine folds into an envelope; postage is the only thing going up.

Exercise bikes cue stationary implicitly; stationer supplies writing materials. The envelope and postage turn a fitness purchase into a postal product. The adjective-to-supplier connection is loose.

Review recommended: the job of the paper-goods supplier supports the absurd bicycle, but the implicit adjective-to-person sound substitution is loose.

### 3. principal / principles — 0.9000

Original second word: principle; letter edits: 1.

> The school board wanted principles in the head office. Three rulebooks got the job. None has returned a parent's call.

School leadership cues principal implicitly; principles become rulebooks installed in the office. The unanswered calls literalize the books as incapable administrators. Number also changes.

Plausible authored substitution; independent humor rating still needed.

### 4. discreet / discredit — 0.7200

Original second word: discrete; letter edits: 3.

> I told my publicist to keep my secrets safe. He launched a campaign to discredit me. Apparently 'safe' meant backed up on every billboard in town.

Protecting secrets cues discreet implicitly; discredit reverses the assignment into reputation damage. The billboard backup is the final ironic reinterpretation of safe storage. The inferred instruction also shifts grammar.

Review recommended: the mishearing also changes the grammatical instruction; sound alone does not establish the intended joke.

### 5. council / counsels — 0.8571

Original second word: counsel; letter edits: 1.

> Our mayor counsels every pothole through its abandonment issues. The roads still aren't repaired, but they've stopped blaming their parents.

An elected town leader cues council implicitly; counsels supplies therapy rather than repairs. Potholes become patients with family issues. This noun-to-verb substitution is loose.

Review recommended: the therapist and potholes supply an absurd situation, but the change from a noun to a verb makes this a looser substitution.

### 6. ascent / asset — 0.7320

Original second word: assent; letter edits: 1.

> My broker offered to help me up the mountain with an asset. The market's rising. I'm still in the car park.

Getting up a mountain cues ascent implicitly; asset supplies a financial holding. The final rising-market contrast explains why the broker has not helped the actual climb.

Plausible authored substitution; independent humor rating still needed.

### 7. cereal / aerial — 0.7733

Original second word: serial; letter edits: 1.

> Breakfast came with an aerial in the bowl. I asked for extra fiber and got the shipping forecast.

Breakfast, a bowl and extra fiber cue cereal implicitly; aerial supplies an antenna. The shipping forecast completes the shift from food to radio reception.

Plausible authored substitution; independent humor rating still needed.

### 8. palette / palace — 0.8900

Original second word: palate; letter edits: 1.

> 'Your new palace is ready,' said my painting assistant. I wanted somewhere to mix colors. Now I have to heat the east wing.

A surface for mixing colors cues palette implicitly; palace supplies an expensive residence. Heating an entire wing is the consequence of the mistaken art purchase.

Plausible authored substitution; independent humor rating still needed.

### 9. capital / capitols — 0.7925

Original second word: capitol; letter edits: 1.

> Our investors promised us capitols. We needed cash; they delivered two domes and a filibuster. The company is now permanently in session.

Investors and cash cue capital implicitly; capitols supplies legislative buildings. Domes, a filibuster and being in session literalize the wrong kind of funding. Number changes.

Plausible authored substitution; independent humor rating still needed.

### 10. currant / currents — 0.8333

Original second word: current; letter edits: 1.

> The baker's new fruitcake is full of currents. The recipe says, 'Serve with cream and insulated gloves.'

Fruitcake cues currant implicitly; currents supplies electricity. Insulated gloves substitute for ordinary serving instructions. Number changes.

Plausible authored substitution; independent humor rating still needed.

### 11. marshal / martian — 0.9083

Original second word: martial; letter edits: 1.

> Why did the parade committee hire a Martian? Because it wanted someone who could keep the floats in orbit.

The parade leadership role cues marshal implicitly; Martian supplies an alien. Keeping floats in orbit reinterprets organizing the parade as managing spacecraft.

Plausible authored substitution; independent humor rating still needed.

### 12. prophet / profits — 0.7629

Original second word: profit; letter edits: 1.

> My accountant started telling fortunes. He only consults profits. Apparently a tall, dark audit is coming into my life.

Telling fortunes cues prophet implicitly; profits supplies accounting earnings. The familiar mysterious-stranger prediction is replaced by a tall, dark audit. Number changes.

Plausible authored substitution; independent humor rating still needed.

### 13. medal / middle — 0.9280

Original second word: meddle; letter edits: 1.

> Why did the sprinter celebrate at the halfway line? Because he was going for the middle.

An athletic goal cues medal implicitly; middle supplies the halfway point. Celebrating before the finish literalizes the wrong goal. Articles differ across the readings.

Review recommended: the inferred sporting phrase and explicit halfway instruction differ in articles as well as pronunciation.

### 14. altar / alder — 0.9000

Original second word: alter; letter edits: 1.

> Why did the wedding planner bring a watering can? Because the couple had booked an alder.

A wedding ceremony cues altar implicitly; alder supplies a tree. A watering can makes the ceremonial booking an act of gardening.

Plausible authored substitution; independent humor rating still needed.

### 15. canvas / canvassed — 0.8571

Original second word: canvass; letter edits: 2.

> I sent my assistant out for painting supplies. He canvassed the whole neighborhood. I still have nothing to paint on, but apparently I'd win an election.

Painting supplies cue canvas implicitly; canvassed supplies political surveying. The assistant returns with electoral support instead of something to paint on. Grammatical category changes.

Plausible authored substitution; independent humor rating still needed.

### 16. sensor / censer — 1.0000

Original second word: censor; letter edits: 1.

> The installer fitted a censer in our smoke alarm. It produces the smoke, then congratulates itself for finding it.

A smoke alarm component cues sensor implicitly; censer supplies an incense burner. Creating and then detecting the same smoke makes the appliance absurdly self-congratulatory.

Plausible authored substitution; independent humor rating still needed.

### 17. allusion / illusions — 0.7629

Original second word: illusion; letter edits: 1.

> My English teacher said my essay needed more illusions. I made the conclusion disappear. She said that was the strongest argument I'd made.

An English essay cues literary allusion implicitly; illusions supplies stage magic. The disappearing conclusion becomes the strongest argument. Number changes.

Plausible authored substitution; independent humor rating still needed.

### 18. appraise / apprised — 0.7500

Original second word: apprise; letter edits: 1.

> 'Keep the vase apprised,' the auctioneer said. I told it the latest prices. It looked shattered.

Auction pricing cues appraise implicitly; apprised supplies informing rather than valuing the vase. Shattered adds a figurative emotional response suited to breakable pottery. The implicit reading may require an inflection.

Review recommended: the natural implicit reading would use an inflected first word; scores here still compare the supplied candidate words, not complete spoken sentences.

### 19. elicit / solicit — 0.7629

Original second word: illicit; letter edits: 2.

> I paid a dog trainer to get a response out of my puppy. Now it can solicit donations. 'Sit' costs a dollar; 'stay' requires a subscription.

Training a response cues elicit implicitly; solicit supplies fundraising. Paid commands and a subscription literalize the wrong training objective. The two verbs have overlapping senses.

Review recommended: drawing out and asking for a response overlap in meaning. The fundraising context must do the work of separating the readings.

### 20. emigrate / immigrated — 0.7378

Original second word: immigrate; letter edits: 1.

> I was halfway through leaving the country when the officer stamped 'immigrated' on my papers. They gave me a welcome basket. I recognized everything in it from my leaving party.

Leaving the country cues emigrate implicitly; immigrated supplies arrival. Receiving the same party goods as a welcome reverses the departure. Tense changes.

Plausible authored substitution; independent humor rating still needed.

### 21. prescribe / proscribed — 0.8178

Original second word: proscribe; letter edits: 1.

> The doctor's note said cake was proscribed. The pharmacist handed me a police evidence bag. For once, dessert really was a guilty pleasure.

A medical note cues prescribe implicitly; proscribed supplies a ban. The evidence bag and guilty pleasure enact treating dessert as contraband. Tense changes.

Plausible authored substitution; independent humor rating still needed.

### 22. adverse / obverse — 0.8420

Original second word: averse; letter edits: 2.

> I asked the coin dealer for the worst possible assessment of my collection. He examined the obverse and said, 'That nose is doing the economy no favors.'

An unfavorable assessment cues adverse implicitly; obverse supplies the front of a coin. Critiquing the portrait replaces evaluating the collection as an investment.

Plausible authored substitution; independent humor rating still needed.

### 23. parameter / perimeters — 0.8100

Original second word: perimeter; letter edits: 1.

> I asked the programmer to tweak the settings. He adjusted the perimeters. Three fences later, even the bug reports couldn't get in.

Software settings cue parameter implicitly; perimeters supplies physical boundaries. Fences exclude even incoming bug reports. Number changes.

Plausible authored substitution; independent humor rating still needed.

### 24. ingenious / ingenue — 0.6913

Original second word: ingenuous; letter edits: 3.

> The playwright promised me a brilliantly clever heroine. He delivered an ingenue who gave the villain a spare key. Her master plan was to ask for it back nicely.

A brilliantly clever heroine cues ingenious implicitly; ingenue supplies an innocent character. Trusting the villain and politely asking for the key back illustrate the mistaken role. This changes grammatical category and remains below cutoff.

Weak phonetic candidate: below 0.70. The theater context explains the meaning switch but does not repair the sound mismatch.

### 25. vocation / vacations — 0.7775

Original second word: vacation; letter edits: 1.

> My careers adviser recommended vacations. I now have five years' experience in lying down.

Career advice cues vocation implicitly; vacations supplies holidays. A resume-style claim of experience in lying down resolves the swapped advice. Number changes.

Plausible authored substitution; independent humor rating still needed.

### 26. collusion / collisions — 0.7775

Original second word: collision; letter edits: 1.

> The conspirators prepared for collisions. Their secret handshake now ends with everyone fastening a seat belt.

A conspiratorial secret meeting cues collusion implicitly; collisions supplies crashes. Seat belts become part of the clandestine ritual. Number changes.

Plausible authored substitution; independent humor rating still needed.

### 27. collaborate / corroborates — 0.6275

Original second word: corroborate; letter edits: 1.

> I invited a detective to help write my fantasy novel. He only corroborates. We're six months behind schedule while he tries to get a dragon to swear an oath.

Helping write a novel cues collaborate implicitly; corroborates supplies factual verification. Requiring a fictional dragon to swear an oath blocks creative teamwork. Inflection changes and the pair remains below cutoff.

Weak phonetic candidate: below 0.70. This remains an authored near-sound experiment, not a successful retrieval at the configured cutoff.

## Validation and reproduction

Validation checks all 54 records against the current authoring data, unique IDs, balanced labels, all 27 changed dictionary words, second-word-only joke text, a majority avoiding Why/Because openings, original-word provenance, variant audit, all saved scores and phones, identical joke/control scores, score range, symmetry and identity, the six unchanged required comparisons, the currant supplement, and explicit rejection of unknown words.

Run from this folder with cmudict installed:

```powershell
python phonetics.py
python build_evaluation.py
python analyze_evaluation.py
```

If using the project-local dependency installation in this workspace, set `$env:PYTHONPATH = (Join-Path (Get-Location) ".project2_dependencies")` and use a working Python executable.

The main finding is that the rewritten contexts create intended reinterpretations while the literal controls do not. Phonetic similarity supplies candidates but cannot establish that difference. Independent human annotation and integration of a semantic decision stage remain future work.

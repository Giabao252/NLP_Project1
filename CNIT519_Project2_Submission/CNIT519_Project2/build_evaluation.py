import csv,json,sys
from pathlib import Path
from phonetics import compare
ROOT=Path(__file__).resolve().parent
# Positive instances are deliberately authored stimulus labels, NOT independently judged classifier predictions.
PAIRS = [
    ('compliment', 'complement',
     'The food critic gave the chef a compliment because the sauce was the perfect complement to the meal.',
     'Praise versus something that completes or enhances another thing.'),

    ('stationary', 'stationery',
     'The stationery shop had such beautiful notebooks that customers stood stationary just to admire them.',
     'Remaining motionless versus writing materials.'),

    ('principal', 'principle',
     'The school principal insisted that honesty was the most important principle, especially during exams.',
     'School administrator versus a fundamental rule or belief.'),

    ('discreet', 'discrete',
     'The mathematician kept the discrete data points so discreet that even the other researchers could not find them.',
     'Carefully secretive versus separate and individually distinct.'),

    ('council', 'counsel',
     'The city council hired legal counsel to determine whether its endless meetings were legally necessary.',
     'Governing committee versus professional advice or legal representation.'),

    ('ascent', 'assent',
     'The climber refused to begin the dangerous ascent until every member of the expedition gave their assent.',
     'Upward movement versus agreement or approval.'),

    ('cereal', 'serial',
     'The detective finally caught the serial cereal thief after discovering breakfast crumbs at every crime scene.',
     'Breakfast food versus something occurring repeatedly in sequence.'),

    ('palette', 'palate',
     'The chef used a colorful palette of ingredients to impress every guest whose palate demanded something extraordinary.',
     'Range of colors versus the sense of taste.'),

    ('capital', 'capitol',
     'The tour guide said the capital had one Capitol building but enough political arguments to fill a hundred.',
     'Seat of government versus a legislative building.'),

    ('currant', 'current',
     'The baker checked the current price of currants and immediately decided that raisins were more affordable.',
     'Small dried fruit versus something happening in the present.'),

    ('marshal', 'martial',
     'The town marshal opened a martial arts academy because chasing criminals had become his daily workout.',
     'Law enforcement officer versus matters relating to combat.'),

    ('prophet', 'profit',
     'The investment firm hired a prophet to predict its profit, but he only foresaw an expensive consultation fee.',
     'Person claiming prophetic knowledge versus financial gain.'),

    ('medal', 'meddle',
     'The coach promised a medal to any player who managed not to meddle in his carefully planned strategy.',
     'Award for achievement versus interfering in someone else’s affairs.'),

    ('altar', 'alter',
     'The wedding planner refused to alter the altar, even after discovering that it completely blocked the entrance.',
     'Ceremonial structure versus the act of changing something.'),

    ('canvas', 'canvass',
     'The politician commissioned a portrait on canvas while campaign volunteers went door to door to canvass for votes.',
     'Painting material versus systematically soliciting support.'),

    ('sensor', 'censor',
     'The museum installed a sensor to detect visitors attempting to censor the controversial exhibition.',
     'Detection device versus suppression or removal of information.'),

    ('allusion', 'illusion',
     'The magician made an allusion to his disappearing assistant before creating an illusion that made the entire audience gasp.',
     'Indirect reference versus deceptive visual appearance.'),

    ('appraise', 'apprise',
     'The antique dealer was instructed to appraise the mysterious vase and apprise its owner before the cat knocked it over.',
     'Evaluate monetary value versus inform someone of a situation.'),

    ('elicit', 'illicit',
     'The detective tried to elicit a confession about the illicit underground cake-smuggling operation.',
     'Draw out information versus something forbidden or unlawful.'),

    ('emigrate', 'immigrate',
     'The traveler decided to emigrate from Iceland and immigrate to Spain because his winter wardrobe needed a vacation.',
     'Leaving one country versus entering another to reside.'),

    ('prescribe', 'proscribe',
     'The doctor wanted to prescribe afternoon naps, but the productivity consultant insisted on proscribing them.',
     'Recommend or authorize a treatment versus officially forbid something.'),

    ('adverse', 'averse',
     'The sailor was averse to sailing in adverse weather, especially after his umbrella flew into the ocean.',
     'Unfavorable conditions versus reluctance or opposition.'),

    ('parameter', 'perimeter',
     'The security engineer adjusted one parameter and accidentally activated alarms around the entire perimeter of the parking lot.',
     'Variable or setting versus the outer boundary of an area.'),

    ('ingenious', 'ingenuous',
     'The ingenious magician pretended to be ingenuous so the audience would never suspect how carefully he had planned his tricks.',
     'Inventively clever versus innocently trusting or naive.'),

    ('vocation', 'vacation',
     'The career counselor misunderstood my request for a vocation and immediately booked me a vacation in the Caribbean.',
     'Profession or calling versus a period of leisure and travel.'),

    ('collusion', 'collision',
     'The insurance investigator suspected collusion when both drivers rehearsed exactly the same explanation for their collision.',
     'Secret cooperation for deception versus a physical impact.'),

    ('collaborate', 'corroborate',
     'The detectives agreed to collaborate to corroborate the witness testimony but spent the entire meeting arguing about who should take notes.',
     'Working together versus independently confirming evidence.')
]
rows=[]
for idx,(a,b,joke,reason) in enumerate(PAIRS,1):
    if idx<=23:
        # Negative contexts preserve both utterances and their phonetic similarity.
        negative=f'The dictionary exercise listed “{a}” and “{b}” as two entries to compare for pronunciation.'
        examples=[('positive',joke,reason),('negative',negative,'Pronunciation comparison is literal; no comic reinterpretation.')]
    else:
        examples=[('supplied_probe',joke,reason)]
    for cls,txt,note in examples:
        r=compare(a,b)
        rows.append({'id':f'{cls[0].upper()}{idx:02d}','reference_class':cls,'text':txt,'candidate_a':a,'candidate_b':b,'similarity':r['similarity'],'weighted_distance':r['weighted_distance'],'phones_a':r['phones_a'],'phones_b':r['phones_b'],'annotation_note':note})
with (ROOT/'evaluation.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
with (ROOT/'required_pairs.csv').open('w',newline='',encoding='utf-8') as f:
    required_pairs=[('cat','cad'),('cat','cash'),('drum','drama'),('knight','night'),('bat','pat'),('pat','pit')]
    writer=csv.DictWriter(f,fieldnames=['a','b','phones_a','phones_b','weighted_distance','similarity']);writer.writeheader();writer.writerows(compare(a,b) for a,b in required_pairs)
print('Total:',len(rows),'positives:',sum(r['reference_class']=='positive' for r in rows),'negatives:',sum(r['reference_class']=='negative' for r in rows),'probes:',sum(r['reference_class']=='supplied_probe' for r in rows))

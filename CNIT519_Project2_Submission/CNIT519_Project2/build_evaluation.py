import csv,json,sys
from pathlib import Path
from phonetics import compare
ROOT=Path(__file__).resolve().parent
# Positive instances are deliberately authored stimulus labels, NOT independently judged classifier predictions.
PAIRS=[
('night','knight','The knight worked all night because he was on a knight shift.','Night duty becomes a medieval knight’s shift.'),
('sea','see','Why did the sailor stare at the water? He wanted to see the sea.','Seeing versus the sea.'),
('flour','flower','Why did the baker bring a flower to work? He thought the recipe said flour.','Floral object substituted for baking flour.'),
('pair','pear','The fruit seller opened a dating service to help every pear find its pair.','Fruit pear and couple pair.'),
('sole','soul','The cobbler gave the singer a new sole so she could sing with soul.','Shoe sole and spirit.'),
('write','right','The author asked for the right to write and was handed a pencil.','Entitlement versus writing.'),
('plane','plain','The pilot wanted a plain meal, so the chef served it on a plane.','Simple food versus aircraft.'),
('mail','male','The postman took his son to work; he called it male mail.','Gender versus post.'),
('sun','son','The astronomer asked for the sun, but his assistant brought his son.','Star versus child.'),
('brake','break','The driver said he needed a break, and the mechanic checked his brake.','Rest versus vehicle stopping system.'),
('deer','dear','The zookeeper wrote Dear Deer on the envelope to his favorite animal.','Term of address versus animal.'),
('cent','scent','The perfume shop charged just one cent for its newest scent.','Money versus smell.'),
('be','bee','The insect asked, To be or not to bee?','Existence versus insect.'),
('meet','meat','At the butcher’s conference, everyone was excited to meet the meat.','Meeting people versus food.'),
('tail','tale','The fox became an author because he had a long tail and a longer tale.','Body part versus story.'),
('peace','piece','The tired baker said all he wanted was peace and a piece of cake.','Tranquility versus portion.'),
('knot','not','The sailor said the rope was not ready; the apprentice replied, Knot ready?','Negation versus rope knot.'),
('hour','our','Our clock is so possessive it calls every hour our hour.','Possession versus duration.'),
('waist','waste','The tailor said, Do not waste fabric; use it around the waist.','Discard versus body part.'),
('allowed','aloud','The librarian said no shouting was allowed, so I read the rule aloud.','Permission versus spoken volume.'),
('steak','stake','The vampire bought a steak, but the hunter asked for a stake.','Meat versus pointed weapon.'),
('blue','blew','Why was the wind sad? It blew so hard it turned blue.','Wind action versus color/mood.'),
('board','bored','The carpenter was bored until he found a board to work on.','State of mind versus wood.'),
('cat','cad','Why did the cat stop dating the cad? Because she realized he was only purr-suing her for his own gain!','Cat/cad supplies context; purr-suing/pursuing is the stronger phonetic joke.'),
('cat','cash','Why did the cat start working at a bank? Because she wanted to turn her cat-nap into cash.','Bank/cash context exists, but the cat-nap-to-cash substitution is weak.'),
('drum','drama','When the band broke up, it wasn’t drama — it was just drum!','Sound similarity and music context exist; grammatical substitution is weak.'),
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
    pairs=[('cat','cad'),('cat','cash'),('drum','drama'),('knight','night'),('bat','pat'),('pat','pit')]
    writer=csv.DictWriter(f,fieldnames=['a','b','phones_a','phones_b','weighted_distance','similarity']);writer.writeheader();writer.writerows(compare(a,b) for a,b in pairs)
print('Total:',len(rows),'positives:',sum(r['reference_class']=='positive' for r in rows),'negatives:',sum(r['reference_class']=='negative' for r in rows),'probes:',sum(r['reference_class']=='supplied_probe' for r in rows))

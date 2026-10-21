"""Transparent articulatory-weighted ARPAbet edit similarity (not a library metric)."""
import re
import cmudict
LEXICON=cmudict.dict()
# Explicit dictionary supplement for the evaluation corpus: currant/current
# share this US English pronunciation. Other unknown words still raise KeyError.
PRONUNCIATION_OVERRIDES={'currant': ['K', 'ER1', 'AH0', 'N', 'T']}
VOWELS={'AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY','OW','OY','UH','UW'}
PLACE={'P':'bilabial','B':'bilabial','M':'bilabial','W':'labial-velar','F':'labiodental','V':'labiodental','TH':'dental','DH':'dental','T':'alveolar','D':'alveolar','N':'alveolar','S':'alveolar','Z':'alveolar','L':'alveolar','R':'postalveolar','SH':'postalveolar','ZH':'postalveolar','CH':'postalveolar','JH':'postalveolar','Y':'palatal','K':'velar','G':'velar','NG':'velar','HH':'glottal'}
MANNER={**dict.fromkeys(['P','B','T','D','K','G'],'stop'),**dict.fromkeys(['F','V','TH','DH','S','Z','SH','ZH','HH'],'fricative'),**dict.fromkeys(['CH','JH'],'affricate'),**dict.fromkeys(['M','N','NG'],'nasal'),**dict.fromkeys(['L','R','W','Y'],'approximant')}
VOICED=set('B D G V DH Z ZH JH M N NG L R W Y'.split())
# Illustrative vowels in F1/F2-like groups; hand-defined, not measured acoustic formants.
VFEAT={'AA':(0,2),'AE':(1,0),'AH':(1,1),'AO':(0,3),'AW':(1,3),'AY':(2,1),'EH':(2,0),'ER':(1,1),'EY':(3,0),'IH':(3,0),'IY':(4,0),'OW':(2,3),'OY':(2,2),'UH':(3,3),'UW':(4,3)}
def phonemes(word):
    words=re.findall(r"[a-zA-Z]+",word.lower())
    if not words: raise ValueError('No alphabetic word')
    phones=[]
    for w in words:
        if w in PRONUNCIATION_OVERRIDES:
            phones.extend(PRONUNCIATION_OVERRIDES[w])
        elif w in LEXICON:
            phones.extend(LEXICON[w][0])
        else:
            raise KeyError(f'Out-of-vocabulary: {w}')
    return [re.sub(r'\d','',p) for p in phones]
def substitute(a,b):
    if a==b:return 0.
    av,bv=a in VOWELS,b in VOWELS
    if av and bv:
        x,y=VFEAT[a],VFEAT[b]
        return min(0.95,0.20+0.16*abs(x[0]-y[0])+0.14*abs(x[1]-y[1]))
    if av != bv:return 1.0
    return min(1.,0.20+0.35*(MANNER.get(a)!=MANNER.get(b))+0.25*(PLACE.get(a)!=PLACE.get(b))+0.20*((a in VOICED)!=(b in VOICED)))
def compare(a,b):
    x,y=phonemes(a),phonemes(b)
    dp=[[0.]*(len(y)+1) for _ in range(len(x)+1)]
    for i in range(len(x)+1):dp[i][0]=float(i)
    for j in range(len(y)+1):dp[0][j]=float(j)
    for i,pa in enumerate(x,1):
        for j,pb in enumerate(y,1):
            dp[i][j]=min(dp[i-1][j]+1,dp[i][j-1]+1,dp[i-1][j-1]+substitute(pa,pb))
    distance=dp[-1][-1]
    return {'a':a,'b':b,'phones_a':' '.join(x),'phones_b':' '.join(y),'weighted_distance':round(distance,4),'similarity':round(max(0,1-distance/max(len(x),len(y))),4)}
if __name__=='__main__':
    for p in [('cat','cad'),('cat','cash'),('drum','drama'),('knight','night'),('bat','pat'),('pat','pit')]:print(compare(*p))

def find_similar_utterances(word, vocabulary, min_similarity=0.70, top_k=20):
    """Phonetic candidate generation, ranked but WITHOUT deciding whether text is funny."""
    out=[]
    for alternative in vocabulary:
        if alternative.lower()==word.lower():
            continue
        try: result=compare(word,alternative)
        except (KeyError,ValueError): continue
        if result['similarity']>=min_similarity:out.append(result)
    return sorted(out,key=lambda z:(-z['similarity'],z['b']))[:top_k]

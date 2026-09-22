"""Score saved LLM output; does not call an LLM or perform joke inference."""
import argparse
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding='utf8').splitlines() if line.strip()]

def score(gold,predictions,key):
    gold_by_id={r['id']:r for r in gold}
    assert len(gold_by_id)==len(gold),'Duplicate gold IDs'
    assert len({r['id'] for r in predictions})==len(predictions),'Duplicate prediction IDs'
    assert {key[r['id']] for r in predictions}==set(gold_by_id),'Missing or unexpected records'
    assert len(set(key.values()))==len(key),'Non-unique ID mapping'
    tp=fp=tn=fn=abstentions=localized=pair_ok=0
    errors=[]; decisions={}; groups={}
    for p in predictions:
        r=gold_by_id[key[p['id']]]
        assert p['status'] in ['joke','non_joke','uncertain'],'Invalid evaluation status'
        assert p['age']==r['age'],'Age mismatch'
        for sense in p['senses']:
            assert sense['evidence_quote'] in r['text'],'Evidence quotation not found in input'
        predicted=p['status']=='joke'
        abstentions+=p['status']=='uncertain'
        correct=(r['label']==int(predicted)) and p['status']!='uncertain'
        if r['label']:
            tp+=predicted; fn+=not predicted
            localized+=p['target']==r.get('gold',{}).get('target')
        else:
            fp+=predicted; tn+=not predicted
        decisions[r['id']]=p
        kind=r.get('kind','diagnostic')
        groups.setdefault(kind,dict(correct=0,total=0))
        groups[kind]['correct']+=correct; groups[kind]['total']+=1
        if not correct: errors.append(dict(id=r['id'],run_id=p['id'],status=p['status'],reason=p['rejection_or_uncertainty_reason']))
    def div(a,b): return a/b if b else 0.0
    precision=div(tp,tp+fp); recall=div(tp,tp+fn); specificity=div(tn,tn+fp)
    pairs={r.get('pair_id') for r in gold if r.get('pair_id')}
    for pair in pairs:
        members=[r for r in gold if r.get('pair_id')==pair]
        pair_ok+=all(decisions[r['id']]['status']==('joke' if r['label'] else 'non_joke') for r in members)
    answered=[r for r in gold if decisions[r['id']]['status']!='uncertain']
    answer_correct=sum(int(decisions[r['id']]['status']=='joke')==r['label'] for r in answered)
    return dict(n=len(gold),tp=tp,fp=fp,tn=tn,fn=fn,accuracy=div(tp+tn,len(gold)),precision=precision,recall=recall,
                f1=div(2*tp,2*tp+fp+fn),specificity=specificity,false_positive_rate=1-specificity,
                balanced_accuracy=(recall+specificity)/2,macro_f1=(div(2*tp,2*tp+fp+fn)+div(2*tn,2*tn+fp+fn))/2,
                strict_accuracy=div(sum(g['correct'] for g in groups.values()),len(gold)),
                abstentions=abstentions,coverage=div(len(answered),len(gold)),answered_only_accuracy=div(answer_correct,len(answered)),
                paired_success_count=pair_ok,pair_count=len(pairs),paired_success_rate=div(pair_ok,len(pairs)),
                target_localization_including_abstentions=div(localized,sum(r['label'] for r in gold)) if all('gold' in r for r in gold) else None,
                subgroups=groups,errors=errors,
                age_recommendations=dict(Counter(decisions[r['id']]['recommendation'] for r in gold if r['label'])),
                scope='Non-blind in-chat LLM pilot. Unknown sense-specific AoA; no independent explanation or age accuracy.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--predictions',type=Path,default=ROOT/'predictions.jsonl')
    args=p.parse_args()
    gold=read_jsonl(ROOT/'corpus.jsonl'); predictions=read_jsonl(args.predictions)
    key=json.loads((ROOT/'evaluation_key.json').read_text())
    result=score(gold,predictions,key)
    cases=read_jsonl(ROOT/'challenge_cases.jsonl')
    diagnostic=score(cases,read_jsonl(ROOT/'challenge_predictions.jsonl'),{r['id']:r['id'] for r in cases})
    output=dict(corpus=result,instructor_diagnostics=diagnostic)
    (ROOT/'metrics.json').write_text(json.dumps(output,indent=2),encoding='utf8')
    print(json.dumps(output,indent=2))

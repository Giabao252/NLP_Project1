"""Prepare a provider-neutral LLM request. Does not call a model or contain answers."""
import argparse
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def request(records):
    cleaned=[]
    for r in records:
        if not isinstance(r.get('text'),str) or not r['text'].strip():
            raise ValueError('Each text must be a nonempty string.')
        if isinstance(r.get('age'),bool) or not isinstance(r.get('age'),int) or not 0<=r['age']<=120:
            raise ValueError('Each age must be an integer between 0 and 120.')
        cleaned.append({k:r[k] for k in ['id','text','age']})
    return (ROOT/'llm_procedure.md').read_text(encoding='utf8')+'\n\n## Records to analyze\n\n'+json.dumps(cleaned,indent=2,ensure_ascii=False)+'\n'

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument('--text')
    group.add_argument('--inputs',type=Path)
    p.add_argument('--age',type=int)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    if args.text is not None:
        if args.age is None: p.error('--age is required with --text')
        records=[dict(id='input-1',text=args.text,age=args.age)]
    else:
        records=[json.loads(s) for s in args.inputs.read_text(encoding='utf8').splitlines() if s.strip()]
        if args.age is not None:
            for r in records: r['age']=args.age
    try: content=request(records)
    except (ValueError,KeyError) as e: p.error(str(e))
    args.out.write_text(content,encoding='utf8')
    print(f'Prepared {len(records)} inputs. Submit this request to an LLM; this script does not run inference.')

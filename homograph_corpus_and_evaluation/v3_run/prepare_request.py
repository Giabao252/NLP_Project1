"""Build an LLM request from text and age, or JSONL. Does not call an LLM."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def request(records, prompt_path=None):
    cleaned = []
    seen = set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError('Each input must be a JSON object.')
        identifier = record.get('id')
        if not isinstance(identifier, str) or not identifier.strip():
            raise ValueError('Each ID must be a nonempty string.')
        if identifier in seen:
            raise ValueError(f'Duplicate ID: {identifier}')
        seen.add(identifier)
        text = record.get('text')
        age = record.get('age')
        if not isinstance(text, str) or not text.strip():
            raise ValueError('Each text must be a nonempty string.')
        if isinstance(age, bool) or not isinstance(age, int) or not 0 <= age <= 120:
            raise ValueError('Each age must be an integer between 0 and 120.')
        item = {'id': identifier, 'text': text, 'age': age}
        if 'age_evidence' in record:
            if not isinstance(record['age_evidence'], list):
                raise ValueError('age_evidence must be a list.')
            item['age_evidence'] = record['age_evidence']
        cleaned.append(item)
    if not cleaned:
        raise ValueError('Supply at least one input.')
    prompt = Path(prompt_path or ROOT / 'llm_procedure.md').read_text(encoding='utf-8')
    return prompt + '\n\n## Records to analyze\n\n' + json.dumps(cleaned, indent=2, ensure_ascii=False) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--text')
    group.add_argument('--inputs', type=Path)
    parser.add_argument('--age', type=int, help='Required for --text; overrides ages in --inputs when supplied.')
    parser.add_argument('--prompt', type=Path, default=ROOT / 'llm_procedure.md')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.text is not None and args.age is None:
        parser.error('--age is required with --text')
    try:
        if args.text is not None:
            records = [{'id': 'input-1', 'text': args.text, 'age': args.age}]
        else:
            records = [json.loads(line) for line in args.inputs.read_text(encoding='utf-8-sig').splitlines() if line.strip()]
            if args.age is not None:
                records = [dict(record, age=args.age) if isinstance(record, dict) else record for record in records]
        content = request(records, args.prompt)
        args.out.write_text(content, encoding='utf-8')
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(f'Prepared {len(records)} inputs in {args.out}. Submit the file contents to an LLM and save its JSONL response.')


if __name__ == '__main__':
    main()

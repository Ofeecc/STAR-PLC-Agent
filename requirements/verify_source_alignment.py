"""Compare extracted official PDF text with the unchanged supplied English JSON.

Run pdftotext -layout -enc UTF-8 first; this script uses only Python's stdlib.
The token checks are evidence of source alignment, not a formal semantic proof.
"""
from __future__ import annotations
from collections import Counter
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path
import re
import unicodedata

HERE = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def tokens(text):
    text = unicodedata.normalize('NFKC', text)
    text = re.sub(r'(?m)^\s*[-*]\s+', '', text)
    return re.findall(r'[A-Za-z0-9_]+|<=|>=|<>|:=|!=|==|[<>=+*/%#-]', text)

def clean_interface_pdf(text):
    return '\n'.join(line for line in text.splitlines()
        if not ('Direction' in line and 'Variable/Field' in line)
        and line.strip() not in ('Data', 'Type')
        and not re.match(r'^\s*Field\s+Description\s*$', line))

def clean_interface_json(text):
    text = text.replace('<br>', ' ').replace('**', '')
    return '\n'.join(line for line in text.splitlines()
        if not (line.lstrip().startswith('| Direction')
            or line.lstrip().startswith('| Field |')
            or line.lstrip().startswith('| ---')))

def main():
    pdf_path = HERE/'source/大作业题库.pdf'
    bank_path = HERE/'source/public_bank_original.json'
    assignment = HERE/'source/Final project_ENGLISH.docx'
    text_path = HERE/'public_bank_pdf.txt'
    text = text_path.read_text(encoding='utf-8')
    flat = text.replace('\f', '\n')
    parts = re.split(r'(?m)^\s*(\d{2}) · ', flat)[1:]
    sections = {int(parts[i]):parts[i+1] for i in range(0,len(parts),2)}
    source = json.loads(bank_path.read_text(encoding='utf-8-sig'))
    questions = [(group,x['en']) for group in ('easy','medium','hard') for x in source[group]]
    rows = []
    for i,(difficulty,raw) in enumerate(questions,1):
        section = sections[i]
        title = raw.splitlines()[0].lstrip('# ')
        pdf_title = section.splitlines()[0].strip()
        jreq = raw.split('## Requirements',1)[1].split('## Interface Definition',1)[0]
        preq = section.split('Requirements',1)[1].split('Interface Definition',1)[0]
        left,right = tokens(jreq),tokens(preq)
        interface_j = clean_interface_json(raw.split('## Interface Definition',1)[1])
        interface_p = clean_interface_pdf(section.split('Interface Definition',1)[1])
        jc,pc = Counter(tokens(interface_j)),Counter(tokens(interface_p))
        rows.append({'task_id':f'PUB{i:03d}','title':title,'pdf_title':pdf_title,
            'title_matches':title==pdf_title,
            'difficulty_matches':f'Difficulty: {difficulty.capitalize()} ({difficulty})' in section,
            'requirements_tokens_match':left==right,
            'requirements_token_ratio':SequenceMatcher(a=left,b=right,autojunk=False).ratio(),
            'interface_tokens_match_as_multiset':jc==pc,
            'interface_missing_tokens':dict(jc-pc),'interface_extra_tokens':dict(pc-jc)})
    success = len(sections)==len(questions)==20 and all(r['title_matches'] and r['difficulty_matches']
        and r['requirements_tokens_match'] and r['interface_tokens_match_as_multiset'] for r in rows)
    result = {'pdf_pages_from_formfeed_extraction':text.count('\f'),
        'pdf_question_sections':len(sections),'json_question_count':len(questions),
        'aligned_under_documented_normalization':success,
        'comparison_method':'NFKC normalization; requirements word/operator token sequences; interface word/operator token multisets after removing table headers and HTML line-break markers. Page wrapping/table reading order and Markdown styling are ignored.',
        'limitations':'Token comparison is not byte equality or a formal semantic proof. Interface column association is retained by the original PDF/JSON and reviewed in the source records. Source descriptions remain unchanged in task requirements.',
        'sources':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in (assignment,bank_path,pdf_path,text_path)},
        'tasks':rows}
    (HERE/'source_alignment.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'aligned':success,'pdf_sections':len(sections),'json_questions':len(questions),
        'pages':text.count('\f'),'discrepancies':[r for r in rows if not (r['title_matches'] and r['difficulty_matches'] and r['requirements_tokens_match'] and r['interface_tokens_match_as_multiset'])]},ensure_ascii=False,indent=2))
    return 0 if success else 1

if __name__=='__main__':
    raise SystemExit(main())

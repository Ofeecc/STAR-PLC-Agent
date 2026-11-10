# Supplied assignment and public question sources

The project retains the supplied assignment, original question-bank JSON and original PDF in `requirements/source/`. These copies are byte-for-byte snapshots of the user-provided files; no API configuration file is included. The canonical structured benchmark preserves the original English `en` string for every public question. Interpretations, LTL and test cases are added separately.

| Snapshot | Source supplied beside the project | Purpose |
| --- | --- | --- |
| `source/Final project_ENGLISH.docx` | `Final project_ENGLISH.docx` | Complete assignment and grading rubric, including embedded example equations |
| `source/public_bank_original.json` | `大作业题库json/大作业题库json/大作业题库.json` | Canonical machine-readable public task text |
| `source/大作业题库.pdf` | `大作业题库.pdf` | Human-readable official question bank |

The PDF contains **25 pages and 20 questions**: six easy, eight medium and six hard. All twenty titles and difficulty labels match the JSON, in the same order. `public_bank_pdf.txt` preserves the full `pdftotext -layout -enc UTF-8` extraction, including page form-feed boundaries. The original PDF remains the authority for column association and visual layout; line breaks and table whitespace in extracted text are not semantic changes.

`verify_source_alignment.py` checks every question. After Unicode NFKC normalization and removal of Markdown/table-header formatting, all twenty requirement word/operator token sequences match exactly. The complete interface and trailing type/binding material also has matching word/operator token multisets. This accommodates PDF column wrapping and repeated table headings while retaining identifiers, values, types and operators. No substantive PDF/JSON difference was detected. These checks are not byte equality between two different formats and are not a formal proof that arbitrary prose is semantically equivalent. They also do not validate the project's added assumptions against the instructor's intent.

The source alignment audit is stored in `source_alignment.json`, with all twenty per-question checks, byte lengths and binary SHA-256 hashes. Reproduce it from the project root:

```powershell
pdftotext -layout -enc UTF-8 '.\requirements\source\大作业题库.pdf' '.\requirements\public_bank_pdf.txt'
& "$env:USERPROFILE\.conda\envs\Project1\python.exe" -X utf8 '.\requirements\verify_source_alignment.py'
```

The checked snapshots have these binary file hashes:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| Assignment DOCX | 21703 | `ef34f149d4153bb2aef180f4ef3c183028bc78616ad9013e36f1dca6731181f3` |
| Original public JSON | 50616 | `05170ae18c1ec7c316d8334a84b6ecd48de322c8236735d519b50f72f2d8d362` |
| Original question PDF | 317165 | `2c69ce26107e158aea4a9f1bd2efad272b994a9d5207f5e2b20500fdef6e2100` |

Binary source hashes identify the exact supplied files. The dataset/campaign code additionally computes canonical JSON-object digests; those intentionally differ from a raw file hash because they identify structured content independently of file whitespace. Do not compare the two hash kinds as if they were the same operation.

| Public ID | Official title | Difficulty |
| --- | --- | --- |
| PUB001 | Automated Filling Line Control | Easy |
| PUB002 | Dual-Word Edge Detection | Easy |
| PUB003 | Alarm Handling | Easy |
| PUB004 | Jam Pump Debouncing and Runtime Maintenance | Easy |
| PUB005 | Weld Gap Alarm and Startup Inhibition | Easy |
| PUB006 | Aeration Blower Delayed Start | Easy |
| PUB007 | Multi-Pump Switching Control System | Medium |
| PUB008 | Analog Batch Processing | Medium |
| PUB009 | Calculate Moving Average | Medium |
| PUB010 | Temperature Logic Control | Medium |
| PUB011 | Automated Production Line Control | Medium |
| PUB012 | Slab Thickness Alarm and Fault History | Medium |
| PUB013 | Office HVAC Multi-mode Energy-Saving Control | Medium |
| PUB014 | IPv4 Parsing with Format and Range Checks | Medium |
| PUB015 | Material Proportioning Process Control | Hard |
| PUB016 | Flexible Processing Control | Hard |
| PUB017 | Recipe Management System | Hard |
| PUB018 | FIFO First-In-First-Out Queue | Hard |
| PUB019 | Mechanical Arm Control | Hard |
| PUB020 | Production Control | Hard |

The assignment's motor example remains a separate timing ambiguity: its next-step formulas/table differ from a natural same-call reading of the prose. The benchmark explicitly records end-of-call observation and supplies the same convention to both frameworks. Agreement between the public PDF and JSON does not resolve that assignment example automatically.

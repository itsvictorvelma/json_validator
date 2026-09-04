# json-parser

Hand written JSON Parser. My solution for John Crickett's coding challenge at https://codingchallenges.substack.com/p/coding-challenge-2?utm_source=publication-search. Validates files via CLI (exit `0` / `1`).

```bash
python3 parser.py -f tests/step1/valid.json
```

```
scanner.py   lexer
parser.py    parser + CLI
tests/       step fixtures
```

Supports objects, arrays, strings, numbers, booleans, null through the challenge step 4 fixtures. No full escape sequences / exponents / AST build.

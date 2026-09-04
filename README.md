# json-parser

Hand-written JSON lexer + recursive-descent parser. Validates files via CLI (exit `0` / `1`). Not a `json` module replacement.

```bash
python3 parser.py -f tests/step1/valid.json
./run_tests.sh
```

```
scanner.py   lexer
parser.py    parser + CLI
tests/       step fixtures
run_tests.sh
```

Supports objects, arrays, strings, numbers, booleans, null through the challenge step 4 fixtures. No full escape sequences / exponents / AST build.

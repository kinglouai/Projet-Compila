# Pseudocode Compiler - Walkthrough

## Summary

Successfully implemented a French pseudocode to Python compiler with 4 clearly separated phases as required for the compilation course project.

## Project Structure

```
Compilateur/
├── lexer.py          # Phase 1: Lexical Analysis (320 lines)
├── parser.py         # Phase 2: Syntax Analysis (570 lines)
├── semantic.py       # Phase 3: Semantic Analysis (280 lines)
├── codegen.py        # Phase 4: Code Generation (310 lines)
├── main.py           # Main entry point (200 lines)
├── README.md         # Documentation
└── examples/
    ├── simple.algo       # Basic variable test
    ├── factorielle.algo  # Factorial with POUR loop
    ├── moyenne.algo      # Average calculation
    ├── condition.algo    # IF/ELSE demonstration
    └── boucles.algo      # Loops demonstration
```

---

## Phase 1: Lexer ([lexer.py](file:///c:/Users/jazou/Downloads/Compila/Compilateur/lexer.py))

**Converts source text into tokens**

### Key Classes
- `Token` - Stores type, value, and line number
- `Lexer` - Tokenizes the source code
- `LexerError` - Reports lexical errors with line numbers

### Supported Tokens
| Category | Examples |
|----------|----------|
| Keywords | `ALGORITHME`, `VAR`, `DEBUT`, `FIN`, `SI`, `POUR`, `TANT_QUE`... |
| Types | `ENTIER`, `REEL`, `CHAINE`, `BOOLEEN` |
| Operators | `←`, `+`, `-`, `*`, `/`, `=`, `<`, `>`, `≠`, `ET`, `OU` |
| Literals | Numbers, Strings, Booleans |

---

## Phase 2: Parser ([parser.py](file:///c:/Users/jazou/Downloads/Compila/Compilateur/parser.py))

**Builds Abstract Syntax Tree (AST) from tokens**

### AST Node Classes
- `ProgramNode` - Root of the program
- `DeclarationNode` - Variable declarations
- `AssignmentNode` - Assignments (x ← value)
- `BinaryOpNode` - Binary operations (a + b)
- `IfNode`, `WhileNode`, `ForNode` - Control structures
- `PrintNode`, `ReadNode` - I/O operations

### Parser Features
- Recursive descent parsing
- Proper operator precedence (multiplicative > additive > comparison > logical)
- Clear error messages with line numbers

---

## Phase 3: Semantic Analyzer ([semantic.py](file:///c:/Users/jazou/Downloads/Compila/Compilateur/semantic.py))

**Validates the AST for semantic errors**

### Key Classes
- `SymbolTable` - Tracks declared variables with types
- `SemanticAnalyzer` - Walks AST and validates

### Checks Performed
- ✅ Variable declared before use
- ✅ No duplicate declarations
- ✅ Loop variables exist

---

## Phase 4: Code Generator ([codegen.py](file:///c:/Users/jazou/Downloads/Compila/Compilateur/codegen.py))

**Produces executable Python code**

### Translations
| Pseudocode | Python |
|------------|--------|
| `VAR x : ENTIER` | `x = 0  # ENTIER` |
| `x ← 10` | `x = 10` |
| `ECRIRE(x)` | `print(x)` |
| `SI x > 5 ALORS...` | `if x > 5:` |
| `POUR i DE 1 A n FAIRE...` | `for i in range(1, n + 1):` |
| `TANT_QUE x < 10 FAIRE...` | `while x < 10:` |

---

## Usage Examples

### Compile a file
```bash
python main.py examples/simple.algo
```

### Compile and run
```bash
python main.py examples/factorielle.algo -r
```

### Example Output
```
============================================================
  Compilateur Pseudocode → Python
============================================================
  Fichier source: examples/factorielle.algo
  Fichier cible:  examples/factorielle.py
============================================================

Phase 1: Analyse Lexicale...
  ✓ 46 tokens générés
Phase 2: Analyse Syntaxique...
  ✓ AST construit: Factorielle
    - 3 déclaration(s)
    - 4 instruction(s)
Phase 3: Analyse Sémantique...
  ✓ Aucune erreur sémantique
    - 3 variable(s) dans la table des symboles
Phase 4: Génération de Code...
  ✓ Code Python généré

============================================================
  ✓ Compilation réussie!
============================================================
```

---

## Testing Summary

| Module | Tests | Result |
|--------|-------|--------|
| `lexer.py` | 6 tests | ✅ All pass |
| `parser.py` | 6 tests | ✅ All pass |
| `semantic.py` | 6 tests | ✅ All pass |
| `codegen.py` | 6 tests | ✅ All pass |
| Integration | 5 examples | ✅ All compile and run |

---

## Features Implemented

- ✅ All 4 compilation phases clearly separated
- ✅ French keywords and syntax
- ✅ Variable declarations with types
- ✅ Arithmetic and logical expressions with precedence
- ✅ IF/ELSE conditionals
- ✅ FOR loops (POUR)
- ✅ WHILE loops (TANT_QUE)
- ✅ Print statements
- ✅ Comments support (//)
- ✅ Clear error messages with line numbers
- ✅ Generated Python code is executable

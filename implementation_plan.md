# Pseudocode Compiler - Implementation Plan

A French pseudocode to Python compiler with 4 clearly separated phases for a compilation course project.

## Proposed Changes

### Phase 1: Lexer Component

#### [NEW] [lexer.py](file:///c:/Users/jazou/Downloads/Compila/Compilateur/lexer.py)

Implements the lexical analysis phase:
- **Token class**: Represents individual tokens with type, value, and line number
- **Lexer class**: Breaks pseudocode text into tokens
- Supports all French keywords, data types, operators, and symbols
- Clear error messages with line numbers

---

### Phase 2: Parser Component

#### [NEW] [parser.py](file:///c:/Users/jazou/Downloads/Compila/Compilateur/parser.py)

Implements the syntax analysis phase:
- **AST Node classes**: DeclarationNode, AssignmentNode, NumberNode, VariableNode, BinaryOpNode, PrintNode, IfNode, ProgramNode
- **Parser class**: Builds AST from token stream using recursive descent parsing
- Supports variable declarations, assignments, expressions, print statements, and IF statements

---

### Phase 3: Semantic Analyzer Component

#### [NEW] [semantic.py](file:///c:/Users/jazou/Downloads/Compila/Compilateur/semantic.py)

Implements the semantic analysis phase:
- **SymbolTable class**: Stores variable declarations with type and line info
- **SemanticAnalyzer class**: Validates the AST
- Checks: variable declared before use, no duplicate declarations

---

### Phase 4: Code Generator Component

#### [NEW] [codegen.py](file:///c:/Users/jazou/Downloads/Compila/Compilateur/codegen.py)

Implements the code generation phase:
- **CodeGenerator class**: Converts validated AST to Python code
- Handles declarations, assignments, expressions, print statements, and control flow
- Manages Python indentation for control structures

---

### Integration

#### [NEW] [main.py](file:///c:/Users/jazou/Downloads/Compila/Compilateur/main.py)

Main entry point that chains all 4 phases:
1. Read pseudocode from `.algo` file
2. Run lexer → tokens
3. Run parser → AST
4. Run semantic analyzer → validated AST
5. Run code generator → Python code
6. Write output to `.py` file

#### [NEW] [examples/test_simple.algo](file:///c:/Users/jazou/Downloads/Compila/Compilateur/examples/test_simple.algo)

Simple test file with variable declarations and print statements.

#### [NEW] [README.md](file:///c:/Users/jazou/Downloads/Compila/Compilateur/README.md)

Documentation with usage instructions and examples.

---

## Verification Plan

### Automated Tests
- Test lexer with simple input: `VAR x : ENTIER`
- Test parser with tokens from lexer
- Test semantic analyzer with valid and invalid programs
- Test code generator by running generated Python code with `exec()`

### Manual Verification
- Run `python main.py test_simple.algo`
- Verify generated `.py` file runs correctly

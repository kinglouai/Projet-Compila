# Pseudocode Compiler Project

## Overview
Building a French pseudocode to Python compiler with 4 phases: Lexer, Parser, Semantic Analyzer, and Code Generator.

## Phase 1: Lexer (Analyse Lexicale)
- [x] Create Token class
- [x] Create Lexer class with tokenize() method
- [x] Support keywords: ALGORITHME, VAR, DEBUT, FIN, ECRIRE, LIRE, SI, ALORS, SINON, FIN_SI, TANT_QUE, FAIRE, FIN_TANT_QUE, POUR, DE, A, FIN_POUR
- [x] Support types: ENTIER, REEL, CHAINE, BOOLEEN
- [x] Support operators: ←, +, -, *, /, =, <, >, <=, >=, ≠, ET, OU, NON
- [x] Support symbols: :, ,, (, )
- [x] Support identifiers and numbers
- [x] Add error handling with line numbers
- [x] Test lexer with examples

## Phase 2: Parser (Analyse Syntaxique)
- [x] Create AST node classes
- [x] Create Parser class
- [x] Parse declarations
- [x] Parse assignments
- [x] Parse expressions
- [x] Parse print statements
- [x] Parse IF statements
- [x] Test parser with examples

## Phase 3: Semantic Analyzer (Analyse Sémantique)
- [x] Create SymbolTable class
- [x] Create SemanticAnalyzer class
- [x] Check variable declared before use
- [x] Check no duplicate declarations
- [x] Test semantic analyzer

## Phase 4: Code Generator (Génération de Code)
- [x] Create CodeGenerator class
- [x] Handle declarations
- [x] Handle assignments
- [x] Handle print statements
- [x] Handle expressions
- [x] Test code generator

## Integration
- [x] Create main.py entry point
- [x] Create test files
- [x] Create README.md

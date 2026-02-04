"""
Compilateur Pseudocode → Python
Point d'entrée principal

Usage:
    python main.py <fichier.algo>
    python main.py examples/factorielle.algo

Ce compilateur transforme du pseudocode français en code Python exécutable.
Il passe par 4 phases: Lexer → Parser → Semantic → CodeGen
"""

import sys
import os

# Configuration de l'encodage pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from lexer import Lexer, LexerError
from parser import Parser, ParserError
from semantic import SemanticAnalyzer, SemanticError
from codegen import CodeGenerator


def compile_file(input_filename, output_filename=None, execute=False):
    """
    Compile un fichier pseudocode en Python.
    
    Args:
        input_filename: Chemin du fichier .algo source
        output_filename: Chemin du fichier .py de sortie (optionnel)
        execute: Si True, exécute le code généré après compilation
        
    Returns:
        True si la compilation réussit, False sinon
    """
    # Générer le nom de fichier de sortie si non spécifié
    if output_filename is None:
        base_name = os.path.splitext(input_filename)[0]
        output_filename = f"{base_name}.py"
    
    print("=" * 60)
    print(f"  Compilateur Pseudocode → Python")
    print("=" * 60)
    print(f"  Fichier source: {input_filename}")
    print(f"  Fichier cible:  {output_filename}")
    print("=" * 60)
    print()
    
    try:
        # Lire le fichier source
        with open(input_filename, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # ============================================
        # Phase 1: Analyse Lexicale
        # ============================================
        print("Phase 1: Analyse Lexicale...")
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        print(f"  ✓ {len(tokens)} tokens générés")
        
        # ============================================
        # Phase 2: Analyse Syntaxique
        # ============================================
        print("Phase 2: Analyse Syntaxique...")
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"  ✓ AST construit: {ast.name}")
        print(f"    - {len(ast.declarations)} déclaration(s)")
        print(f"    - {len(ast.statements)} instruction(s)")
        
        # ============================================
        # Phase 3: Analyse Sémantique
        # ============================================
        print("Phase 3: Analyse Sémantique...")
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        print(f"  ✓ Aucune erreur sémantique")
        print(f"    - {len(analyzer.symbol_table.symbols)} variable(s) dans la table des symboles")
        
        # ============================================
        # Phase 4: Génération de Code
        # ============================================
        print("Phase 4: Génération de Code...")
        generator = CodeGenerator()
        python_code = generator.generate(ast)
        print(f"  ✓ Code Python généré")
        
        # Écrire le fichier de sortie
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(python_code)
        
        print()
        print("=" * 60)
        print(f"  ✓ Compilation réussie!")
        print(f"  Fichier généré: {output_filename}")
        print("=" * 60)
        
        # Afficher le code généré
        print()
        print("Code Python généré:")
        print("-" * 40)
        print(python_code)
        print("-" * 40)
        
        # Exécuter si demandé
        if execute:
            print()
            print("Exécution du programme:")
            print("-" * 40)
            exec(python_code)
            print("-" * 40)
        
        return True
        
    except FileNotFoundError:
        print(f"  ✗ Erreur: Fichier '{input_filename}' introuvable")
        return False
    
    except LexerError as e:
        print(f"  ✗ {e}")
        return False
    
    except ParserError as e:
        print(f"  ✗ {e}")
        return False
    
    except SemanticError as e:
        print(f"  ✗ {e}")
        return False
    
    except Exception as e:
        print(f"  ✗ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        return False


def print_help():
    """Affiche l'aide d'utilisation."""
    print("""
Compilateur Pseudocode → Python

USAGE:
    python main.py <fichier.algo>           Compile le fichier
    python main.py <fichier.algo> -r        Compile et exécute
    python main.py <fichier.algo> -o <out>  Spécifie le fichier de sortie
    python main.py --help                   Affiche cette aide

EXEMPLES:
    python main.py examples/simple.algo
    python main.py examples/factorielle.algo -r
    python main.py mon_programme.algo -o sortie.py

PHASES DE COMPILATION:
    1. Analyse Lexicale   - Convertit le texte en tokens
    2. Analyse Syntaxique - Construit l'arbre syntaxique (AST)
    3. Analyse Sémantique - Vérifie les erreurs (variables non déclarées)
    4. Génération de Code - Produit le code Python
""")


def main():
    """Point d'entrée principal."""
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
    
    # Aide
    if sys.argv[1] in ('--help', '-h', '/?'):
        print_help()
        sys.exit(0)
    
    # Fichier source
    input_file = sys.argv[1]
    output_file = None
    execute = False
    
    # Parser les options
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == '-o' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        elif arg in ('-r', '--run'):
            execute = True
            i += 1
        else:
            print(f"Option inconnue: {arg}")
            sys.exit(1)
    
    # Compiler
    success = compile_file(input_file, output_file, execute)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

"""
Code Generator (Génération de Code) - Phase 4 du Compilateur
Génère du code Python exécutable à partir de l'AST

Ce module parcourt l'AST validé et produit du code Python
équivalent au pseudocode source.
"""

from parser import (
    ASTNode, ProgramNode, DeclarationNode, AssignmentNode,
    NumberNode, StringNode, BooleanNode, VariableNode,
    BinaryOpNode, UnaryOpNode, PrintNode, ReadNode,
    IfNode, WhileNode, ForNode,
    FunctionDefNode, FunctionCallNode, ReturnNode,
    ArrayDeclarationNode, ArrayAccessNode, ArrayAssignmentNode
)


class CodeGenerator:
    """
    Générateur de code Python à partir de l'AST.
    
    Parcourt l'AST et produit du code Python équivalent
    avec une gestion correcte de l'indentation.
    """
    
    def __init__(self):
        """Initialise le générateur de code."""
        self.code = []  # Liste des lignes de code
        self.indent_level = 0  # Niveau d'indentation actuel
    
    def indent(self):
        """Retourne l'indentation actuelle (4 espaces par niveau)."""
        return "    " * self.indent_level
    
    def add_line(self, line):
        """Ajoute une ligne de code avec l'indentation actuelle."""
        self.code.append(f"{self.indent()}{line}")
    
    def generate(self, node):
        """
        Génère le code Python à partir d'un noeud AST.
        
        Args:
            node: Le noeud AST racine (normalement un ProgramNode)
            
        Returns:
            String contenant le code Python généré
        """
        if isinstance(node, ProgramNode):
            return self._generate_program(node)
        else:
            raise Exception(f"Attendu ProgramNode, reçu {type(node)}")
    
    def _generate_program(self, node):
        """Génère le code pour un programme complet."""
        # En-tête avec commentaire
        self.code.append(f"# Programme généré à partir de: {node.name}")
        self.code.append(f"# Compilateur Pseudocode → Python")
        self.code.append("")
        
        # Générer les fonctions en premier
        if node.functions:
            self.code.append("# Définitions des fonctions")
            for func in node.functions:
                self._generate_function(func)
            self.code.append("")
        
        # Générer les déclarations (initialisation des variables)
        if node.declarations:
            self.code.append("# Déclarations des variables")
            for decl in node.declarations:
                if isinstance(decl, ArrayDeclarationNode):
                    self._generate_array_declaration(decl)
                else:
                    self._generate_declaration(decl)
            self.code.append("")
        
        # Générer les instructions
        if node.statements:
            self.code.append("# Instructions")
            for stmt in node.statements:
                self._generate_statement(stmt)
        
        return "\n".join(self.code)
    
    def _generate_declaration(self, node):
        """
        Génère le code pour une déclaration de variable.
        
        VAR x : ENTIER → x = 0
        VAR y : REEL → y = 0.0
        VAR msg : CHAINE → msg = ""
        VAR flag : BOOLEEN → flag = False
        """
        init_values = {
            'ENTIER': '0',
            'REEL': '0.0',
            'CHAINE': '""',
            'BOOLEEN': 'False'
        }
        
        init_value = init_values.get(node.var_type, 'None')
        self.add_line(f"{node.variable} = {init_value}  # {node.var_type}")
    
    def _generate_array_declaration(self, node):
        """
        Génère le code pour une déclaration de tableau.
        
        VAR tab : TABLEAU[10] DE ENTIER → tab = [0] * 10
        """
        init_values = {
            'ENTIER': '0',
            'REEL': '0.0',
            'CHAINE': '""',
            'BOOLEEN': 'False'
        }
        
        init_value = init_values.get(node.element_type, 'None')
        size_code = self._generate_expression(node.size)
        self.add_line(f"{node.variable} = [{init_value}] * {size_code}  # TABLEAU DE {node.element_type}")
    
    def _generate_function(self, node):
        """
        Génère le code pour une définition de fonction.
        
        FONCTION carre(x: ENTIER) : ENTIER → def carre(x):
        """
        # Paramètres
        params = ", ".join([p[0] for p in node.parameters])
        self.add_line(f"def {node.name}({params}):")
        
        self.indent_level += 1
        
        # Déclarations locales
        for decl in node.declarations:
            self._generate_declaration(decl)
        
        # Corps de la fonction
        for stmt in node.body:
            self._generate_statement(stmt)
        
        self.indent_level -= 1
        self.code.append("")  # Ligne vide après la fonction
    
    def _generate_statement(self, node):
        """Génère le code pour une instruction."""
        if isinstance(node, AssignmentNode):
            self._generate_assignment(node)
        
        elif isinstance(node, PrintNode):
            self._generate_print(node)
        
        elif isinstance(node, ReadNode):
            self._generate_read(node)
        
        elif isinstance(node, IfNode):
            self._generate_if(node)
        
        elif isinstance(node, WhileNode):
            self._generate_while(node)
        
        elif isinstance(node, ForNode):
            self._generate_for(node)
        
        elif isinstance(node, ReturnNode):
            self._generate_return(node)
        
        elif isinstance(node, FunctionCallNode):
            self._generate_function_call_statement(node)
        
        elif isinstance(node, ArrayAssignmentNode):
            self._generate_array_assignment(node)
        
        else:
            raise Exception(f"Type d'instruction inconnu: {type(node)}")
    
    def _generate_return(self, node):
        """
        Génère le code pour une instruction RETOURNER.
        
        RETOURNER x * x → return x * x
        """
        value_code = self._generate_expression(node.value)
        self.add_line(f"return {value_code}")
    
    def _generate_array_assignment(self, node):
        """
        Génère le code pour une affectation à un élément de tableau.
        
        tab[i] ← 10 → tab[i] = 10
        """
        index_code = self._generate_expression(node.index)
        value_code = self._generate_expression(node.value)
        self.add_line(f"{node.array_name}[{index_code}] = {value_code}")
    
    def _generate_function_call_statement(self, node):
        """Génère le code pour un appel de fonction comme instruction."""
        args = ", ".join([self._generate_expression(arg) for arg in node.arguments])
        self.add_line(f"{node.name}({args})")
    
    def _generate_assignment(self, node):
        """
        Génère le code pour une affectation.
        
        x ← 10 → x = 10
        """
        value_code = self._generate_expression(node.value)
        self.add_line(f"{node.target} = {value_code}")
    
    def _generate_print(self, node):
        """
        Génère le code pour une instruction ECRIRE.
        
        ECRIRE(x) → print(x)
        ECRIRE("Hello", x) → print("Hello", x)
        """
        expressions = [self._generate_expression(expr) for expr in node.expressions]
        self.add_line(f"print({', '.join(expressions)})")
    
    def _generate_read(self, node):
        """
        Génère le code pour une instruction LIRE.
        
        LIRE(x) → x = int(input())  (pour ENTIER)
        
        Note: On utilise int() par défaut, mais idealement
        il faudrait vérifier le type de la variable.
        """
        # Par simplicité, on suppose que c'est toujours un entier
        # Une amélioration serait de passer la table des symboles
        self.add_line(f"{node.variable} = int(input())")
    
    def _generate_if(self, node):
        """
        Génère le code pour une instruction SI.
        
        SI x > 5 ALORS        →  if x > 5:
            ECRIRE(x)         →      print(x)
        SINON                 →  else:
            ECRIRE("petit")   →      print("petit")
        FIN_SI                →
        """
        condition_code = self._generate_expression(node.condition)
        self.add_line(f"if {condition_code}:")
        
        # Bloc ALORS
        self.indent_level += 1
        for stmt in node.then_branch:
            self._generate_statement(stmt)
        self.indent_level -= 1
        
        # Bloc SINON (si présent)
        if node.else_branch:
            self.add_line("else:")
            self.indent_level += 1
            for stmt in node.else_branch:
                self._generate_statement(stmt)
            self.indent_level -= 1
    
    def _generate_while(self, node):
        """
        Génère le code pour une boucle TANT_QUE.
        
        TANT_QUE x < 10 FAIRE  →  while x < 10:
            ECRIRE(x)          →      print(x)
            x ← x + 1          →      x = x + 1
        FIN_TANT_QUE           →
        """
        condition_code = self._generate_expression(node.condition)
        self.add_line(f"while {condition_code}:")
        
        self.indent_level += 1
        for stmt in node.body:
            self._generate_statement(stmt)
        self.indent_level -= 1
    
    def _generate_for(self, node):
        """
        Génère le code pour une boucle POUR.
        
        POUR i DE 1 A 10 FAIRE  →  for i in range(1, 10 + 1):
            ECRIRE(i)           →      print(i)
        FIN_POUR                →
        """
        start_code = self._generate_expression(node.start)
        end_code = self._generate_expression(node.end)
        
        # En Python, range() exclut la borne supérieure, donc on ajoute 1
        self.add_line(f"for {node.variable} in range({start_code}, {end_code} + 1):")
        
        self.indent_level += 1
        for stmt in node.body:
            self._generate_statement(stmt)
        self.indent_level -= 1
    
    def _generate_expression(self, node):
        """
        Génère le code pour une expression.
        
        Returns:
            String contenant l'expression Python
        """
        if isinstance(node, NumberNode):
            return str(node.value)
        
        elif isinstance(node, StringNode):
            # Échapper les guillemets dans la chaîne
            escaped = node.value.replace('"', '\\"')
            return f'"{escaped}"'
        
        elif isinstance(node, BooleanNode):
            return "True" if node.value else "False"
        
        elif isinstance(node, VariableNode):
            return node.name
        
        elif isinstance(node, BinaryOpNode):
            return self._generate_binary_op(node)
        
        elif isinstance(node, UnaryOpNode):
            return self._generate_unary_op(node)
        
        elif isinstance(node, FunctionCallNode):
            args = ", ".join([self._generate_expression(arg) for arg in node.arguments])
            return f"{node.name}({args})"
        
        elif isinstance(node, ArrayAccessNode):
            index_code = self._generate_expression(node.index)
            return f"{node.array_name}[{index_code}]"
        
        else:
            raise Exception(f"Type d'expression inconnu: {type(node)}")
    
    def _generate_binary_op(self, node):
        """
        Génère le code pour une opération binaire.
        
        Convertit les opérateurs pseudocode en Python:
        - = (comparaison) → ==
        - ≠ → !=
        - ET → and
        - OU → or
        """
        left = self._generate_expression(node.left)
        right = self._generate_expression(node.right)
        
        # Mapping des opérateurs pseudocode vers Python
        op_mapping = {
            '=': '==',      # Égalité
            '≠': '!=',      # Différent
            'ET': 'and',    # ET logique
            'OU': 'or',     # OU logique
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '<': '<',
            '>': '>',
            '<=': '<=',
            '>=': '>='
        }
        
        python_op = op_mapping.get(node.operator, node.operator)
        
        return f"({left} {python_op} {right})"
    
    def _generate_unary_op(self, node):
        """
        Génère le code pour une opération unaire.
        
        - NON x → not x
        - -x → -x
        """
        operand = self._generate_expression(node.operand)
        
        if node.operator == 'NON':
            return f"(not {operand})"
        else:
            return f"({node.operator}{operand})"


# ============================================================
# Tests du générateur de code
# ============================================================

if __name__ == '__main__':
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    from lexer import Lexer
    from parser import Parser
    from semantic import SemanticAnalyzer
    
    def compile_and_run(code, description):
        """Compile le pseudocode et exécute le Python généré."""
        print(f"=== {description} ===")
        print("Pseudocode:")
        print(code)
        print()
        
        try:
            # Phase 1: Lexer
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            
            # Phase 2: Parser
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Phase 3: Semantic Analysis
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            
            # Phase 4: Code Generation
            generator = CodeGenerator()
            python_code = generator.generate(ast)
            
            print("Code Python généré:")
            print(python_code)
            print()
            
            print("Exécution:")
            print("-" * 30)
            exec(python_code)
            print("-" * 30)
            print("✓ Succès!")
            
        except Exception as e:
            print(f"✗ Erreur: {e}")
        
        print()
    
    # Test 1: Programme simple
    compile_and_run("""ALGORITHME TestSimple
VAR x : ENTIER
VAR y : ENTIER
DEBUT
    x ← 10
    y ← 20
    ECRIRE(x + y)
FIN
""", "Test 1: Programme simple")
    
    # Test 2: Expressions arithmétiques
    compile_and_run("""ALGORITHME TestArith
VAR a : ENTIER
VAR b : ENTIER
VAR resultat : ENTIER
DEBUT
    a ← 15
    b ← 25
    resultat ← a + b * 2
    ECRIRE("Resultat:", resultat)
FIN
""", "Test 2: Expressions arithmétiques")
    
    # Test 3: Condition SI
    compile_and_run("""ALGORITHME TestSi
VAR x : ENTIER
DEBUT
    x ← 10
    SI x > 5 ALORS
        ECRIRE("x est grand")
    SINON
        ECRIRE("x est petit")
    FIN_SI
FIN
""", "Test 3: Condition SI")
    
    # Test 4: Boucle POUR
    compile_and_run("""ALGORITHME TestPour
VAR i : ENTIER
VAR somme : ENTIER
DEBUT
    somme ← 0
    POUR i DE 1 A 5 FAIRE
        somme ← somme + i
    FIN_POUR
    ECRIRE("Somme de 1 a 5:", somme)
FIN
""", "Test 4: Boucle POUR")
    
    # Test 5: Boucle TANT_QUE
    compile_and_run("""ALGORITHME TestTantQue
VAR x : ENTIER
DEBUT
    x ← 1
    TANT_QUE x <= 3 FAIRE
        ECRIRE("x =", x)
        x ← x + 1
    FIN_TANT_QUE
    ECRIRE("Fin de la boucle")
FIN
""", "Test 5: Boucle TANT_QUE")
    
    # Test 6: Factorielle
    compile_and_run("""ALGORITHME Factorielle
VAR n : ENTIER
VAR resultat : ENTIER
VAR i : ENTIER
DEBUT
    n ← 5
    resultat ← 1
    POUR i DE 1 A n FAIRE
        resultat ← resultat * i
    FIN_POUR
    ECRIRE("Factorielle de", n, "=", resultat)
FIN
""", "Test 6: Factorielle")
    
    print("✓ Tous les tests du générateur de code terminés!")

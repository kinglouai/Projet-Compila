"""
Parser (Analyse Syntaxique) - Phase 2 du Compilateur
Construit un arbre syntaxique abstrait (AST) à partir des tokens

Ce module prend la liste de tokens produite par le lexer et
construit une structure d'arbre représentant le programme.
"""

from lexer import Token, Lexer, LexerError


# ============================================================
# Classes de noeuds AST (Abstract Syntax Tree)
# ============================================================

class ASTNode:
    """Classe de base pour tous les noeuds de l'AST."""
    pass


class ProgramNode(ASTNode):
    """
    Représente un programme complet.
    
    Attributes:
        name: Nom de l'algorithme
        declarations: Liste des déclarations de variables
        functions: Liste des définitions de fonctions
        statements: Liste des instructions
    """
    
    def __init__(self, name, declarations, statements, functions=None):
        self.name = name
        self.declarations = declarations
        self.functions = functions or []
        self.statements = statements
    
    def __repr__(self):
        return f"Program({self.name}, decls={len(self.declarations)}, funcs={len(self.functions)}, stmts={len(self.statements)})"


class DeclarationNode(ASTNode):
    """
    Représente une déclaration de variable: VAR x : ENTIER
    
    Attributes:
        variable: Nom de la variable
        var_type: Type de la variable (ENTIER, REEL, etc.)
        line: Numéro de ligne pour les erreurs
    """
    
    def __init__(self, variable, var_type, line=1):
        self.variable = variable
        self.var_type = var_type
        self.line = line
    
    def __repr__(self):
        return f"Declare({self.variable}: {self.var_type})"


class AssignmentNode(ASTNode):
    """
    Représente une affectation: x ← 10
    
    Attributes:
        target: Nom de la variable cible
        value: Expression à assigner (peut être un noeud)
        line: Numéro de ligne
    """
    
    def __init__(self, target, value, line=1):
        self.target = target
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"Assign({self.target} = {self.value})"


class NumberNode(ASTNode):
    """
    Représente un nombre littéral: 10, 3.14
    
    Attributes:
        value: La valeur numérique
    """
    
    def __init__(self, value, line=1):
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"Number({self.value})"


class StringNode(ASTNode):
    """
    Représente une chaîne littérale: "Bonjour"
    
    Attributes:
        value: La valeur de la chaîne
    """
    
    def __init__(self, value, line=1):
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"String({repr(self.value)})"


class BooleanNode(ASTNode):
    """
    Représente une valeur booléenne: VRAI, FAUX
    
    Attributes:
        value: True ou False
    """
    
    def __init__(self, value, line=1):
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"Boolean({self.value})"


class VariableNode(ASTNode):
    """
    Représente une référence à une variable: x
    
    Attributes:
        name: Nom de la variable
    """
    
    def __init__(self, name, line=1):
        self.name = name
        self.line = line
    
    def __repr__(self):
        return f"Var({self.name})"


class BinaryOpNode(ASTNode):
    """
    Représente une opération binaire: a + b, x * 2
    
    Attributes:
        left: Opérande gauche
        operator: L'opérateur (+, -, *, /, =, <, >, etc.)
        right: Opérande droite
    """
    
    def __init__(self, left, operator, right, line=1):
        self.left = left
        self.operator = operator
        self.right = right
        self.line = line
    
    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"


class UnaryOpNode(ASTNode):
    """
    Représente une opération unaire: NON x, -5
    
    Attributes:
        operator: L'opérateur (NON, -)
        operand: L'opérande
    """
    
    def __init__(self, operator, operand, line=1):
        self.operator = operator
        self.operand = operand
        self.line = line
    
    def __repr__(self):
        return f"({self.operator} {self.operand})"


class PrintNode(ASTNode):
    """
    Représente une instruction ECRIRE: ECRIRE(x)
    
    Attributes:
        expressions: Liste d'expressions à afficher
    """
    
    def __init__(self, expressions, line=1):
        self.expressions = expressions if isinstance(expressions, list) else [expressions]
        self.line = line
    
    def __repr__(self):
        return f"Print({self.expressions})"


class ReadNode(ASTNode):
    """
    Représente une instruction LIRE: LIRE(x)
    
    Attributes:
        variable: Nom de la variable à lire
    """
    
    def __init__(self, variable, line=1):
        self.variable = variable
        self.line = line
    
    def __repr__(self):
        return f"Read({self.variable})"


class IfNode(ASTNode):
    """
    Représente une instruction SI: SI condition ALORS ... SINON ... FIN_SI
    
    Attributes:
        condition: Expression de condition
        then_branch: Liste d'instructions si vrai
        else_branch: Liste d'instructions si faux (peut être None)
    """
    
    def __init__(self, condition, then_branch, else_branch=None, line=1):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
        self.line = line
    
    def __repr__(self):
        if self.else_branch:
            return f"If({self.condition}, then={len(self.then_branch)}, else={len(self.else_branch)})"
        return f"If({self.condition}, then={len(self.then_branch)})"


class WhileNode(ASTNode):
    """
    Représente une boucle TANT_QUE: TANT_QUE condition FAIRE ... FIN_TANT_QUE
    
    Attributes:
        condition: Expression de condition
        body: Liste d'instructions du corps de la boucle
    """
    
    def __init__(self, condition, body, line=1):
        self.condition = condition
        self.body = body
        self.line = line
    
    def __repr__(self):
        return f"While({self.condition}, body={len(self.body)})"


class ForNode(ASTNode):
    """
    Représente une boucle POUR: POUR i DE 1 A n FAIRE ... FIN_POUR
    
    Attributes:
        variable: Variable de boucle
        start: Expression de début
        end: Expression de fin
        body: Liste d'instructions du corps
    """
    
    def __init__(self, variable, start, end, body, line=1):
        self.variable = variable
        self.start = start
        self.end = end
        self.body = body
        self.line = line
    
    def __repr__(self):
        return f"For({self.variable} from {self.start} to {self.end}, body={len(self.body)})"


class FunctionDefNode(ASTNode):
    """
    Représente une définition de fonction:
    FONCTION nom(param1: TYPE, param2: TYPE) : TYPE_RETOUR
    
    Attributes:
        name: Nom de la fonction
        parameters: Liste de tuples (nom, type)
        return_type: Type de retour (peut être None pour procédure)
        declarations: Déclarations locales
        body: Liste d'instructions
    """
    
    def __init__(self, name, parameters, return_type, declarations, body, line=1):
        self.name = name
        self.parameters = parameters  # [(nom, type), ...]
        self.return_type = return_type
        self.declarations = declarations
        self.body = body
        self.line = line
    
    def __repr__(self):
        params = ", ".join([f"{p[0]}:{p[1]}" for p in self.parameters])
        return f"Function({self.name}({params}) -> {self.return_type})"


class FunctionCallNode(ASTNode):
    """
    Représente un appel de fonction: nom(arg1, arg2)
    
    Attributes:
        name: Nom de la fonction
        arguments: Liste d'expressions (arguments)
    """
    
    def __init__(self, name, arguments, line=1):
        self.name = name
        self.arguments = arguments
        self.line = line
    
    def __repr__(self):
        return f"Call({self.name}, args={len(self.arguments)})"


class ReturnNode(ASTNode):
    """
    Représente une instruction RETOURNER: RETOURNER expression
    
    Attributes:
        value: Expression à retourner
    """
    
    def __init__(self, value, line=1):
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"Return({self.value})"


class ArrayDeclarationNode(ASTNode):
    """
    Représente une déclaration de tableau: VAR tab : TABLEAU[10] DE ENTIER
    
    Attributes:
        variable: Nom du tableau
        size: Expression représentant la taille
        element_type: Type des éléments (ENTIER, REEL, etc.)
        line: Numéro de ligne
    """
    
    def __init__(self, variable, size, element_type, line=1):
        self.variable = variable
        self.size = size
        self.element_type = element_type
        self.line = line
    
    def __repr__(self):
        return f"ArrayDeclare({self.variable}: TABLEAU[{self.size}] DE {self.element_type})"


class ArrayAccessNode(ASTNode):
    """
    Représente un accès à un élément de tableau: tab[i]
    
    Attributes:
        array_name: Nom du tableau
        index: Expression représentant l'index
        line: Numéro de ligne
    """
    
    def __init__(self, array_name, index, line=1):
        self.array_name = array_name
        self.index = index
        self.line = line
    
    def __repr__(self):
        return f"ArrayAccess({self.array_name}[{self.index}])"


class ArrayAssignmentNode(ASTNode):
    """
    Représente une affectation à un élément de tableau: tab[i] ← valeur
    
    Attributes:
        array_name: Nom du tableau
        index: Expression représentant l'index
        value: Expression à assigner
        line: Numéro de ligne
    """
    
    def __init__(self, array_name, index, value, line=1):
        self.array_name = array_name
        self.index = index
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"ArrayAssign({self.array_name}[{self.index}] = {self.value})"


# ============================================================
# Erreur de syntaxe
# ============================================================

class ParserError(Exception):
    """Exception levée lors d'une erreur de syntaxe."""
    
    def __init__(self, message, line):
        self.message = message
        self.line = line
        super().__init__(f"Erreur Syntaxique (ligne {line}): {message}")


# ============================================================
# Parser - Analyseur syntaxique
# ============================================================

class Parser:
    """
    Analyseur syntaxique pour le pseudocode français.
    
    Utilise la technique de descente récursive (recursive descent)
    pour construire l'AST à partir des tokens.
    """
    
    def __init__(self, tokens):
        """
        Initialise le parser avec la liste de tokens.
        
        Args:
            tokens: Liste de Token produite par le Lexer
        """
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
    
    def advance(self):
        """Avance au token suivant."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def peek(self, offset=1):
        """Regarde un token à l'avance sans avancer."""
        peek_pos = self.pos + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return None
    
    def eat(self, token_type, expected_value=None):
        """
        Consomme un token du type attendu.
        
        Args:
            token_type: Le type de token attendu
            expected_value: Optionnel, la valeur attendue
            
        Raises:
            ParserError: Si le token ne correspond pas
        """
        if self.current_token is None:
            raise ParserError(f"Fin de fichier inattendue, attendu {token_type}", 
                            self.tokens[-1].line if self.tokens else 1)
        
        if self.current_token.type != token_type:
            raise ParserError(
                f"Attendu {token_type}, trouvé {self.current_token.type} ('{self.current_token.value}')",
                self.current_token.line
            )
        
        if expected_value is not None and self.current_token.value != expected_value:
            raise ParserError(
                f"Attendu '{expected_value}', trouvé '{self.current_token.value}'",
                self.current_token.line
            )
        
        token = self.current_token
        self.advance()
        return token
    
    def match(self, token_type, expected_value=None):
        """
        Vérifie si le token actuel correspond au type/valeur attendu.
        
        Returns:
            True si ça correspond, False sinon
        """
        if self.current_token is None:
            return False
        if self.current_token.type != token_type:
            return False
        if expected_value is not None and self.current_token.value != expected_value:
            return False
        return True
    
    # ========================================
    # Règles de grammaire
    # ========================================
    
    def parse(self):
        """
        Parse un programme complet.
        
        Grammar:
            program → ALGORITHME identifier declarations functions DEBUT statements FIN
        """
        # ALGORITHME nom
        self.eat('KEYWORD', 'ALGORITHME')
        name_token = self.eat('IDENTIFIER')
        name = name_token.value
        
        # Déclarations (VAR ...)
        declarations = []
        while self.match('KEYWORD', 'VAR'):
            declarations.append(self.parse_declaration())
        
        # Fonctions (FONCTION ...)
        functions = []
        while self.match('KEYWORD', 'FONCTION'):
            functions.append(self.parse_function())
        
        # DEBUT
        self.eat('KEYWORD', 'DEBUT')
        
        # Instructions
        statements = []
        while not self.match('KEYWORD', 'FIN'):
            if self.current_token is None or self.match('EOF'):
                raise ParserError("Mot-clé FIN manquant", self.tokens[-1].line)
            statements.append(self.parse_statement())
        
        # FIN
        self.eat('KEYWORD', 'FIN')
        
        return ProgramNode(name, declarations, statements, functions)
    
    def parse_declaration(self):
        """
        Parse une déclaration de variable.
        
        Grammar:
            declaration → VAR identifier : type
                       | VAR identifier : TABLEAU[size] DE type
        """
        line = self.current_token.line
        self.eat('KEYWORD', 'VAR')
        var_name = self.eat('IDENTIFIER').value
        self.eat('COLON')
        
        # Vérifier si c'est un tableau
        if self.match('KEYWORD', 'TABLEAU'):
            self.eat('KEYWORD', 'TABLEAU')
            self.eat('LBRACKET')
            size = self.parse_expression()
            self.eat('RBRACKET')
            self.eat('KEYWORD', 'DE')
            element_type = self.eat('TYPE').value
            return ArrayDeclarationNode(var_name, size, element_type, line)
        
        # Déclaration normale
        var_type = self.eat('TYPE').value
        return DeclarationNode(var_name, var_type, line)
    
    def parse_function(self):
        """
        Parse une définition de fonction.
        
        Grammar:
            function → FONCTION identifier ( params ) : type declarations statements FIN_FONCTION
            params → identifier : type (, identifier : type)*
        """
        line = self.current_token.line
        self.eat('KEYWORD', 'FONCTION')
        
        func_name = self.eat('IDENTIFIER').value
        
        # Paramètres
        self.eat('LPAREN')
        parameters = []
        
        if not self.match('RPAREN'):
            # Premier paramètre
            param_name = self.eat('IDENTIFIER').value
            self.eat('COLON')
            param_type = self.eat('TYPE').value
            parameters.append((param_name, param_type))
            
            # Paramètres suivants
            while self.match('COMMA'):
                self.eat('COMMA')
                param_name = self.eat('IDENTIFIER').value
                self.eat('COLON')
                param_type = self.eat('TYPE').value
                parameters.append((param_name, param_type))
        
        self.eat('RPAREN')
        
        # Type de retour (optionnel pour procédures/fonctions void)
        return_type = None
        if self.match('COLON'):
            self.eat('COLON')
            return_type = self.eat('TYPE').value
        
        # Déclarations locales
        declarations = []
        while self.match('KEYWORD', 'VAR'):
            declarations.append(self.parse_declaration())
        
        # Corps de la fonction
        body = []
        while not self.match('KEYWORD', 'FIN_FONCTION'):
            if self.current_token is None or self.match('EOF'):
                raise ParserError("FIN_FONCTION manquant", line)
            body.append(self.parse_statement())
        
        self.eat('KEYWORD', 'FIN_FONCTION')
        
        return FunctionDefNode(func_name, parameters, return_type, declarations, body, line)
    
    def parse_statement(self):
        """
        Parse une instruction.
        
        Grammar:
            statement → assignment | array_assignment | print | read | if | while | for | return
        """
        if self.match('IDENTIFIER'):
            # Vérifier si c'est un appel de fonction, un accès tableau, ou une affectation
            next_token = self.peek()
            if next_token and next_token.type == 'LPAREN':
                return self.parse_function_call_statement()
            elif next_token and next_token.type == 'LBRACKET':
                return self.parse_array_assignment()
            return self.parse_assignment()
        
        elif self.match('KEYWORD', 'ECRIRE'):
            return self.parse_print()
        
        elif self.match('KEYWORD', 'LIRE'):
            return self.parse_read()
        
        elif self.match('KEYWORD', 'SI'):
            return self.parse_if()
        
        elif self.match('KEYWORD', 'TANT_QUE'):
            return self.parse_while()
        
        elif self.match('KEYWORD', 'POUR'):
            return self.parse_for()
        
        elif self.match('KEYWORD', 'RETOURNER'):
            return self.parse_return()
        
        else:
            raise ParserError(
                f"Instruction inattendue: {self.current_token.value}",
                self.current_token.line
            )
    
    def parse_function_call_statement(self):
        """Parse un appel de fonction comme instruction."""
        line = self.current_token.line
        func_name = self.eat('IDENTIFIER').value
        
        self.eat('LPAREN')
        arguments = []
        
        if not self.match('RPAREN'):
            arguments.append(self.parse_expression())
            while self.match('COMMA'):
                self.eat('COMMA')
                arguments.append(self.parse_expression())
        
        self.eat('RPAREN')
        
        return FunctionCallNode(func_name, arguments, line)
    
    def parse_return(self):
        """
        Parse une instruction RETOURNER.
        
        Grammar:
            return → RETOURNER [expression]
        
        Pour les procédures (fonctions void), RETOURNER peut être utilisé
        sans expression pour sortir de la fonction.
        """
        line = self.current_token.line
        self.eat('KEYWORD', 'RETOURNER')
        
        # Vérifier si RETOURNER est suivi d'une expression ou non (pour void)
        # Seulement FIN_FONCTION indique un retour void (pas d'expression)
        if self.match('KEYWORD', 'FIN_FONCTION'):
            return ReturnNode(None, line)
        
        value = self.parse_expression()
        return ReturnNode(value, line)
    
    def parse_assignment(self):
        """
        Parse une affectation.
        
        Grammar:
            assignment → identifier ← expression
        """
        line = self.current_token.line
        var_name = self.eat('IDENTIFIER').value
        self.eat('ASSIGN')
        value = self.parse_expression()
        
        return AssignmentNode(var_name, value, line)
    
    def parse_array_assignment(self):
        """
        Parse une affectation à un élément de tableau.
        
        Grammar:
            array_assignment → identifier [ expression ] ← expression
        """
        line = self.current_token.line
        array_name = self.eat('IDENTIFIER').value
        self.eat('LBRACKET')
        index = self.parse_expression()
        self.eat('RBRACKET')
        self.eat('ASSIGN')
        value = self.parse_expression()
        
        return ArrayAssignmentNode(array_name, index, value, line)
    
    def parse_print(self):
        """
        Parse une instruction ECRIRE.
        
        Grammar:
            print → ECRIRE ( expression_list )
        """
        line = self.current_token.line
        self.eat('KEYWORD', 'ECRIRE')
        self.eat('LPAREN')
        
        expressions = [self.parse_expression()]
        
        while self.match('COMMA'):
            self.eat('COMMA')
            expressions.append(self.parse_expression())
        
        self.eat('RPAREN')
        
        return PrintNode(expressions, line)
    
    def parse_read(self):
        """
        Parse une instruction LIRE.
        
        Grammar:
            read → LIRE ( identifier )
        """
        line = self.current_token.line
        self.eat('KEYWORD', 'LIRE')
        self.eat('LPAREN')
        var_name = self.eat('IDENTIFIER').value
        self.eat('RPAREN')
        
        return ReadNode(var_name, line)
    
    def parse_if(self):
        """
        Parse une instruction SI.
        
        Grammar:
            if → SI condition ALORS statements [SINON statements] FIN_SI
        """
        line = self.current_token.line
        self.eat('KEYWORD', 'SI')
        
        condition = self.parse_expression()
        
        self.eat('KEYWORD', 'ALORS')
        
        then_branch = []
        while not self.match('KEYWORD', 'SINON') and not self.match('KEYWORD', 'FIN_SI'):
            if self.current_token is None or self.match('EOF'):
                raise ParserError("FIN_SI manquant", line)
            then_branch.append(self.parse_statement())
        
        else_branch = None
        if self.match('KEYWORD', 'SINON'):
            self.eat('KEYWORD', 'SINON')
            else_branch = []
            while not self.match('KEYWORD', 'FIN_SI'):
                if self.current_token is None or self.match('EOF'):
                    raise ParserError("FIN_SI manquant", line)
                else_branch.append(self.parse_statement())
        
        self.eat('KEYWORD', 'FIN_SI')
        
        return IfNode(condition, then_branch, else_branch, line)
    
    def parse_while(self):
        """
        Parse une boucle TANT_QUE.
        
        Grammar:
            while → TANT_QUE condition FAIRE statements FIN_TANT_QUE
        """
        line = self.current_token.line
        self.eat('KEYWORD', 'TANT_QUE')
        
        condition = self.parse_expression()
        
        self.eat('KEYWORD', 'FAIRE')
        
        body = []
        while not self.match('KEYWORD', 'FIN_TANT_QUE'):
            if self.current_token is None or self.match('EOF'):
                raise ParserError("FIN_TANT_QUE manquant", line)
            body.append(self.parse_statement())
        
        self.eat('KEYWORD', 'FIN_TANT_QUE')
        
        return WhileNode(condition, body, line)
    
    def parse_for(self):
        """
        Parse une boucle POUR.
        
        Grammar:
            for → POUR identifier DE expression A expression FAIRE statements FIN_POUR
        """
        line = self.current_token.line
        self.eat('KEYWORD', 'POUR')
        
        var_name = self.eat('IDENTIFIER').value
        
        self.eat('KEYWORD', 'DE')
        start = self.parse_expression()
        
        self.eat('KEYWORD', 'A')
        end = self.parse_expression()
        
        self.eat('KEYWORD', 'FAIRE')
        
        body = []
        while not self.match('KEYWORD', 'FIN_POUR'):
            if self.current_token is None or self.match('EOF'):
                raise ParserError("FIN_POUR manquant", line)
            body.append(self.parse_statement())
        
        self.eat('KEYWORD', 'FIN_POUR')
        
        return ForNode(var_name, start, end, body, line)
    
    # ========================================
    # Expressions (avec précédence d'opérateurs)
    # ========================================
    
    def parse_expression(self):
        """
        Parse une expression.
        
        Grammar:
            expression → or_expr
        """
        return self.parse_or_expr()
    
    def parse_or_expr(self):
        """
        Parse une expression OU.
        
        Grammar:
            or_expr → and_expr (OU and_expr)*
        """
        left = self.parse_and_expr()
        
        while self.match('KEYWORD', 'OU'):
            line = self.current_token.line
            self.eat('KEYWORD', 'OU')
            right = self.parse_and_expr()
            left = BinaryOpNode(left, 'OU', right, line)
        
        return left
    
    def parse_and_expr(self):
        """
        Parse une expression ET.
        
        Grammar:
            and_expr → not_expr (ET not_expr)*
        """
        left = self.parse_not_expr()
        
        while self.match('KEYWORD', 'ET'):
            line = self.current_token.line
            self.eat('KEYWORD', 'ET')
            right = self.parse_not_expr()
            left = BinaryOpNode(left, 'ET', right, line)
        
        return left
    
    def parse_not_expr(self):
        """
        Parse une expression NON.
        
        Grammar:
            not_expr → NON not_expr | comparison
        """
        if self.match('KEYWORD', 'NON'):
            line = self.current_token.line
            self.eat('KEYWORD', 'NON')
            operand = self.parse_not_expr()
            return UnaryOpNode('NON', operand, line)
        
        return self.parse_comparison()
    
    def parse_comparison(self):
        """
        Parse une comparaison.
        
        Grammar:
            comparison → additive ((= | < | > | <= | >= | ≠) additive)*
        """
        left = self.parse_additive()
        
        while self.current_token and self.current_token.type == 'OPERATOR' and \
              self.current_token.value in ('=', '<', '>', '<=', '>=', '≠'):
            line = self.current_token.line
            op = self.current_token.value
            self.advance()
            right = self.parse_additive()
            left = BinaryOpNode(left, op, right, line)
        
        return left
    
    def parse_additive(self):
        """
        Parse une expression additive.
        
        Grammar:
            additive → multiplicative ((+ | -) multiplicative)*
        """
        left = self.parse_multiplicative()
        
        while self.current_token and self.current_token.type == 'OPERATOR' and \
              self.current_token.value in ('+', '-'):
            line = self.current_token.line
            op = self.current_token.value
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOpNode(left, op, right, line)
        
        return left
    
    def parse_multiplicative(self):
        """
        Parse une expression multiplicative.
        
        Grammar:
            multiplicative → unary ((* | /) unary)*
        """
        left = self.parse_unary()
        
        while self.current_token and self.current_token.type == 'OPERATOR' and \
              self.current_token.value in ('*', '/'):
            line = self.current_token.line
            op = self.current_token.value
            self.advance()
            right = self.parse_unary()
            left = BinaryOpNode(left, op, right, line)
        
        return left
    
    def parse_unary(self):
        """
        Parse une expression unaire.
        
        Grammar:
            unary → -unary | primary
        """
        if self.current_token and self.current_token.type == 'OPERATOR' and \
           self.current_token.value == '-':
            line = self.current_token.line
            self.advance()
            operand = self.parse_unary()
            return UnaryOpNode('-', operand, line)
        
        return self.parse_primary()
    
    def parse_primary(self):
        """
        Parse une expression primaire.
        
        Grammar:
            primary → NUMBER | REAL_NUMBER | STRING | VRAI | FAUX | identifier | ( expression )
        """
        token = self.current_token
        
        if token is None:
            raise ParserError("Expression attendue", self.tokens[-1].line)
        
        # Nombre entier
        if token.type == 'NUMBER':
            self.advance()
            return NumberNode(token.value, token.line)
        
        # Nombre réel
        if token.type == 'REAL_NUMBER':
            self.advance()
            return NumberNode(token.value, token.line)
        
        # Chaîne
        if token.type == 'STRING':
            self.advance()
            return StringNode(token.value, token.line)
        
        # Booléens
        if token.type == 'KEYWORD' and token.value == 'VRAI':
            self.advance()
            return BooleanNode(True, token.line)
        
        if token.type == 'KEYWORD' and token.value == 'FAUX':
            self.advance()
            return BooleanNode(False, token.line)
        
        # Identificateur (variable ou appel de fonction)
        if token.type == 'IDENTIFIER':
            self.advance()
            # Vérifier si c'est un appel de fonction
            if self.match('LPAREN'):
                self.eat('LPAREN')
                arguments = []
                if not self.match('RPAREN'):
                    arguments.append(self.parse_expression())
                    while self.match('COMMA'):
                        self.eat('COMMA')
                        arguments.append(self.parse_expression())
                self.eat('RPAREN')
                return FunctionCallNode(token.value, arguments, token.line)
            # Vérifier si c'est un accès tableau
            if self.match('LBRACKET'):
                self.eat('LBRACKET')
                index = self.parse_expression()
                self.eat('RBRACKET')
                return ArrayAccessNode(token.value, index, token.line)
            return VariableNode(token.value, token.line)
        
        # Expression entre parenthèses
        if token.type == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            self.eat('RPAREN')
            return expr
        
        raise ParserError(f"Expression inattendue: {token.value}", token.line)


# ============================================================
# Tests du parser
# ============================================================

if __name__ == '__main__':
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # Test 1: Programme simple
    print("=== Test 1: Programme simple ===")
    code = """ALGORITHME TestSimple
VAR x : ENTIER
VAR y : ENTIER
DEBUT
    x ← 10
    y ← 20
    ECRIRE(x + y)
FIN
"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"Programme: {ast}")
    print(f"  Declarations: {ast.declarations}")
    print(f"  Statements: {ast.statements}")
    print()
    
    # Test 2: Expressions arithmétiques
    print("=== Test 2: Expressions arithmétiques ===")
    code = """ALGORITHME TestExpr
VAR a : ENTIER
VAR b : ENTIER
VAR resultat : ENTIER
DEBUT
    a ← 5
    b ← 3
    resultat ← a + b * 2
    ECRIRE(resultat)
FIN
"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"Statement: {ast.statements[2]}")  # resultat ← a + b * 2
    print()
    
    # Test 3: Condition SI
    print("=== Test 3: Condition SI ===")
    code = """ALGORITHME TestSi
VAR x : ENTIER
DEBUT
    x ← 10
    SI x > 5 ALORS
        ECRIRE("x est grand")
    SINON
        ECRIRE("x est petit")
    FIN_SI
FIN
"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    if_node = ast.statements[1]
    print(f"If statement: {if_node}")
    print(f"  Condition: {if_node.condition}")
    print()
    
    # Test 4: Boucle POUR
    print("=== Test 4: Boucle POUR ===")
    code = """ALGORITHME TestPour
VAR i : ENTIER
VAR somme : ENTIER
DEBUT
    somme ← 0
    POUR i DE 1 A 10 FAIRE
        somme ← somme + i
    FIN_POUR
    ECRIRE(somme)
FIN
"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    for_node = ast.statements[1]
    print(f"For statement: {for_node}")
    print()
    
    # Test 5: Boucle TANT_QUE
    print("=== Test 5: Boucle TANT_QUE ===")
    code = """ALGORITHME TestTantQue
VAR x : ENTIER
DEBUT
    x ← 0
    TANT_QUE x < 5 FAIRE
        ECRIRE(x)
        x ← x + 1
    FIN_TANT_QUE
FIN
"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    while_node = ast.statements[1]
    print(f"While statement: {while_node}")
    print()
    
    # Test 6: Erreur de syntaxe
    print("=== Test 6: Erreur de syntaxe ===")
    code = """ALGORITHME TestErreur
VAR x : ENTIER
DEBUT
    x ← 
FIN
"""
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
    except ParserError as e:
        print(f"Erreur capturée: {e}")
    print()
    
    print("✓ Tous les tests du parser terminés!")

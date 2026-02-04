"""
Semantic Analyzer (Analyse Sémantique) - Phase 3 du Compilateur
Vérifie la cohérence sémantique du programme

Ce module analyse l'AST pour détecter les erreurs sémantiques:
- Variables utilisées sans être déclarées
- Variables déclarées plusieurs fois
- Vérification complète des types
"""

from parser import (
    ASTNode, ProgramNode, DeclarationNode, ArrayDeclarationNode, AssignmentNode,
    NumberNode, StringNode, BooleanNode, VariableNode, ArrayAccessNode, ArrayAssignmentNode,
    BinaryOpNode, UnaryOpNode, PrintNode, ReadNode,
    IfNode, WhileNode, ForNode,
    FunctionDefNode, FunctionCallNode, ReturnNode
)


class SemanticError(Exception):
    """Exception levée lors d'une erreur sémantique."""
    
    def __init__(self, message, line=None):
        self.message = message
        self.line = line
        if line:
            super().__init__(f"Erreur Sémantique (ligne {line}): {message}")
        else:
            super().__init__(f"Erreur Sémantique: {message}")


class SymbolTable:
    """
    Table des symboles pour stocker les informations sur les variables.
    
    Garde une trace de toutes les variables déclarées avec leur type
    et leur ligne de déclaration.
    """
    
    def __init__(self):
        """Initialise une table des symboles vide."""
        self.symbols = {}  # {nom: {'type': type, 'line': ligne}}
    
    def declare(self, name, var_type, line, is_array=False, array_size=None):
        """
        Déclare une nouvelle variable ou tableau.
        
        Args:
            name: Nom de la variable
            var_type: Type de la variable (ENTIER, REEL, etc.)
            line: Numéro de ligne de la déclaration
            is_array: True si c'est un tableau
            array_size: Taille du tableau (si applicable)
            
        Raises:
            SemanticError: Si la variable est déjà déclarée
        """
        if name in self.symbols:
            original_line = self.symbols[name]['line']
            raise SemanticError(
                f"Variable '{name}' déjà déclarée à la ligne {original_line}",
                line
            )
        
        self.symbols[name] = {
            'type': var_type,
            'line': line,
            'is_array': is_array,
            'array_size': array_size
        }
    
    def lookup(self, name, line=None):
        """
        Recherche une variable dans la table.
        
        Args:
            name: Nom de la variable à rechercher
            line: Numéro de ligne pour le message d'erreur
            
        Returns:
            Dict avec 'type' et 'line' de la variable
            
        Raises:
            SemanticError: Si la variable n'est pas déclarée
        """
        if name not in self.symbols:
            raise SemanticError(
                f"Variable '{name}' utilisée sans être déclarée",
                line
            )
        
        return self.symbols[name]
    
    def exists(self, name):
        """
        Vérifie si une variable existe.
        
        Args:
            name: Nom de la variable
            
        Returns:
            True si la variable est déclarée, False sinon
        """
        return name in self.symbols
    
    def get_type(self, name):
        """
        Retourne le type d'une variable.
        
        Args:
            name: Nom de la variable
            
        Returns:
            Le type de la variable ou None si non déclarée
        """
        if name in self.symbols:
            return self.symbols[name]['type']
        return None
    
    def is_array(self, name):
        """
        Vérifie si une variable est un tableau.
        
        Args:
            name: Nom de la variable
            
        Returns:
            True si la variable est un tableau, False sinon
        """
        if name in self.symbols:
            return self.symbols[name].get('is_array', False)
        return False
    
    def __repr__(self):
        return f"SymbolTable({self.symbols})"


class SemanticAnalyzer:
    """
    Analyseur sémantique pour le pseudocode français.
    
    Parcourt l'AST et vérifie:
    - Que les variables sont déclarées avant utilisation
    - Qu'il n'y a pas de déclarations en double
    - Que les types sont compatibles dans les expressions et affectations
    - Que les conditions sont de type BOOLEEN
    - Que les boucles POUR utilisent des variables ENTIER
    """
    
    # Opérateurs arithmétiques
    ARITHMETIC_OPS = {'+', '-', '*', '/'}
    
    # Opérateurs de comparaison
    COMPARISON_OPS = {'=', '≠', '<', '<=', '>', '>='}
    
    # Opérateurs logiques
    LOGICAL_OPS = {'ET', 'OU'}
    
    def __init__(self):
        """Initialise l'analyseur avec une table des symboles vide."""
        self.symbol_table = SymbolTable()
        self.function_table = {}  # {nom: {'params': [...], 'return_type': type}}
        self.errors = []  # Liste des erreurs (mode collecte)
        self.warnings = []  # Liste des avertissements
    
    def analyze(self, node):
        """
        Analyse sémantique d'un noeud AST.
        
        Args:
            node: Le noeud AST à analyser
            
        Raises:
            SemanticError: Si une erreur sémantique est détectée
        """
        if isinstance(node, ProgramNode):
            self._analyze_program(node)
        
        elif isinstance(node, DeclarationNode):
            self._analyze_declaration(node)
        
        elif isinstance(node, AssignmentNode):
            self._analyze_assignment(node)
        
        elif isinstance(node, NumberNode):
            pass  # Les nombres sont toujours valides
        
        elif isinstance(node, StringNode):
            pass  # Les chaînes sont toujours valides
        
        elif isinstance(node, BooleanNode):
            pass  # Les booléens sont toujours valides
        
        elif isinstance(node, VariableNode):
            self._analyze_variable(node)
        
        elif isinstance(node, BinaryOpNode):
            self._analyze_binary_op(node)
        
        elif isinstance(node, UnaryOpNode):
            self._analyze_unary_op(node)
        
        elif isinstance(node, PrintNode):
            self._analyze_print(node)
        
        elif isinstance(node, ReadNode):
            self._analyze_read(node)
        
        elif isinstance(node, IfNode):
            self._analyze_if(node)
        
        elif isinstance(node, WhileNode):
            self._analyze_while(node)
        
        elif isinstance(node, ForNode):
            self._analyze_for(node)
        
        elif isinstance(node, FunctionDefNode):
            self._analyze_function_def(node)
        
        elif isinstance(node, FunctionCallNode):
            self._analyze_function_call(node)
        
        elif isinstance(node, ReturnNode):
            self._analyze_return(node)
        
        elif isinstance(node, ArrayDeclarationNode):
            self._analyze_array_declaration(node)
        
        elif isinstance(node, ArrayAccessNode):
            self._analyze_array_access(node)
        
        elif isinstance(node, ArrayAssignmentNode):
            self._analyze_array_assignment(node)
        
        else:
            raise SemanticError(f"Type de noeud inconnu: {type(node)}")
    
    def infer_type(self, node):
        """
        Infère le type d'une expression.
        
        Args:
            node: Le noeud AST de l'expression
            
        Returns:
            Le type inféré: 'ENTIER', 'REEL', 'CHAINE', ou 'BOOLEEN'
            
        Raises:
            SemanticError: Si le type ne peut pas être inféré ou si incompatibilité
        """
        # Littéraux
        if isinstance(node, NumberNode):
            # Déterminer si c'est un entier ou un réel
            if isinstance(node.value, float):
                return 'REEL'
            return 'ENTIER'
        
        if isinstance(node, StringNode):
            return 'CHAINE'
        
        if isinstance(node, BooleanNode):
            return 'BOOLEEN'
        
        # Variable
        if isinstance(node, VariableNode):
            symbol = self.symbol_table.lookup(node.name, node.line)
            return symbol['type']
        
        # Opération binaire
        if isinstance(node, BinaryOpNode):
            return self._infer_binary_op_type(node)
        
        # Opération unaire
        if isinstance(node, UnaryOpNode):
            return self._infer_unary_op_type(node)
        
        # Appel de fonction
        if isinstance(node, FunctionCallNode):
            if node.name in self.function_table:
                return self.function_table[node.name]['return_type']
            raise SemanticError(
                f"Fonction '{node.name}' non définie",
                node.line
            )
        
        # Accès à un élément de tableau
        if isinstance(node, ArrayAccessNode):
            return self.symbol_table.get_type(node.array_name)
        
        raise SemanticError(
            f"Impossible d'inférer le type de l'expression: {type(node).__name__}",
            getattr(node, 'line', None)
        )
    
    def _infer_binary_op_type(self, node):
        """
        Infère le type d'une opération binaire.
        
        Règles:
        - Arithmétique (+, -, *, /):
          * ENTIER op ENTIER → ENTIER (sauf / → REEL)
          * ENTIER op REEL ou REEL op ENTIER → REEL
          * REEL op REEL → REEL
          * CHAINE + CHAINE → CHAINE (concaténation)
          * Autres combinaisons: erreur
        
        - Comparaison (=, ≠, <, <=, >, >=):
          * Numériques entre eux → BOOLEEN
          * CHAINE avec CHAINE (= et ≠ seulement) → BOOLEEN
          * BOOLEEN avec BOOLEEN (= et ≠ seulement) → BOOLEEN
        
        - Logique (ET, OU):
          * BOOLEEN op BOOLEEN → BOOLEEN
        """
        left_type = self.infer_type(node.left)
        right_type = self.infer_type(node.right)
        op = node.operator
        line = node.line
        
        # Opérateurs arithmétiques
        if op in self.ARITHMETIC_OPS:
            return self._check_arithmetic_types(left_type, right_type, op, line)
        
        # Opérateurs de comparaison
        if op in self.COMPARISON_OPS:
            return self._check_comparison_types(left_type, right_type, op, line)
        
        # Opérateurs logiques
        if op in self.LOGICAL_OPS:
            return self._check_logical_types(left_type, right_type, op, line)
        
        raise SemanticError(f"Opérateur inconnu: '{op}'", line)
    
    def _check_arithmetic_types(self, left_type, right_type, op, line):
        """Vérifie les types pour les opérations arithmétiques."""
        
        # Cas spécial: concaténation de chaînes
        if op == '+' and left_type == 'CHAINE' and right_type == 'CHAINE':
            return 'CHAINE'
        
        # Types numériques uniquement pour l'arithmétique
        numeric_types = {'ENTIER', 'REEL'}
        
        if left_type not in numeric_types:
            raise SemanticError(
                f"Opérateur '{op}' invalide: opérande gauche de type {left_type} "
                f"(attendu ENTIER ou REEL)",
                line
            )
        
        if right_type not in numeric_types:
            raise SemanticError(
                f"Opérateur '{op}' invalide: opérande droite de type {right_type} "
                f"(attendu ENTIER ou REEL)",
                line
            )
        
        # Division retourne toujours REEL
        if op == '/':
            return 'REEL'
        
        # Si au moins un opérande est REEL, le résultat est REEL
        if left_type == 'REEL' or right_type == 'REEL':
            return 'REEL'
        
        # ENTIER op ENTIER → ENTIER
        return 'ENTIER'
    
    def _check_comparison_types(self, left_type, right_type, op, line):
        """Vérifie les types pour les opérations de comparaison."""
        
        numeric_types = {'ENTIER', 'REEL'}
        equality_ops = {'=', '≠'}
        
        # Comparaisons numériques (tous les opérateurs)
        if left_type in numeric_types and right_type in numeric_types:
            return 'BOOLEEN'
        
        # Comparaisons de chaînes (= et ≠ seulement)
        if left_type == 'CHAINE' and right_type == 'CHAINE':
            if op in equality_ops:
                return 'BOOLEEN'
            raise SemanticError(
                f"Opérateur '{op}' invalide pour les chaînes "
                f"(seuls = et ≠ sont autorisés)",
                line
            )
        
        # Comparaisons de booléens (= et ≠ seulement)
        if left_type == 'BOOLEEN' and right_type == 'BOOLEEN':
            if op in equality_ops:
                return 'BOOLEEN'
            raise SemanticError(
                f"Opérateur '{op}' invalide pour les booléens "
                f"(seuls = et ≠ sont autorisés)",
                line
            )
        
        # Types incompatibles
        raise SemanticError(
            f"Comparaison '{op}' invalide entre {left_type} et {right_type}",
            line
        )
    
    def _check_logical_types(self, left_type, right_type, op, line):
        """Vérifie les types pour les opérations logiques."""
        
        if left_type != 'BOOLEEN':
            raise SemanticError(
                f"Opérateur '{op}' requiert un opérande gauche de type BOOLEEN, "
                f"mais {left_type} trouvé",
                line
            )
        
        if right_type != 'BOOLEEN':
            raise SemanticError(
                f"Opérateur '{op}' requiert un opérande droite de type BOOLEEN, "
                f"mais {right_type} trouvé",
                line
            )
        
        return 'BOOLEEN'
    
    def _infer_unary_op_type(self, node):
        """
        Infère le type d'une opération unaire.
        
        Règles:
        - NON: opérande doit être BOOLEEN, retourne BOOLEEN
        - -: opérande doit être numérique, retourne le même type
        """
        operand_type = self.infer_type(node.operand)
        op = node.operator
        line = node.line
        
        if op == 'NON':
            if operand_type != 'BOOLEEN':
                raise SemanticError(
                    f"Opérateur 'NON' requiert un opérande de type BOOLEEN, "
                    f"mais {operand_type} trouvé",
                    line
                )
            return 'BOOLEEN'
        
        if op == '-':
            if operand_type not in {'ENTIER', 'REEL'}:
                raise SemanticError(
                    f"Opérateur '-' unaire requiert un opérande numérique, "
                    f"mais {operand_type} trouvé",
                    line
                )
            return operand_type
        
        raise SemanticError(f"Opérateur unaire inconnu: '{op}'", line)
    
    def _analyze_program(self, node):
        """Analyse un programme complet."""
        # D'abord, traiter toutes les déclarations globales
        for decl in node.declarations:
            self.analyze(decl)
        
        # Ensuite, enregistrer les fonctions dans la table des fonctions
        for func in node.functions:
            if func.name in self.function_table:
                raise SemanticError(f"Fonction '{func.name}' déjà définie", func.line)
            self.function_table[func.name] = {
                'params': func.parameters,
                'return_type': func.return_type,
                'line': func.line
            }
        
        # Analyser le corps des fonctions
        for func in node.functions:
            self._analyze_function_def(func)
        
        # Enfin, traiter toutes les instructions du programme principal
        for stmt in node.statements:
            self.analyze(stmt)
    
    def _analyze_declaration(self, node):
        """Analyse une déclaration de variable."""
        self.symbol_table.declare(node.variable, node.var_type, node.line)
    
    def _analyze_array_declaration(self, node):
        """Analyse une déclaration de tableau."""
        self.symbol_table.declare(node.variable, node.element_type, node.line,
                                   is_array=True, array_size=node.size)
    
    def _analyze_array_access(self, node):
        """Analyse un accès à un élément de tableau."""
        # Vérifier que le tableau existe
        self.symbol_table.lookup(node.array_name, node.line)
        
        # Vérifier que c'est bien un tableau
        if not self.symbol_table.is_array(node.array_name):
            raise SemanticError(
                f"Variable '{node.array_name}' n'est pas un tableau",
                node.line
            )
        
        # Analyser et vérifier le type de l'indice
        self.analyze(node.index)
        index_type = self.infer_type(node.index)
        if index_type != 'ENTIER':
            raise SemanticError(
                f"L'indice du tableau doit être de type ENTIER, mais {index_type} trouvé",
                node.line
            )
    
    def _analyze_array_assignment(self, node):
        """
        Analyse une affectation à un élément de tableau: tab[i] ← valeur
        
        Vérifie:
        - Que le tableau existe
        - Que l'indice est de type ENTIER
        - Que la valeur est compatible avec le type des éléments
        """
        # Vérifier que le tableau existe
        arr_info = self.symbol_table.lookup(node.array_name, node.line)
        
        # Vérifier que c'est bien un tableau
        if not self.symbol_table.is_array(node.array_name):
            raise SemanticError(
                f"Variable '{node.array_name}' n'est pas un tableau",
                node.line
            )
        
        # Analyser et vérifier le type de l'indice
        self.analyze(node.index)
        index_type = self.infer_type(node.index)
        if index_type != 'ENTIER':
            raise SemanticError(
                f"L'indice du tableau doit être de type ENTIER, mais {index_type} trouvé",
                node.line
            )
        
        # Analyser la valeur et vérifier la compatibilité de type
        self.analyze(node.value)
        value_type = self.infer_type(node.value)
        element_type = arr_info['type']
        
        if not self._is_assignable(element_type, value_type):
            raise SemanticError(
                f"Impossible d'affecter {value_type} à un élément du tableau "
                f"'{node.array_name}' de type {element_type}",
                node.line
            )
    
    def _analyze_assignment(self, node):
        """
        Analyse une affectation avec vérification des types.
        
        Règles d'affectation:
        - ENTIER ← ENTIER seulement
        - REEL ← REEL ou ENTIER (promotion implicite)
        - CHAINE ← CHAINE seulement
        - BOOLEEN ← BOOLEEN seulement
        """
        # Gérer l'accès à un élément de tableau comme cible
        if isinstance(node.target, ArrayAccessNode):
            self._analyze_array_access(node.target)
            target_type = self.symbol_table.get_type(node.target.array_name)
            target_name = node.target.array_name
        else:
            # Variable simple
            target_info = self.symbol_table.lookup(node.target, node.line)
            target_type = target_info['type']
            target_name = node.target
            
            # Erreur si on essaie d'affecter à un tableau sans indice
            if self.symbol_table.is_array(node.target):
                raise SemanticError(
                    f"Tableau '{node.target}' doit être utilisé avec un indice",
                    node.line
                )
        
        # Analyser l'expression de valeur et inférer son type
        self.analyze(node.value)
        value_type = self.infer_type(node.value)
        
        # Vérifier la compatibilité des types
        if not self._is_assignable(target_type, value_type):
            raise SemanticError(
                f"Impossible d'affecter {value_type} à '{target_name}' "
                f"de type {target_type}",
                node.line
            )
    
    def _is_assignable(self, target_type, value_type):
        """
        Vérifie si un type peut être affecté à un autre.
        
        Args:
            target_type: Type de la variable cible
            value_type: Type de la valeur à affecter
            
        Returns:
            True si l'affectation est valide, False sinon
        """
        # Même type: toujours OK
        if target_type == value_type:
            return True
        
        # Promotion ENTIER → REEL
        if target_type == 'REEL' and value_type == 'ENTIER':
            return True
        
        # Toute autre combinaison: erreur
        return False
    
    def _analyze_variable(self, node):
        """Analyse une référence à une variable."""
        self.symbol_table.lookup(node.name, node.line)
        
        # Erreur si on utilise un tableau sans indice
        if self.symbol_table.is_array(node.name):
            raise SemanticError(
                f"Tableau '{node.name}' doit être utilisé avec un indice",
                node.line
            )
    
    def _analyze_binary_op(self, node):
        """Analyse une opération binaire avec vérification des types."""
        self.analyze(node.left)
        self.analyze(node.right)
        # La vérification des types est faite par infer_type
        self.infer_type(node)
    
    def _analyze_unary_op(self, node):
        """Analyse une opération unaire avec vérification des types."""
        self.analyze(node.operand)
        # La vérification des types est faite par infer_type
        self.infer_type(node)
    
    def _analyze_print(self, node):
        """
        Analyse une instruction ECRIRE.
        
        Tous les types sont acceptés (printables).
        """
        for expr in node.expressions:
            self.analyze(expr)
            # Inférer le type pour vérifier que l'expression est valide
            self.infer_type(expr)
    
    def _analyze_read(self, node):
        """
        Analyse une instruction LIRE.
        
        Vérifie que la variable est déclarée.
        Le type de la variable détermine la conversion d'entrée.
        """
        # Vérifier que la variable est déclarée
        var_info = self.symbol_table.lookup(node.variable, node.line)
        # Stocker le type attendu pour le code generator
        node.var_type = var_info['type']
    
    def _analyze_if(self, node):
        """
        Analyse une instruction SI.
        
        La condition doit être de type BOOLEEN.
        """
        # Analyser la condition
        self.analyze(node.condition)
        
        # Vérifier que la condition est booléenne
        condition_type = self.infer_type(node.condition)
        if condition_type != 'BOOLEEN':
            raise SemanticError(
                f"La condition du SI doit être de type BOOLEEN, "
                f"mais {condition_type} trouvé",
                node.line
            )
        
        # Analyser le bloc ALORS
        for stmt in node.then_branch:
            self.analyze(stmt)
        
        # Analyser le bloc SINON si présent
        if node.else_branch:
            for stmt in node.else_branch:
                self.analyze(stmt)
    
    def _analyze_while(self, node):
        """
        Analyse une boucle TANT_QUE.
        
        La condition doit être de type BOOLEEN.
        """
        # Analyser la condition
        self.analyze(node.condition)
        
        # Vérifier que la condition est booléenne
        condition_type = self.infer_type(node.condition)
        if condition_type != 'BOOLEEN':
            raise SemanticError(
                f"La condition du TANT_QUE doit être de type BOOLEEN, "
                f"mais {condition_type} trouvé",
                node.line
            )
        
        # Analyser le corps de la boucle
        for stmt in node.body:
            self.analyze(stmt)
    
    def _analyze_for(self, node):
        """
        Analyse une boucle POUR.
        
        Règles:
        - La variable de boucle doit être de type ENTIER
        - Les expressions de début et fin doivent être de type ENTIER
        """
        # Vérifier que la variable de boucle est déclarée
        var_info = self.symbol_table.lookup(node.variable, node.line)
        
        # Vérifier que la variable de boucle est de type ENTIER
        if var_info['type'] != 'ENTIER':
            raise SemanticError(
                f"La variable de boucle POUR '{node.variable}' doit être de type ENTIER, "
                f"mais {var_info['type']} trouvé",
                node.line
            )
        
        # Analyser et vérifier le type de l'expression de début
        self.analyze(node.start)
        start_type = self.infer_type(node.start)
        if start_type != 'ENTIER':
            raise SemanticError(
                f"La valeur de début de la boucle POUR doit être de type ENTIER, "
                f"mais {start_type} trouvé",
                node.line
            )
        
        # Analyser et vérifier le type de l'expression de fin
        self.analyze(node.end)
        end_type = self.infer_type(node.end)
        if end_type != 'ENTIER':
            raise SemanticError(
                f"La valeur de fin de la boucle POUR doit être de type ENTIER, "
                f"mais {end_type} trouvé",
                node.line
            )
        
        # Analyser le corps de la boucle
        for stmt in node.body:
            self.analyze(stmt)
    
    def _analyze_function_def(self, node):
        """Analyse une définition de fonction."""
        # Sauvegarder la table des symboles actuelle
        saved_symbols = self.symbol_table.symbols.copy()
        
        # Ajouter les paramètres à la table des symboles
        for param_name, param_type in node.parameters:
            self.symbol_table.declare(param_name, param_type, node.line)
        
        # Traiter les déclarations locales
        for decl in node.declarations:
            self.analyze(decl)
        
        # Analyser le corps de la fonction
        for stmt in node.body:
            self.analyze(stmt)
        
        # Restaurer la table des symboles (sortie de portée)
        self.symbol_table.symbols = saved_symbols
    
    def _analyze_function_call(self, node):
        """Analyse un appel de fonction."""
        # Vérifier que la fonction existe
        if node.name not in self.function_table:
            raise SemanticError(
                f"Fonction '{node.name}' non définie",
                node.line
            )
        
        # Vérifier le nombre d'arguments
        func_info = self.function_table[node.name]
        expected_params = len(func_info['params'])
        actual_args = len(node.arguments)
        
        if expected_params != actual_args:
            raise SemanticError(
                f"Fonction '{node.name}' attend {expected_params} argument(s), "
                f"mais {actual_args} fourni(s)",
                node.line
            )
        
        # Analyser et vérifier les types des arguments
        for i, (arg, (param_name, param_type)) in enumerate(zip(node.arguments, func_info['params'])):
            self.analyze(arg)
            arg_type = self.infer_type(arg)
            if not self._is_assignable(param_type, arg_type):
                raise SemanticError(
                    f"Argument {i+1} de la fonction '{node.name}': "
                    f"attendu {param_type}, mais {arg_type} fourni",
                    node.line
                )
    
    def _analyze_return(self, node):
        """Analyse une instruction RETOURNER."""
        # Si il y a une expression de retour, l'analyser
        if node.value is not None:
            self.analyze(node.value)
            # Inférer le type pour vérifier que l'expression est valide
            self.infer_type(node.value)
        # Si node.value est None, c'est un RETOURNER sans valeur (pour void)


# ============================================================
# Tests de l'analyseur sémantique
# ============================================================

if __name__ == '__main__':
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    from lexer import Lexer
    from parser import Parser
    
    def test_semantic(code, description, should_pass=True):
        """Teste l'analyseur sémantique sur un code donné."""
        print(f"=== {description} ===")
        print(f"Attendu: {'SUCCÈS' if should_pass else 'ERREUR'}")
        print()
        
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        
        try:
            analyzer.analyze(ast)
            if should_pass:
                print(f"✓ Aucune erreur sémantique (comme attendu)")
            else:
                print(f"✗ ERREUR: Aucune erreur détectée alors qu'une erreur était attendue!")
        except SemanticError as e:
            if should_pass:
                print(f"✗ ERREUR: {e}")
            else:
                print(f"✓ Erreur détectée (comme attendu): {e}")
        print()
    
    # ========== Tests qui doivent PASSER ==========
    
    # Test 1: Types numériques compatibles
    test_semantic("""ALGORITHME TestNumerique
VAR x : ENTIER
VAR y : REEL
VAR z : REEL
DEBUT
    x ← 10
    y ← 3.14
    z ← x + y
    z ← x * 2
    y ← x / 2
FIN
""", "Test 1: Arithmétique numérique mixte", should_pass=True)
    
    # Test 2: Concaténation de chaînes
    test_semantic("""ALGORITHME TestChaines
VAR nom : CHAINE
VAR message : CHAINE
DEBUT
    nom ← "Alice"
    message ← "Bonjour " + nom
    ECRIRE(message)
FIN
""", "Test 2: Concaténation de chaînes", should_pass=True)
    
    # Test 3: Conditions booléennes
    test_semantic("""ALGORITHME TestBooleen
VAR x : ENTIER
VAR y : ENTIER
VAR ok : BOOLEEN
DEBUT
    x ← 10
    y ← 20
    ok ← x < y
    SI ok ET x > 5 ALORS
        ECRIRE("OK")
    FIN_SI
    TANT_QUE x < y FAIRE
        x ← x + 1
    FIN_TANT_QUE
FIN
""", "Test 3: Conditions booléennes", should_pass=True)
    
    # ========== Tests qui doivent ÉCHOUER ==========
    
    # Test 4: Affectation de type incompatible
    test_semantic("""ALGORITHME TestErreurAffectation
VAR x : ENTIER
DEBUT
    x ← "texte"
FIN
""", "Test 4: Affectation CHAINE à ENTIER", should_pass=False)
    
    # Test 5: Arithmétique avec CHAINE
    test_semantic("""ALGORITHME TestErreurArith
VAR x : ENTIER
VAR msg : CHAINE
DEBUT
    msg ← "hello"
    x ← x + msg
FIN
""", "Test 5: Arithmétique ENTIER + CHAINE", should_pass=False)
    
    # Test 6: Condition non booléenne
    test_semantic("""ALGORITHME TestErreurCondition
VAR x : ENTIER
DEBUT
    x ← 10
    SI x ALORS
        ECRIRE("erreur")
    FIN_SI
FIN
""", "Test 6: ENTIER utilisé comme condition", should_pass=False)
    
    # Test 7: ET avec non-booléens
    test_semantic("""ALGORITHME TestErreurLogique
VAR x : ENTIER
VAR msg : CHAINE
DEBUT
    x ← 10
    msg ← "test"
    SI x ET msg ALORS
        ECRIRE("erreur")
    FIN_SI
FIN
""", "Test 7: ET avec ENTIER et CHAINE", should_pass=False)
    
    # Test 8: Boucle POUR avec variable non-ENTIER
    test_semantic("""ALGORITHME TestErreurPour
VAR i : REEL
DEBUT
    POUR i DE 1 A 10 FAIRE
        ECRIRE(i)
    FIN_POUR
FIN
""", "Test 8: Boucle POUR avec REEL", should_pass=False)
    
    # Test 9: Comparaison incompatible
    test_semantic("""ALGORITHME TestErreurComp
VAR x : ENTIER
VAR msg : CHAINE
DEBUT
    x ← 10
    msg ← "test"
    SI x = msg ALORS
        ECRIRE("erreur")
    FIN_SI
FIN
""", "Test 9: Comparaison ENTIER = CHAINE", should_pass=False)
    
    print("✓ Tous les tests de l'analyseur sémantique terminés!")

    
    print("✓ Tous les tests de l'analyseur sémantique terminés!")

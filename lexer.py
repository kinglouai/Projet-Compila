"""
Lexer (Analyse Lexicale) - Phase 1 du Compilateur
Convertit le texte source en tokens (unités lexicales)

Ce module lit le pseudocode caractère par caractère et produit
une liste de tokens qui seront utilisés par le parser.
"""


class Token:
    """
    Représente un token (unité lexicale).
    
    Attributes:
        type: Le type du token (KEYWORD, IDENTIFIER, NUMBER, etc.)
        value: La valeur réelle du token
        line: Le numéro de ligne pour les messages d'erreur
    """
    
    def __init__(self, type, value, line=1):
        self.type = type
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line})"
    
    def __eq__(self, other):
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        return False


class LexerError(Exception):
    """Exception levée lors d'une erreur lexicale."""
    
    def __init__(self, message, line):
        self.message = message
        self.line = line
        super().__init__(f"Erreur Lexicale (ligne {line}): {message}")


class Lexer:
    """
    Analyseur lexical pour le pseudocode français.
    
    Convertit le texte source en une liste de tokens.
    Gère les mots-clés, identificateurs, nombres, opérateurs et symboles.
    """
    
    # Mots-clés du langage pseudocode
    KEYWORDS = {
        'ALGORITHME', 'VAR', 'DEBUT', 'FIN',
        'SI', 'ALORS', 'SINON', 'FIN_SI',
        'TANT_QUE', 'FAIRE', 'FIN_TANT_QUE',
        'POUR', 'DE', 'A', 'FIN_POUR',
        'ECRIRE', 'LIRE',
        'ET', 'OU', 'NON',
        'VRAI', 'FAUX',
        'FONCTION', 'FIN_FONCTION', 'RETOURNER',
        'TABLEAU'
    }
    
    # Types de données
    TYPES = {'ENTIER', 'REEL', 'CHAINE', 'BOOLEEN', 'VOID'}
    
    def __init__(self, text):
        """
        Initialise le lexer avec le texte source.
        
        Args:
            text: Le code source pseudocode à analyser
        """
        self.text = text
        self.pos = 0  # Position actuelle dans le texte
        self.line = 1  # Numéro de ligne actuel
        self.current_char = self.text[0] if text else None
    
    def advance(self):
        """Avance au caractère suivant."""
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
            if self.current_char == '\n':
                self.line += 1
        else:
            self.current_char = None
    
    def peek(self):
        """Regarde le caractère suivant sans avancer."""
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None
    
    def skip_whitespace(self):
        """Ignore les espaces et tabulations (mais compte les nouvelles lignes)."""
        while self.current_char is not None and self.current_char in ' \t\n\r':
            if self.current_char == '\n':
                pass  # La ligne est déjà incrémentée dans advance()
            self.advance()
    
    def skip_comment(self):
        """Ignore les commentaires // jusqu'à la fin de ligne."""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
    
    def read_number(self):
        """
        Lit un nombre (entier ou réel).
        
        Returns:
            Token de type NUMBER avec la valeur numérique
        """
        result = ''
        start_line = self.line
        
        # Partie entière
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        # Partie décimale (pour les réels)
        if self.current_char == '.' and self.peek() and self.peek().isdigit():
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token('REAL_NUMBER', float(result), start_line)
        
        return Token('NUMBER', int(result), start_line)
    
    def read_string(self):
        """
        Lit une chaîne de caractères entre guillemets.
        
        Returns:
            Token de type STRING avec la valeur de la chaîne
        """
        start_line = self.line
        quote_char = self.current_char  # " ou '
        self.advance()  # Passer le guillemet ouvrant
        
        result = ''
        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == '\n':
                raise LexerError("Chaîne non terminée", start_line)
            result += self.current_char
            self.advance()
        
        if self.current_char is None:
            raise LexerError("Chaîne non terminée", start_line)
        
        self.advance()  # Passer le guillemet fermant
        return Token('STRING', result, start_line)
    
    def read_identifier(self):
        """
        Lit un identificateur ou mot-clé.
        
        Returns:
            Token de type KEYWORD, TYPE ou IDENTIFIER
        """
        result = ''
        start_line = self.line
        
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        upper_result = result.upper()
        
        # Les mots-clés doivent être en majuscules dans le code source
        # (sauf pour les identificateurs qui commencent par une minuscule)
        if result == upper_result or result[0].isupper():
            # Vérifier si c'est un mot-clé
            if upper_result in self.KEYWORDS:
                return Token('KEYWORD', upper_result, start_line)
            
            # Vérifier si c'est un type
            if upper_result in self.TYPES:
                return Token('TYPE', upper_result, start_line)
        
        # Sinon c'est un identificateur
        return Token('IDENTIFIER', result, start_line)
    
    def tokenize(self):
        """
        Analyse le texte et retourne la liste des tokens.
        
        Returns:
            Liste de Token
            
        Raises:
            LexerError: Si un caractère invalide est rencontré
        """
        tokens = []
        
        while self.current_char is not None:
            # Ignorer les espaces blancs
            if self.current_char in ' \t\n\r':
                self.skip_whitespace()
                continue
            
            # Commentaires //
            if self.current_char == '/' and self.peek() == '/':
                self.skip_comment()
                continue
            
            # Nombres
            if self.current_char.isdigit():
                tokens.append(self.read_number())
                continue
            
            # Chaînes de caractères
            if self.current_char in '"\'':
                tokens.append(self.read_string())
                continue
            
            # Identificateurs et mots-clés
            if self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.read_identifier())
                continue
            
            # Opérateur d'affectation ←
            if self.current_char == '←':
                tokens.append(Token('ASSIGN', '←', self.line))
                self.advance()
                continue
            
            # Alternative pour l'affectation: <-
            if self.current_char == '<' and self.peek() == '-':
                tokens.append(Token('ASSIGN', '←', self.line))
                self.advance()
                self.advance()
                continue
            
            # Opérateur différent ≠ ou <>
            if self.current_char == '≠':
                tokens.append(Token('OPERATOR', '≠', self.line))
                self.advance()
                continue
            
            if self.current_char == '<' and self.peek() == '>':
                tokens.append(Token('OPERATOR', '≠', self.line))
                self.advance()
                self.advance()
                continue
            
            # Opérateurs de comparaison
            if self.current_char == '<':
                if self.peek() == '=':
                    tokens.append(Token('OPERATOR', '<=', self.line))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(Token('OPERATOR', '<', self.line))
                    self.advance()
                continue
            
            if self.current_char == '>':
                if self.peek() == '=':
                    tokens.append(Token('OPERATOR', '>=', self.line))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(Token('OPERATOR', '>', self.line))
                    self.advance()
                continue
            
            if self.current_char == '=':
                tokens.append(Token('OPERATOR', '=', self.line))
                self.advance()
                continue
            
            # Opérateurs arithmétiques
            if self.current_char == '+':
                tokens.append(Token('OPERATOR', '+', self.line))
                self.advance()
                continue
            
            if self.current_char == '-':
                tokens.append(Token('OPERATOR', '-', self.line))
                self.advance()
                continue
            
            if self.current_char == '*':
                tokens.append(Token('OPERATOR', '*', self.line))
                self.advance()
                continue
            
            if self.current_char == '/':
                tokens.append(Token('OPERATOR', '/', self.line))
                self.advance()
                continue
            
            # Symboles
            if self.current_char == ':':
                tokens.append(Token('COLON', ':', self.line))
                self.advance()
                continue
            
            if self.current_char == ',':
                tokens.append(Token('COMMA', ',', self.line))
                self.advance()
                continue
            
            if self.current_char == '(':
                tokens.append(Token('LPAREN', '(', self.line))
                self.advance()
                continue
            
            if self.current_char == ')':
                tokens.append(Token('RPAREN', ')', self.line))
                self.advance()
                continue
            
            # Crochets pour les tableaux
            if self.current_char == '[':
                tokens.append(Token('LBRACKET', '[', self.line))
                self.advance()
                continue
            
            if self.current_char == ']':
                tokens.append(Token('RBRACKET', ']', self.line))
                self.advance()
                continue
            
            # Caractère invalide
            raise LexerError(f"Caractère invalide '{self.current_char}'", self.line)
        
        # Ajouter un token de fin de fichier
        tokens.append(Token('EOF', None, self.line))
        
        return tokens


# Tests du lexer
if __name__ == '__main__':
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # Test 1: Déclaration simple
    print("=== Test 1: Déclaration simple ===")
    lexer = Lexer("VAR x : ENTIER")
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
    print()
    
    # Test 2: Affectation
    print("=== Test 2: Affectation ===")
    lexer = Lexer("x ← 10")
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
    print()
    
    # Test 3: Expression arithmétique
    print("=== Test 3: Expression arithmétique ===")
    lexer = Lexer("resultat ← a + b * 2")
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
    print()
    
    # Test 4: Programme complet
    print("=== Test 4: Programme complet ===")
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
    for token in tokens:
        print(token)
    print()
    
    # Test 5: Chaîne de caractères
    print("=== Test 5: Chaîne de caractères ===")
    lexer = Lexer('ECRIRE("Bonjour le monde")')
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
    print()
    
    # Test 6: Erreur - caractère invalide
    print("=== Test 6: Erreur - caractère invalide ===")
    try:
        lexer = Lexer("VAR @invalid : ENTIER")
        tokens = lexer.tokenize()
    except LexerError as e:
        print(f"Erreur capturée: {e}")
    print()
    
    print("✓ Tous les tests du lexer terminés!")

# Compilateur Pseudocode → Python

Un compilateur éducatif qui transforme du pseudocode français en code Python exécutable.

## 🎓 Projet de Cours

Ce projet a été développé dans le cadre du cours de **Compilation** pour démontrer les 4 phases d'un compilateur:

1. **Analyse Lexicale** (`lexer.py`) - Convertit le texte en tokens
2. **Analyse Syntaxique** (`parser.py`) - Construit l'arbre syntaxique (AST)
3. **Analyse Sémantique** (`semantic.py`) - Vérifie les erreurs (variables non déclarées, etc.)
4. **Génération de Code** (`codegen.py`) - Produit le code Python

## 📁 Structure du Projet

```
Compilateur/
├── lexer.py          # Phase 1: Analyseur lexical
├── parser.py         # Phase 2: Analyseur syntaxique
├── semantic.py       # Phase 3: Analyseur sémantique
├── codegen.py        # Phase 4: Générateur de code
├── main.py           # Point d'entrée principal
├── examples/         # Exemples de programmes
│   ├── simple.algo
│   ├── factorielle.algo
│   ├── moyenne.algo
│   ├── condition.algo
│   ├── boucles.algo
│   └── fonction.algo
└── README.md
```

## 🚀 Utilisation

### Compilation simple
```bash
python main.py examples/simple.algo
```

### Compilation avec exécution
```bash
python main.py examples/factorielle.algo -r
```

### Spécifier le fichier de sortie
```bash
python main.py mon_programme.algo -o sortie.py
```

## 📝 Syntaxe du Pseudocode

### Structure d'un programme
```
ALGORITHME NomDuProgramme
VAR variable1 : TYPE
VAR variable2 : TYPE

DEBUT
    // Instructions ici
FIN
```

### Types de données
| Type | Description | Exemple |
|------|-------------|---------|
| `ENTIER` | Nombre entier | `VAR x : ENTIER` |
| `REEL` | Nombre à virgule | `VAR y : REEL` |
| `CHAINE` | Texte | `VAR msg : CHAINE` |
| `BOOLEEN` | Vrai/Faux | `VAR ok : BOOLEEN` |

### Affectation
```
x ← 10
resultat ← a + b * 2
```

### Entrées/Sorties
```
ECRIRE("Message", variable)
LIRE(variable)
```

### Conditions
```
SI condition ALORS
    // Instructions si vrai
SINON
    // Instructions si faux
FIN_SI
```

### Boucle POUR
```
POUR i DE 1 A 10 FAIRE
    // Instructions
FIN_POUR
```

### Boucle TANT_QUE
```
TANT_QUE condition FAIRE
    // Instructions
FIN_TANT_QUE
```

### Fonctions
```
FONCTION nom(param1 : TYPE, param2 : TYPE) : TYPE_RETOUR
VAR local : TYPE
    // Instructions
    RETOURNER valeur
FIN_FONCTION
```

Exemple:
```
FONCTION carre(n : ENTIER) : ENTIER
    RETOURNER n * n
FIN_FONCTION
```

### Opérateurs
| Catégorie | Opérateurs |
|-----------|------------|
| Arithmétiques | `+`, `-`, `*`, `/` |
| Comparaison | `=`, `<`, `>`, `<=`, `>=`, `≠` (ou `<>`) |
| Logiques | `ET`, `OU`, `NON` |
| Affectation | `←` (ou `<-`) |

## 📋 Exemples

### Programme Simple
```
ALGORITHME Exemple
VAR x : ENTIER
VAR y : ENTIER

DEBUT
    x ← 10
    y ← 20
    ECRIRE("Somme:", x + y)
FIN
```

### Factorielle
```
ALGORITHME Factorielle
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
```

### Fonction avec appel
```
ALGORITHME TestFonction
VAR x : ENTIER

FONCTION carre(n : ENTIER) : ENTIER
    RETOURNER n * n
FIN_FONCTION

DEBUT
    x ← carre(5)
    ECRIRE("Le carré de 5 est", x)
FIN
```

## ✅ Fonctionnalités Supportées

- ✅ Déclarations de variables typées
- ✅ Affectations avec expressions complexes
- ✅ Opérations arithmétiques (+, -, *, /)
- ✅ Opérations de comparaison
- ✅ Opérations logiques (ET, OU, NON)
- ✅ Instruction ECRIRE (print)
- ✅ Instruction LIRE (input)
- ✅ Conditions SI/SINON/FIN_SI
- ✅ Boucles POUR/FIN_POUR
- ✅ Boucles TANT_QUE/FIN_TANT_QUE
- ✅ **Fonctions avec paramètres et retour**
- ✅ Commentaires avec //
- ✅ Messages d'erreur clairs avec numéros de ligne

## 🔍 Gestion des Erreurs

Le compilateur détecte et signale clairement:

- **Erreurs lexicales**: Caractères invalides
- **Erreurs syntaxiques**: Structure incorrecte du programme
- **Erreurs sémantiques**: Variables non déclarées, double déclaration

Exemple:
```
Erreur Sémantique (ligne 5): Variable 'y' utilisée sans être déclarée
```

## 🧪 Tests

Chaque module peut être testé individuellement:

```bash
python lexer.py      # Tests du lexer
python parser.py     # Tests du parser
python semantic.py   # Tests de l'analyseur sémantique
python codegen.py    # Tests du générateur de code
```

## 👥 Équipe

Projet réalisé pour le cours de Compilation.

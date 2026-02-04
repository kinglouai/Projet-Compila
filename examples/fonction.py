# Programme généré à partir de: TestFonction
# Compilateur Pseudocode → Python

# Définitions des fonctions
def carre(n):
    return (n * n)

def somme(a, b):
    total = 0  # ENTIER
    total = (a + b)
    return total

def factorielle(n):
    i = 0  # ENTIER
    result = 0  # ENTIER
    result = 1
    for i in range(1, n + 1):
        result = (result * i)
    return result


# Déclarations des variables
x = 0  # ENTIER
y = 0  # ENTIER
resultat = 0  # ENTIER

# Instructions
x = 5
y = 3
resultat = carre(x)
print("Le carre de", x, "est", resultat)
resultat = somme(x, y)
print("La somme de", x, "et", y, "est", resultat)
resultat = factorielle(x)
print("Factorielle de", x, "est", resultat)
resultat = carre(somme(2, 3))
print("carre(somme(2, 3)) =", resultat)
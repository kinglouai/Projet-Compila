# Programme généré à partir de: Factorielle
# Compilateur Pseudocode → Python

# Déclarations des variables
n = 0  # ENTIER
resultat = 0  # ENTIER
i = 0  # ENTIER

# Instructions
n = 5
resultat = 1
for i in range(1, n + 1):
    resultat = (resultat * i)
print("Factorielle de", n, "=", resultat)
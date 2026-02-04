# Programme généré à partir de: TestTablau
# Compilateur Pseudocode → Python

# Déclarations des variables
tab = [0] * 5  # TABLEAU DE ENTIER
i = 0  # ENTIER
somme = 0  # ENTIER

# Instructions
for i in range(0, 4 + 1):
    tab[i] = (i + 1)
somme = 0
for i in range(0, 4 + 1):
    somme = (somme + tab[i])
print("Somme des elements:", somme)
print("Elements du tableau:")
for i in range(0, 4 + 1):
    print("tab[", i, "] =", tab[i])
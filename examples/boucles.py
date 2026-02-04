# Programme généré à partir de: Boucles
# Compilateur Pseudocode → Python

# Déclarations des variables
i = 0  # ENTIER
compteur = 0  # ENTIER
somme = 0  # ENTIER

# Instructions
print("Boucle POUR de 1 a 5:")
for i in range(1, 5 + 1):
    print("  i =", i)
print("Boucle TANT_QUE:")
compteur = 1
while (compteur <= 3):
    print("  compteur =", compteur)
    compteur = (compteur + 1)
somme = 0
for i in range(1, 10 + 1):
    somme = (somme + i)
print("Somme de 1 a 10 =", somme)
# Programme généré à partir de: TestFonctions2
# Compilateur Pseudocode → Python

# Définitions des fonctions
def zero():
    return 0

def double(n):
    return (n * 2)

def addition(x, y):
    return (x + y)

def moyenne(val1, val2):
    return ((val1 + val2) / 2.0)

def estPositif(n):
    if (n > 0):
        return True
    else:
        return False

def factorielle(n):
    i = 0  # ENTIER
    result = 0  # ENTIER
    result = 1
    for i in range(1, n + 1):
        result = (result * i)
    return result


# Déclarations des variables
a = 0  # ENTIER
b = 0  # ENTIER
c = 0  # ENTIER
r1 = 0  # ENTIER
r2 = 0  # ENTIER
r3 = 0.0  # REEL
msg = ""  # CHAINE
flag = False  # BOOLEEN

# Instructions
r1 = zero()
print("zero() =", r1)
a = 5
r1 = double(a)
print("double(5) =", r1)
a = 10
b = 7
r1 = addition(a, b)
print("addition(10, 7) =", r1)
r2 = addition(3, 4)
print("addition(3, 4) =", r2)
r3 = moyenne(10, 20)
print("moyenne(10, 20) =", r3)
flag = estPositif(5)
print("estPositif(5) =", flag)
flag = estPositif((-3))
print("estPositif(-3) =", flag)
r1 = factorielle(5)
print("factorielle(5) =", r1)
r1 = double(addition(2, 3))
print("double(addition(2, 3)) =", r1)
c = (addition(a, b) + double(2))
print("addition(10, 7) + double(2) =", c)
print("=== Tous les tests de fonctions terminés ===")



# Código principal
with open("entrada.txt", "r") as file:
    N = file.readline().strip()
    m, k, r, n = map(int, file.readline().split())
    numeros = list(map(int, file.readline().split()))

if N == "P":
    polifasica(m, k, r, n, numeros)

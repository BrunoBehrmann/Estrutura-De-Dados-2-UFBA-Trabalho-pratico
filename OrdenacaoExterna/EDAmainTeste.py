import heapq


def adicionar_com_peso(heap, valor, peso):
    # Inserindo como uma tupla (valor, peso)
    heapq.heappush(heap, (valor, peso))

def remove_menor_heap(heap)
    menor, menor_peso = extrair_menor_com_peso_0(heap)
    # IMPLEMENTAR
    heapq.heappop(heap)

def extrair_menor_com_peso_0(heap):
    # Itera sobre a heap para encontrar o menor elemento com peso 0

    for i in range(len(heap)):
        valor, peso = heap[i]
        if peso == 0:
            if i == 0:
                valor01 = valor, peso
            elif i == 1:
                valor02 = valor, peso
            elif i == 2:
                valor03 = valor, peso
        else:
            if i == 0:
                valor01 = 9999, peso
            elif i == 1:
                valor02 = 9999, peso
            elif i == 2:
                valor03 = 9999, peso

    menor, menor_peso = min(valor01, valor02, valor03)
    return menor, menor_peso


def multicaminhos(m, k, r, n, entradas):
    heap = []
    sequencias = []
    sequencia_atual = []
    ultimo_elemento = 0
    qnt_numeros_com_peso = 0

    for numero_atual in entradas:
        # Caso o heap tenha espaço disponível, inserir diretamente
        if len(heap) < m:  # Tamanho máximo da heap
            adicionar_com_peso(heap, numero_atual, 0)
        else:

            menor, menor_peso = extrair_menor_com_peso_0(heap)

            # Se o número atual é >= ao menor número da heap
            if numero_atual >= ultimo_elemento:

                # Adicionar o menor na sequência atual
                sequencia_atual.append(menor)
                ultimo_elemento = menor

                # Remover o menor da heap
                remove_menor_heap(heap)


                # Adicionar o número atual à heap
                if (numero_atual >= ultimo_elemento):
                    adicionar_com_peso(heap, numero_atual, 0)
                    heapq.heapify(heap)
                else:
                    adicionar_com_peso(heap, numero_atual, 1)
                    qnt_numeros_com_peso += 1
                    heapq.heapify(heap)
            else:
                # Se o menor número da heap for menor que o último da sequência
                # e o menor número está com peso 0, ele recebe peso 1
                if menor_peso == 0:
                    # Remover o menor da heap
                    heapq.heappop(heap)

                    adicionar_com_peso(heap, numero_atual, 1)
                    qnt_numeros_com_peso += 1
                else:
                    sequencia_atual.append(menor)
                    ultimo_elemento = menor

            # Adiciona o menor número na sequência atual se a sequência ainda não atingiu o tamanho máximo
            if len(sequencia_atual) >= (n // m):
                sequencias.append(sequencia_atual)
                sequencia_atual = []

            # Se a heap ficou vazia, recomeça com os elementos restantes
            if len(heap) == 0:
                break

    # Adicionar a última sequência se houver elementos
    if sequencia_atual:
        sequencias.append(sequencia_atual)

    return sequencias

    '''
    # Divide a lista em k sublistas
    sublists = [numeros[i::k] for i in range(k)]

    # Ordena cada sublista individualmente
    sublists = [sorted(sublist) for sublist in sublists]

    # Início do processo de K-way Merge Sort
    min_heap = []

    # Adiciona o primeiro elemento de cada sublista no heap com seus respectivos índices
    for i, lst in enumerate(sublists):
        if lst:  # Verifica se a lista não está vazia
            heapq.heappush(min_heap, (lst[0], i, 0))

    sorted_list = []

    # Realiza o processo de merge
    while min_heap:
        val, list_idx, element_idx = heapq.heappop(min_heap)
        sorted_list.append(val)

        # Se ainda houver elementos na sublista, adiciona o próximo ao heap
        if element_idx + 1 < len(sublists[list_idx]):
            next_tuple = (sublists[list_idx][element_idx + 1], list_idx, element_idx + 1)
            heapq.heappush(min_heap, next_tuple)

    # Fim do processo de K-way Merge Sort

    print("Lista ordenada pelo método multicaminhos:\n", sorted_list)
    return sorted_list
    '''

def polifasica():
    # Geração da sequência de Fibonacci
    fib = [1, 1]
    while sum(fib) < n:
        fib.append(fib[-1] + fib[-2])

    # Simulação da distribuição de dados em fitas
    sublists = [[] for _ in range(3)]  # Criando três sublistas (simulando fitas)
    index = 0
    temp_list = sorted(numeros)
    for f in fib[::-1]:  # Inverte a sequência de Fibonacci para distribuição
        sublists[index % 3].extend(temp_list[:f])
        temp_list = temp_list[f:]
        index += 1

    print("Distribuição inicial em fitas:")
    for i, sublist in enumerate(sublists):
        print(f"Fita {i + 1}: {sublist}")

    # Inicia o processo de fusão polifásica
    sorted_list = []
    while any(len(sublist) > 0 for sublist in sublists[:-1]):
        merged_list = []
        for sublist in sublists[:-1]:  # Exceto a última fita
            if sublist:
                merged_list.append(sublist.pop(0))

        if merged_list:
            sorted_list.append(min(merged_list))  # Adiciona o menor elemento à lista ordenada
            merged_list.remove(min(merged_list))

        # Redistribui de volta os elementos restantes para as fitas iniciais
        for sublist in sublists[:-1]:
            if merged_list:
                sublist.append(merged_list.pop(0))

    # Finaliza o processamento dos elementos restantes
    remaining_elements = []
    for sublist in sublists[:-1]:
        remaining_elements.extend(sublist)
    remaining_elements.extend(sublists[-1])

    sorted_list.extend(sorted(remaining_elements))

    print("Lista ordenada pelo método polifásico:\n", sorted_list)
    return sorted_list


def cascata():
    def merge(left, right):
        sorted_list = []
        while left and right:
            if left[0] <= right[0]:
                sorted_list.append(left.pop(0))
            else:
                sorted_list.append(right.pop(0))
        sorted_list.extend(left or right)
        return sorted_list

    def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left_half = merge_sort(arr[:mid])
        right_half = merge_sort(arr[mid:])
        return merge(left_half, right_half)

    # Dividindo a lista inicial em sublistas menores
    sublists = [numeros[i:i + r] for i in range(0, len(numeros), r)]
    print("Divisão inicial das sublistas:")
    for i, sublist in enumerate(sublists):
        print(f"Sublista {i + 1}: {sublist}")

    # Ordena cada sublista usando Merge Sort
    sorted_sublists = [merge_sort(sublist) for sublist in sublists]

    # Fusão escalonada das sublistas
    while len(sorted_sublists) > 1:
        merged_sublists = []
        for i in range(0, len(sorted_sublists), 2):
            if i + 1 < len(sorted_sublists):
                merged_sublists.append(merge(sorted_sublists[i], sorted_sublists[i + 1]))
            else:
                merged_sublists.append(sorted_sublists[i])
        sorted_sublists = merged_sublists

    sorted_list = sorted_sublists[0] if sorted_sublists else []
    print("Lista ordenada pelo método cascata:\n", sorted_list)
    return sorted_list
"""
N = input() # Pede uma entrada ao usuário
while N not in ['B', 'P', 'C']:
    N = input("Entrada inválida. Digite B, P ou C: ") # Essa condição garante que apenas sejam aceitas as respostas B, P e C fornecidas pelos usuários
entrada = input()
valores = entrada.split()
while len(valores) != 4:
    print("Digite quatro valores separados por espaço.")
    entrada = input()
    valores = entrada.split()
m, k, r, n = map(int, valores) # Converte todas as variáveis para inteiros
minimo = 1
maximo = 100
numeros = [random.randint(minimo, maximo) for i in range(n)] # Gera e armazena n números aleatórios em uma lista
print("Números aleatórios gerados:\n", numeros) # Imprime a lista de números aleatórios
"""
N = "B"
m = 3
k = 4
r = 3
n = 17

with open("entrada.txt", "r") as file:
    entrada = file.read()

# Convertendo o conteúdo do arquivo em uma lista de inteiros
numeros = list(map(int, entrada.split(' ')))

if N=="B":
    multicaminhos(m,k,r,n,numeros)
elif N=='P':
    polifasica()
elif N=='C':
    cascata()
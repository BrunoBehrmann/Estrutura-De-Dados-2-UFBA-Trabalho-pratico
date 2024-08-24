import heapq

def calculoBeta(m, paginas):
    r = sum(len(pagina) for pagina in paginas if pagina)
    # Calcular a soma dos tamanhos das sublistas
    total_registros = sum(len(subpagina) for pagina in paginas for subpagina in pagina if pagina)
    Beta = (1 / (m * r)) * total_registros
    # Arredondar Beta para até dois decimais
    Beta = round(Beta, 2)
    return Beta

def imprimir_estado(fase, paginas, m):
    beta = calculoBeta(m, paginas)
    print(f"fase {fase} {beta}")
    for i, pagina in enumerate(paginas):
        if any(pagina):
            conteudo_formatado = "".join(f"{{{' '.join(map(str, lista))}}}" for lista in pagina if lista)
            print(f"{i + 1}: {conteudo_formatado}")

def multicaminhos(m, k, r, n, numeros):
    def extrair_menor_com_peso_0(heap, m):
        menor_valor, menor_peso = float('inf'), None
        for valor, peso in heap[:m]:
            if peso == 0 and valor < menor_valor:
                menor_valor, menor_peso = valor, peso
        return (menor_valor, menor_peso) if menor_peso is not None else (None, None)

    def adicionar_com_peso(heap, valor, peso):
        heapq.heappush(heap, (valor, peso))

    def zera_peso_heap(heap):
        heap = [list(item) for item in heap]
        for item in heap:
            item[1] = 0
        return [tuple(item) for item in heap], 0

    def geraSequenciasOrdenadas(m, entradas):
        heap = []
        sequencias = []
        sequencia_atual = []
        ultimo_elemento = 0
        qnt_numeros_com_peso = 0

        for numero_atual in entradas:
            if len(heap) < m:
                adicionar_com_peso(heap, numero_atual, 0)
            else:
                if qnt_numeros_com_peso == 3:
                    heap, qnt_numeros_com_peso = zera_peso_heap(heap)

                menor, menor_peso = extrair_menor_com_peso_0(heap, m)

                if numero_atual >= ultimo_elemento:
                    sequencia_atual.append(menor)
                    ultimo_elemento = menor
                    heap = [item for item in heap if not (item[0] == menor and item[1] == menor_peso)]

                    if numero_atual >= ultimo_elemento:
                        adicionar_com_peso(heap, numero_atual, 0)
                    else:
                        adicionar_com_peso(heap, numero_atual, 1)
                        qnt_numeros_com_peso += 1
                else:
                    if menor_peso == 0:
                        sequencia_atual.append(menor)
                        ultimo_elemento = menor
                        heap = [item for item in heap if not (item[0] == menor and item[1] == menor_peso)]
                        adicionar_com_peso(heap, numero_atual, 1)
                        qnt_numeros_com_peso += 1
                    else:
                        sequencia_atual.append(menor)
                        ultimo_elemento = menor

                if len(sequencia_atual) >= (len(entradas) // m):
                    sequencias.append(sequencia_atual)
                    sequencia_atual = []
                    heap, qnt_numeros_com_peso = zera_peso_heap(heap)
                    ultimo_elemento = 0

                if len(heap) == 0:
                    break

        if sequencia_atual:
            sequencias.append(sequencia_atual)
        return sequencias

    def criar_listas(k):
        return [[] for _ in range(k)]

    def intercala_pagina(k, sequenciasOrdenadas):
        paginasPorFase = k // 2
        paginas = criar_listas(k)
        pagina_atual = 0

        for sequencia in sequenciasOrdenadas:
            paginas[pagina_atual].append(sequencia)
            pagina_atual = (pagina_atual + 1) % paginasPorFase

        return paginas

    def intercala_pagina_lado(k, sequenciasOrdenadas, esquerda, paginas):
        paginasPorFase = k // 2
        pagina_atual = 0 if esquerda == 1 else (k // 2)
        primeira_iteracao = True

        for sequencia in sequenciasOrdenadas:
            if primeira_iteracao and paginas[pagina_atual]:
                pagina_atual = (pagina_atual + 1) % k
                paginas[pagina_atual].append(sequencia)
                primeira_iteracao = False
            else:
                paginas[pagina_atual].append(sequencia)
                pagina_atual = (pagina_atual + 1) % k

        return paginas

    def coleta_listas_direita(k, paginas):
        metade = k // 2
        listas_direita = []
        while any(paginas[i] for i in range(metade, k)):
            for i in range(metade, k):
                if paginas[i]:
                    lista_temp = paginas[i].pop(0)
                    listas_direita.append(lista_temp)
        return listas_direita

    def coleta_listas_esqueda(k, paginas):
        metade = k // 2
        listas_esqueda = []
        while any(paginas[i] for i in range(metade)):
            for i in range(metade):
                if paginas[i]:
                    lista_temp = paginas[i].pop(0)
                    listas_esqueda.append(lista_temp)
        return listas_esqueda

    def distribui_direita_esqueda(k, paginas):
        listas_direita = coleta_listas_direita(k, paginas)
        paginas = intercala_pagina_lado(k, listas_direita, 1, paginas)
        return paginas

    def distribui_esqueda_direita(k, paginas):
        listas_esqueda = coleta_listas_esqueda(k, paginas)
        paginas = intercala_pagina_lado(k, listas_esqueda, 0, paginas)
        return paginas

    def ordenacao_multicaminhos(paginas, contador_escrita, fase, r, m):
        k = len(paginas)

        if fase == 0:
            imprimir_estado(fase, paginas, m)

        if len([p for p in paginas if p]) > 1:
            lista_temp = []
            for pagina in paginas:
                if pagina and isinstance(pagina[0], list):
                    lista_temp.extend(pagina.pop(0))

            lista_temp.sort()
            contador_escrita += len(lista_temp)
            contador_escrita += sum(len(subpagina) for pagina in paginas for subpagina in pagina if pagina)
            pagina_index = k // 2

            if fase == 0:
                paginas[pagina_index] = [lista_temp]
                paginas = distribui_esqueda_direita(k, paginas)
            elif fase % 2 == 0:
                paginas[pagina_index].insert(0, lista_temp)
                paginas = distribui_direita_esqueda(k, paginas)
            else:
                paginas[pagina_index] = [lista_temp]
                paginas = distribui_esqueda_direita(k, paginas)

            r = len(paginas)
            fase += 1
            imprimir_estado(fase, paginas, m)
            return ordenacao_multicaminhos(paginas, contador_escrita, fase, r, m)
        else:
            total_registros = sum(len(subpagina) for pagina in paginas for subpagina in pagina if pagina)
            alfa = contador_escrita / total_registros
            alfa = round(alfa, 2)
            print(f"final {alfa}")

        return paginas, contador_escrita

    fase = 0
    contador_escrita = 0
    sequencias = geraSequenciasOrdenadas(m, numeros)
    paginas = intercala_pagina(k, sequencias)
    ordenacao_multicaminhos(paginas, contador_escrita, fase, r, m)

def polifasica(m, k, r, n, numeros):
    fib = [1, 1]
    while sum(fib) < n:
        fib.append(fib[-1] + fib[-2])

    sublists = [[] for _ in range(k)]
    index = 0
    temp_list = sorted(numeros)
    for f in fib[::-1]:
        sublists[index % 3].extend(temp_list[:f])
        temp_list = temp_list[f:]
        index += 1

    print("Distribuição inicial em fitas:")
    for i, sublist in enumerate(sublists):
        print(f"Fita {i + 1}: {sublist}")

    sorted_list = []
    while any(len(sublist) > 0 for sublist in sublists[:-1]):
        merged_list = []
        for sublist in sublists[:-1]:
            if sublist:
                merged_list.append(sublist.pop(0))

        if merged_list:
            sorted_list.append(min(merged_list))
            merged_list.remove(min(merged_list))

        for sublist in sublists[:-1]:
            if merged_list:
                sublist.append(merged_list.pop(0))

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

    sublists = [numeros[i:i + r] for i in range(0, len(numeros), r)]
    print("Divisão inicial das sublistas:")
    for i, sublist in enumerate(sublists):
        print(f"Sublista {i + 1}: {sublist}")

    sorted_sublists = [merge_sort(sublist) for sublist in sublists]

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

# Código principal
with open("entrada.txt", "r") as file:
    N = file.readline().strip()
    m, k, r, n = map(int, file.readline().split())
    numeros = list(map(int, file.readline().split()))

if N == "B":
    multicaminhos(m, k, r, n, numeros)
elif N == 'P':
    polifasica(m, k, r, n, numeros)
elif N == 'C':
    cascata()
else:
    print("Entrada inválida.")

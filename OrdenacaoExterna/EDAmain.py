import heapq

def calculoBeta(m, paginas):
    r = sum(len(pagina) for pagina in paginas if pagina)
    total_registros = sum(len(subpagina) for pagina in paginas for subpagina in pagina if pagina)
    Beta = (1 / (m * r)) * total_registros
    Beta = round(Beta, 2)
    return Beta

def imprimir_estado(fase, paginas, m, contador_escrita):
    total_registros = sum(len(subpagina) for pagina in paginas for subpagina in pagina if pagina)
    alfa = contador_escrita / total_registros
    alfa = round(alfa, 2)

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
                if qnt_numeros_com_peso == m:
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
                    if menor_peso == 0 and menor > ultimo_elemento:
                        sequencia_atual.append(menor)
                        ultimo_elemento = menor
                        heap = [item for item in heap if not (item[0] == menor and item[1] == menor_peso)]
                        adicionar_com_peso(heap, numero_atual, 1)
                        qnt_numeros_com_peso += 1
                    elif menor_peso == 0 and menor < ultimo_elemento:
                        sequencias.append(sequencia_atual)
                        sequencia_atual = []
                        ultimo_elemento = 0
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

    def intercala_pagina(k, sequenciasOrdenadas):
        paginasPorFase = k // 2
        paginas = [[] for _ in range(k)]
        pagina_atual = 0

        for sequencia in sequenciasOrdenadas:
            paginas[pagina_atual].append(sequencia)
            pagina_atual = (pagina_atual + 1) % paginasPorFase

        return paginas

    def intercala_pagina_lado(k, sequenciasOrdenadas, esquerda, paginas):
        paginasPorFase = k // 2
        pagina_atual = 0 if esquerda == 1 else (k // 2)
        primeira_iteracao = True

        if esquerda:
            for sequencia in sequenciasOrdenadas:

                # se ja tiver sublista no primeiro index
                if primeira_iteracao and paginas[pagina_atual]:
                    if pagina_atual == (k // 2) - 1:
                        # se ja existir, volta
                        pagina_atual = 0
                        paginas[pagina_atual].append(sequencia)

                    else: # se nao for o ultimo da esquerda
                        pagina_atual = (pagina_atual + 1)
                        paginas[pagina_atual].append(sequencia)

                    primeira_iteracao = False

                else: # resto das interacoes
                    # se estiver no ultimo index da esquerda
                    if pagina_atual == (k // 2) - 1:
                        paginas[pagina_atual].append(sequencia)
                        pagina_atual = 0
                    else:
                        paginas[pagina_atual].append(sequencia)
                        pagina_atual = (pagina_atual + 1)



        else: #direita
            for sequencia in sequenciasOrdenadas:

                # se ja tiver sublista no primeiro index
                if primeira_iteracao and paginas[pagina_atual]:
                    if pagina_atual == k - 1:
                        # se ja existir, volta
                        pagina_atual = k // 2
                        paginas[pagina_atual].append(sequencia)

                    else:  # se nao for o ultimo da direita
                        pagina_atual = (pagina_atual + 1)
                        paginas[pagina_atual].append(sequencia)

                    primeira_iteracao = False

                else:  # resto das interacoes
                    # se estiver no ultimo index da direita
                    if pagina_atual == k - 1:
                        paginas[pagina_atual].append(sequencia)
                        pagina_atual = k // 2

                    else: # se nao for o ultimo da direita
                        paginas[pagina_atual].append(sequencia)
                        pagina_atual = (pagina_atual + 1)

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
            imprimir_estado(fase, paginas, m, contador_escrita)


        if len([p for p in paginas if p]) > 1:
            lista_temp = []
            for pagina in paginas:
                if pagina and isinstance(pagina[0], list):
                    lista_temp.extend(pagina.pop(0))

            lista_temp.sort()
            contador_escrita += len(lista_temp)
            contador_escrita += sum(len(subpagina) for pagina in paginas for subpagina in pagina if pagina)
            pagina_index = k // 2

            if fase == 0 or fase % 2 == 0:
                paginas[pagina_index] = [lista_temp]
                paginas = distribui_esqueda_direita(k, paginas)
            else:
                paginas[pagina_index].insert(0, lista_temp)
                paginas = distribui_direita_esqueda(k, paginas)

            r = len(paginas)
            fase += 1
            imprimir_estado(fase, paginas, m, contador_escrita)
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

""" INTERCALAÇÃO POLIFÁSICA """
def gerar_array(n, k):
    # Passo base
    array_atual = [0] * k
    array_atual[-1] = 1  # O último elemento é 1

    for depth in range(1, n + 1):  # +1 para garantir que possamos verificar até o último passo
        novo_array = [0] * k

        # Índices do maior e menor valor do array anterior
        maior_valor = max(array_atual)
        index_maior_valor = array_atual.index(maior_valor)
        menor_valor = min(array_atual)
        index_menor_valor = array_atual.index(menor_valor)

        # Passo 1: Coloca o maior valor no índice do menor valor do array anterior
        novo_array[index_menor_valor] = maior_valor

        # Passo 2: Coloca 0 no índice do maior valor do array anterior
        novo_array[index_maior_valor] = 0

        # Passo 3: Para os demais índices, soma o maior valor com o valor do array anterior
        for i in range(k):
            if i not in (index_maior_valor, index_menor_valor):
                novo_array[i] = maior_valor + array_atual[i]

        array_atual = novo_array

        # Verifica se a soma do array é >= n
        if sum(array_atual) >= n:
            return array_atual

    return array_atual

def gera_fase_inicial(k, n, numeros):
    # Gera o array inicial de fases
    fase_inicial = gerar_array(n, k)

    # Cria a estrutura de páginas como uma lista de listas
    paginas = [[] for _ in range(k)]

    # Preenche as páginas de acordo com fase_inicial
    posicao_atual = 0
    for i, tamanho in enumerate(fase_inicial):
        pagina = []
        for _ in range(tamanho):
            if posicao_atual < len(numeros):
                pagina.append([numeros[posicao_atual]])
                posicao_atual += 1
            else:
                pagina.append([float('inf')])  # Preenche com float('inf') se não houver mais números
        paginas[i] = pagina

    return paginas
def imprime_paginas_final(paginas, fase, contador_escrita):

    # grafico
    total_registros = sum(len(subpagina) for pagina in paginas for subpagina in pagina if pagina)
    alfa = contador_escrita / total_registros
    alfa = round(alfa, 2)

    beta = calculoBeta(m, paginas)
    print(f"Fase {fase} {beta}")
    for i, pagina in enumerate(paginas):
        elementos = ' '.join(
            f"{{{' '.join(str(elem) for elem in sublista if elem != float('inf'))}}}"
            for sublista in pagina if any(elem != float('inf') for elem in sublista)
        )
        print(f"{i + 1}: {elementos}")
    print(f"final {alfa}")

def imprime_paginas(paginas, fase, m, contador_escrita):
    # grafico
    total_registros = sum(len(subpagina) for pagina in paginas for subpagina in pagina if pagina)
    alfa = contador_escrita / total_registros
    alfa = round(alfa, 2)

    beta = calculoBeta(m, paginas)
    print(f"Fase {fase} {beta}")
    for i, pagina in enumerate(paginas):
        elementos = ' '.join(f"{{{' '.join(map(str, sublista))}}}" for sublista in pagina)
        print(f"{i + 1}: {elementos}")

def polifasica(m, k, r, n, numeros):
    paginas = gera_fase_inicial(k, n, numeros)
    # verificar
    contador_escrita = sum(len(pagina) for pagina in paginas if pagina)
    fase = 0
    while True:
        imprime_paginas(paginas, fase, m, contador_escrita)

        # Encontra a menor página não vazia e o índice da página vazia
        tamanhos = [len(pagina) for pagina in paginas]
        menor_pagina = min([tamanho for tamanho in tamanhos if tamanho > 0])
        index_pagina_vazia = tamanhos.index(0)

        if menor_pagina == 0:
            break
        lista = []
        for _ in range(menor_pagina):
            elementos_para_remover = []
            for i in range(k):
                if i != index_pagina_vazia and paginas[i]:
                    elementos_para_remover.extend(paginas[i].pop(0))

            lista.append(sorted(elementos_para_remover))

        contador_escrita += sum(len(sublista) for sublista in lista)
        paginas[index_pagina_vazia] = lista

        fase += 1

        # Verifica se todas as páginas exceto uma estão vazias
        paginas_nao_vazias = [pagina for pagina in paginas if len(pagina) > 0]
        if len(paginas_nao_vazias) == 1:
            break

    imprime_paginas_final(paginas, fase, contador_escrita)

def cascata(m, k, r, n, numeros):
    paginas = gera_fase_inicial(k, n, numeros)
    # verificar
    contador_escrita = sum(len(pagina) for pagina in paginas if pagina)
    fase = 0
    while True:
        imprime_paginas(paginas, fase, m, contador_escrita)
        tamanhos = [len(pagina) for pagina in paginas]
        menor_pagina = min([tamanho for tamanho in tamanhos if tamanho > 0])
        index_pagina_vazia = tamanhos.index(0)

        if menor_pagina == 0:
            break
        lista = []
        for _ in range(menor_pagina):
            elementos_para_remover = []
            for i in range(k):
                if i != index_pagina_vazia and paginas[i]:
                    elementos_para_remover.extend(paginas[i].pop(0))

            lista.append(sorted(elementos_para_remover))

        contador_escrita += sum(len(sublista) for sublista in lista)
        paginas[index_pagina_vazia] = lista

        fase += 1
        paginas_nao_vazias = [pagina for pagina in paginas if len(pagina) > 0]
        if len(paginas_nao_vazias) == 1:
            break

    imprime_paginas_final(paginas, fase, contador_escrita)

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
    cascata(m, k, r, n, numeros)
else:
    print("Entrada inválida.")
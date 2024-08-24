def gerar_array(n, k):
    # Passo base
    array_atual = [0] * k
    array_atual[-1] = 1  # O último elemento é 1

    print(f"Depth 0: {array_atual}")

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
        print(f"Depth {depth}: {array_atual}")

        # Verifica se a soma do array é >= n
        if sum(array_atual) >= n:
            return array_atual

    return array_atual


# Exemplo de uso
resultado = gerar_array(17, 4)
print(f"Resultado final: {resultado}")

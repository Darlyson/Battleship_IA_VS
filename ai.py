import random

# =====================================================
# GERAÇÃO AUTOMÁTICA DE FROTAS
# =====================================================

def gerar_posicionamento_valido(tamanhos):

    grelha = [['🟦' for _ in range(10)] for _ in range(10)]
    frota = []

    for tamanho in tamanhos:

        colocado = False

        while not colocado:

            orientacao = random.choice(["H", "V"])

            if orientacao == "H":

                linha = random.randint(0, 9)
                coluna = random.randint(0, 10 - tamanho)

                livre = True

                for i in range(tamanho):
                    if grelha[linha][coluna + i] != '🟦':
                        livre = False
                        break

                if livre:

                    coords = []

                    for i in range(tamanho):

                        grelha[linha][coluna + i] = 'N'
                        coords.append((linha, coluna + i))

                    frota.append((tamanho, coords))
                    colocado = True

            else:

                linha = random.randint(0, 10 - tamanho)
                coluna = random.randint(0, 9)

                livre = True

                for i in range(tamanho):

                    if grelha[linha + i][coluna] != '🟦':
                        livre = False
                        break

                if livre:

                    coords = []

                    for i in range(tamanho):

                        grelha[linha + i][coluna] = 'N'
                        coords.append((linha + i, coluna))

                    frota.append((tamanho, coords))
                    colocado = True

    return frota


# =====================================================
# IA BETA
# Busca Heurística
# =====================================================

class AgenteHeuristico:

    def __init__(self):

        self.nome = "IA Beta"

        self.alvos_disponiveis = [
            (l, c)
            for l in range(10)
            for c in range(10)
        ]

        self.pilha_alvos = []

    def posicionar_frota(self, tamanhos):

        return gerar_posicionamento_valido(tamanhos)

    def escolher_ataque(self):

        while self.pilha_alvos:

            alvo = self.pilha_alvos.pop()

            if alvo in self.alvos_disponiveis:

                self.alvos_disponiveis.remove(alvo)
                return alvo

        alvo = random.choice(self.alvos_disponiveis)

        self.alvos_disponiveis.remove(alvo)

        return alvo

    def registrar_resultado(self, alvo, acertou):

        if not acertou:
            return

        l, c = alvo

        vizinhos = [

            (l - 1, c),
            (l + 1, c),
            (l, c - 1),
            (l, c + 1)

        ]

        for vl, vc in vizinhos:

            if 0 <= vl < 10 and 0 <= vc < 10:

                if (vl, vc) in self.alvos_disponiveis:

                    self.pilha_alvos.append((vl, vc))

    def registrar_afundamento(self, tamanho):

        self.pilha_alvos.clear()
        
# =====================================================
# IA ALPHA
# Minimax + Poda Alfa Beta
# =====================================================

def calcular_heuristica(radar, navios_restantes):

    matriz = [[0 for _ in range(10)] for _ in range(10)]

    if not navios_restantes:
        navios_restantes = [5,4,3,3,2]

    for tamanho in navios_restantes:

        # Horizontal

        for l in range(10):

            for c in range(10-tamanho+1):

                valido = True
                peso = 1

                for i in range(tamanho):

                    cel = radar[l][c+i]

                    if cel == '💦':
                        valido = False
                        break

                    if cel == '💥':
                        peso *= 20

                if valido:

                    for i in range(tamanho):

                        if radar[l][c+i] == '🟦':

                            matriz[l][c+i] += peso

        # Vertical

        for c in range(10):

            for l in range(10-tamanho+1):

                valido = True
                peso = 1

                for i in range(tamanho):

                    cel = radar[l+i][c]

                    if cel == '💦':
                        valido = False
                        break

                    if cel == '💥':
                        peso *= 20

                if valido:

                    for i in range(tamanho):

                        if radar[l+i][c] == '🟦':

                            matriz[l+i][c] += peso

    return matriz


class AgenteAlpha:

    def __init__(self, profundidade=2):

        self.nome = "IA Alpha"

        self.profundidade = profundidade

        self.navios_restantes = [5,4,3,3,2]

        # radar da IA
        self.radar = [

            ['🟦' for _ in range(10)]

            for _ in range(10)

        ]

    def posicionar_frota(self, tamanhos):

        return gerar_posicionamento_valido(tamanhos)

    def registrar_resultado(self, linha, coluna, acertou):

        if acertou:
            self.radar[linha][coluna] = '💥'
        else:
            self.radar[linha][coluna] = '💦'

    def registrar_afundamento(self, tamanho):

        if tamanho in self.navios_restantes:
            self.navios_restantes.remove(tamanho)

    def melhores_jogadas(self, matriz, limite=6):

        jogadas = []

        for l in range(10):

            for c in range(10):

                if self.radar[l][c] == '🟦':

                    jogadas.append(

                        (matriz[l][c], (l,c))

                    )

        jogadas.sort(reverse=True)

        return [j[1] for j in jogadas[:limite]]

    def avaliar(self, radar):

        matriz = calcular_heuristica(

            radar,

            self.navios_restantes

        )

        maior = 0

        for linha in matriz:

            maior = max(maior, max(linha))

        return maior

    def minimax(

        self,

        radar,

        profundidade,

        alpha,

        beta,

        maximizando

    ):

        if profundidade == 0:

            return self.avaliar(radar)

        matriz = calcular_heuristica(

            radar,

            self.navios_restantes

        )

        candidatos = self.melhores_jogadas(

            matriz,

            4

        )

        if not candidatos:

            return self.avaliar(radar)

        if maximizando:

            melhor = -999999

            for l,c in candidatos:

                novo = [x[:] for x in radar]

                novo[l][c] = '💥'

                valor = self.minimax(

                    novo,

                    profundidade-1,

                    alpha,

                    beta,

                    False

                )

                melhor = max(melhor, valor)

                alpha = max(alpha, valor)

                if beta <= alpha:
                    break

            return melhor

        else:

            pior = 999999

            for l,c in candidatos:

                novo = [x[:] for x in radar]

                novo[l][c] = '💦'

                valor = self.minimax(

                    novo,

                    profundidade-1,

                    alpha,

                    beta,

                    True

                )

                pior = min(pior, valor)

                beta = min(beta, valor)

                if beta <= alpha:
                    break

            return pior

    def escolher_ataque(self):

        matriz = calcular_heuristica(

            self.radar,

            self.navios_restantes

        )

        candidatos = self.melhores_jogadas(

            matriz,

            5

        )

        melhor = candidatos[0]

        melhor_valor = -999999

        alpha = -999999
        beta = 999999

        for l,c in candidatos:

            novo = [x[:] for x in self.radar]

            novo[l][c] = '💥'

            valor = self.minimax(

                novo,

                self.profundidade,

                alpha,

                beta,

                False

            )

            if valor > melhor_valor:

                melhor_valor = valor

                melhor = (l,c)

        return melhor, matriz
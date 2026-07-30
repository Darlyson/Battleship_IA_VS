# ai.py
import random

# =====================================================
# GERAÇÃO AUTOMÁTICA DE FROTAS
# =====================================================
def gerar_posicionamento_valido(tamanhos):
    """Posiciona os navios aleatoriamente sem sobreposição (Tentativa e Erro)."""
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
# IA BETA - ALGORITMO: BUSCA HEURÍSTICA (Hunt and Target)
# =====================================================
# EXPLICAÇÃO DO ALGORITMO:
# Esta IA possui dois estados: "Caçando" (Hunt) e "Alvejando" (Target).
# 1. Caçando: Atira aleatoriamente no tabuleiro.
# 2. Alvejando: Quando acerta um navio, empilha as coordenadas vizinhas (Cima, Baixo, Esquerda, Direita) 
#    em uma Pilha (Stack). Nos turnos seguintes, ela atira nessas vizinhanças até afundar o navio, 
#    otimizando a busca local.
# =====================================================
class AgenteHeuristico:
    def __init__(self):
        self.nome = "IA Beta"
        self.alvos_disponiveis = [(l, c) for l in range(10) for c in range(10)]
        self.pilha_alvos = [] # Stack usada para o modo "Target"

    def posicionar_frota(self, tamanhos):
        return gerar_posicionamento_valido(tamanhos)

    def escolher_ataque(self):
        # Modo Target: Se há alvos na pilha (vizinhança de um acerto anterior), atire lá.
        while self.pilha_alvos:
            alvo = self.pilha_alvos.pop()
            if alvo in self.alvos_disponiveis:
                self.alvos_disponiveis.remove(alvo)
                return alvo

        # Modo Hunt: Busca aleatória pelo mapa
        alvo = random.choice(self.alvos_disponiveis)
        self.alvos_disponiveis.remove(alvo)
        return alvo

    def registrar_resultado(self, alvo, acertou):
        if not acertou:
            return

        # Acertou! Adiciona os vizinhos ortogonais na pilha (Busca Local)
        l, c = alvo
        vizinhos = [(l - 1, c), (l + 1, c), (l, c - 1), (l, c + 1)]

        for vl, vc in vizinhos:
            if 0 <= vl < 10 and 0 <= vc < 10:
                if (vl, vc) in self.alvos_disponiveis:
                    self.pilha_alvos.append((vl, vc))

    def registrar_afundamento(self, tamanho):
        # Limpa a pilha para voltar ao modo Hunt (evita atirar na água atoa)
        self.pilha_alvos.clear()
        
# =====================================================
# IA ALPHA - ALGORITMO: MINIMAX COM PODA ALFA-BETA E MATRIZ DE CALOR
# =====================================================
# EXPLICAÇÃO DO ALGORITMO:
# 1. Matriz de Densidade de Probabilidade (Heurística): Calcula matematicamente 
#    quantas formas os navios restantes podem caber em cada célula vazia do radar.
# 2. Minimax: Simula "jogadas futuras". Assume que se ela atirar num lugar, qual será 
#    a melhor resposta no futuro? Tenta Maximizar seus pontos e Minimizar perdas.
# 3. Poda Alfa-Beta: Descarta galhos da árvore de simulação que já se provaram piores 
#    que as opções atuais, poupando processamento (memória).
# =====================================================
def calcular_heuristica(radar, navios_restantes):
    """Gera um mapa de calor matemático cruzando as posições possíveis dos navios."""
    matriz = [[0 for _ in range(10)] for _ in range(10)]
    if not navios_restantes:
        navios_restantes = [5, 4, 3, 3, 2]

    for tamanho in navios_restantes:
        # Varredura Horizontal
        for l in range(10):
            for c in range(10 - tamanho + 1):
                valido = True
                peso = 1
                for i in range(tamanho):
                    cel = radar[l][c+i]
                    if cel == '💦':
                        valido = False # Não cabe navio onde há água atingida
                        break
                    if cel == '💥':
                        peso *= 20 # Multiplica probabilidade se cruzar com um acerto
                if valido:
                    for i in range(tamanho):
                        if radar[l][c+i] == '🟦':
                            matriz[l][c+i] += peso

        # Varredura Vertical
        for c in range(10):
            for l in range(10 - tamanho + 1):
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
        self.navios_restantes = [5, 4, 3, 3, 2]
        self.radar = [['🟦' for _ in range(10)] for _ in range(10)] # Memória da IA

    def posicionar_frota(self, tamanhos):
        return gerar_posicionamento_valido(tamanhos)

    def registrar_resultado(self, linha, coluna, acertou):
        # Atualiza a memória da IA
        if acertou:
            self.radar[linha][coluna] = '💥'
        else:
            self.radar[linha][coluna] = '💦'

    def registrar_afundamento(self, tamanho):
        # Mantém controle dos navios vivos inimigos para calcular o mapa de calor correto
        if tamanho in self.navios_restantes:
            self.navios_restantes.remove(tamanho)

    def melhores_jogadas(self, matriz, limite=6):
        # Extrai as N coordenadas com maior probabilidade matemática de ter um navio
        jogadas = []
        for l in range(10):
            for c in range(10):
                if self.radar[l][c] == '🟦':
                    jogadas.append((matriz[l][c], (l, c)))
        jogadas.sort(reverse=True)
        return [j[1] for j in jogadas[:limite]]

    def avaliar(self, radar):
        # Retorna o valor mais alto da matriz de probabilidade como "nota" deste estado
        matriz = calcular_heuristica(radar, self.navios_restantes)
        maior = 0
        for linha in matriz:
            maior = max(maior, max(linha))
        return maior

    def minimax(self, radar, profundidade, alpha, beta, maximizando):
        """Algoritmo principal de tomada de decisão baseada em árvore de busca."""
        if profundidade == 0:
            return self.avaliar(radar)

        matriz = calcular_heuristica(radar, self.navios_restantes)
        candidatos = self.melhores_jogadas(matriz, 4)

        if not candidatos:
            return self.avaliar(radar)

        if maximizando:
            melhor = -999999
            for l, c in candidatos:
                novo = [x[:] for x in radar] # Copia o radar para não alterar o original
                novo[l][c] = '💥'
                
                # Desce na árvore simulando o próximo turno
                valor = self.minimax(novo, profundidade - 1, alpha, beta, False)
                melhor = max(melhor, valor)
                
                # Poda Alfa-Beta (Corte de processamento inútil)
                alpha = max(alpha, valor)
                if beta <= alpha:
                    break
            return melhor
        else:
            pior = 999999
            for l, c in candidatos:
                novo = [x[:] for x in radar]
                novo[l][c] = '💦'
                
                valor = self.minimax(novo, profundidade - 1, alpha, beta, True)
                pior = min(pior, valor)
                
                beta = min(beta, valor)
                if beta <= alpha:
                    break
            return pior

    def escolher_ataque(self):
        matriz = calcular_heuristica(self.radar, self.navios_restantes)
        candidatos = self.melhores_jogadas(matriz, 5)

        melhor = candidatos[0]
        melhor_valor = -999999
        alpha = -999999
        beta = 999999

        # Testa as melhores candidatas na árvore Minimax
        for l, c in candidatos:
            novo = [x[:] for x in self.radar]
            novo[l][c] = '💥' 
            
            valor = self.minimax(novo, self.profundidade, alpha, beta, False)
            if valor > melhor_valor:
                melhor_valor = valor
                melhor = (l, c)

        return melhor, matriz
class Coordenada:
    def __init__(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna


class Ataque:
    def __init__(
        self,
        atacante,
        coordenada,
        resultado,
        tiros_atacante,
        tiros_defensor,
        pts_atacante,
        pts_defensor,
        matriz_probabilidade=None,
    ):
        self.atacante = atacante
        self.coordenada = coordenada
        self.resultado = resultado
        self.tiros_atacante = tiros_atacante
        self.tiros_defensor = tiros_defensor
        self.pts_atacante = pts_atacante
        self.pts_defensor = pts_defensor
        self.matriz_probabilidade = matriz_probabilidade


class Navio:
    def __init__(self, nome, tamanho, coordenadas):
        self.nome = nome
        self.tamanho = tamanho
        self.coordenadas = coordenadas
        self.acertos = 0

    @property
    def afundado(self):
        return self.acertos >= self.tamanho


class Tabuleiro:

    TAMANHO = 10

    def __init__(self):
        self.grelha = [
            ['🟦' for _ in range(self.TAMANHO)]
            for _ in range(self.TAMANHO)
        ]

    def limpar(self):
        for l in range(self.TAMANHO):
            for c in range(self.TAMANHO):
                self.grelha[l][c] = '🟦'

    def marcar_navio(self, coordenadas):
        for l, c in coordenadas:
            self.grelha[l][c] = 'N'

    def atacar(self, linha, coluna):

        atual = self.grelha[linha][coluna]

        if atual == 'N':
            self.grelha[linha][coluna] = '💥'
            return 'N'

        if atual == '🟦':
            self.grelha[linha][coluna] = '💦'
            return '🟦'

        return atual

    def ja_atacado(self, linha, coluna):
        return self.grelha[linha][coluna] in ('💥', '💦')


class Jogador:

    def __init__(self, nome, agente):

        self.nome = nome
        self.agente = agente
        self.tabuleiro = Tabuleiro()

        self.pontos = 0
        self.tiros = 0
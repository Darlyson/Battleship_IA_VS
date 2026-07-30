# models.py

class Coordenada:
    """Representa um ponto no tabuleiro."""
    def __init__(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna

class Ataque:
    """Registra o histórico e os dados de cada jogada para a interface gráfica."""
    def __init__(
        self, atacante, coordenada, resultado, tiros_atacante, 
        tiros_defensor, pts_atacante, pts_defensor, matriz_probabilidade=None
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
    """Modelo de um navio (atualmente gerenciado pelos dicionários no simulador)."""
    def __init__(self, nome, tamanho, coordenadas):
        self.nome = nome
        self.tamanho = tamanho
        self.coordenadas = coordenadas
        self.acertos = 0

    @property
    def afundado(self):
        return self.acertos >= self.tamanho

class Tabuleiro:
    """
    Representa a grelha física do jogo.
    Mantém o estado real (navios escondidos, água, acertos).
    """
    TAMANHO = 10

    def __init__(self):
        # Matriz 10x10 preenchida com água ('🟦')
        self.grelha = [['🟦' for _ in range(self.TAMANHO)] for _ in range(self.TAMANHO)]

    def limpar(self):
        for l in range(self.TAMANHO):
            for c in range(self.TAMANHO):
                self.grelha[l][c] = '🟦'

    def marcar_navio(self, coordenadas):
        # Coloca o caractere 'N' nas coordenadas indicadas
        for l, c in coordenadas:
            self.grelha[l][c] = 'N'

    def atacar(self, linha, coluna):
        """Muda o estado da célula com base no ataque e retorna o resultado."""
        atual = self.grelha[linha][coluna]

        if atual == 'N':
            self.grelha[linha][coluna] = '💥' # Acerto
            return 'N'

        if atual == '🟦':
            self.grelha[linha][coluna] = '💦' # Água
            return '🟦'

        return atual

    def ja_atacado(self, linha, coluna):
        # Evita que a mesma coordenada seja atacada duas vezes
        return self.grelha[linha][coluna] in ('💥', '💦')

class Jogador:
    """Unifica o Agente (Cérebro) e o Tabuleiro (Corpo) sob uma mesma entidade."""
    def __init__(self, nome, agente):
        self.nome = nome
        self.agente = agente
        self.tabuleiro = Tabuleiro()
        self.pontos = 0
        self.tiros = 0
# game.py
from models import Coordenada, Ataque

class SimuladorBatalha:
    def __init__(self, jogador1, jogador2, modo="padrao"):
        self.jogador1 = jogador1
        self.jogador2 = jogador2
        self.modo = modo

        self.mapa_pontos_ia1 = {}
        self.mapa_pontos_ia2 = {}
        self.mapa_id_navio_ia1 = {}
        self.mapa_id_navio_ia2 = {}
        
        self.vida_navios_ia1 = {}
        self.vida_navios_ia2 = {}
        self.tamanho_original_ia1 = {}
        self.tamanho_original_ia2 = {}

        self.log_jogadas = []

    def posicionar_navios(self):
        tamanhos_padrao = [5, 4, 3, 3, 2]

        # Posiciona frota do Jogador 1 (Alpha)
        frotas1 = self.jogador1.agente.posicionar_frota(tamanhos_padrao)
        id_navio = 0
        for navio in frotas1:
            tamanho, coords = navio if isinstance(navio, tuple) else (len(navio), navio)
            
            self.vida_navios_ia1[id_navio] = tamanho
            self.tamanho_original_ia1[id_navio] = tamanho
            
            # Delega para a classe Tabuleiro
            self.jogador1.tabuleiro.marcar_navio(coords)
            
            for l, c in coords:
                self.mapa_pontos_ia1[(l, c)] = tamanho * 10
                self.mapa_id_navio_ia1[(l, c)] = id_navio
            id_navio += 1

        # Posiciona frota do Jogador 2 (Beta)
        frotas2 = self.jogador2.agente.posicionar_frota(tamanhos_padrao)
        id_navio = 0
        for navio in frotas2:
            tamanho, coords = navio if isinstance(navio, tuple) else (len(navio), navio)
            
            self.vida_navios_ia2[id_navio] = tamanho
            self.tamanho_original_ia2[id_navio] = tamanho
            
            # Delega para a classe Tabuleiro
            self.jogador2.tabuleiro.marcar_navio(coords)
            
            for l, c in coords:
                self.mapa_pontos_ia2[(l, c)] = tamanho * 10
                self.mapa_id_navio_ia2[(l, c)] = id_navio
            id_navio += 1

        return len(self.mapa_pontos_ia1), len(self.mapa_pontos_ia2)

    def calcular_pontuacao_final(self, id_jogador):
        pontos_totais = 0
        vida_navios = self.vida_navios_ia2 if id_jogador == 1 else self.vida_navios_ia1
        tamanho_original = self.tamanho_original_ia2 if id_jogador == 1 else self.tamanho_original_ia1

        for k, vida in vida_navios.items():
            tamanho = tamanho_original[k]
            if vida == 0:
                valor_base = tamanho * 10
                pecas_atingidas = tamanho
                pontos_totais += ((valor_base * (tamanho + 1)) + pecas_atingidas)

        return pontos_totais

    def pre_calcular_batalha(self):
        qtd_navios_ia1, qtd_navios_ia2 = self.posicionar_navios()

        tiros_1 = qtd_navios_ia1 + 1 if self.modo == "profissional" else float('inf')
        tiros_2 = qtd_navios_ia2 + 1 if self.modo == "profissional" else float('inf')

        acertos_restantes_1 = 17
        acertos_restantes_2 = 17

        while acertos_restantes_1 > 0 and acertos_restantes_2 > 0:
            if self.modo == "profissional" and tiros_1 <= 0 and tiros_2 <= 0:
                break

            # ==========================
            # TURNO JOGADOR 1 (ALPHA)
            # ==========================
            if acertos_restantes_2 > 0 and (self.modo != "profissional" or tiros_1 > 0):
                # Alpha retorna tupla com a melhor jogada e a matriz de calor
                jogada, matriz_alpha = self.jogador1.agente.escolher_ataque()
                l1, c1 = jogada

                # Ataca o Tabuleiro do oponente (Jogador 2)
                resultado = self.jogador2.tabuleiro.atacar(l1, c1)
                acertou = (resultado == 'N')

                # Alimenta o radar do agente Alpha
                self.jogador1.agente.registrar_resultado(l1, c1, acertou)
                alvo_char = 'N' if acertou else '🟦'

                if acertou:
                    acertos_restantes_2 -= 1
                    id_nav = self.mapa_id_navio_ia2[(l1, c1)]
                    self.vida_navios_ia2[id_nav] -= 1
                    
                    if self.vida_navios_ia2[id_nav] == 0:
                        tamanho = self.tamanho_original_ia2[id_nav]
                        self.jogador1.agente.registrar_afundamento(tamanho)
                else:
                    if self.modo == "profissional":
                        tiros_1 -= 1

                ataque = Ataque(
                    self.jogador1.nome, Coordenada(l1, c1), alvo_char,
                    tiros_1, tiros_2, 0, 0, matriz_alpha
                )
                self.log_jogadas.append(ataque)

            if acertos_restantes_2 == 0:
                break

            # ==========================
            # TURNO JOGADOR 2 (BETA)
            # ==========================
            if acertos_restantes_1 > 0 and (self.modo != "profissional" or tiros_2 > 0):
                # Evita atirar na mesma coordenada através do método ja_atacado do Tabuleiro
                while True:
                    l2, c2 = self.jogador2.agente.escolher_ataque()
                    if not self.jogador1.tabuleiro.ja_atacado(l2, c2):
                        break

                # Ataca o Tabuleiro do oponente (Jogador 1)
                resultado = self.jogador1.tabuleiro.atacar(l2, c2)
                acertou = (resultado == 'N')

                # Alimenta o radar do agente Beta (Beta recebe a coordenada como tupla)
                self.jogador2.agente.registrar_resultado((l2, c2), acertou)
                alvo_char = 'N' if acertou else '🟦'

                if acertou:
                    acertos_restantes_1 -= 1
                    id_nav = self.mapa_id_navio_ia1[(l2, c2)]
                    self.vida_navios_ia1[id_nav] -= 1
                    
                    if self.vida_navios_ia1[id_nav] == 0:
                        tamanho = self.tamanho_original_ia1[id_nav]
                        self.jogador2.agente.registrar_afundamento(tamanho)
                else:
                    if self.modo == "profissional":
                        tiros_2 -= 1

                ataque = Ataque(
                    self.jogador2.nome, Coordenada(l2, c2), alvo_char,
                    tiros_1, tiros_2, 0, 0, None
                )
                self.log_jogadas.append(ataque)

        return self.log_jogadas
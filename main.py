# main.py
from models import Jogador
from ai import AgenteAlpha, AgenteHeuristico
from game import SimuladorBatalha
from gui import VisualizadorBatalha
import tkinter as tk

def iniciar_jogo():
    print("========================================")
    print("CONFIGURAÇÃO DA BATALHA NAVAL IA")
    print("========================================")
    print("1 - Modo Padrão (Tiros Infinitos)")
    print("2 - Modo Profissional (Tiros Limitados)")
    
    escolha = input("Selecione o modo (1 ou 2): ").strip()
    modo = "profissional" if escolha == "2" else "padrao"

    # ==========================================
    # NOVA ARQUITETURA DE DEPENDÊNCIAS
    # IA ➔ Agente ➔ Jogador ➔ Tabuleiro
    # ==========================================
    
    # 1. Instanciar os Agentes
    agente_alpha = AgenteAlpha(profundidade=2)
    agente_beta = AgenteHeuristico()
    
    # 2. Injetar os Agentes nos Jogadores (o Tabuleiro é gerado internamente)
    jogador_alpha = Jogador("IA Alpha (Minimax)", agente_alpha)
    jogador_beta = Jogador("IA Beta (Heurística)", agente_beta)

    # 3. Passar os Jogadores completos para o simulador
    simulacao = SimuladorBatalha(jogador_alpha, jogador_beta, modo=modo)

    root = tk.Tk()
    app = VisualizadorBatalha(root, simulacao)
    root.mainloop()

if __name__ == "__main__":
    iniciar_jogo()
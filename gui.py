# gui.py
import tkinter as tk

class VisualizadorBatalha:
    def __init__(self, master, simulacao):
        self.master = master
        self.master.title(f"Batalha Naval Inteligente - Modo {simulacao.modo.capitalize()}")
        self.master.geometry("1400x850") 
        self.master.configure(bg="#2C3E50")
        
        self.simulacao = simulacao
        self.log_jogadas = simulacao.pre_calcular_batalha()
        self.passo_atual = 0

        self.navios_iniciais = [5, 4, 3, 3, 2]
        self.navios_ativos_alpha = list(self.navios_iniciais)
        self.navios_ativos_beta = list(self.navios_iniciais)

        self.frame_top = tk.Frame(master, bg="#2C3E50")
        self.frame_top.pack(pady=10)
        
        self.lbl_status = tk.Label(self.frame_top, text="Fase de Preparação!", 
                                   font=("Arial", 14, "bold"), bg="#2C3E50", fg="#F1C40F")
        self.lbl_status.pack()

        self.frame_botoes = tk.Frame(self.frame_top, bg="#2C3E50")
        self.frame_botoes.pack(pady=8)

        self.btn_avancar = tk.Button(self.frame_botoes, text="Avançar Turno ⏩", 
                                     command=self.avancar_animacao, font=("Arial", 11, "bold"), 
                                     bg="#27AE60", fg="white", activebackground="#2ECC71", state="disabled")
        self.btn_avancar.pack(side="left", padx=5)

        self.btn_resultado = tk.Button(self.frame_botoes, text="Ir ao Resultado ⚡", 
                                       command=self.ir_para_resultado, font=("Arial", 11, "bold"), 
                                       bg="#E67E22", fg="white", activebackground="#D35400", state="disabled")
        self.btn_resultado.pack(side="left", padx=5)

        self.frame_boards = tk.Frame(master, bg="#2C3E50")
        self.frame_boards.pack(pady=5)

        # ==========================================================
        # PAINEL DA IA ALPHA (Esquerda)
        # ==========================================================
        self.container_ia1 = tk.LabelFrame(self.frame_boards, text=f" {simulacao.jogador1.nome} ", 
                                            font=("Arial", 13, "bold"), bg="#2C3E50", fg="#3498DB", bd=3, relief="groove")
        self.container_ia1.grid(row=0, column=0, padx=15, ipadx=10, ipady=5)
        
        self.lbl_stats_ia1 = tk.Label(self.container_ia1, text="Pontos: [Revelado ao Fim]", font=("Arial", 11, "bold"), bg="#2C3E50", fg="#F1C40F")
        self.lbl_stats_ia1.pack(pady=2)

        self.lbl_frota_ia1 = tk.Label(self.container_ia1, text=f"Navios em Jogo: {self.navios_ativos_alpha}", font=("Arial", 10), bg="#2C3E50", fg="#ECF0F1")
        self.lbl_frota_ia1.pack(pady=2)

        sub_ia1 = tk.Frame(self.container_ia1, bg="#2C3E50")
        sub_ia1.pack()

        f_frota1 = tk.Frame(sub_ia1, bg="#2C3E50")
        f_frota1.pack(side="left", padx=10)
        tk.Label(f_frota1, text="[ SUA FROTA ]", font=("Arial", 10, "bold"), bg="#2C3E50", fg="white").pack()
        self.botoes_frota_ia1 = self.criar_grelha(f_frota1, simulacao.mapa_pontos_ia1, revelar_navios=True)

        f_radar1 = tk.Frame(sub_ia1, bg="#2C3E50")
        f_radar1.pack(side="left", padx=10)
        tk.Label(f_radar1, text="[ RADAR DE ATAQUE ]", font=("Arial", 10, "bold"), bg="#2C3E50", fg="white").pack()
        self.botoes_radar_ia1 = self.criar_grelha(f_radar1, {}, revelar_navios=False)


        # ==========================================================
        # PAINEL DA IA BETA (Direita)
        # ==========================================================
        self.container_ia2 = tk.LabelFrame(self.frame_boards, text=f" {simulacao.jogador2.nome} ", 
                                            font=("Arial", 13, "bold"), bg="#2C3E50", fg="#E74C3C", bd=3, relief="groove")
        self.container_ia2.grid(row=0, column=1, padx=15, ipadx=10, ipady=5)
        
        self.lbl_stats_ia2 = tk.Label(self.container_ia2, text="Pontos: [Revelado ao Fim]", font=("Arial", 11, "bold"), bg="#2C3E50", fg="#F1C40F")
        self.lbl_stats_ia2.pack(pady=2)

        self.lbl_frota_ia2 = tk.Label(self.container_ia2, text=f"Navios em Jogo: {self.navios_ativos_beta}", font=("Arial", 10), bg="#2C3E50", fg="#ECF0F1")
        self.lbl_frota_ia2.pack(pady=2)

        sub_ia2 = tk.Frame(self.container_ia2, bg="#2C3E50")
        sub_ia2.pack()

        f_frota2 = tk.Frame(sub_ia2, bg="#2C3E50")
        f_frota2.pack(side="left", padx=10)
        tk.Label(f_frota2, text="[ SUA FROTA ]", font=("Arial", 10, "bold"), bg="#2C3E50", fg="white").pack()
        self.botoes_frota_ia2 = self.criar_grelha(f_frota2, simulacao.mapa_pontos_ia2, revelar_navios=True)

        f_radar2 = tk.Frame(sub_ia2, bg="#2C3E50")
        f_radar2.pack(side="left", padx=10)
        tk.Label(f_radar2, text="[ RADAR DE ATAQUE ]", font=("Arial", 10, "bold"), bg="#2C3E50", fg="white").pack()
        self.botoes_radar_ia2 = self.criar_grelha(f_radar2, {}, revelar_navios=False)

        self.tempo_restante = 5
        self.iniciar_contagem()

    def criar_grelha(self, container, mapa_pontos_iniciais, revelar_navios):
        frame_grelha = tk.Frame(container, bg="#34495E", bd=2, relief="solid")
        frame_grelha.pack(pady=5)
        botoes = []
        for linha in range(10):
            linha_btn = []
            for coluna in range(10):
                tem_navio = (linha, coluna) in mapa_pontos_iniciais
                
                if revelar_navios and tem_navio:
                    texto_btn = "🚢"
                    cor_fundo = "#F1C40F" 
                else:
                    texto_btn = "🟦"
                    cor_fundo = "#2980B9"
                
                btn = tk.Button(frame_grelha, text=texto_btn, width=2, height=1, 
                                font=("Arial", 10, "bold"), bg=cor_fundo, state="disabled", 
                                disabledforeground="black")
                btn.grid(row=linha, column=coluna, padx=1, pady=1)
                linha_btn.append(btn)
            botoes.append(linha_btn)
        return botoes

    def iniciar_contagem(self):
        if self.tempo_restante > 0:
            self.lbl_status.config(text=f"Memorize as frotas em 'Sua Frota'! Escondendo em {self.tempo_restante}s...")
            self.tempo_restante -= 1
            self.master.after(1000, self.iniciar_contagem)
        else:
            self.esconder_frotas()

    def esconder_frotas(self):
        for l in range(10):
            for c in range(10):
                self.botoes_frota_ia1[l][c].configure(text="🟦", bg="#2980B9")
                self.botoes_frota_ia2[l][c].configure(text="🟦", bg="#2980B9")
                
        self.lbl_status.config(text="A Batalha Começou! Pode avançar os turnos.", fg="white")
        self.btn_avancar.config(state="normal") 
        self.btn_resultado.config(state="normal")

    def processar_passo(self, ataque):
        atacante = ataque.atacante
        linha = ataque.coordenada.linha
        coluna = ataque.coordenada.coluna
        resultado = ataque.resultado
        
        if self.simulacao.jogador1.nome in atacante:
            btn_radar_atacante = self.botoes_radar_ia1[linha][coluna]
            btn_frota_alvo = self.botoes_frota_ia2[linha][coluna]
            
            if ataque.matriz_probabilidade:
                for r in range(10):
                    for c in range(10):
                        b_radar = self.botoes_radar_ia1[r][c]
                        if b_radar.cget("text") not in ["💥", "💦"]:
                            val = ataque.matriz_probabilidade[r][c]
                            b_radar.configure(text=str(val) if val > 0 else "🟦", disabledforeground="black")
        else:
            btn_radar_atacante = self.botoes_radar_ia2[linha][coluna]
            btn_frota_alvo = self.botoes_frota_ia1[linha][coluna]

        if resultado == 'N':
            btn_radar_atacante.configure(text="💥", bg="#E74C3C", disabledforeground="white") 
            btn_frota_alvo.configure(text="💥", bg="#E74C3C", disabledforeground="white") 
        else:
            btn_radar_atacante.configure(text="💦", bg="#7F8C8D", disabledforeground="white") 
            btn_frota_alvo.configure(text="💦", bg="#7F8C8D", disabledforeground="white") 

        for k, vida in self.simulacao.vida_navios_ia2.items():
            if vida == 0:
                tamanho = self.simulacao.tamanho_original_ia2[k]
                if tamanho in self.navios_ativos_beta:
                    self.navios_ativos_beta.remove(tamanho)
        for k, vida in self.simulacao.vida_navios_ia1.items():
            if vida == 0:
                tamanho = self.simulacao.tamanho_original_ia1[k]
                if tamanho in self.navios_ativos_alpha:
                    self.navios_ativos_alpha.remove(tamanho)

        self.lbl_frota_ia1.config(text=f"Em jogo: {self.navios_ativos_alpha} | Afundados: {[n for n in self.navios_iniciais if n not in self.navios_ativos_alpha]}")
        self.lbl_frota_ia2.config(text=f"Em jogo: {self.navios_ativos_beta} | Afundados: {[n for n in self.navios_iniciais if n not in self.navios_ativos_beta]}")

    def avancar_animacao(self):
        if self.passo_atual < len(self.log_jogadas):
            ataque = self.log_jogadas[self.passo_atual]
            self.processar_passo(ataque)
            
            atacante = ataque.atacante
            texto_res = "ACERTOU O NAVIO!" if ataque.resultado == 'N' else "Água."
            self.lbl_status.config(text=f"{atacante} ataca ({ataque.coordenada.linha},{ataque.coordenada.coluna}) ➔ {texto_res}", fg="white")
            
            self.passo_atual += 1
            
            if self.passo_atual == len(self.log_jogadas):
                self.anunciar_vencedor()

    def ir_para_resultado(self):
        while self.passo_atual < len(self.log_jogadas):
            ataque = self.log_jogadas[self.passo_atual]
            self.processar_passo(ataque)
            self.passo_atual += 1
            
        self.anunciar_vencedor()

    def anunciar_vencedor(self):
        self.btn_avancar.config(state="disabled")
        self.btn_resultado.config(state="disabled")
        
        p_alpha = self.simulacao.calcular_pontuacao_final(1)
        p_beta = self.simulacao.calcular_pontuacao_final(2)
        
        self.lbl_stats_ia1.config(text=f"Pontos Finais: {p_alpha}")
        self.lbl_stats_ia2.config(text=f"Pontos Finais: {p_beta}")
        
        vencedor = "EMPATE!"
        if p_alpha > p_beta:
            vencedor = f"🏆 {self.simulacao.jogador1.nome} Venceu!"
        elif p_beta > p_alpha:
            vencedor = f"🏆 {self.simulacao.jogador2.nome} Venceu!"
            
        self.lbl_status.config(text=f"FIM DE JOGO: {vencedor} (Alpha: {p_alpha} pts | Beta: {p_beta} pts)", fg="#2ECC71", font=("Arial", 13, "bold"))
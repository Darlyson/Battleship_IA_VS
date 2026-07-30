# 🚢 Batalha Naval Inteligente (AI vs AI)

Um simulador interativo e visual de Batalha Naval desenvolvido em Python, onde o combate não ocorre entre humanos, mas sim entre **duas Inteligências Artificiais** com abordagens algorítmicas completamente diferentes. 

O projeto foi construído utilizando **Programação Orientada a Objetos (POO)** para garantir uma arquitetura limpa, separando a interface visual (`Tkinter`) da lógica de negócios e dos motores cognitivos das IAs.

![Fase de Preparação do Jogo](image_bbdf58.png)
*Tela inicial de memorização das frotas antes do combate.*

---

## 🧠 Os Algoritmos (As Inteligências)

O projeto coloca frente a frente duas abordagens clássicas da Ciência da Computação:

### 1. IA Alpha (Minimax com Poda Alfa-Beta + Matriz de Calor)
A IA Alpha joga de forma puramente matemática e preditiva:
* **Matriz de Densidade de Probabilidade:** Avalia constantemente o tabuleiro (radar) para calcular em quais células é mais provável que os navios inimigos restantes caibam. 
* **Árvore Minimax:** Antes de atirar, ela simula jogadas futuras. Ela tenta encontrar o movimento que *Maximiza* sua vantagem enquanto *Minimiza* as chances de erro no turno seguinte.
* **Poda Alfa-Beta:** Otimiza o algoritmo descartando simulações ("galhos" da árvore de decisão) que já se provaram ineficientes, poupando processamento computacional.

### 2. IA Beta (Busca Heurística - *Hunt and Target*)
A IA Beta joga simulando o raciocínio humano clássico:
* **Hunt (Caça):** Realiza disparos aleatórios pelas coordenadas ainda não atacadas do tabuleiro.
* **Target (Alvo):** Assim que acerta uma peça de navio, ela abandona a aleatoriedade e empilha as coordenadas vizinhas (ortogonais: cima, baixo, esquerda, direita) em uma estrutura de Pilha (*Stack*). Nos próximos turnos, ela dispara nestes vizinhos até afundar o alvo, para então voltar ao modo de caça.

---

## 🏗️ Arquitetura do Projeto

O código foi refatorado para garantir alta coesão e baixo acoplamento. A hierarquia de dependências funciona da seguinte forma:

`IA (Agente) ➔ Jogador ➔ Tabuleiro ➔ Motor de Jogo ➔ Interface Gráfica`

* **`models.py`**: Define as entidades base do jogo (`Jogador`, `Tabuleiro`, `Navio`, `Ataque`, `Coordenada`).
* **`ai.py`**: Contém o cérebro matemático dos agentes (`AgenteAlpha` e `AgenteHeuristico`).
* **`game.py`**: Simulador do jogo (regras, cálculo de danos, controle de turnos).
* **`gui.py`**: Interface gráfica responsiva construída em Tkinter.
* **`main.py`**: Ponto de entrada, responsável pela injeção de dependências e configuração do modo de jogo.

---

## 🎮 Modos de Jogo e Pontuação

Ao iniciar o programa via terminal, é possível escolher entre dois modos de jogo:
1. **Modo Padrão:** Tiros infinitos até que uma frota seja totalmente destruída.
2. **Modo Profissional:** Munição limitada baseada no número de embarcações iniciais.

### Cálculo de Pontos
No final da partida, os pontos são calculados rigorosamente baseados no desempenho, sendo a fórmula definida por:

$ \text{Pontos} = (\text{Valor Base} \times (\text{Tamanho} + 1)) + \text{Peças Atingidas} $

* **Navios totalmente afundados:** Recebem o bônus total de afundamento.
* **Navios parcialmente atingidos:** No modo Profissional, caso a munição acabe, as IAs recebem os pontos equivalentes ao número de peças avariadas. A pontuação máxima perfeita (destruição total) é de **800 pontos**.

---

## 🚀 Como Executar

**Pré-requisitos:**
* Python 3.x instalado na máquina.

**Passo a passo:**
1. Clone este repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
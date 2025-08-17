# Forest Adventure

`Forest Adventure` é um jogo de plataforma 2D desenvolvido em Python com a biblioteca Pygame Zero. O jogador controla um herói que deve derrotar inimigos em uma floresta misteriosa para avançar por diferentes fases.

## 📜 Sobre o Jogo

Este projeto foi desenvolvido como uma demonstração de habilidades em Python e na criação de jogos, seguindo um conjunto específico de requisitos técnicos. O jogo apresenta mecânicas clássicas de plataforma, incluindo movimentação lateral, pulos, combate com projéteis e inimigos com comportamento de patrulha e perseguição.

O objetivo é simples: sobreviver, derrotar todos os inimigos da fase e avançar até a vitória final!

## ✨ Funcionalidades

- **Menu Principal Completo**: Um menu inicial com opções para Iniciar Jogo, Ligar/Desligar Música e Sair.
- **Sistema de Fases**: O jogo é dividido em fases, com um número crescente de inimigos a serem derrotados para avançar.
- **Combate com Projéteis**: O jogador pode atirar para derrotar os inimigos à distância.
- **Inimigos com IA Simples**: Os inimigos patrulham uma área específica e começam a perseguir o jogador quando ele se aproxima.
- **Animações de Sprite**: Animações de quadro a quadro para o jogador e inimigos, incluindo estados de "parado" (idle), "correndo" (run) e "pulando" (jump).
- **Física Básica**: O jogo implementa gravidade, pulos e detecção de colisões.
- **Áudio Imersivo**: Música de fundo que pode ser ligada ou desligada e efeitos sonoros para ações como pular, atirar e receber dano.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído utilizando apenas as bibliotecas permitidas pelos requisitos:

- **Python 3**
- **Pygame Zero**

Nenhuma outra biblioteca externa é necessária para a execução do jogo.

## 🚀 Como Executar o Jogo

Para jogar, siga os passos abaixo:

1.  **Pré-requisitos**: Certifique-se de ter o Python 3 instalado em seu sistema.

2.  **Instale o Pygame Zero**: Abra seu terminal ou prompt de comando e execute o seguinte comando:

    ```bash
    pip install pgzero
    ```

3.  **Clone ou Baixe o Projeto**: Baixe os arquivos do projeto para o seu computador.

4.  **Estrutura de Pastas**: Certifique-se de que os assets (recursos como imagens, sons e músicas) estão organizados nas pastas corretas, como o Pygame Zero exige:

    ```
    forest-adventure/
    ├── game.py
    ├── characters.py
    ├── images/
    │   ├── player/
    │   └── enemy/
    ├── music/
    └── sounds/
    ```

5.  **Execute o Jogo**: Navegue até o diretório principal do projeto pelo terminal e execute o seguinte comando:
    ```bash
    pgzrun game.py
    ```

## 🎮 Controles

| Tecla               | Ação                  |
| ------------------- | --------------------- |
| **A**               | Mover para a esquerda |
| **D**               | Mover para a direita  |
| **Barra de Espaço** | Pular                 |
| **K**               | Atirar                |
| **ESC**             | Pausar / Retomar      |
| **Mouse**           | Interagir com o menu  |

## 📁 Estrutura do Projeto

- `game.py`: Arquivo principal que contém o loop do jogo, gerenciamento de estados (menu, jogando, game over), e a lógica geral.
- `characters.py`: Define as classes `Character`, `Player` e `Enemy`, controlando o comportamento, a física e a animação dos personagens.
- `images/`: Pasta que contém imagens usadas no jogo, como personagens, backgrounds, etc.
- `music/`: Contém os arquivos de música de fundo.
- `sounds/`: Contém os arquivos de efeitos sonoros.

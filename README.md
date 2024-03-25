# Solver de Cubo Mágico

Este projeto é uma implementação em Python de um solver para o Cubo Mágico, desenvolvido como parte de um projeto de extensão na universidade. Ele utiliza o algoritmo de Kociemba para encontrar uma solução com uma quantidade mínima de movimentos.

## Características

- **Linguagem**: Python
- **Algoritmo de Resolução**: Kociemba
- **Funcionalidades**:
  - Mostra a solução do Cubo Mágico ao preencher a projeção de um cubo com as cores.
  - Encontra uma solução com uma quantidade de movimentos próxima ao "número de Deus".
  - Facilidade de uso através de uma interface em kivy.
  
## Algoritmo de Kociemba

O algoritmo de Kociemba reduz o cubo a um estado que requer apenas movimentações duplas exceto em duas camadas opostas, "transformando" o cubo em um 3x3x2, e depois resolve o cubo com um máximo de 29 movimentos.

## Número de Deus

O "número de Deus" é uma métrica que se refere à quantidade máxima de movimentos necessários para resolver qualquer configuração do Cubo Mágico, independentemente de como ele esteja embaralhado. Estudos matemáticos demonstraram que o número de Deus é 20.

## Como Rodar o Código

1. Clone o repositório do projeto:
   ```bash
   git clone https://github.com/ffneiva/cubo-extensao.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd cubo-extensao
   ```

3. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o código principal para executar o programa:
   ```bash
   python main.py
   ```
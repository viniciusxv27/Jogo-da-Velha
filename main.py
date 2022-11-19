# começaremos impotando o módulo pygame
import pygame
from pygame.locals import *

# inicializando o pygame
pygame.init()

# setando a resolução da tela
largura = 300
altura = 300

# criando a tela
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Velha")

# setando algumas variaveis
largura_linha = 8
marcadores = []
clicado = False
pos = []
jogador = 1
vencedor = 0
fim_de_jogo = False

# criando o retângulo de jogar novamente
botao_jogar_novamente = Rect(largura // 2 - 80, altura // 2, 160, 50)


# desenhando o tabuleiro
def desenha_tabuleiro(tela):
    background = (0, 0, 0)  # cor de fundo -> utilizamos o código RGB
    linhas = (255, 128, 0)  # cor das linhas -> utilizamos o código RGB
    tela.fill(background)

    for x in range(1, 3):
        # desenhando as linhas horizontais
        pygame.draw.line(tela, linhas, (0, 100 * x), (largura, 100 * x), largura_linha)
        # desenhando as linhas verticais
        pygame.draw.line(tela, linhas, (100 * x, 0), (100 * x, altura), largura_linha)


for x in range(3):
    linha = [0] * 3  # criando uma lista de linha com 3 zeros
    marcadores.append(linha)  # adicionando a linha criada na lista de marcadores


# desenhando os marcadores
def desenha_marcador(tela):
    x_pos = 0
    for x in marcadores:
        y_pos = 0
        for y in x:
            if y == 1:
                # desenhando o marcador do jogador 1 (X)
                pygame.draw.line(tela, (255, 0, 0), (x_pos * 100 + 15, y_pos * 100 + 15),
                                 (x_pos * 100 + 85, y_pos * 100 + 85), largura_linha)
                pygame.draw.line(tela, (255, 0, 0), (x_pos * 100 + 85, y_pos * 100 + 15),
                                 (x_pos * 100 + 15, y_pos * 100 + 85), largura_linha)
            if y == -1:
                # desenhando o marcador do jogador 2 (O)
                pygame.draw.circle(tela, (0, 0, 255), (x_pos * 100 + 50, y_pos * 100 + 50), 38, largura_linha)
            y_pos += 1
        x_pos += 1


# Função que checa o vencedor
def checa_vencedor():
    global vencedor
    global fim_de_jogo

    y_pos = 0
    for x in marcadores:
        # checando as colunas para o jogador 1
        if sum(x) == 3:
            vencedor = 1
            fim_de_jogo = True

        # checando as colunas para o jogador 2
        if sum(x) == -3:
            vencedor = 2
            fim_de_jogo = True

        # checando as linhas para o jogador 1
        if marcadores[0][y_pos] + marcadores[1][y_pos] + marcadores[2][y_pos] == 3:
            vencedor = 1
            fim_de_jogo = True

        # checando as linhas para o jogador 2
        if marcadores[0][y_pos] + marcadores[1][y_pos] + marcadores[2][y_pos] == -3:
            vencedor = 2
            fim_de_jogo = True
        y_pos += 1

    # checando as diagonais para o jogador 1
    if marcadores[0][0] + marcadores[1][1] + marcadores[2][2] == 3 or marcadores[0][2] + marcadores[1][1] + \
            marcadores[2][0] == 3:
        vencedor = 1
        fim_de_jogo = True

    # checando as diagonais para o jogador 2
    if marcadores[0][0] + marcadores[1][1] + marcadores[2][2] == -3 or marcadores[0][2] + marcadores[1][1] + \
            marcadores[2][0] == -3:
        vencedor = 2
        fim_de_jogo = True

    # checando empate
    if fim_de_jogo == False:
        empate = True
        for linha in marcadores:
            for i in linha:
                if i == 0:
                    empate = False

        if empate == True:
            vencedor = 0
            fim_de_jogo = True


# Função que anuncia o vencedor
def anuncia_vencedor(tela, vencedor):
    # definindo o texto que será impresso na tela
    if vencedor != 0:
        texto_vencedor = '  Jogador ' + str(vencedor) + ' venceu!'
    elif vencedor == 0:
        texto_vencedor = "        Deu Velha!"

    # selecionando a fonte
    fonte = pygame.font.SysFont('Roboto', 30)
    # convertendo o texto para imagem
    texto_imagem = fonte.render(texto_vencedor, True, (255, 255, 255))
    # para ter um contraste com o plano de fundo, vamos adicionar um retângulo
    pygame.draw.rect(tela, (0, 200, 0), (largura // 2 - 100, altura // 2 - 60, 200, 50))
    tela.blit(texto_imagem, (largura // 2 - 100, altura // 2 - 50))

    # definindo o texto que pergunta se queremos jogar de novo
    texto_pergunta = '  Recomeçar?'
    # transformando o texto para imagem
    imagem_recomecar = fonte.render(texto_pergunta, True, (255, 255, 255))
    # cria o botão de recomeçar
    pygame.draw.rect(tela, (0, 200, 0), botao_jogar_novamente)
    tela.blit(imagem_recomecar, (largura // 2 - 80, altura // 2 + 10))


# criando o game loop
jogo = True

while jogo:

    desenha_tabuleiro(tela)
    desenha_marcador(tela)

    # cirando os eventos(event)
    for event in pygame.event.get():
        # evento de fechar a tela
        if event.type == QUIT:
            jogo = False

        if fim_de_jogo == 0:
            # evento de clique do mouse
            if event.type == MOUSEBUTTONDOWN and clicado == False:
                clicado = True
            if event.type == MOUSEBUTTONUP and clicado == True:
                clicado = False
                # pegando a posição do mouse
                pos = pygame.mouse.get_pos()
                # Agora vamos extrair a posição x e y do mouse
                pos_x = pos[0]
                pos_y = pos[1]

                if marcadores[pos_x // 100][pos_y // (100)] == 0:
                    # turno do jogador 1
                    marcadores[pos_x // (100)][pos_y // (100)] = jogador
                    # mudando para o turno do jogador 2
                    jogador *= -1
                    checa_vencedor()

    # definindo o vencedor
        if fim_de_jogo == True:
            anuncia_vencedor(tela, vencedor)
            # checando se o jogador clicou em jogar novamente
            if event.type == MOUSEBUTTONDOWN and clicado == False:
                clicado = True
            if event.type == MOUSEBUTTONUP and clicado == True:
                clicado = False
                pos = pygame.mouse.get_pos()
                if botao_jogar_novamente.collidepoint(pos):
                    # reiniciando o jogo
                    fim_de_jogo = False
                    jogador = 1
                    vencedor = 0
                    marcadores = []
                    pos = (0, 0)
                    for x in range(3):
                        linha = [0] * 3
                        marcadores.append(linha)

        pygame.display.update()

pygame.quit()
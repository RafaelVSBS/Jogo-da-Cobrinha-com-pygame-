import pygame
import time
import random

pygame.init()

largura = 600
altura = 400
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Cobrinha")

cores = {
    'branco': (255, 255, 255),
    'verde': (120, 196, 137),
    'preto': (0, 0, 0),
    'vermelho': (235, 81, 93)
}

clock = pygame.time.Clock()
velocidade = 5
tamanho_bloco = 20

fonte = pygame.font.SysFont(None, 35)

def mostrar_pontuacao(pontos):
    texto = fonte.render(f"Pontos: {pontos}", True, cores['preto'])
    tela.blit(texto, [10, 10])

def jogo():
    x = largura // 2
    y = altura // 2

    # Começa se movendo (evita bug)
    x_mudanca = tamanho_bloco
    y_mudanca = 0

    cobra = []
    comprimento_cobra = 1

    comida_x = round(random.randrange(0, largura - tamanho_bloco) / 20) * 20
    comida_y = round(random.randrange(0, altura - tamanho_bloco) / 20) * 20

    fim_de_jogo = False

    while not fim_de_jogo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_de_jogo = True

            if evento.type == pygame.KEYDOWN:
                # Impede virar 180°
                if evento.key == pygame.K_LEFT and x_mudanca == 0:
                    x_mudanca = -tamanho_bloco
                    y_mudanca = 0
                elif evento.key == pygame.K_RIGHT and x_mudanca == 0:
                    x_mudanca = tamanho_bloco
                    y_mudanca = 0
                elif evento.key == pygame.K_UP and y_mudanca == 0:
                    y_mudanca = -tamanho_bloco
                    x_mudanca = 0
                elif evento.key == pygame.K_DOWN and y_mudanca == 0:
                    y_mudanca = tamanho_bloco
                    x_mudanca = 0

        x += x_mudanca
        y += y_mudanca

        # Colisão com borda
        if x >= largura or x < 0 or y >= altura or y < 0:
            fim_de_jogo = True

        tela.fill(cores['branco'])

        # Desenha comida
        pygame.draw.rect(tela, cores['vermelho'], [comida_x, comida_y, tamanho_bloco, tamanho_bloco])

        # Cabeça da cobra
        cabeca = [x, y]
        cobra.append(cabeca)

        # Mantém tamanho correto
        if len(cobra) > comprimento_cobra:
            del cobra[0]

        # Colisão com o próprio corpo (corrigido)
        if cabeca in cobra[:-1]:
            fim_de_jogo = True

        # Desenha cobra
        for bloco in cobra:
            pygame.draw.rect(tela, cores['verde'], [bloco[0], bloco[1], tamanho_bloco, tamanho_bloco])

        mostrar_pontuacao(comprimento_cobra - 1)

        pygame.display.update()

        # Comer comida
        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, largura - tamanho_bloco) / 20) * 20
            comida_y = round(random.randrange(0, altura - tamanho_bloco) / 20) * 20
            comprimento_cobra += 1

        clock.tick(velocidade)

    # Tela de game over
    tela.fill(cores['branco'])
    texto = fonte.render(f"GAME OVER! Pontos: {comprimento_cobra - 1}", True, cores['vermelho'])
    tela.blit(texto, [largura / 6, altura / 3])
    pygame.display.update()
    time.sleep(3)

    pygame.quit()

jogo()
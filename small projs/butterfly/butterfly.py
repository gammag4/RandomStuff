import pygame
import math

from pygame.locals import *#contem todas as funcoes

from sys import exit #fechar janela

#incicializar as funcoes
pygame.init()

#criar janela
largura = 700
altura = 700

meio = (largura / 2, altura / 2)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo')

#loop infinito

def get_y(x, a):
    b = 1 / a
    return (abs(1 - (1 - (a * x) ** (2 * b)) ** (1.5 - b)) ** (0.5 + b)) * b

def get_radius(i, div):
    return 1 / (1 - i / (2 * div))

def draw_wing(i, div, size, xsig, ysig):
    a = get_radius(i, div)
    stop = math.ceil(size / a) + 1
    step = math.floor(size / div)

    for k in range(0, stop, step):
        k2 = k / size
        m = math.ceil(get_y(k2 ** 0.8, a) * size)
        n = size * k2 ** 0.8
        pos1 = (largura / 2 + n * xsig, altura / 2 + m * ysig)
        pos2 = (largura / 2 + m * xsig, altura / 2 + n * ysig)

        blue = 255 * math.cos(math.pi * m / (2 * size)) * math.cos(math.pi * n / (2 * stop))

        color = (255 * k2, 255, abs(blue))
        radius = (k + size) / 15

        pygame.draw.circle(tela, color, pos1, radius)
        pygame.draw.circle(tela, color, pos2, radius)

    if i < div:
        draw_wing(i + 1, div, size, xsig, ysig)

def get_y2(x, a):
    return a * (x * x - 1)

def draw_body(i, div, size):
    a = get_radius(i, div)
    c = i / div
    stop = math.ceil(size / a) + 1
    step = math.floor(size / div)

    for k in range(0, stop, step):
        k2 = k / size
        m = ((2 * k2 * (3 * c + 1) - 1) ** 2 - 1) * (1 - c) * size / 20
        n = k - size / 4 - c * size / 2
        pos1 = (largura / 2 + m, altura / 2 + n)
        pos2 = (largura / 2 - m, altura / 2 + n)

        blue = 255 * math.cos(math.pi * m / (2 * size)) * math.cos(math.pi * n / (2 * stop))

        color = (255 * (1 - k2), 100, 255)
        radius = (k + size) / 12

        pygame.draw.circle(tela, color, pos1, radius)
        pygame.draw.circle(tela, color, pos2, radius)

    if i < div:
        draw_body(i + 1, div, size)

def draw_antenna(div, size):
    for i in range(div + 1):
        j = i / div
        x = j * j * size * 0.2
        y = -size * 0.8 -j * size * 0.2

        pos1 = (x + largura / 2, y + altura / 2)
        pos2 = (-x + largura / 2, y + altura / 2)

        color = (255 - 100 * i / div, 100 + 155 * i / div, 255 - 100 * i / div)
        radius = size * i / (div * 80) + size / 60

        pygame.draw.circle(tela, color, pos1, radius)
        pygame.draw.circle(tela, color, pos2, radius)

def draw_butterfly(div, size):
    draw_wing(0, div, size * 0.8, 1, 1)
    draw_wing(0, div, size, 1, -1)
    draw_wing(0, div, size * 0.8, -1, 1)
    draw_wing(0, div, size, -1, -1)

    draw_body(0, div, size)

    draw_antenna(div, size)

while True:
    #for para checar eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    draw_butterfly(50, 250)

    pygame.display.update()

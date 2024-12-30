import pygame
import sys
import random
from pygame.locals import *

# Inicialização do pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Hockey")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Configurações do jogo
FPS = 60
clock = pygame.time.Clock()

# Elementos do jogo
PUSHER_RADIUS = 40
PUCK_RADIUS = 20

# Definição das áreas de gol
GOAL_WIDTH = 20  # Largura do gol na lateral
GOAL_HEIGHT = HEIGHT // 4  # Altura do gol
GOAL_CENTER = HEIGHT // 2  # Posição central do gol
GOAL_TOP = GOAL_CENTER - GOAL_HEIGHT // 2  # Topo do gol
GOAL_BOTTOM = GOAL_CENTER + GOAL_HEIGHT // 2  # Base do gol

# Inicializações
pusher1_pos = [150, HEIGHT // 2]
pusher2_pos = [WIDTH - 150, HEIGHT // 2]
puck_pos = [WIDTH // 2, HEIGHT // 2]
puck_velocity = [random.choice([-10, 10]), random.choice([-10, 10])]

pusher1_speed = 6
pusher2_speed = 6

# Pontuação
score1 = 0
score2 = 0

# Timer
start_ticks = pygame.time.get_ticks()
game_duration = 180  # 3 minutos em segundos

# Função para exibir texto na tela
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Função para resetar a posição inicial do disco
def reset_puck():
    puck_pos[0] = WIDTH // 2
    puck_pos[1] = HEIGHT // 2
    puck_velocity[0] = random.choice([-10, 10])
    puck_velocity[1] = random.choice([-10, 10])

# Função para controlar a IA
def ai_movement():
    if puck_pos[1] > pusher2_pos[1] + PUSHER_RADIUS:
        pusher2_pos[1] += pusher2_speed
    elif puck_pos[1] < pusher2_pos[1] - PUSHER_RADIUS:
        pusher2_pos[1] -= pusher2_speed

    if puck_pos[0] > pusher2_pos[0] + PUSHER_RADIUS:
        pusher2_pos[0] += pusher2_speed
    elif puck_pos[0] < pusher2_pos[0] - PUSHER_RADIUS:
        pusher2_pos[0] -= pusher2_speed

    pusher2_pos[1] = max(PUSHER_RADIUS, min(pusher2_pos[1], HEIGHT - PUSHER_RADIUS))
    pusher2_pos[0] = max(WIDTH // 2 + PUSHER_RADIUS, min(pusher2_pos[0], WIDTH - PUSHER_RADIUS))

# Escolha do modo de jogo
against_ai = False
mode_selected = False

while not mode_selected:
    screen.fill(WHITE)
    draw_text("Pressione 1 para Jogador vs Jogador", small_font, BLACK, WIDTH // 2 - 200, HEIGHT // 2 - 40)
    draw_text("Pressione 2 para Jogador vs Máquina", small_font, BLACK, WIDTH // 2 - 200, HEIGHT // 2 + 10)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_1:
                against_ai = False
                mode_selected = True
            elif event.key == K_2:
                against_ai = True
                mode_selected = True

# Loop principal
playing = True
while playing:
    screen.fill(GREEN)

    # Desenhar linha central
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)

    # Desenhar as áreas de gol
    pygame.draw.rect(screen, WHITE, (0, GOAL_TOP, GOAL_WIDTH, GOAL_HEIGHT))  # Gol do Jogador 1
    pygame.draw.rect(screen, WHITE, (WIDTH - GOAL_WIDTH, GOAL_TOP, GOAL_WIDTH, GOAL_HEIGHT))  # Gol do Jogador 2

    # Timer regressivo
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = max(game_duration - seconds, 0)

    # Calcular minutos e segundos
    minutes = time_left // 60
    seconds = time_left % 60
    time_formatted = f"{minutes:02}:{seconds:02}"

    if time_left == 0:
        playing = False

    # Eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Movimento do jogador 1
    keys = pygame.key.get_pressed()
    if keys[K_w] and pusher1_pos[1] - PUSHER_RADIUS > 0:
        pusher1_pos[1] -= pusher1_speed
    if keys[K_s] and pusher1_pos[1] + PUSHER_RADIUS < HEIGHT:
        pusher1_pos[1] += pusher1_speed
    if keys[K_a] and pusher1_pos[0] - PUSHER_RADIUS > 0:
        pusher1_pos[0] -= pusher1_speed
    if keys[K_d] and pusher1_pos[0] + PUSHER_RADIUS < WIDTH // 2:
        pusher1_pos[0] += pusher1_speed

    # Movimento do jogador 2 ou IA
    if against_ai:
        ai_movement()
    else:
        if keys[K_UP] and pusher2_pos[1] - PUSHER_RADIUS > 0:
            pusher2_pos[1] -= pusher2_speed
        if keys[K_DOWN] and pusher2_pos[1] + PUSHER_RADIUS < HEIGHT:
            pusher2_pos[1] += pusher2_speed
        if keys[K_LEFT] and pusher2_pos[0] - PUSHER_RADIUS > WIDTH // 2:
            pusher2_pos[0] -= pusher2_speed
        if keys[K_RIGHT] and pusher2_pos[0] + PUSHER_RADIUS < WIDTH:
            pusher2_pos[0] += pusher2_speed

    # Movimento do disco
    puck_pos[0] += puck_velocity[0]
    puck_pos[1] += puck_velocity[1]

    # Colisão com as paredes (excluindo as áreas de gol)
    if puck_pos[1] - PUCK_RADIUS <= 0 or puck_pos[1] + PUCK_RADIUS >= HEIGHT:
        puck_velocity[1] = -puck_velocity[1]

    # Colisão com as laterais, exceto nas áreas de gol
    if puck_pos[0] - PUCK_RADIUS <= GOAL_WIDTH and GOAL_TOP <= puck_pos[1] <= GOAL_BOTTOM:
        puck_velocity[0] = abs(puck_velocity[0])  # Permitir passagem pelo gol
    elif puck_pos[0] + PUCK_RADIUS >= WIDTH - GOAL_WIDTH and GOAL_TOP <= puck_pos[1] <= GOAL_BOTTOM:
        puck_velocity[0] = -abs(puck_velocity[0])  # Permitir passagem pelo gol
    elif puck_pos[0] - PUCK_RADIUS <= 0:
        puck_velocity[0] = abs(puck_velocity[0])  # Colisão com a parede esquerda
    elif puck_pos[0] + PUCK_RADIUS >= WIDTH:
        puck_velocity[0] = -abs(puck_velocity[0])  # Colisão com a parede direita

    # Colisão com os gols (somente se o disco estiver completamente dentro da área do gol)
    if puck_pos[0] - PUCK_RADIUS <= GOAL_WIDTH and GOAL_TOP <= puck_pos[1] <= GOAL_BOTTOM:
        score2 += 1
        reset_puck()
    elif puck_pos[0] + PUCK_RADIUS >= WIDTH - GOAL_WIDTH and GOAL_TOP <= puck_pos[1] <= GOAL_BOTTOM:
        score1 += 1
        reset_puck()

    # Colisão com os empurradores
    dist1 = ((puck_pos[0] - pusher1_pos[0])**2 + (puck_pos[1] - pusher1_pos[1])**2)**0.5
    dist2 = ((puck_pos[0] - pusher2_pos[0])**2 + (puck_pos[1] - pusher2_pos[1])**2)**0.5

    if dist1 <= PUSHER_RADIUS + PUCK_RADIUS:
        puck_velocity[0] = abs(puck_velocity[0])
    if dist2 <= PUSHER_RADIUS + PUCK_RADIUS:
        puck_velocity[0] = -abs(puck_velocity[0])

    # Desenho dos elementos
    pygame.draw.circle(screen, RED, pusher1_pos, PUSHER_RADIUS)
    pygame.draw.circle(screen, BLUE, pusher2_pos, PUSHER_RADIUS)
    pygame.draw.circle(screen, BLACK, puck_pos, PUCK_RADIUS)

    # Placar e timer
    draw_text(str(score1), font, RED, WIDTH // 4, 20)
    draw_text(str(score2), font, BLUE, WIDTH * 3 // 4, 20)
    draw_text(f"Tempo: {time_formatted}", small_font, BLACK, WIDTH // 2 - 100, 20)

    # Atualização da tela
    pygame.display.flip()
    clock.tick(FPS)

# Mensagem de fim de jogo
screen.fill(WHITE)
if score1 > score2:
    draw_text("Jogador 1 Venceu!", font, RED, WIDTH // 2 - 200, HEIGHT // 2 - 40)
elif score2 > score1:
    draw_text("Jogador 2 Venceu!", font, BLUE, WIDTH // 2 - 200, HEIGHT // 2 - 40)
else:
    draw_text("O jogo terminou empatado!", font, BLACK, WIDTH // 2 - 300, HEIGHT // 2 - 40)

pygame.display.flip()
pygame.time.wait(5000)
pygame.quit()
sys.exit()

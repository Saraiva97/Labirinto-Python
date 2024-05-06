import pygame
import random

# Definindo cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Configurações do labirinto
WIDTH = 20
HEIGHT = 20
MARGIN = 1
ROWS = 35
COLS = 25

# Configurações do jogador
PLAYER_COLOR = RED
PLAYER_SIZE = 18
PLAYER_MOVE_DELAY = 15

# Função para gerar um labirinto
def generate_maze():
    grid = []
    for row in range(ROWS):
        grid.append([])
        for column in range(COLS):
            grid[row].append(1)

    stack = []
    current_cell = (0, 0)
    visited_cells = set()

    while True:
        visited_cells.add(current_cell)
        neighbors = []

        for i, j in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current_cell[0] + i, current_cell[1] + j)
            if neighbor not in visited_cells and 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS:
                neighbors.append(neighbor)

        if neighbors:
            stack.append(current_cell)
            next_cell = random.choice(neighbors)
            grid[current_cell[0]][current_cell[1]] = 0
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()
        else:
            break

    grid[ROWS - 2][COLS - 2] = 2

    return grid

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WINDOW_WIDTH = WIDTH * COLS + MARGIN * (COLS + 1)
WINDOW_HEIGHT = HEIGHT * ROWS + MARGIN * (ROWS + 1)
WINDOW_SIZE = [WINDOW_WIDTH, WINDOW_HEIGHT]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Labirinto")

# Função para desenhar o labirinto
def draw_maze(grid):
    for row in range(ROWS):
        for column in range(COLS):
            color = WHITE
            if grid[row][column] == 0:
                color = BLACK
            elif grid[row][column] == 2:
                color = GREEN
            pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

# Função para desenhar o jogador
def draw_player(x, y):
    pygame.draw.rect(screen, PLAYER_COLOR, [(MARGIN + WIDTH) * x + MARGIN, (MARGIN + HEIGHT) * y + MARGIN, PLAYER_SIZE, PLAYER_SIZE])

# Função para mover o jogador mais lentamente
def move_player_slow(player_x, player_y, maze):
    keys = pygame.key.get_pressed()
    new_x, new_y = player_x, player_y
    if keys[pygame.K_LEFT]:
        new_x -= 1
    elif keys[pygame.K_RIGHT]:
        new_x += 1
    elif keys[pygame.K_UP]:
        new_y -= 1
    elif keys[pygame.K_DOWN]:
        new_y += 1

    # Verifica se a nova posição é válida
    if (0 <= new_x < COLS) and (0 <= new_y < ROWS) and maze[new_y][new_x] != 1:
        return new_x, new_y

    return player_x, player_y

# Loop principal
running = True
frame_count = 0
while running:
    maze = generate_maze()
    player_x = 1
    player_y = 1
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_running = False

        frame_count += 1

        if frame_count % PLAYER_MOVE_DELAY == 0:
            player_x, player_y = move_player_slow(player_x, player_y, maze)
            if maze[player_y][player_x] == 2:
                print("Você chegou à saída! Gerando um novo labirinto...")
                game_running = False
            frame_count = 0

        screen.fill(BLACK)
        draw_maze(maze)
        draw_player(player_x, player_y)
        pygame.display.flip()

pygame.quit()

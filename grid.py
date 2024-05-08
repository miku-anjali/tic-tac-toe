import pygame
from pygame.locals import *
import time

pygame.init()
run = True

screen_width = 300
screen_height = 300
background_color = (20, 189, 172)  # Background color

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("TicTacToe")

font = pygame.font.SysFont('arial', 48, bold=True)
font1 = pygame.font.SysFont('arial', 30, bold=True, italic=True)

# Load the background image and set the icon
screen.fill(background_color)


def draw_x(x, y):
    pygame.draw.line(screen, (89, 81, 84), (x + 15, y + 15),
                     ((x + screen_width // grid_size) - 15, (y + screen_height // grid_size) - 15), 12)
    pygame.draw.line(screen, (89, 81, 84), (x + 15, (y + screen_height // grid_size) - 15),
                     ((x + screen_width // grid_size) - 15, y + 15), 12)


def draw_o(x, y):
    center = (x + screen_width // (2 * grid_size), y + screen_height // (2 * grid_size))
    pygame.draw.circle(screen, (255, 224, 178), center, screen_width // (3 * grid_size), 8)


def grid():
    grids = (34, 34, 34)
    width = 5
    for x in range(1, grid_size):
        pygame.draw.line(screen, grids, (x * screen_width // grid_size, 0),
                         (x * screen_width // grid_size, screen_height), width)
        pygame.draw.line(screen, grids, (0, x * screen_height // grid_size),
                         (screen_width, x * screen_height // grid_size), width)


def clear_screen():
    alpha_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    for alpha in range(255, 0, -10):  # Gradually decrease alpha from 255 to 0
        alpha_surface.fill((background_color[0], background_color[1], background_color[2], alpha))
        screen.blit(alpha_surface, (0, 0))
        pygame.display.flip()
        pygame.time.wait(10)


def win_text(winner_symbol):
    if winner_symbol == 'X':
        colour = (255, 224, 178)
    else:
        colour = (89, 81, 84)
    txt = " Wins!"
    win_img = font.render(txt, True, colour)
    x = 120
    y = 135
    text_rect = win_img.get_rect(topleft=(x, y))  # Set the top-left corner of the text rectangle
    screen.blit(win_img, text_rect)


def play_again():
    colour = (255, 224, 178)
    retry()
    txt = "Retry"
    win_img = font1.render(txt, True, colour)
    x = 210
    y = 260
    text_rect = win_img.get_rect(topleft=(x, y))  # Set the top-left corner of the text rectangle
    screen.blit(win_img, text_rect)


def retry():
    rect = pygame.draw.rect(screen, (89, 81, 84), (198, 248, 100, 50))


# creating small grids for clicks
grid_size = 3
# creating a list consisting of a list of rows
grid_rects = []

cur_player = 'X'

# Initialize gridx as a 2D list of zeros
gridx = [[''] * grid_size for _ in range(grid_size)]

retry_button_x = 198
retry_button_y = 248
retry_button_width = 100
retry_button_height = 50
retry_rect = pygame.Rect(retry_button_x, retry_button_y, retry_button_width, retry_button_height)


def winner():
    for x in range(grid_size):
        # rows
        if gridx[x][0] == gridx[x][1] == gridx[x][2] != '':
            return gridx[x][0], 'row', x
        # columns
        if gridx[0][x] == gridx[1][x] == gridx[2][x] != '':
            return gridx[0][x], 'column', x
        # diagonals
    if gridx[0][0] == gridx[1][1] == gridx[2][2] != '':
        return gridx[0][0], 'diagonal', 0
    if gridx[0][2] == gridx[1][1] == gridx[2][0] != '':
        return gridx[0][2], 'diagonal', 1
    return None

def initialize_game():
    global game_over, cur_player, gridx
    game_over = False
    cur_player = 'X'
    gridx = [[''] * grid_size for _ in range(grid_size)]


for rows in range(grid_size):
    rows_rects = []
    for col in range(grid_size):
        rect = pygame.Rect(col * (screen_width // grid_size), rows * (screen_height // grid_size),
                           screen_width // grid_size, screen_height // grid_size)
        rows_rects.append(rect)
    grid_rects.append(rows_rects)
game_over = False

while run:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == MOUSEBUTTONDOWN and not game_over:
            print("Mouse button pressed at")
            for rows in range(grid_size):
                for col in range(grid_size):
                    if grid_rects[rows][col].collidepoint(event.pos) and gridx[rows][col] == '':
                        gridx[rows][col] = cur_player
                        if cur_player == 'X':
                            draw_x(grid_rects[rows][col].left, grid_rects[rows][col].top)
                            cur_player = 'O'
                        else:
                            draw_o(grid_rects[rows][col].left, grid_rects[rows][col].top)
                            cur_player = 'X'
                        # Inside the event loop
                        win_result = winner()
                        if win_result is not None:
                            winner_symbol, win_type, win_index = win_result
                            print(f"Player {winner_symbol} wins!")
                            game_over = True
                            clear_screen()
                            if winner_symbol == 'X':
                                draw_x(30, 100)
                            else:
                                draw_o(30, 100)
                            win_text(winner_symbol)
                            play_again()


                        elif event.type == MOUSEBUTTONDOWN and game_over:
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            if retry_rect.collidepoint(mouse_x, mouse_y):
                                initialize_game()
                                screen.fill(background_color)
                                grid()
                                pygame.display.update()

    if not game_over:
        grid()  # Draw the grid if the game is not over
    # Update the display after drawing symbols and lines
    pygame.display.update()

pygame.quit()

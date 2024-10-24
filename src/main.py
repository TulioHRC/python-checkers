import pygame
import logic

initial_board = [
    [None, 'R', None, 'R', None, 'R', None, 'R'],
    ['R', None, 'R', None, 'R', None, 'R', None],
    [None, 'R', None, 'R', None, 'R', None, 'R'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['B', None, 'B', None, 'B', None, 'B', None],
    [None, 'B', None, 'B', None, 'B', None, 'B'],
    ['B', None, 'B', None, 'B', None, 'B', None]
]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (37, 150, 190)
LIGHTER_BLUE = (192, 225, 236)

pygame.init()
pygame.font.init()

SCREEN_CONFIG = {
  "width": 800,
  "height": 800,
  "title": "Checkers Game",
  "square_size": 80
}
my_font = pygame.font.SysFont('Comic Sans MS', 30)

screen = pygame.display.set_mode((SCREEN_CONFIG["width"], SCREEN_CONFIG["height"]))
pygame.display.set_caption(SCREEN_CONFIG["title"])

def draw_board(board):
  pygame.draw.rect(screen, BLUE, (0, 0, 642, 642))
  for row in range(8):
    for column in range(8):
      if (row + column) % 2 == 0:
        pygame.draw.rect(screen, WHITE, (column * SCREEN_CONFIG['square_size'], row * SCREEN_CONFIG['square_size'], SCREEN_CONFIG['square_size'], SCREEN_CONFIG['square_size']))
      else:
        if board[row][column] != None and board[row][column][-1] == 's': # Selected square
          pygame.draw.rect(screen, LIGHT_BLUE, (column * SCREEN_CONFIG['square_size'], row * SCREEN_CONFIG['square_size'], SCREEN_CONFIG['square_size'], SCREEN_CONFIG['square_size']))
        else: 
          pygame.draw.rect(screen, BLACK, (column * SCREEN_CONFIG['square_size'], row * SCREEN_CONFIG['square_size'], SCREEN_CONFIG['square_size'], SCREEN_CONFIG['square_size']))
      
      if (board[row][column] != None and board[row][column][0] == 'o'): # Option to move
        pygame.draw.circle(screen, LIGHTER_BLUE, (column * SCREEN_CONFIG['square_size'] + SCREEN_CONFIG['square_size'] // 2, row * SCREEN_CONFIG['square_size'] + SCREEN_CONFIG['square_size'] // 2), SCREEN_CONFIG['square_size'] // 3)
        pygame.draw.circle(screen, BLACK, (column * SCREEN_CONFIG['square_size'] + SCREEN_CONFIG['square_size'] // 2, row * SCREEN_CONFIG['square_size'] + SCREEN_CONFIG['square_size'] // 2), SCREEN_CONFIG['square_size'] // 5)

      if (board[row][column] != None and board[row][column][0] == 'R'):
        pygame.draw.circle(screen, RED, (column * SCREEN_CONFIG['square_size'] + SCREEN_CONFIG['square_size'] // 2, row * SCREEN_CONFIG['square_size'] + SCREEN_CONFIG['square_size'] // 2), SCREEN_CONFIG['square_size'] // 3)
      if (board[row][column] != None and board[row][column][0] == 'B'):
        pygame.draw.circle(screen, BLUE, (column * SCREEN_CONFIG['square_size'] + SCREEN_CONFIG['square_size'] // 2, row * SCREEN_CONFIG['square_size'] + SCREEN_CONFIG['square_size'] // 2), SCREEN_CONFIG['square_size'] // 3)

def draw_status(status):
  text = my_font.render(F"Turn: {status['turn']}", False, WHITE)
  screen.blit(text, (650,20))

status = {
  "turn": "BLUE",
  "board": initial_board,
  "selected": None
}

while True:
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONUP:
      pos = pygame.mouse.get_pos()
      
      for row in range(8):
        for col in range(8):
          if status["board"][row][col] != None and status["board"][row][col][-1] == 's':
            status["board"][row][col] = status["board"][row][col][:-1]
          elif status["board"][row][col] == 'o': status["board"][row][col] = None

      row = pos[1] // 80
      column = pos[0] // 80
      if row >= 8 or column >= 8: 
        selected = None
        continue
      if (row + column) % 2 != 0 and status["board"][row][column] != None and status["board"][row][column][0] == status["turn"][0] and status["board"][row][column][-1] != "s":
        status["board"][row][column] += "s"
        selected = (row, column)
        for possibility in logic.get_possibilities_to_move_on_place(status["board"], row, column):
          status["board"][possibility[0]][possibility[1]] = "o"
      else:
        selected = None
        

    if event.type == pygame.QUIT:
      pygame.quit()
      quit()
  
  draw_board(status["board"])
  draw_status(status)
  pygame.display.flip()

def get_possibilities_to_move_on_place(board, row, column, last_kill):
  if last_kill != None and (row != last_kill[0] or column != last_kill[1]):
    return []
  possibilities = []
  to_kill = 'R' if board[row][column][0] != 'R' else 'B'

  if board[row][column][:-1] == 'B':
    if column != 0:
      if board[row-1][column-1] == None:
        possibilities.append((row-1, column-1))
    if column != 7:
      if board[row-1][column+1] == None:
        possibilities.append((row-1, column+1))

  elif board[row][column][:-1] == 'R':
    if column != 0:
      if board[row+1][column-1] == None:
        possibilities.append((row+1, column-1))
    if column != 7:
      if board[row+1][column+1] == None:
        possibilities.append((row+1, column+1))
  
  else:
    r, c = (row, column)
    while r - 1 >= 0 and c - 1 >= 0: # left north
      r -= 1
      c -= 1
      if board[r][c] == None:
        possibilities.append((r, c))
      else: break
    r, c = (row, column)
    while r - 1 >= 0 and c + 1 <= 7: # right north
      r -= 1
      c += 1
      if board[r][c] == None:
        possibilities.append((r, c))
      else: break
    r, c = (row, column)
    while r + 1 <= 7 and c - 1 >= 0: # left south
      r += 1
      c -= 1
      if board[r][c] == None:
        possibilities.append((r, c))
      else: break
    r, c = (row, column)
    while r + 1 <= 7 and c + 1 <= 7: # right south
      r += 1
      c += 1
      if board[r][c] == None:
        possibilities.append((r, c))
      else: break

  kills = get_possibilities_to_kill_on_place(board, row, column, to_kill)
  
  if len(get_possibilities_to_kill_on_board(board, board[row][column][:-1], to_kill)) > 0 and len(kills) == 0:
    return []

  return kills if len(kills) > 0 else possibilities

def get_possibilities_to_kill_on_place(board, row, column, to_kill): # Returns a list of possible kills (from, to)
  kills = []

  if "promoved" in board[row][column]:
    r, c = (row, column)
    is_killing = False
    while r - 1 >= 0 and c - 1 >= 0: # left north
      r -= 1
      c -= 1
      if board[r][c] == None and is_killing:
        kills.append((r, c))
      elif board[r][c] and board[r][c][0] == to_kill:
        if is_killing: break
        else: is_killing = True
    r, c = (row, column)
    is_killing = False
    while r - 1 >= 0 and c + 1 <= 7: # right north
      r -= 1
      c += 1
      if board[r][c] == None and is_killing:
        kills.append((r, c))
      elif board[r][c] and board[r][c][0] == to_kill:
        if is_killing: break
        else: is_killing = True
    r, c = (row, column)
    is_killing = False
    while r + 1 <= 7 and c - 1 >= 0: # left south
      r += 1
      c -= 1
      if board[r][c] == None and is_killing:
        kills.append((r, c))
      elif board[r][c] and board[r][c][0] == to_kill:
        if is_killing: break
        else: is_killing = True
    r, c = (row, column)
    is_killing = False
    while r + 1 <= 7 and c + 1 <= 7: # right south
      r += 1
      c += 1
      if board[r][c] == None and is_killing:
        kills.append((r, c))
      elif board[r][c] and board[r][c][0] == to_kill:
        if is_killing: break
        else: is_killing = True
  else:
    if (row >= 2 and column <= 5) and board[row-1][column+1] and board[row-1][column+1][0] == to_kill and board[row-2][column+2] == None:
      kills.append((row-2, column+2))
    if (row >= 2 and column >= 2) and board[row-1][column-1] and board[row-1][column-1][0] == to_kill and board[row-2][column-2] == None:
      kills.append((row-2, column-2))
    if (row <= 5 and column <= 5) and board[row+1][column+1] and board[row+1][column+1][0] == to_kill and board[row+2][column+2] == None:
      kills.append((row+2, column+2))
    if (row <= 5 and column >= 2) and board[row+1][column-1] and board[row+1][column-1][0] == to_kill and board[row+2][column-2] == None:
      kills.append((row+2, column-2))

  return kills


def get_possibilities_to_kill_on_board(board, turn, to_kill): # Returns a list of possible kills (from, to)
  kills = []
  for r in range(8):
    for c in range(8):
      if board[r][c] != None and board[r][c][0] == turn:
        k = get_possibilities_to_kill_on_place(board, r, c, to_kill)
        for kill in k: kill += (r, c)
        kills += k
  
  return kills

def get_kills_and_turn_none_jumped_cells(board, _from, _to):
  actual = _from
  kills = -1
  while actual[0] != _to[0] and actual[1] != _to[1]:
    board[actual[0]][actual[1]] = None
    actual = (actual[0] - 1 if actual[0] > _to[0] else actual[0] + 1, actual[1] - 1 if actual[1] > _to[1] else actual[1] + 1)
    kills += 1

  return kills

def is_game_over(board, turn):
  for r in range(8):
    for c in range(8):
      if board[r][c] != None and board[r][c][0] == turn:
        if len(get_possibilities_to_move_on_place(board, r, c, None)) > 0:
          return False
  return True
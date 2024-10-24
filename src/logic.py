def get_possibilities_to_move_on_place(board, row, column):
  possibilities = []
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
  
  return possibilities

def can_move(board, _from, _to):
  print(_from, _to)
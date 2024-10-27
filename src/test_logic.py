from hypothesis import given, strategies as st
import pytest
from logic import *

# Function to generate a valid board as a strategy
@st.composite
def valid_board_strategy(draw):
    valid_positions = [(row, col) for row in range(8) for col in range(8) if (row + col) % 2 == 1]
    board = [[None for _ in range(8)] for _ in range(8)]
    
    for (row, col) in valid_positions:
        if draw(st.booleans()): # random bool generate (hypothesis will test all the options, based on the properties of the inputs)
            if row == 7:
                piece_type = draw(st.one_of(st.just('B_promoved_'), st.just('B'), st.just('R_promoved_'))) 
            elif row == 0:
                piece_type = draw(st.one_of(st.just('B_promoved_'), st.just('R_promoved_'), st.just('R'))) 
            else:
                piece_type = draw(st.one_of(st.just('R'), st.just('B'), st.just('R_promoved_'), st.just('B_promoved_')))
            
            board[row][col] = piece_type

    return board

@given(board=valid_board_strategy())
def test_get_possibilities_to_move_on_place(board):
    for row in range(8):
        for column in range(8):
            if board[row][column] is not None:
                last_kill = None
                possibilities = get_possibilities_to_move_on_place(board, row, column, last_kill)
                kills = get_possibilities_to_kill_on_board(board, board[row][column][0], 'R' if board[row][column][0] != 'R' else 'B')
                assert isinstance(possibilities, list)
                assert isinstance(kills, list)
                for pos in possibilities:
                    assert 0 <= pos[0] < 8 and pos[0] >= 0
                    assert 0 <= pos[1] < 8 and pos[1] >= 0
                    if len(kills) > 0:
                        assert pos in kills
                

@given(board=valid_board_strategy())
def test_get_possibilities_to_kill_on_place(board):
    for row in range(8):
        for column in range(8):
            if board[row][column] is not None:
                to_kill = 'B' if board[row][column][0] == 'R' else 'R'
                kills = get_possibilities_to_kill_on_place(board, row, column, to_kill)
                assert isinstance(kills, list)
                for pos in kills:
                    assert 0 <= pos[0] < 8 and pos[0] >= 0
                    assert 0 <= pos[1] < 8 and pos[1] >= 0

@given(board=valid_board_strategy())
def test_is_game_over(board):
    assert isinstance(is_game_over(board, 'R'), bool)
    assert isinstance(is_game_over(board, 'B'), bool)

if __name__ == "__main__":
    pytest.main()

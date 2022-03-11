import random


def draw_board(board):
    print('-' * 9)
    print(f'| {board[(1,1)]} {board[(1, 2)]} {board[1, 3]} |')
    print(f'| {board[2, 1]} {board[2, 2]} {board[2, 3]} |')
    print(f'| {board[3, 1]} {board[3, 2]} {board[3, 3]} |')
    print('-' * 9)


def game_status(board):
    if win_check(board) == 'X':
        print("X wins\n")
        return 1
    elif win_check(board) == 'O':
        print("O wins\n")
        return 1
    elif win_check(board) == 0:
        print("Draw")
        return 1
    return 0


def win_check(board):
    # check rows and columns
    for i in range(1, 4):
        if board[(i, 1)] == board[(i, 2)] == board[(i, 3)] != ' ':
            return board[(i, 1)]
        elif board[(1, i)] == board[(2, i)] == board[(3, i)] != ' ':
            return board[(1, i)]

    # check diagonals
    if board[(1, 1)] == board[(2, 2)] == board[(3, 3)] != ' ' or board[(3, 1)] == board[(2, 2)] == board[(1, 3)] != ' ':
        return board[(2, 2)]

    # check for draw
    if all(board[coord] != ' ' for coord in board):
        return 0
    return -1


def player_move(board):
    while True:
        try:
            coord_input = input("Enter the coordinates: ").strip()
            if coord_input == 'exit':
                quit()
            coord_input = map(int, coord_input.split())
            x, y = coord_input
            if x not in range(1, 4) or y not in range(1, 4):
                raise KeyError
        except ValueError:
            print("You should enter numbers!")
        except KeyError:
            print("Coordinates should be from 1 to 3!")
        else:
            cell = (x, y)
            if board[cell] != ' ':
                print('This cell is occupied! Choose another one!')
                continue
            return cell


def easy(board):
    possible_moves = [cell for cell, value in board.items() if board[cell] == ' ']
    cell = random.choice(possible_moves)
    return cell


def medium(board, symbol):
    if symbol == 'X':
        win_status = 'X'
        lose_status = 'O'
    else:
        win_status = 'O'
        lose_status = 'X'

    # rule 1: check if comp can win
    for cell in board:
        if board[cell] == ' ':
            board[cell] = symbol
            if win_check(board) == win_status:
                board[cell] = ' '
                return cell
            else:
                board[cell] = ' '

    # rule 2: check if comp will lose and prevent it
    for cell in board:
        if board[cell] == ' ':
            board[cell] = lose_status
            if win_check(board) == lose_status:
                board[cell] = ' '
                return cell
            else:
                board[cell] = ' '
    return easy(board)


def hard(board, player_current):
    if all(board[cell] == ' ' for cell in board):
        return easy(board)

    symbol_current = player_current
    new_board = board

    def minimax(reboard, symbol, player):
        if player == 'X':
            opponent = 'O'
        else:
            opponent = 'X'

        if win_check(reboard) == player:
            return [None, 10]
        elif win_check(reboard) == opponent:
            return [None, -10]
        elif win_check(reboard) == 0:
            return [None, 0]

        moves = {}
        possible_moves = [cell for cell, value in reboard.items() if reboard[cell] == ' ']

        for cell in possible_moves:
            reboard[cell] = symbol

            if symbol == player:
                result = minimax(reboard, opponent, player)[1]
                moves[cell] = result
            else:
                result = minimax(reboard, player, player)[1]
                moves[cell] = result

            reboard[cell] = ' '

        if symbol == player:
            best_move_cell = max(moves, key=moves.get)
        else:
            best_move_cell = min(moves, key=moves.get)

        return best_move_cell, moves[best_move_cell]

    move_cell = minimax(new_board, symbol_current, player_current)[0]
    return move_cell


def computer_move(board, symbol, level):
    print(f'Making move level "{level}"')
    if level == 'easy':
        return easy(board)
    elif level == 'medium':
        return medium(board, symbol)
    elif level == 'hard':
        return hard(board, symbol)


def menu():
    while True:
        try:
            user_menu_input = input("Input command: ")
            if user_menu_input[:4] == 'exit':
                quit()
            menu_main, player_1, player_2 = user_menu_input.strip().split()
            if menu_main not in ('start', 'exit') or player_1 not in ('easy', 'medium', 'hard', 'user')\
                    or player_2 not in ('easy', 'medium', 'hard', 'user'):
                raise ValueError
        except ValueError:
            print("Bad parameters!")
        else:
            return player_1, player_2


def play_move(player, board, move_status):
    if player == 'user':
        board[player_move(board)] = move_status
    else:
        board[computer_move(board, move_status, player)] = move_status


def main():
    print("Welcome to Tic-Tac-Toe!")
    print("_" * 79)
    print("To start the game input 'start' followed by two words specifying each of the players(separated by spaces):")
    print("user   -> let's you make the moves")
    print("easy   -> computer plays random moves")
    print("medium -> computer plays a slightly more challenging game")
    print("hard   -> computer plays the best possible moves, ensuring it's win or draw in any situation")
    print("_" * 79)
    print("Enter exit to quit playing the game!")
    print("_" * 79)
    print("The game will begin now...")
    print("Good luck!")
    print("_" * 79, '\n')

    while True:
        player_1, player_2 = menu()

        board = {(1, 1): ' ', (1, 2): ' ', (1, 3): ' ', (2, 1): ' ', (2, 2): ' ', (2, 3): ' ',
                 (3, 1): ' ', (3, 2): ' ', (3, 3): ' '}
        draw_board(board)

        move_status = 'X'
        while True:
            if move_status == 'X':
                play_move(player_1, board, move_status)
                move_status = 'O'
            else:
                play_move(player_2, board, move_status)
                move_status = 'X'
            draw_board(board)
            if game_status(board):
                break


if __name__ == "__main__":
    main()

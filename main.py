import time
import random


HEAD = "HEAD"
TAIL = "TAIL"
FIRST_PLAYER = SECOND_PLAYER = ""
HUMAN = ""
MACHINE = "MACHINE"
FIRST_PLAYER_SIGN = 'X'
SECOND_PLAYER_SIGN = 'O'
MACHINE_SIGN = HUMAN_SIGN = ''
INVALID_INPUT_MESSAGE = "Please enter two integers from 1 to 3 as input"
CELL_NOT_EMPTY_MESSAGE = "Cell not empty. Try again."


def get_score(table, is_machines_turn, depth):
    if win(table):
        if is_machines_turn:
            return -10
        return 10
    if draw(table):
        return 0
    if is_machines_turn:
        max_score = -1000
        for row in range(3):
            for col in range(3):
                if table[row][col] == '.':
                    table[row][col] = MACHINE_SIGN
                    max_score = max(max_score, get_score(table, not is_machines_turn, depth + 1))
                    table[row][col] = '.'
        return max_score
    else:
        min_score = 1000
        for row in range(3):
            for col in range(3):
                if table[row][col] == '.':
                    table[row][col] = HUMAN_SIGN
                    min_score = min(min_score, get_score(table, not is_machines_turn, depth + 1))
                    table[row][col] = '.'
        return min_score


def get_best_move(table):
    max_score = -1000
    best_move = [-1, -1]
    for row in range(3):
        for col in range(3):
            if table[row][col] == '.':
                table[row][col] = MACHINE_SIGN
                score = get_score(table, False, 0)
                table[row][col] = '.'
                if score > max_score:
                    max_score = score
                    best_move = [row, col]
    return best_move


def machine_move(table):
    best_move = get_best_move(table)
    table[best_move[0]][best_move[1]] = MACHINE_SIGN
    return table


def print_table(table):
    for i in range(3):
        for j in range(3):
            print(table[i][j], end=" ")
        print()


def win(table):
    for row in range(3):
        if table[row][0] == table[row][1] == table[row][2] and table[row][1] != '.':
            return True
    for col in range(3):
        if table[0][col] == table[1][col] == table[2][col] and table[1][col] != '.':
            return True
    if table[0][0] == table[1][1] == table[2][2] and table[1][1] != '.':
        return True
    if table[0][2] == table[1][1] == table[2][0] and table[1][1] != '.':
        return True
    return False


def draw(table):
    for row in range(3):
        for col in range(3):
            if table[row][col] == '.':
                return False
    return True


def take_input_and_check_validity(table, current_sign):
    user_input = None
    try:
        user_input = list(map(int, input().strip().split()))
    except ValueError:
        print(INVALID_INPUT_MESSAGE)
        return None
    if user_input is not None:
        if len(user_input) != 2:
            print(INVALID_INPUT_MESSAGE)
            return None
        row, col = user_input
        if row > 3 or row < 1 or col > 3 or col < 1:
            print(INVALID_INPUT_MESSAGE)
            return None
        row -= 1
        col -= 1
        if table[row][col] != '.':
            print(CELL_NOT_EMPTY_MESSAGE)
            return None
        table[row][col] = current_sign
        return table
    else:
        print("Please provide an input")
        return None


if __name__ == '__main__':
    table = [['.', '.', '.'],
             ['.', '.', '.'],
             ['.', '.', '.']]
    print("Welcome to tic tac toe!")
    print("Please enter your name:")
    HUMAN = input()
    print(f"Hi {HUMAN}!")
    print('#' * 25)
    print("'.' -> Empty cell \n'X' -> Move by first player \n'O' -> Move by second player")
    print("TABLE: ")
    print_table(table)
    print('#' * 25)
    time.sleep(2)
    print("I'll toss a coin. If the outcome is HEAD you get to start first, otherwise I'll start first.")
    print("The player who starts first will use X to fill the box. The other player will use O to fill the box.")
    print("On your turn, enter two integers from 1 to 3 to mark your cell with your sign. \n"
          "I'll toss the coin after 20 secs. Feel free to go through the info once again.")
    time.sleep(20)
    print("AND THE COIN IS UP IN THE AIR!")
    for i in range(4):
        print('.')
        time.sleep(0.5)
    coin_outcome = [HEAD, TAIL]
    result = random.choice(coin_outcome)
    print(result)
    if result == HEAD:
        FIRST_PLAYER = HUMAN
        SECOND_PLAYER = MACHINE
        print("Your turn!")
    else:
        FIRST_PLAYER = MACHINE
        SECOND_PLAYER = HUMAN
        print("My turn!")
    if FIRST_PLAYER == MACHINE:
        MACHINE_SIGN = 'X'
        HUMAN_SIGN = 'O'
    else:
        MACHINE_SIGN = 'O'
        HUMAN_SIGN = 'X'
    turn = [FIRST_PLAYER, SECOND_PLAYER]
    sign = ['X', 'O']
    turn_index = 0
    while True:
        current_player = turn[turn_index]
        current_sign = sign[turn_index]
        if current_player == HUMAN:
            output = take_input_and_check_validity(table, current_sign)
            if not output:
                continue
            table = output
        else:
            table = machine_move(table)
        print("TABLE: ")
        print_table(table)
        time.sleep(1)
        if win(table):
            if current_player == HUMAN:
                print("Congratulations! You won the game!")
            else:
                print(f"Better luck next time, {HUMAN}")
            break
        if draw(table):
            print(f"The game ended in a draw. Better luck next time, {HUMAN}")
            break
        turn_index = (turn_index + 1) % 2

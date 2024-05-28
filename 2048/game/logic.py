import random

def move(direction, board):
    if direction == "w":
        return move_up(board)
    if direction == "s":
        return move_down(board)
    if direction == "a":
        return move_left(board)
    if direction == "d":
        return move_right(board)

def check_game_status(board, max_tile=2048):
    flat_board = [cell for row in board for cell in row]
    if max_tile in flat_board:
        return "WIN"

    for i in range(4):
        for j in range(4):
            if j != 3 and board[i][j] == board[i][j+1] or i != 3 and board[i][j] == board[i + 1][j]:
                return "PLAY"

    if 0 not in flat_board:
        return "LOSE"
    else:
        return "PLAY"

def fill_two_or_four(board, iter=1):
    for _ in range(iter):
        a = random.randint(0, 3)
        b = random.randint(0, 3)
        while(board[a][b] != 0):
            a = random.randint(0, 3)
            b = random.randint(0, 3)

        if sum([cell for row in board for cell in row]) in (0, 2):
            board[a][b] = 2
        else:
            board[a][b] = random.choice((2, 4))
    return board

def move_left(board):
    shift_left(board)
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j + 1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j + 1] = 0
                j = 0
    shift_left(board)
    return board

def move_up(board):
    board = rotate_left(board)
    board = move_left(board)
    board = rotate_right(board)
    return board

def move_right(board):
    shift_right(board)
    for i in range(4):
        for j in range(3, 0, -1):
            if board[i][j] == board[i][j - 1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j - 1] = 0
                j = 0
    shift_right(board)
    return board

def move_down(board):
    board = rotate_left(board)
    board = move_left(board)
    shift_right(board)
    board = rotate_right(board)
    return board

def shift_left(board):
    for i in range(4):
        nums, count = [], 0
        for j in range(4):
            if board[i][j] != 0:
                nums.append(board[i][j])
                count += 1
        board[i] = nums
        board[i].extend([0] * (4 - count))

def shift_right(board):
    for i in range(4):
        nums, count = [], 0
        for j in range(4):
            if board[i][j] != 0:
                nums.append(board[i][j])
                count += 1
        board[i] = [0] * (4 - count)
        board[i].extend(nums)

def rotate_left(board):
    return [[board[j][i] for j in range(4)] for i in range(3, -1, -1)]

def rotate_right(board):
    board = rotate_left(board)
    board = rotate_left(board)
    return rotate_left(board)

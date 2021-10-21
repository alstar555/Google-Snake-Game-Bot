from PIL import ImageGrab
import pyautogui
import webbrowser
import time
from constants import GLOBAL_border, GLOBAL_dark_square, GLOBAL_light_square, GLOBAL_apple


def open_game():
    webbrowser.open("https://www.google.com/search?q=google+snake&rlz=1C1CHBF_enUS918US918&oq=google+snake&aqs=chrome.0.69i59j0i433i512j0i131i433i512l3j0i512j0i131i433i512j0i512l3.1487j0j7&sourceid=chrome&ie=UTF-8")
    time.sleep(2)
    pyautogui.click(x = 650, y = 931, clicks = 1, button = 'left')
    time.sleep(0.5)
    pyautogui.click(x = 906, y = 873, clicks = 1, button = 'left')
    time.sleep(0.5)

def print_grid():
    #square = 48x48 pxls
    board_start = (606, 332)
    coords = board_start
    next_y = coords[1]
    screenshot = pyautogui.screenshot()
    screenshot = screenshot.resize((1920, 1080))
    while coords[0] < 1430 and coords[1] < 1030:
        #pyautogui.click(x = coords[0], y = coords[1], clicks = 0, button = 'left')
        current = screenshot.getpixel(coords)
            #print border/ keep in bounds
        if coords[0] >= 1400:
            print(".")
            next_y = coords[1]+48
            next_x = board_start[0]
        else:
            next_x = coords[0]+48
            if current[2] >= 100: #print snake #blue(0, 0, 255)
                print("~", end = "") 
            elif current[1] >= 100: # green (0, 255, 0)
                print("X", end="")
            elif current[0] >= 100: #red (255, 0, 0)
                print("@", end="") 
        coords = (next_x, next_y)

def grab_board(dims):
    board = []
    board_row = ""
    #square = 48x48 pxls
    board_start = (24, 24)
    coords = board_start
    next_y = coords[1]
    screenshot = grab_and_crop(dims)
    screenshot.show()
    while coords[0] < 816 and coords[1] < 720:
        pyautogui.click(x = coords[0], y = coords[1], clicks = 0, button = 'left')
        current = screenshot.getpixel(coords)
            #print border/ keep in bounds
        if coords[0] >= 816:
            board.append(board_row)
            board_row = ""
            next_y = coords[1]+48
            next_x = board_start[0]
        else:
            next_x = coords[0]+48
            if current[2] >= 100: #print snake #blue(0, 0, 255)
                board_row += "1"
            elif current[1] >= 100: # green (0, 255, 0)
                board_row += "0"
            elif current[0] >= 100: #red (255, 0, 0)
                board_row += "2"
        coords = (next_x, next_y)
    return board

# def grab_board():
#     board = ""
#     #square = 48x48 pxls
#     board_start = (558, 332)
#     coords = board_start
#     next_y = coords[1]
#     screenshot = pyautogui.screenshot()
#     screenshot = screenshot.resize((1920, 1080))
#     width = 0
#     height=0
#     count =0
#     while coords[0] < 1430 and coords[1] < 1030:
#         #pyautogui.click(x = coords[0], y = coords[1], clicks = 0, button = 'left')
#         current = screenshot.getpixel(coords)
#             #print border/ keep in bounds
#         if coords[0] >= 1400:
#             width+=1
#             height = count
#             next_y = coords[1]+48
#             next_x = board_start[0]
#         else:
#             next_x = coords[0]+48
#             if current[2] >= 100: #print snake #blue(0, 0, 255)
#                 board += "1"
#             elif current[1] >= 100: # green (0, 255, 0)
#                 board += "0"
#             elif current[0] >= 100: #red (255, 0, 0)
#                 board += "2"
#         coords = (next_x, next_y)
#     return board


def print_board(board):
    for x in board:
        print(x)
    print()

def move(dir):
    #controls
    if dir=="r":
        pyautogui.press('right')
    elif dir=="u":
        pyautogui.press('up')
    elif dir=="l":
        pyautogui.press('left')
    elif dir=="d":
        pyautogui.press('down')
    #time.sleep(.2)

#coordinates of snake=1, apple=2
# def find_in_board(charecter, board, snake_width):
#     coord = -1
#     coord_x = -1
#     coord_y = -1
#     for x in board:
#         coord_y+=1
#         coord_x = 0
#         for y in x:
#             coord_x+=1
#             if y == charecter:
#                 coord = (coord_x+snake_width, coord_y)
#                 return coord
#     return coord

def find_in_board(charecter, board, snake_width):
    coord_y = -1
    for x in board:
        coord_y+=1
        coord_x = x.find(charecter)
        if coord_x != -1:
            coord = (coord_x, coord_y)
            return coord
    return -1

#direction snake should move towards apple
def dir_to_apple(current_dir, apple, snake):
    dir = current_dir
    if apple[0] > snake[0] and current_dir !="l":
        dir = "r"
    elif apple[0] < snake[0]  and current_dir !="r":
        dir = "l"
    elif apple[1] > snake[1] and current_dir !="u":
        dir = "d"
    elif apple[1] < snake[1]  and current_dir !="d":
        dir = "u"
    return dir

# def find_path_to_apple(current_dir, apple, snake):
#     moves = []
#     return moves


def move_to_apple(current_dir, board, snake_width, dims):
    snake_pos =  find_in_board("1", board, snake_width) #snake=1 on board
    apple_pos = find_in_board("2", board, snake_width) #apple = 2
    gameover = False;
    while(apple_pos != -1 and not gameover):
        gameover =  check_gameover()
        direction_to_apple = dir_to_apple(current_dir, apple_pos, snake_pos)
        current_dir = direction_to_apple
        move(direction_to_apple) # r, u, l, d
        board = grab_board(dims) #update board
        snake_pos =  find_in_board("1", board, snake_width) #snake=2 on board
        apple_pos = find_in_board("2", board, snake_width) #apple = 1
    return gameover
    
def check_gameover():
    gameover = False
    screenshot = pyautogui.screenshot()
    screenshot = screenshot.resize((1920, 1080))
    value = screenshot.getpixel((1045, 415))
    if value[0] >= 200 and value[1]>= 190:
        gameover = True
    elif value == (12, 12, 12):
        gameover =True
    return gameover
    

def grab_and_crop(dim):
    # screenshot = pyautogui.screenshot()
    # screenshot = screenshot.resize((816,720))
    return ImageGrab.grab().crop(dim).resize((816,720))

def find_edge(screen, pos, pval, direction):
    """
    Finds the edge of the current empty grid square by going up or to the left
    """
    if direction == "left":
        left = 0
        # Loops until the pixel value changes
        while screen.getpixel((pos[0]-left, pos[1])) != pval:
                left += 1
        return (pos[0]-left+1, pos[1])
    if direction == "down":
        down = 0
        # Loops until the pixel value changes
        while screen.getpixel((pos[0], pos[1]+down)) != pval:
                down += 1
        return (pos[0], pos[1]+down-1)
    
def find_dim(screen, pos, pval, dir):
    """
    Finds the width of the empty square by counting the number of pixels that the value doesnt change
    """
    if dir == "right":
        right = 0
        # Loops until the pixel value changes
        while screen.getpixel((pos[0]+right, pos[1])) != pval:
                right += 1
        return right
    if dir == "up":
        up = 0
        # Loops until the pixel value changes
        while screen.getpixel((pos[0], pos[1]-up)) != pval:
                up += 1
        return up-1
    
def get_grid():
    start_w = pyautogui.size()[0]*0.5
    start_h = pyautogui.size()[1]*0.5
    screen = ImageGrab.grab()
    start_w, start_h = find_edge(screen, (start_w, start_h), GLOBAL_border, "down")
    start_w, start_h = find_edge(screen, (start_w, start_h), GLOBAL_border, "left")
    width = find_dim(screen, (start_w, start_h), GLOBAL_border, "right")
    height = find_dim(screen, (start_w, start_h), GLOBAL_border, "up")
    return start_w, start_h-height, start_w+width, start_h



if __name__=="__main__":
    #start game
    snake_width=3
    board = []
    open_game()
    dims = get_grid()
    screen = grab_and_crop(dims)
    current_dir = "r"
    move(current_dir)
    time.sleep(.5)
    board = grab_board(dims)
    print_board(board)

    #logic
    gameover = False
    while(not gameover):
        gameover = move_to_apple(current_dir, board, snake_width, dims)
        board = grab_board(dims)
        #print_board(board)
        snake_width+=1
       
    


    




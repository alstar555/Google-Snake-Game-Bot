from PIL import ImageGrab
import pyautogui
import webbrowser
import time
from constants import GLOBAL_border, GLOBAL_dark_square, GLOBAL_height, GLOBAL_light_square, GLOBAL_apple, GLOBAL_width


def open_game():
    webbrowser.open("https://www.google.com/search?q=google+snake&rlz=1C1CHBF_enUS918US918&oq=google+snake&aqs=chrome.0.69i59j0i433i512j0i131i433i512l3j0i512j0i131i433i512j0i512l3.1487j0j7&sourceid=chrome&ie=UTF-8")
    time.sleep(3)
    pyautogui.click(x = 650, y = 931, clicks = 1, button = 'left')
    time.sleep(0.5)
    pyautogui.click(x = 906, y = 873, clicks = 1, button = 'left')
    time.sleep(0.5)


def grab_board(dims):
    board = ""
    #square = 48x48 pxls
    board_start = (24, 24)
    coords = board_start
    next_y = coords[1]
    screenshot = grab_and_crop(dims)
    while coords[1] < 720:
        #pyautogui.click(x = coords[0], y = coords[1], clicks = 0, button = 'left')
        current = screenshot.getpixel(coords)
            #print border/ keep in bounds
        if coords[0] >= 792:
            next_y = coords[1]+48
            next_x = board_start[0]
        else:
            next_x = coords[0]+48
            if current[2] >= 100: #print snake #blue(0, 0, 255)
                board += "1"
            elif current[1] >= 100: # green (0, 255, 0)
                board += "0"
            elif current[0] >= 100: #red (255, 0, 0)
                board += "2"
        coords = (next_x, next_y)
    return board


def print_board(board):
    count=0
    for x in board:
        count+=1
        print(x,end="")
        if count%GLOBAL_width==0:
            print()
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

def find_in_board(charecter, board, snake_width):
    index = board.find(charecter)
    if index != -1:
        x = int(index%GLOBAL_width)
        y = index//GLOBAL_width
        coords = (x, y)
        return coords
    return index

#direction snake should move towards apple
def dir_to_apple(current_dir, apple, snake):
    dir = current_dir
    if apple[0] > snake[0] and current_dir !="l" and current_dir !="r":
        dir = "r"
    elif apple[0] < snake[0]  and current_dir !="r" and current_dir !="l":
        dir = "l"
    elif apple[1] > snake[1] and current_dir !="u" and current_dir !="d":
        dir = "d"
    elif apple[1] < snake[1]  and current_dir !="d" and current_dir !="u":
        dir = "u"
    return dir

def stay_in_bounds(snake):
    bound = 3
    dir = -1
    if snake[0]<bound:
        dir = ("d", "r")
    elif snake[1] <bound:
        dir = ("r", "d")
    elif snake[0] > (GLOBAL_width-bound):
        dir = ("d", "l")
    elif snake[1] > (GLOBAL_height-bound): 
        dir = ("l", "u")
    return dir


def move_to_apple(current_dir, board, snake_width, dims):
    snake_pos =  find_in_board("1", board, snake_width) #snake=1 on board
    apple_pos = find_in_board("2", board, snake_width) #apple = 2
    gameover = False;
    while(not gameover):
        if(apple_pos==-1):
             dirs = stay_in_bounds(snake_pos) # r, u, l, d
             if dirs != -1:
                move(dirs[0])
                move(dirs[1])
        else:
            gameover =  check_gameover(dims)
            direction_to_apple = dir_to_apple(current_dir, apple_pos, snake_pos)
            current_dir = direction_to_apple
            move(direction_to_apple) # r, u, l, d
            board = grab_board(dims) #update board
            snake_pos =  find_in_board("1", board, snake_width) #snake=2 on board
            apple_pos = find_in_board("2", board, snake_width) #apple = 1
            dirs = stay_in_bounds(snake_pos) # r, u, l, d
            if dirs != -1:
                move(dirs[0])
                move(dirs[1])
    return gameover
    
def check_gameover(dims):
    gameover = False
    screenshot = grab_and_crop(dims)
    value = screenshot.getpixel((505, 105))
    if value[0] >= 200 and value[1]>= 190:
        gameover = True
    elif value == (12, 12, 12):
        gameover =True
    return gameover
    

def grab_and_crop(dims):
    return ImageGrab.grab().crop(dims).resize((816,720))

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

    #logic
    gameover = False
    while(not gameover):
        gameover = move_to_apple(current_dir, board, snake_width, dims)
        board = grab_board(dims)
        # print_board(board)
        snake_width+=1
       
    


    




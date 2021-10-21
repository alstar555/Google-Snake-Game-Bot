from PIL import ImageGrab
from PIL import Image
import pyautogui
import webbrowser
import time

from constants import GLOBAL_border, GLOBAL_dark_square, GLOBAL_light_square, GLOBAL_apple

def grab_and_crop(dim):
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

def advance(screen, pos, pval, direction):
    """
    Finds the number of pixels needed to move to the next square
    """
    if direction == "right":
        right = 0
        # Loops until the pixel value changes
        while screen.getpixel((pos[0]+right, pos[1])) == pval:
                right += 1
        return right
    if direction == "down":
        down = 0
        # Loops until the pixel value changes
        while screen.getpixel((pos[0], pos[1]+down)) == pval:
                down += 1
        return down
    
def get_grid():
    start_w = pyautogui.size()[0]*0.5
    start_h = pyautogui.size()[1]*0.5
    screen = ImageGrab.grab()
    start_w, start_h = find_edge(screen, (start_w, start_h), GLOBAL_border, "down")
    start_w, start_h = find_edge(screen, (start_w, start_h), GLOBAL_border, "left")
    width = find_dim(screen, (start_w, start_h), GLOBAL_border, "right")
    height = find_dim(screen, (start_w, start_h), GLOBAL_border, "up")
    return start_w, start_h-height, start_w+width, start_h

def update_grid(screen):
    if screen.getpixel((505, 105)) == (253, 192, 1):
        return [], (0,0)
    grid = []
    width = 48
    apple_pos = (0,0)
    #Loops through the number of rows
    for n in range(15):
        grid.append([])
        #Loops through the number of columns
        for i in range(17):
            #Gets the pixel value at the center of the grid square
            new = screen.getpixel(((width/2)+width*i, (width/2)+width*n))
            #Some debugging to show what pixel value your code is seeing, pls don't put in a for loop im begging
            """new_screen = screen.crop((0, 0, start_w+right, start_h+down))
            new_screen.show()"""
            if new[2] >= 100: #print snake #blue(0, 0, 255)
                grid[-1].append("Snake")
            elif new[1] >= 100: # green (0, 255, 0)
                grid[-1].append("Empty")
            elif new[0] >= 100: #red (255, 0, 0)
                grid[-1].append("Apple") 
                apple_pos = (width/2)+width*i, (width/2)+width*n
    return grid, apple_pos

def print_grid(grid):
    values = {"Empty": "🚫", "Snake": "🐍", "Apple": "🍎"}
    print("-"*52)
    for n in grid:
        for m in n:
            print("|{}".format(values[m]), end="")
        print("|\n" + "-"*52)

def construct_grid(grid):
    values = {"Empty": (181, 213, 101), "Snake": (89, 118, 229), "Apple": (207, 83, 47)}
    im = Image.new("RGB", (1700, 1500))
    for n in range(len(grid)):
        for m in range(len(grid[n])):
            color = Image.new("RGB", (100,100), values[grid[n][m]])
            im.paste(color, (100*m, 100*n))
    return im

def get_apple_vals(apple_pos, width, screen = ImageGrab.grab()):
    y = apple_pos[0]
    x = apple_pos[1]
    offset = (width/2)*0.5
    images = []
    images.append(screen.getpixel((y+offset,x)))
    images.append(screen.getpixel((y-offset,x)))
    images.append(screen.getpixel((y,x+offset)))
    images.append(screen.getpixel((y,x-offset)))
    return images

def check_apple(apple_pos, width, references):
    images= get_apple_vals(apple_pos, width)
    return False not in [images[n]==references[n] for n in range(len(images))]
    

# https://www.topcoder.com/thrive/articles/python-for-gui-automation-pyautogui
grids = []
width = 0

webbrowser.open("https://www.google.com/search?q=google+snake&rlz=1C1CHBF_enUS918US918&oq=google+snake&aqs=chrome.0.69i59j0i433i512j0i131i433i512l3j0i512j0i131i433i512j0i512l3.1487j0j7&sourceid=chrome&ie=UTF-8")
time.sleep(2)

pyautogui.click(x = 1269, y = 1550, clicks = 1, button = 'left')
time.sleep(0.5)
pyautogui.click(x = 1800, y = 1600, clicks = 1, button = 'left')
time.sleep(0.25)
dims = get_grid()
screen = grab_and_crop(dims)
pyautogui.press('right')
time.sleep(0.25)
grid, apple_pos= update_grid(grab_and_crop(dims))
print_grid(grid)
grids.append(construct_grid(grid))
i = 0
while i < 6:
    screen = grab_and_crop(dims)
    apple_val = screen.getpixel(apple_pos)
    #refs = get_apple_vals(apple_pos, width, screen)
    #while check_apple(apple_pos, width, refs):
    #    continue
    while grab_and_crop(dims).getpixel(apple_pos) == apple_val:
        if len(update_grid(grab_and_crop(dims))[0]) == 0:
            break
        continue
    grid, apple_pos= update_grid(grab_and_crop(dims))
    if len(grid) == 0:
        break
    print_grid(grid)
    grids.append(construct_grid(grid))
    print()


for n in grids:
    n.show()
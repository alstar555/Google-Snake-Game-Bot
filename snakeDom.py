from PIL import ImageGrab
from PIL import Image
import pyautogui
import webbrowser
import time

def find_edge(screen, pos, pval, direction):
    """
    Finds the edge of the current empty grid square by going up or to the left
    """
    if direction == "left":
        left = 0
        # Loops until the pixel value changes
        while screen.getpixel((pos[0]-left, pos[1])) == pval:
                left += 1
        return (pos[0]-left+1, pos[1])
    if direction == "up":
        up = 0
        # Loops until the pixel value changes
        while screen.getpixel((pos[0], pos[1]-up)) == pval:
                up += 1
        return (pos[0], pos[1]-up+1)
    
def find_width(screen, pos, pval):
    """
    Finds the width of the empty square by counting the number of pixels that the value doesnt change
    """
    right = 0
    # Loops until the pixel value changes
    while screen.getpixel((pos[0]+right, pos[1])) == pval:
            right += 1
    return right

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
    

def update_grid():
    #My attempt at using screen percentages to generalize the code
    start_w = pyautogui.size()[0]*0.33
    start_h = pyautogui.size()[1]*0.32
    screen = ImageGrab.grab()
    if screen.getpixel((2061,821)) == (253, 192, 1):
        return [], (0,0)
    grid = []
    #Gets the light square pixel value
    pval_light = screen.getpixel((start_w, start_h))
    #Gets the center of the apple, using percents, I hope its generalized
    apple = screen.getpixel((pyautogui.size()[0]*0.325, pyautogui.size()[1]*0.234))
    # Starts in the general region of the first square, and navigates to the top corner of it
    start_w, start_h = find_edge(screen, (start_w, start_h), pval_light, "left")
    start_w, start_h = find_edge(screen, (start_w, start_h), pval_light, "up")
    #Gets the square width for your board
    width = find_width(screen, (start_w, start_h), pval_light)
    #Increments the starting positions to the center of the first square based on the width
    start_w += width/2
    start_h += width/2
    #Sets the offsets used to navigate the board to zero
    right = 0
    down = 0
    #Gets the dark square pixel value
    pval_dark = screen.getpixel((start_w+width+right, start_h))
    apple_pos = (0,0)
    #Loops through the number of rows
    for n in range(15):
        grid.append([])
            #Loops through the number of columns
        for i in range(17):
            #Gets the pixel value at the center of the grid square
            new = screen.getpixel((start_w+right, start_h+down))
            #Some debugging to show what pixel value your code is seeing, pls don't put in a for loop im begging
            """new_screen = screen.crop((0, 0, start_w+right, start_h+down))
            new_screen.show()"""
            if new == pval_light or new == pval_dark:
                #If it finds an empty square, it adds empty to the grid, and advances the offsets to the center of the next grid space
                grid[-1].append("Empty")
                right += advance(screen, (start_w+right, start_h+down), new, "right")
                right += width/2
            elif new == apple:
              #If it finds the apple, it just shifts the offsets to the next square but code is mean so I dont use the function, and keeps track of the apple position to return later
                grid[-1].append("Apple")
                right += width
                apple_pos = (start_w+right, start_h+down)
            else:
              #If its not empty and not an apple, its a snake (Cant code for color cause the snake is ombre ☹) 
                grid[-1].append("Snake")
                right += width
        right = 0
        #Loop runs to make sure that shifting down relies on an empty square and not one with a snake or apple, will have to add a stop to this loop in case every square in the row has something in it
        while screen.getpixel((start_w+right, start_h+down)) not in (pval_light, pval_dark):
            right += width
        #Moves the offset down to the next grid and then resets the right offset to the first square
        down += advance(screen, (start_w+right, start_h+down), screen.getpixel((start_w+right, start_h+down)), "down")
        down += width/2
        right = 0
    return grid, apple_pos


def print_grid(grid):
    values = {"Empty": "🚫", "Snake": "🐍", "Apple": "🍎"}
    print("-"*60)
    for n in grid:
        for m in n:
            print("|{}".format(values[m]), end="")
        print("|\n" + "-"*60)

def construct_grid(grid):
    values = {"Empty": (181, 213, 101), "Snake": (89, 118, 229), "Apple": (207, 83, 47)}
    im = Image.new("RGB", (1700, 1500))
    for n in range(len(grid)):
        for m in range(len(grid[n])):
            color = Image.new("RGB", (100,100), values[grid[n][m]])
            im.paste(color, (100*m, 100*n))
    return im
            
    

# https://www.topcoder.com/thrive/articles/python-for-gui-automation-pyautogui
grids = []

# webbrowser.open("https://www.google.com/search?q=google+snake&rlz=1C1CHBF_enUS918US918&oq=google+snake&aqs=chrome.0.69i59j0i433i512j0i131i433i512l3j0i512j0i131i433i512j0i512l3.1487j0j7&sourceid=chrome&ie=UTF-8")
# time.sleep(4)

# pyautogui.click(x = 650, y = 931, clicks = 1, button = 'left')
# time.sleep(0.5)
# pyautogui.click(x = 906, y = 873, clicks = 1, button = 'left')

webbrowser.open("https://www.google.com/search?q=google+snake&rlz=1C1CHBF_enUS918US918&oq=google+snake&aqs=chrome.0.69i59j0i433i512j0i131i433i512l3j0i512j0i131i433i512j0i512l3.1487j0j7&sourceid=chrome&ie=UTF-8")
time.sleep(4)
pyautogui.click(x = 650, y = 931, clicks = 1, button = 'left')
time.sleep(0.5)
pyautogui.click(x = 906, y = 873, clicks = 1, button = 'left')
time.sleep(0.5)

pyautogui.press('right')
time.sleep(0.25)
grid, apple_pos= update_grid()
print_grid(grid)
grids.append(construct_grid(grid))
while True:
    time.sleep(0.25)
    grid, apple_pos = update_grid()
    if len(grid) == 0:
        break
    print_grid(grid)
    grids.append(construct_grid(grid))
    print()

for n in grids:
    n.show()
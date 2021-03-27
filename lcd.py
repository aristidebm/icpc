import math


digits = {
          # The first string correspond to:
          # 1: top character.
          # 2: middle character.
          # 3: bottom character.
          # The second string correspond to  charaters between middle and top characters.
          # The third string correspond to characters between middle and bottom charaters.
          "0": ["- -", "| |", "| |"], 
          "1": [" ||", "  |", "  |"],
          "2": ["---", "  |", "|  "],
          "3": ["---", "|  ", "|  "],
          "4": [" -|", "| |", "  |"],
          "5": ["---", "|  ", "  |"],
          "6": ["---", "|  ", "| |"],
          "7": ["-||", "  |", "  |"],
          "8": ["---", "| |", "| |"],
          "9": ["---", "| |", "  |"],
}

def main():
    lcd_function()


def lcd_function():
    """
    This function gets a user input and scale and
    prints it in lcd format until the user hits (q|Q)uit.
    Example:
         -----            -----     -----             -----     -----   -----      -----     -----
        |     |     |          |   |       |     |   |         |             |    |     |   |     |
        |     |     |          |   |       |     |   |         |             |    |     |   |     |
        |     |     |     -----     -----   -----     -----     -----        |     -----     -----
        |     |     |    |         |             |         |   |     |       |    |     |         |
        |     |     |    |         |             |         |   |     |       |    |     |         |
         -----      |     ------    -----        |    -----     -----        |     -----     -----  .  
    """
    anwser = "y"

    # help function
    print_help()

    while True:
        height, width, numbers = input("data@lcd ~> : ").split(" ")
        height = int(height)
        width = int(width)
        mid = compute_mid(height)
        
        for line in range(2*height + 3):
            for number in numbers:
                if line == 0:
                    # on the first line, character is either hiphen
                    # or space.
                    if digits[number][0][0] == "-":
                       print_hiphen_character(width)
                    else:
                        print(" "*width, end="\t")
                elif line == mid:
                    # on the mid line, character is either hipen, space or |
                    char = digits[number][0][1]
                    if char == ' ':
                        print(char*width, end="\t")
                    elif char == "-":
                        print_hiphen_character(width)
                    else:
                        print(" "*(width - 1), end="")
                        print(char, end="\t")
                elif line == 2*height + 2:
                    # On the last line, the character is either hiphen or |
                    char = digits[number][0][2]
                    if char == '-':
                        print_hiphen_character(width)
                    else:
                        print(" "*(width - 1), end="")
                        print(char, end="\t")
                elif 0 < line < mid:
                    print_top_bottom(number, 1, width)

                elif mid < line < 2*height + 2:
                    print_top_bottom(number, 2, width)
                    

            print()
        
        print()
        anwser = input("quit@lcd(hit q to quit) ~> : ")
        if anwser.lower() == 'q':
            break


def compute_mid(height):
    return (2*height + 2) // 2


def print_top_bottom(number, direction, width):
    """
    print element according the direction
    provided.
    direction is:
    1 : for above mid
    2 : for below mid
    """ 
    if digits[number][direction][0] == digits[number][direction][2]:
        char = digits[number][direction][0]
        print(char, end="")
        print(" "*(width - 2), end="")
        print(char, end="\t")
    elif digits[number][direction][0] == "|" and digits[number][direction][2] == " ":
        print("|", end="")
        print(" "*(width - 1), end="\t")
    else:
        print(" "*(width - 1), end="")
        print("|", end="\t")

def print_hiphen_character(width): 
    print(" ", end="")
    print("-"*(width - 2), end="")
    print(" ", end="\t")


def print_help():
    print(
            """
help

data@lcd ~> : <height> <width> <number>
params:
    height - each character height
    width  - each character width
    mumber - number to turn to lcd
Example:
    python lcd.py 10 10 123456789
            """)

if __name__ == "__main__":
    main()

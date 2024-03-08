import random
import tkinter as tk
from tkinter import Canvas, Label, Button


GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 102# Milliseconds
NORMAL_SPEED = 102  # Milliseconds for Normal mode
EXTREME_SPEED = 20  # Milliseconds for Extreme mode
NORMAL_SPACE_SIZE = 35  # Space size for Normal mode
EXTREME_SPACE_SIZE = 20  # Space size for Extreme modeSNAKE_COLOR = None
BODY_PARTS = 5
FOOD_COLOR = "#ADFF2F"
BACKGROUND_COLOR = "#000000"
score = 0
high_score = 0  # Initialize high score


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        self.x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        self.y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [self.x, self.y]

        self.square = canvas.create_rectangle(self.x, self.y, self.x + SPACE_SIZE, self.y + SPACE_SIZE, fill=FOOD_COLOR,
                                              tag="food")

def select_game_mode():
    global SPEED, SPACE_SIZE  # Use global variables for speed and space size
    mode_window = tk.Tk()
    mode_window.title("Select Game Mode")
    mode_window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}")  # Match the game window size

    def choose_mode(is_extreme):
        global SPEED, SPACE_SIZE
        if is_extreme:
            SPEED = EXTREME_SPEED
            SPACE_SIZE = EXTREME_SPACE_SIZE
        else:
            SPEED = NORMAL_SPEED
            SPACE_SIZE = NORMAL_SPACE_SIZE
        mode_window.destroy()  # Close the mode selection window
        select_snake_color()  # Proceed to color selection

    # Centering buttons using place
    button_width = 200  # Width of the button in pixels
    button_height = 50  # Height of the button in pixels
    normal_mode_button = tk.Button(mode_window, text="Normal Mode", command=lambda: choose_mode(False), font=('Arial', 14))
    extreme_mode_button = tk.Button(mode_window, text="Extreme Mode", command=lambda: choose_mode(True), font=('Arial', 14))

    normal_mode_button.place(relx=0.5, rely=0.4, anchor='center', width=button_width, height=button_height)
    extreme_mode_button.place(relx=0.5, rely=0.6, anchor='center', width=button_width, height=button_height)

    mode_window.mainloop()


def select_snake_color():
    color_window = tk.Tk()
    color_window.title("Select Snake Color")
    color_window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}")


    colors = {
        "Pink": "#FF00FF",
        "Blue": "#0000FF",
        "Yellow": "#FFFF00",
        "Green": "#008000",
        "Orange": "#FFA500",
        "Purple": "#836FFF"
    }

    def setup_game(snake_color):
        global SNAKE_COLOR, window, canvas, label, snake, food, score
        SNAKE_COLOR = snake_color
        color_window.destroy()  # Close the color selection window

        # Setup the main game window
        window = tk.Tk()
        window.title("Snake Game")
        window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}")
        window.resizable(False, False)

        canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        canvas.pack()

        label = Label(window, text=f"Score: {score}", font=('consolas', 20))
        label.pack()

        # Bind key events
        window.bind('<Left>', lambda event: change_direction('left'))
        window.bind('<Right>', lambda event: change_direction('right'))
        window.bind('<Up>', lambda event: change_direction('up'))
        window.bind('<Down>', lambda event: change_direction('down'))

        snake = Snake()
        food = Food()

        window.destroy()
        next_turn()  # Start the game loop

        window.mainloop()

    # Create color selection buttons
    button_frame = tk.Frame(color_window)
    button_frame.place(relx=0.5, rely=0.5, anchor='center')

    for color_name, color_hex in colors.items():
        btn = tk.Button(button_frame, text=color_name, bg=color_hex, width=20, height=2,
                        command=lambda color=color_hex: setup_game(color))
        btn.pack(pady=10)

    color_window.mainloop()

def next_turn():
    global direction, score, snake, food, label

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision():
        game_over()
    else:
        window.after(SPEED, next_turn)


def change_direction(new_direction):
    global direction
    direction = new_direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collision():
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


def game_over():
    global score, high_score  # Add high_score as global

    if score > high_score:
        high_score = score  # Update high score if current score is higher

    canvas.delete("all")
    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 50, font=('consolas', 40), text="GAME OVER", fill="red")
    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2, font=('consolas', 20), text=f"High Score: {high_score}",
                       fill="yellow")

    play_again_button = tk.Button(window, text="Play Again", font=('consolas', 20), command=play_again)
    quit_button = tk.Button(window, text="Quit", font=('consolas', 20), command=quit_game)

    canvas.create_window(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 50, window=play_again_button)
    canvas.create_window(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 100, window=quit_button)


def play_again():
    for widget in canvas.winfo_children():
        widget.destroy()

    global score, direction, snake, food, label
    score = 0  # Reset the current score for the new game session
    direction = 'down'
    label.config(text="Score: {}".format(score))
    canvas.delete("all")

    snake = Snake()
    food = Food()
    next_turn()


def quit_game():
    window.destroy()

# Function to display color selection screen


if __name__ == "__main__":
    select_game_mode()



window = tk.Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = "down"

label = Label(window, text="Score: {}".format(score), font=('consolas', 20))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn()

window.mainloop()
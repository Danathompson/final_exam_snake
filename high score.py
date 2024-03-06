import random
import tkinter as tk
from tkinter import Canvas, Label

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 130  # Milliseconds
SPACE_SIZE = 50
BODY_PARTS = 5
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
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


def next_turn():
    global food
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
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
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


window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

label = Label(window, text="Score: 0", font=('consolas', 20))
label.pack()

score = 0
direction = 'down'

snake = Snake()
food = Food()

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()  # Ensure this is correctly instantiated at the global level

next_turn()  # Start the game loop

window.mainloop()
import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define screen dimensions
WIDTH = 800
HEIGHT = 600

# Define snake speed
snake_speed = 15  # Adjusted for a smoother movement

# Define snake block size
snake_block = 10

# Function to draw the snake
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

# Function to display the score
def display_score(score):
    value = pygame.font.SysFont(None, 35).render("Your Score: " + str(score), True, WHITE)
    screen.blit(value, [0, 0])

# Function to place the food at a random location
def place_food(snake_block, x1, x2, y1, y2):
    x = round(random.randrange(x1, x2 - snake_block) / 10.0) * 10.0
    y = round(random.randrange(y1, y2 - snake_block) / 10.0) * 10.0
    return x, y

# Initialize Pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the title of the window
pygame.display.set_caption("Snake Game")

# Clock
clock = pygame.time.Clock()

# Define starting position of the snake
def_x = WIDTH / 2
def_y = HEIGHT / 2

# Define starting snake length
snake_list = []
snake_length = 1

# Define starting direction
x1 = def_x
y1 = def_y
x1_change = 0
y1_change = 0

# Placing the first piece of food
food_x, food_y = place_food(snake_block, 20, WIDTH - 20, 20, HEIGHT - 20)

# Game loop
game_over = False
while not game_over:

    # Get user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and x1_change == 0:
                x1_change = -snake_block
                y1_change = 0
            elif event.key == pygame.K_RIGHT and x1_change == 0:
                x1_change = snake_block
                y1_change = 0
            elif event.key == pygame.K_UP and y1_change == 0:
                y1_change = -snake_block
                x1_change = 0
            elif event.key == pygame.K_DOWN and y1_change == 0:
                y1_change = snake_block
                x1_change = 0

    # Update snake position
    x1 += x1_change
    y1 += y1_change

    # Game over conditions
    if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
        game_over = True

    # Clear the screen
    screen.fill(BLACK)

    # Draw the food
    pygame.draw.rect(screen, RED, [food_x, food_y, snake_block, snake_block])

    # Snake eats food
    if x1 == food_x and y1 == food_y:
        food_x, food_y = place_food(snake_block, 20, WIDTH - 20, 20, HEIGHT - 20)
        snake_length += 1

    # Update the snake's body
    snake_head = [x1, y1]
    snake_list.append(snake_head)
    if len(snake_list) > snake_length:
        del snake_list[0]

    # Check for collision with itself
    for segment in snake_list[:-1]:
        if segment == snake_head:
            game_over = True

    # Draw the snake
    draw_snake(snake_block, snake_list)

    # Display the score
    display_score(snake_length - 1)

    # Update the display
    pygame.display.update()

    # Check for collision with the snake itself here, if needed

    # Control the game speed
    clock.tick(snake_speed)

# Quit the game
pygame.quit()

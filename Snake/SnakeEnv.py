import pygame, random, numpy as np, gym
from gym import spaces

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(SnakeEnv, self).__init__()
        self.width = 800
        self.height = 600
        self.snake_block = 10
        self.snake_speed = 15
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(4)  # [Left, Right, Up, Down]
        # Define the observation space, this part depends heavily on how you define your state
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.height, self.width, 3), dtype=np.uint8)

        pygame.init()
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Set the screen size
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Initialize the game
        self.reset()

    def reset(self):
        # Reset the game state
        self.snake_list = [[self.width / 2, self.height / 2]]
        self.snake_length = 1
        self.food_x, self.food_y = self.place_food()
        self.x1_change = 0
        self.y1_change = 0
        self.game_over = False
        
        # Return the initial state
        state = self.get_state()
        return state
    
    def step(self, action):
        # Implement how the action changes the game state
        rewards = 0

        if action == 0:  # Left
            self.x1_change = -self.snake_block
            self.y1_change = 0
        elif action == 1:  # Right
            self.x1_change = self.snake_block
            self.y1_change = 0
        elif action == 2:  # Up
            self.x1_change = 0
            self.y1_change = -self.snake_block
        elif action == 3:  # Down
            self.x1_change = 0
            self.y1_change = self.snake_block
        
        # Update game state based on action
        # This includes moving the snake, checking for game over, etc.
        x1 = self.snake_list[0] + self.x1_change
        y1 = self.snake_list[1] + self.y1_change
        self.snake_list = [x1, y1]

        # Game over conditions
        if x1 >= self.width or x1 < 0 or y1 >= self.height or y1 < 0:
            self.game_over = True
        
        # Calculate reward
        if self.game_over:
            rewards = -10  # Example penalty
        else:
            rewards = 1  # Example reward for surviving

        # Check if snake eats food
        # Increase reward and snake length, place new food

        state = self.get_state()  # Get the new state
        done = self.game_over

        return state, rewards, done, {}
    
    # Function to draw the snake
    def draw_snake(self, snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.screen, self.GREEN, [x[0], x[1], snake_block, snake_block])

    # Function to display the score
    def display_score(self, score):
        value = pygame.font.SysFont(None, 35).render("Your Score: " + str(score), True,self.WHITE)
        self.screen.blit(value, [0, 0])

    def render(self, mode='human'):

        pass

    def place_food(self):
        pass

    def get_state(self):
        pass
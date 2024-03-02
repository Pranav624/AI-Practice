import pygame, random, time
from Organism import Organism

WIDTH = 700
HEIGHT = 700
ORGANISM_SIZE = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORGANISM_LIST = []

def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(WHITE)
    pygame.display.set_caption("Simulation")
    clock = pygame.time.Clock()

    # Create the organisms
    for _ in range(1000):
        position_x = random.randint(0, 695)
        position_y = random.randint(0, 695)
        o = Organism(position_x, position_y, WIDTH, HEIGHT, ORGANISM_SIZE)
        ORGANISM_LIST.append(o)
        pygame.draw.rect(screen, BLACK, [position_x, position_y, ORGANISM_SIZE, ORGANISM_SIZE])
    pygame.display.update()

    # Make the organisms move around
    for epoch in range(3):
        for _ in range(1000):
            screen.fill(WHITE)
            for organism in ORGANISM_LIST:
                organism.step()
                pygame.draw.rect(screen, BLACK, [organism.get_position()[0], organism.get_position()[1], ORGANISM_SIZE, ORGANISM_SIZE])
            pygame.display.update()
            time.sleep(0.01)
        

    time.sleep(100)

if __name__ == '__main__':
    main()
import pygame, time

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
WIDTH = 700
HEIGHT = 700

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(WHITE)
    pygame.display.set_caption("Simulation")
    clock = pygame.time.Clock()

    board = [['.' for _ in range(7)] for _ in range(6)]
    for i in range(len(board)):
        for j in range(len(board[0])):
            pygame.draw.circle(screen, GRAY, (j*80+110, i*80+110), 30)
    pygame.display.update()

    time.sleep(100)

if __name__ == '__main__':
    main()
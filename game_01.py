import cv2
import numpy as np
import pygame
import random

# Color detection function
def detect_dominant_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    color_ranges = {
        'blue': (np.array([100, 50, 50]), np.array([130, 255, 255])),
        'cyan': (np.array([80, 50, 50]), np.array([100, 255, 255])),
        'red1': (np.array([0, 50, 50]), np.array([10, 255, 255])),
        'red2': (np.array([170, 50, 50]), np.array([180, 255, 255])),
        'orange': (np.array([10, 50, 50]), np.array([25, 255, 255]))
    }
    max_area = 0
    dominant_color = None
    for color, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv, lower, upper)
        area = cv2.countNonZero(mask)
        if color == 'red':
            mask2 = cv2.inRange(hsv, color_ranges['red2'][0], color_ranges['red2'][1])
            area += cv2.countNonZero(mask2)
        if area > max_area:
            max_area = area
            dominant_color = color
    return dominant_color

# Game constants
CELL_SIZE = 40
GRID_WIDTH = 20
GRID_HEIGHT = 15
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT
PACMAN_SPEED = 5
GHOST_SPEED = 3

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color-Controlled Pac-Man")
clock = pygame.time.Clock()

# Initialize webcam
cap = cv2.VideoCapture(0)

# Game classes
class PacMan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0), (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 2)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.direction = pygame.math.Vector2(0, 0)

    def update(self):
        self.rect.move_ip(self.direction * PACMAN_SPEED)
        self.rect.clamp_ip(screen.get_rect())

class Ghost(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 2)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        self.direction = pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1])).normalize()

    def update(self):
        self.rect.move_ip(self.direction * GHOST_SPEED)
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction.x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.direction.y *= -1

class Dot(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE // 4, CELL_SIZE // 4))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)

# Create game objects
pacman = PacMan()
ghosts = pygame.sprite.Group(
    Ghost((255, 0, 0)),  # Red ghost
    Ghost((255, 184, 255)),  # Pink ghost
    Ghost((0, 255, 255)),  # Cyan ghost
    Ghost((255, 184, 82))  # Orange ghost
)
dots = pygame.sprite.Group()

# Generate dots
for x in range(CELL_SIZE // 2, WIDTH, CELL_SIZE):
    for y in range(CELL_SIZE // 2, HEIGHT, CELL_SIZE):
        if random.random() < 0.7:  # 70% chance of placing a dot
            dots.add(Dot((x, y)))

# Main game loop
running = True
score = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capture frame and detect color
    ret, frame = cap.read()
    if not ret:
        break
    dominant_color = detect_dominant_color(frame)

    # Update Pac-Man direction based on dominant color
    if dominant_color == 'blue':
        pacman.direction = pygame.math.Vector2(0, -1)
    elif dominant_color == 'cyan':
        pacman.direction = pygame.math.Vector2(0, 1)
    elif dominant_color == 'red':
        pacman.direction = pygame.math.Vector2(-1, 0)
    elif dominant_color == 'orange':
        pacman.direction = pygame.math.Vector2(1, 0)
    else:
        pacman.direction = pygame.math.Vector2(0, 0)

    # Update game objects
    pacman.update()
    ghosts.update()

    # Check for collisions
    for dot in pygame.sprite.spritecollide(pacman, dots, True):
        score += 10

    if pygame.sprite.spritecollideany(pacman, ghosts):
        running = False

    # Draw everything
    screen.fill((0, 0, 0))
    dots.draw(screen)
    ghosts.draw(screen)
    screen.blit(pacman.image, pacman.rect)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

# Game over
font = pygame.font.Font(None, 72)
game_over_text = font.render("Game Over", True, (255, 0, 0))
screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
pygame.display.flip()

# Wait for a moment before closing
pygame.time.wait(2000)

# Clean up
cap.release()
pygame.quit()

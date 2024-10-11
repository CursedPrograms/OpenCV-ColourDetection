import cv2
import numpy as np
import pygame

def detect_dominant_color(frame):
    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color ranges in HSV
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

def main():
    # Initialize Pygame
    pygame.init()
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pac-Man Color Control")

    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Pac-Man setup
    pacman_pos = [width // 2, height // 2]
    pacman_radius = 20
    speed = 5

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Capture frame from webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Detect dominant color
        dominant_color = detect_dominant_color(frame)

        # Move Pac-Man based on dominant color
        if dominant_color == 'blue':
            pacman_pos[1] -= speed  # Move up
        elif dominant_color == 'cyan':
            pacman_pos[1] += speed  # Move down
        elif dominant_color == 'red':
            pacman_pos[0] -= speed  # Move left
        elif dominant_color == 'orange':
            pacman_pos[0] += speed  # Move right

        # Keep Pac-Man within screen bounds
        pacman_pos[0] = max(pacman_radius, min(width - pacman_radius, pacman_pos[0]))
        pacman_pos[1] = max(pacman_radius, min(height - pacman_radius, pacman_pos[1]))

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw Pac-Man
        pygame.draw.circle(screen, (255, 255, 0), pacman_pos, pacman_radius)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

    # Clean up
    cap.release()
    pygame.quit()

if __name__ == "__main__":
    main()

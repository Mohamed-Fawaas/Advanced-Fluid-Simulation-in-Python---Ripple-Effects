import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Fluid Simulation - Ripple Effects")

# Colors
WHITE = (255, 255, 255)

# Simulation parameters
damping = 0.96
gravity_factor = 1.01

# Create two grids for wave heights
current_grid = np.zeros((WIDTH, HEIGHT))
previous_grid = np.zeros((WIDTH, HEIGHT))

def create_ripple(x, y, magnitude=300):
    """Create a ripple effect at (x, y) with a gradient magnitude."""
    radius = 20
    for dx in range(-radius, radius):
        for dy in range(-radius, radius):
            dist = np.sqrt(dx**2 + dy**2)
            if dist < radius and 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT:
                current_grid[x + dx, y + dy] += magnitude * (1 - dist / radius)

def update_simulation():
    """Update the wave simulation."""
    global current_grid, previous_grid
    next_grid = (
        (current_grid[:-2, 1:-1] + current_grid[2:, 1:-1] +
         current_grid[1:-1, :-2] + current_grid[1:-1, 2:]) / 2
        - previous_grid[1:-1, 1:-1]
    ) * gravity_factor
    next_grid *= damping
    previous_grid = current_grid.copy()
    current_grid[1:-1, 1:-1] = next_grid

def draw_simulation():
    """Render the simulation with red gradient colors."""
    for x in range(WIDTH):
        for y in range(HEIGHT):
            value = current_grid[x, y]
            color_intensity = int(max(0, min(255, value * 0.5)))
            color = (color_intensity, 0, 0)  # Shades of red
            screen.set_at((x, y), color)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        create_ripple(mouse_x, mouse_y)

    update_simulation()
    screen.fill(WHITE)  # White background
    draw_simulation()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

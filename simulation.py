import tkinter as tk
from tkinter import filedialog
import pygame
import pygame_gui
import numpy as np

# Constants for UI
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
ROOM_WIDTH, ROOM_HEIGHT = 400, 400
GREY = "#A19CA2"
BLUE = "#17283D"
ORANGE = "#292021"
WHITE = "#FFFFFF"
BLACK = "#0e0e0e"

# Initialize pygame
pygame.init()

# Parameters for wave simulation
Lx, Ly = 1.0, 1.0    # Domain size
c = 1.0              # Wave speed
nx, ny = 300, 300    # Number of spatial points
dx, dy = Lx / (nx - 1), Ly / (ny - 1)  # Spatial step sizes
dt = 0.001           # Time step size
courant_x = (c * dt / dx)**2
courant_y = (c * dt / dy)**2

# Grid for 2D wave simulation
x = np.linspace(0, Lx, nx)
y = np.linspace(0, Ly, ny)
X, Y = np.meshgrid(x, y)

# Initialize wave arrays
u = np.zeros((ny, nx))        # Current wave state
u_prev = np.zeros((ny, nx))   # Previous wave state
u_next = np.zeros((ny, nx))   # Next wave state

# Function to generate a single impulse wave on button click
def generate_impulse():
    """Creates a single impulse at the center of the domain."""
    global u, u_prev
    center_x, center_y = nx // 2, ny // 2
    # Create a Gaussian-like impulse
    u[center_y, center_x] = 1.0  # Set a single point in the center to a high value (impulse)
    u_prev = u.copy()  # Store current state for the next step

# Function to reset the simulation
def reset_simulation():
    """Resets the wave simulation to its initial state."""
    global u, u_prev, u_next
    u.fill(0)        # Reset current wave state to zero
    u_prev.fill(0)   # Reset previous wave state to zero
    u_next.fill(0)   # Reset next wave state to zero

# Pygame screen size and setup
screen_size = (600, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("2D Wave Simulation")

# Function to rescale wave data to grayscale color values
def rescale_wave_to_grayscale(u):
    """Rescale wave data to a grayscale image."""
    u_min = np.min(u)
    u_max = np.max(u)

    if u_max == u_min:
        u_rescaled = np.zeros_like(u, dtype=np.uint8)
    else:
        u_normalized = (u - u_min) / (u_max - u_min)
        u_rescaled = (u_normalized * 255).astype(np.uint8)

    grayscale_image = np.stack((u_rescaled,) * 3, axis=-1)

    return grayscale_image

# Time evolution of the wave
def update_wave():
    global u, u_prev, u_next
    u_next[1:-1, 1:-1] = (2 * u[1:-1, 1:-1] - u_prev[1:-1, 1:-1] + 
                          courant_x * (u[1:-1, 2:] - 2 * u[1:-1, 1:-1] + u[1:-1, :-2]) +
                          courant_y * (u[2:, 1:-1] - 2 * u[1:-1, 1:-1] + u[:-2, 1:-1]))
    
    u_prev = u.copy()
    u = u_next.copy()

# Main Window setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sound Visualization')

# Manager for pygame_gui
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# Tkinter initialization (for file dialog)
root = tk.Tk()
root.withdraw()

# UI Elements
room_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 50), (200, 40)),
                                           text='Select Room',
                                           manager=manager)

# Additional UI elements...
# (Same as in your previous code...)

# Simulation loop
running = True
clock = pygame.time.Clock()
wave_active = False  # Track whether the wave has been triggered

while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        # Handle Pygame GUI events
        manager.process_events(event)

        # Room button action
        if event.type == pygame.USEREVENT:
            if event.ui_element == room_button:
                open_room_dialog()  # Open the file dialog when the button is clicked
        
        # Trigger wave generation on spacebar press or mouse click
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                generate_impulse()  # Generate a single impulse at the center
                wave_active = True
            elif event.key == pygame.K_r:
                reset_simulation()  # Reset the simulation

    # Update wave only if the wave has been generated
    if wave_active:
        update_wave()
    
    # Rescale to grayscale and create pygame surface
    u_color = rescale_wave_to_grayscale(u)
    surface = pygame.surfarray.make_surface(u_color)
    
    # Draw the UI
    screen.fill(BLUE)

    # Draw room visualization
    pygame.draw.rect(screen, GREY, pygame.Rect(50, 50, ROOM_WIDTH, ROOM_HEIGHT))  # Draw the room
    pygame.draw.rect(screen, ORANGE, pygame.Rect(50, 50, ROOM_WIDTH, ROOM_HEIGHT), 2)  # Draw the outline of the room

    # Scale to screen size and display
    surface = pygame.transform.scale(surface, (ROOM_WIDTH, ROOM_HEIGHT))  # Scale to room size
    screen.blit(surface, (50, 50))  # Blit the wave simulation inside the room

    # Render UI
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()

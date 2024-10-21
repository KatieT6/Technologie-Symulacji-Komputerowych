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
damping_coefficient = 0.01  # Damping coefficient

# Grid for 2D wave simulation
x = np.linspace(0, Lx, nx)
y = np.linspace(0, Ly, ny)
X, Y = np.meshgrid(x, y)

# Initialize wave arrays
u = np.zeros((ny, nx))        # Current wave state
u_prev = np.zeros((ny, nx))   # Previous wave state
u_next = np.zeros((ny, nx))   # Next wave state
amplitude = 0.00000000001  # Default amplitude for the wave

# Function to generate a single impulse wave on button click
def generate_impulse():
    """Creates a single impulse at the center of the domain."""
    global u, u_prev, amplitude
    center_x, center_y = nx // 2, ny // 2
    # Set the impulse to the specified amplitude
    u[center_y, center_x] = amplitude  # Set impulse at the center
    u_prev = u.copy()  # Store current state for the next step

# Function to reset the simulation
def reset_simulation():
    """Resets the wave simulation to its initial state."""
    global u, u_prev, u_next
    u.fill(0)        # Reset current wave state to zero
    u_prev.fill(0)   # Reset previous wave state to zero
    u_next.fill(0)   # Reset next wave state to zero

# Pygame screen size and setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Sound Visualization and Wave Simulation")

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

# Time evolution of the wave with damping and echo
def update_wave():
    global u, u_prev, u_next
    # Update the wave equation
    u_next[1:-1, 1:-1] = (2 * u[1:-1, 1:-1] - u_prev[1:-1, 1:-1] + 
                          courant_x * (u[1:-1, 2:] - 2 * u[1:-1, 1:-1] + u[1:-1, :-2]) +
                          courant_y * (u[2:, 1:-1] - 2 * u[1:-1, 1:-1] + u[:-2, 1:-1]) - 
                          damping_coefficient * u[1:-1, 1:-1])  # Include damping

    # Echo simulation: Reflect the wave at the edges
    u_next[0, :] = u_next[1, :]  # Top edge reflection
    u_next[-1, :] = u_next[-2, :]  # Bottom edge reflection
    u_next[:, 0] = u_next[:, 1]  # Left edge reflection
    u_next[:, -1] = u_next[:, -2]  # Right edge reflection

    u_prev = u.copy()
    u = u_next.copy()

# Draw separator line
separator_y = 150  # y-coordinate for the separator line
separator_color = GREY  # Line color

# Function to draw a separator line
def draw_separator():
    pygame.draw.line(screen, separator_color, (550, separator_y), (750, separator_y), 5)

# Function to open room selection dialog
def open_room_dialog():
    file_path = filedialog.askopenfilename()
    if file_path:  # Check if a file was selected
        print(f"Room file selected: {file_path}")
    else:
        print("No file selected.")

# Main Window setup
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# Tkinter initialization (for file dialog)
root = tk.Tk()
root.withdraw()

# UI Elements
room_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 50), (200, 40)),
                                           text='Select Room',
                                           manager=manager)

wall_material_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=['Wood', 'Concrete', 'Glass'],
                                                            starting_option='Wood',
                                                            relative_rect=pygame.Rect((550, 100), (200, 40)),
                                                            manager=manager)

# Amplitude UI Elements
amplitude_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((575, 150), (150, 20)),
    text="Amplitude",
    manager=manager)

amplitude_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((550, 180), (200, 25)),
                                                          start_value=amplitude, value_range=(0, 1), manager=manager)

# Frequency UI Elements
frequency_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((575, 220), (150, 20)),
    text="Frequency",
    manager=manager)

frequency_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((550, 250), (200, 25)),
                                                          start_value=440, value_range=(20, 2000), manager=manager)

position_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((575, 290), (150, 20)),
    text="Sound Position",
    manager=manager)

x_position_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((550, 320), (50, 30)),
                                                     manager=manager)
x_position_box.set_text("0")

y_position_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((650, 320), (50, 30)),
                                                     manager=manager)
y_position_box.set_text("0")

# Room Visualization Area
room_rect = pygame.Rect(50, 50, ROOM_WIDTH, ROOM_HEIGHT)

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

        # Check for amplitude slider change
        if event.type == pygame.USEREVENT:
            if event.ui_element == amplitude_slider:
                amplitude = amplitude_slider.get_current_value()  # Get the current value of the amplitude slider
                damping_coefficient = amplitude
                print(amplitude)
        
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

    # Scale to room size and display
    surface = pygame.transform.scale(surface, (ROOM_WIDTH, ROOM_HEIGHT))  # Scale to room size

    # Clear the screen before drawing
    screen.fill(BLUE)

    # Draw room visualization
    pygame.draw.rect(screen, GREY, room_rect)  # Draw the room
    pygame.draw.rect(screen, ORANGE, room_rect, 2)  # Draw the outline of the room

    # Blit the wave simulation inside the room
    screen.blit(surface, room_rect.topleft)  # Use topleft to place inside the room

    draw_separator()  # Draw the separator line

    # Render GUI
    manager.update(time_delta)  # Update the GUI manager
    manager.draw_ui(screen)      # Draw the GUI elements

    # Update the display using pygame.display.flip()
    pygame.display.flip()  # Present the entire display

pygame.quit()

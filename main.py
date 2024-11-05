import tkinter as tk
from tkinter import filedialog
import pygame
import pygame_gui
import numpy as np
import matplotlib.cm as cm
import json


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
Lx, Ly = 1.0, 1.0  # Domain size
c = 1.0  # Wave speed
nx, ny = 400, 400  # Number of spatial points
dx, dy = Lx / (nx - 1), Ly / (ny - 1)  # Spatial step sizes
dt = 0.001  # Time step size
courant_x = (c * dt / dx) ** 2
courant_y = (c * dt / dy) ** 2
damping_coefficient = 0.01

# Define damping coefficients for materials
material_damping = {
    "Wood": 0.01,
    "Concrete": 0.05,
    "Glass": 0.02
}

# Grid for 2D wave simulation
x = np.linspace(0, Lx, nx)
y = np.linspace(0, Ly, ny)
X, Y = np.meshgrid(x, y)

# Initialize wave arrays
u = np.zeros((ny, nx))  # Current wave state
u_prev = np.zeros((ny, nx))  # Previous wave state
u_next = np.zeros((ny, nx))  # Next wave state
amplitude = 0.00000000001  # Default amplitude for the wave

# List to store impulse positions for multiple waves
impulses = []

# Grid to store walls (True where walls are present)
walls = np.zeros((ny, nx), dtype=bool)

def generate_impulse_at(x_click, y_click):
    """Creates a single impulse at a specific position in the domain based on click coordinates."""
    global u, u_prev, amplitude, impulses
    # Convert the click position to grid indices
    center_x = int((x_click - room_rect.left) / ROOM_WIDTH * nx)
    center_y = int((y_click - room_rect.top) / ROOM_HEIGHT * ny)

    if 0 <= center_x < nx and 0 <= center_y < ny:
        impulses.append((center_x, center_y, amplitude))  # Store position and amplitude of the impulse


def reset_simulation():
    """Resets the wave simulation to its initial state."""
    global u, u_prev, u_next, impulses, walls
    u.fill(0)
    u_prev.fill(0)
    u_next.fill(0)
    impulses.clear()  # Clear all impulses


def load_room_from_json(file_path):
    """Loads room walls from a JSON file and updates the wall grid."""
    global walls
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Reset walls
    walls.fill(False)

    # Parse walls from JSON
    for wall in data.get("walls", []):
        x_start = int(wall["x_start"] / ROOM_WIDTH * nx)
        y_start = int(wall["y_start"] / ROOM_HEIGHT * ny)
        x_end = int(wall["x_end"] / ROOM_WIDTH * nx)
        y_end = int(wall["y_end"] / ROOM_HEIGHT * ny)

        if x_start == x_end:  # Vertical wall
            y_min, y_max = min(y_start, y_end), max(y_start, y_end)
            walls[y_min:y_max + 1, x_start] = True
        elif y_start == y_end:  # Horizontal wall
            x_min, x_max = min(x_start, x_end), max(x_start, x_end)
            walls[y_start, x_min:x_max + 1] = True


def open_room_dialog():
    """Opens a file dialog to select a room JSON file and loads it."""
    file_path = filedialog.askopenfilename()
    if file_path:  # Check if a file was selected
        print(f"Room file selected: {file_path}")
        load_room_from_json(file_path)  # Load the room configuration


def rescale_wave_to_colormap(u):
    """Rescale wave data to a colormap."""
    u_min, u_max = np.min(u), np.max(u)
    norm = (u - u_min) / (u_max - u_min) if u_max > u_min else np.zeros_like(u)
    color_image = cm.jet(norm)[:, :, :3]
    color_image = (color_image * 255).astype(np.uint8)
    return color_image


def update_wave():
    """Update the wave simulation, accounting for damping and wall boundaries."""
    global u, u_prev, u_next
    for (center_y, center_x, amp) in impulses:
        u[center_y, center_x] += amp

    # Update the wave equation with boundary reflections
    u_next[1:-1, 1:-1] = (
        (2 * u[1:-1, 1:-1] - u_prev[1:-1, 1:-1] +
         courant_x * (u[1:-1, 2:] - 2 * u[1:-1, 1:-1] + u[1:-1, :-2]) +
         courant_y * (u[2:, 1:-1] - 2 * u[1:-1, 1:-1] + u[:-2, 1:-1]) -
         damping_coefficient * u[1:-1, 1:-1])
    )

    # Apply wall boundaries (set to zero where walls are present)
    u_next[walls] = 0  # Waves do not propagate through walls

    u_prev = u.copy()
    u = u_next.copy()

# Main Window setup
# Pygame and UI setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Sound Visualization and Wave Simulation")
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# Draw separator line
separator_y = 150  # y-coordinate for the separator line
separator_color = GREY  # Line color


# Function to draw a separator line
def draw_separator():
    pygame.draw.line(screen, separator_color, (550, separator_y), (750, separator_y), 5)


# Tkinter initialization (for file dialog)
root = tk.Tk()
root.withdraw()

# UI Elements
ui_x_start = 550
y_spacing = 50  # Space between elements

room_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((ui_x_start, 50), (200, 40)),
                                           text='Select Room',
                                           manager=manager)

wall_material_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=['Wood', 'Concrete', 'Glass'],
                                                            starting_option='Wood',
                                                            relative_rect=pygame.Rect((ui_x_start, 100 + y_spacing),
                                                                                      (200, 40)),
                                                            manager=manager)

# Amplitude UI Elements
amplitude_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((ui_x_start + 25, 150 + 2 * y_spacing), (150, 20)),
    text="Amplitude",
    manager=manager)

amplitude_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((ui_x_start, 180 + 2 * y_spacing), (200, 25)),
    start_value=amplitude, value_range=(0, 1), manager=manager)

# Frequency UI Elements
frequency_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((ui_x_start + 25, 220 + 3 * y_spacing), (150, 20)),
    text="Frequency",
    manager=manager)

frequency_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((ui_x_start, 250 + 3 * y_spacing), (200, 25)),
    start_value=440, value_range=(20, 2000), manager=manager)
font = pygame.font.Font(None, 20)

# Sound Position Elements
position_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((ui_x_start + 25, 290 + 4 * y_spacing), (150, 20)),
    text="Sound Position",
    manager=manager)

x_position_box = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((ui_x_start, 320 + 4 * y_spacing), (50, 30)),
    manager=manager)
x_position_box.set_text("0")

y_position_box = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((ui_x_start + 100, 320 + 4 * y_spacing), (50, 30)),
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
                damping_coefficient = amplitude #why tutaj jest tak przypisane
                print(amplitude)


        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == room_button:
                open_room_dialog()

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == wall_material_dropdown:
                # Zamiast event.text używamy selected_option bezpośrednio
                selected_material = wall_material_dropdown.selected_option
                if selected_material is not None:
                    damping_coefficient = material_damping.get(selected_material,
                                                               0.01)  # Domyślny współczynnik tłumienia 0.01
                    print(f"Wybrany materiał: {selected_material}, Współczynnik tłumienia: {damping_coefficient}")
                else:
                    print("Brak wybranego materiału!")

                # Handle mouse click to generate an impulse wave at click location
        if event.type == pygame.MOUSEBUTTONDOWN:
            if room_rect.collidepoint(event.pos):
                generate_impulse_at(event.pos[0], event.pos[1])  # Generate wave at mouse click
                wave_active = True

        # Reset simulation with the 'r' key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_simulation()  # Reset the simulation

        manager.process_events(event)


    # Update wave only if the wave has been generated
    if wave_active:
        update_wave()

    # Rescale to grayscale and create pygame surface
    u_color = rescale_wave_to_colormap(u)
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

    amplitude_text = font.render(f'Amplitude: {amplitude:.3f} m', True, WHITE)
    screen.blit(amplitude_text, (ui_x_start, 400 + 4 * y_spacing))  # Adjust position as needed

    # Render GUI
    manager.update(time_delta)  # Update the GUI manager
    manager.draw_ui(screen)  # Draw the GUI elements

    # Update the display using pygame.display.flip()
    pygame.display.flip()  # Present the entire display

pygame.quit()

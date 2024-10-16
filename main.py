import tkinter as tk
from tkinter import filedialog
import pygame
import pygame_gui
import math

# Constants for UI
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
ROOM_WIDTH, ROOM_HEIGHT = 400, 400
GREY = "#A19CA2"
BLUE = "#17283D"
ORANGE = "#FF8C00"
WHITE = "#FFFFFF"
BLACK = "#0e0e0e"

pygame.init()

# Main Window setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sound Wave Visualization')

# Manager for pygame_gui
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# Tkinter initialization (for file dialog)
root = tk.Tk()
root.withdraw()

# UI Elements
room_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 50), (200, 40)),
                                           text='Wybierz Pomieszczenie',
                                           manager=manager)
wall_material_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=['Wood', 'Concrete', 'Glass'],
                                                            starting_option='Wood',
                                                            relative_rect=pygame.Rect((550, 100), (200, 40)),
                                                            manager=manager)

# Draw separator line
separator_y = 150  # y-coordinate for the separator line
separator_color = GREY  # Line color


# Draw a separator line between the sections
def draw_separator():
    pygame.draw.line(screen, separator_color, (550, separator_y), (750, separator_y), 5)


amplitude_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((575, 150), (150, 20)),
    text="Amplituda",
    manager=manager)

amplitude_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((550, 180), (200, 25)),
                                                          start_value=0.5, value_range=(0, 1), manager=manager)

frequency_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((575, 220), (150, 20)),
    text="Częstotliwość",
    manager=manager)

frequency_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((550, 250), (200, 25)),
                                                          start_value=440, value_range=(20, 2000), manager=manager)

# Room Visualization Area
room_rect = pygame.Rect(50, 50, ROOM_WIDTH, ROOM_HEIGHT)
sound_sources = []  # Stores the positions of sound sources
waves = []  # List of waves to simulate
wall_materials = {'Wood': 0.6, 'Concrete': 0.9, 'Glass': 0.8}  # Wall materials with reflection coefficients

# Walls of the room
walls = [
    pygame.Rect(50, 50, ROOM_WIDTH, 10),  # Top wall
    pygame.Rect(50, 50, 10, ROOM_HEIGHT),  # Left wall
    pygame.Rect(50, 50 + ROOM_HEIGHT - 10, ROOM_WIDTH, 10),  # Bottom wall
    pygame.Rect(50 + ROOM_WIDTH - 10, 50, 10, ROOM_HEIGHT)  # Right wall
]


# Function to calculate reflection
def reflect_wave(wave, wall):
    # Reverse the velocity when hitting a wall
    if wall.width > wall.height:  # Horizontal wall (top/bottom)
        wave.velocity.y = -wave.velocity.y
    else:  # Vertical wall (left/right)
        wave.velocity.x = -wave.velocity.x
    # Apply attenuation based on wall material
    material = wall_material_dropdown.selected_option
    wave.amplitude *= wall_materials[material]

# Function to calculate color based on amplitude
def get_wave_color(amplitude):
    max_color = pygame.Color(255, 255, 255)  # White for max amplitude
    min_color = pygame.Color(0, 0, 255)  # Blue for low amplitude
    color = min_color.lerp(max_color, amplitude)  # Interpolate between blue and white
    return color

# Sound wave class
class SoundWave:
    def __init__(self, position, frequency, amplitude):
        self.position = pygame.Vector2(position)
        self.radius = 0  # Start with a radius of 0
        self.frequency = frequency
        self.amplitude = amplitude
        self.lifespan = 500  # Determines how long the wave will be visible

    def update(self):
        self.radius += 2  # Increase the radius to simulate the wave expanding
        self.lifespan -= 1
        self.amplitude *= 0.995  # Dampen the amplitude over time

    def draw(self, surface):
        if self.amplitude > 0.01:
            color = get_wave_color(self.amplitude)  # Get color based on amplitude
            pygame.draw.circle(surface, color, (int(self.position.x), int(self.position.y)), int(self.radius), 2)


# Function to open room selection dialog
def open_room_dialog():
    file_path = filedialog.askopenfilename()
    print(f"Room file selected: {file_path}")  # For now, we'll just print it


# Main Loop
running = True
while running:
    time_delta = pygame.time.Clock().tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle Pygame GUI events
        if event.type == pygame.USEREVENT:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == room_button:
                    open_room_dialog()

        # Click on the room to add a sound source
        if event.type == pygame.MOUSEBUTTONDOWN:
            if room_rect.collidepoint(event.pos):
                # Add a new sound source
                frequency = frequency_slider.get_current_value()
                amplitude = amplitude_slider.get_current_value()
                waves.append(SoundWave(event.pos, frequency, amplitude))

        manager.process_events(event)

    manager.update(time_delta)

    # Draw the room and UI
    screen.fill(BLUE)

    # Draw room visualization
    pygame.draw.rect(screen, GREY, room_rect, 0)
    pygame.draw.rect(screen, ORANGE, room_rect, 2)

    # Draw the sound waves and update them
    for wave in waves[:]:
        wave.update()
        wave.draw(screen)

        # Check for collisions with walls
        for wall in walls:
            if wall.collidepoint(wave.position):
                reflect_wave(wave, wall)

        if wave.lifespan <= 0:
            waves.remove(wave)  # Remove waves that have dissipated

    # Draw the walls
    for wall in walls:
        pygame.draw.rect(screen, GREY, wall)

    draw_separator()
    # Render UI
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()

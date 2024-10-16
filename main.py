import tkinter as tk
from tkinter import filedialog
import pygame
import pygame_gui

# Constants for UI
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
ROOM_WIDTH, ROOM_HEIGHT = 400, 400
GREY = "#A19CA2"
BLUE = "#17283D"
ORANGE = "#292021"
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

position_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((575, 290), (150, 20)),
    text="Położenie dźwięku",
    manager=manager)

x_position_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((550, 320), (50, 30)),
                                                     manager=manager)
x_position_box.set_text("0")

y_position_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((650, 320), (50, 30)),
                                                     manager=manager)
y_position_box.set_text("0")

# Room Visualization Area
room_rect = pygame.Rect(50, 50, ROOM_WIDTH, ROOM_HEIGHT)
sound_position = None  # Will store the sound source's position
points = []


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

        # Click on the room to set the sound source position
        if event.type == pygame.MOUSEBUTTONDOWN:
            if room_rect.collidepoint(event.pos):
                sound_position = event.pos

        manager.process_events(event)

    manager.update(time_delta)

    # Draw the room and UI
    screen.fill(BLUE)

    # Draw room visualization
    pygame.draw.rect(screen, GREY, room_rect, 0)
    pygame.draw.rect(screen, ORANGE, room_rect, 2)

    # Draw the sound source position
    if sound_position:
        pygame.draw.circle(screen, ORANGE, sound_position, 5)

    draw_separator()
    # Render UI
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()

import pygame
import numpy as np

# Initialize pygame
pygame.init()

# Parameters
Lx, Ly = 1.0, 1.0    # Domain size
c = 1.0              # Wave speed
nx, ny = 300, 300    # Number of spatial points
dx, dy = Lx / (nx - 1), Ly / (ny - 1)  # Spatial step sizes
dt = 0.001           # Time step size
courant_x = (c * dt / dx)**2
courant_y = (c * dt / dy)**2
fade_out_factor = 0.9  # Decay factor for fading out the wave

# Grid for 2D wave simulation
x = np.linspace(0, Lx, nx)
y = np.linspace(0, Ly, ny)
X, Y = np.meshgrid(x, y)

# Initialize wave arrays
u = np.zeros((ny, nx))        # Current wave state
u_prev = np.zeros((ny, nx))   # Previous wave state
u_next = np.zeros((ny, nx))   # Next wave state

# Boundary conditions with damping
def apply_damped_boundary_conditions(u, damping_width=20, damping_factor=0.9):
    """Applies boundary conditions with damping near the edges."""
    for i in range(damping_width):
        factor = damping_factor ** i  # Exponential decay factor

        # Damping in x-direction (left and right boundaries)
        u[i, :] *= factor  # Top boundary
        u[-(i+1), :] *= factor  # Bottom boundary

        # Damping in y-direction (top and bottom boundaries)
        u[:, i] *= factor  # Left boundary
        u[:, -(i+1)] *= factor  # Right boundary

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
    # Normalize u to be between 0 and 1
    u_min = np.min(u)
    u_max = np.max(u)

    if u_max == u_min:
        u_rescaled = np.zeros_like(u, dtype=np.uint8)
    else:
        u_normalized = (u - u_min) / (u_max - u_min)
        u_rescaled = (u_normalized * 255).astype(np.uint8)

    grayscale_image = np.stack((u_rescaled,) * 3, axis=-1)

    return grayscale_image

# Function to apply fading out boundary conditions
def apply_fading_boundary_conditions(u, damping_width=30, damping_factor=0.1):
    """Applies fading out boundary conditions near the edges."""
    for i in range(damping_width):
        factor = damping_factor ** i  # Exponential decay factor
        
        # Apply fading effect to the edges of the wave
        u[i, :] *= factor  # Top boundary
        u[-(i + 1), :] *= factor  # Bottom boundary
        u[:, i] *= factor  # Left boundary
        u[:, -(i + 1)] *= factor  # Right boundary

# Time evolution of the wave
def update_wave():
    global u, u_prev, u_next
    u_next[1:-1, 1:-1] = (2 * u[1:-1, 1:-1] - u_prev[1:-1, 1:-1] + 
                          courant_x * (u[1:-1, 2:] - 2 * u[1:-1, 1:-1] + u[1:-1, :-2]) +
                          courant_y * (u[2:, 1:-1] - 2 * u[1:-1, 1:-1] + u[:-2, 1:-1]))
    
    # Apply fading boundary conditions
    apply_fading_boundary_conditions(u_next)
    
    u_prev = u.copy()
    u = u_next.copy()


# Simulation loop
running = True
clock = pygame.time.Clock()
wave_active = False  # Track whether the wave has been triggered

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
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
    
    # Scale to screen size and display
    surface = pygame.transform.scale(surface, screen_size)
    screen.blit(surface, (0, 0))
    
    # Update the display
    pygame.display.flip()
    
    # Limit the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()

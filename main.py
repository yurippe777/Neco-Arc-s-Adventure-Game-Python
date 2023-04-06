import pygame
frame_count = 0
# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the clock
clock = pygame.time.Clock()

# Load the sprites
idle_sprites = [pygame.transform.scale(pygame.image.load('resources/idle/frame0.gif'), (120, 120)),
                pygame.transform.scale(pygame.image.load('resources/idle/frame1.gif'), (120, 120)),
                pygame.transform.scale(pygame.image.load('resources/idle/frame2.gif'), (120, 120)),
                pygame.transform.scale(pygame.image.load('resources/idle/frame3.gif'), (120, 120))]
moving_sprites = [pygame.transform.scale(pygame.image.load('resources/moving/frame0.gif'), (120, 120)),
                  pygame.transform.scale(pygame.image.load('resources/moving/frame1.gif'), (120, 120)),
                  pygame.transform.scale(pygame.image.load('resources/moving/frame2.gif'), (120, 120)),
                  pygame.transform.scale(pygame.image.load('resources/moving/frame3.gif'), (120, 120))]
background_frames = [pygame.image.load(f'resources/backdrop/christmas/frame{i}.gif') for i in range(5)]

# Set the starting sprite and position
current_sprites = idle_sprites
current_sprite_index = 0
player_x = screen_width // 2
player_y = screen_height // 2

# Set up the movement variables
movement_speed = 5
move_left = False
move_right = False
move_up = False
move_down = False
last_direction = "right"

# Set up the background variables
background_frame_index = 0
background_x = 0
background_y = 0
background_speed = 1
background_image = pygame.transform.scale(pygame.image.load('resources/backdrop/christmas/frame0.gif'), (screen_width, screen_height))
background_rect = background_image.get_rect()

# Define a function to handle input events
def handle_input_events():
    global move_left, move_right, move_up, move_down, last_direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
                last_direction = "left"
            elif event.key == pygame.K_d:
                move_right = True
                last_direction = "right"
            elif event.key == pygame.K_w:
                move_up = True
            elif event.key == pygame.K_s:
                move_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            elif event.key == pygame.K_d:
                move_right = False
            elif event.key == pygame.K_w:
                move_up = False
            elif event.key == pygame.K_s:
                move_down = False


# Define a function to update the game state
# Define a function to update the game state
def update():
    global player_x, player_y, current_sprites, current_sprite_index, frame_count, background_image, background_rect

    # Update the player position based on movement keys
    move_vector = pygame.math.Vector2(0, 0)
    if move_left:
        move_vector.x -= movement_speed
    if move_right:
        move_vector.x += movement_speed
    if move_up:
        move_vector.y -= movement_speed
    if move_down:
        move_vector.y += movement_speed
    if move_vector.length() > 0:
        move_vector.normalize_ip()
        move_vector *= movement_speed
        player_x += move_vector.x
        player_y += move_vector.y
        current_sprites = moving_sprites
    else:
        current_sprites = idle_sprites

    # Update the current sprite based on the current frame
    frame_count += 1
    if frame_count >= 5:
        frame_count = 0
        current_sprite_index += 1
        if current_sprite_index >= len(current_sprites):
            current_sprite_index = 0

    # Update the background image
   # background_rect.x -= 1
    #if background_rect.x < -screen_width:
     #   background_rect.x = 0
    screen.blit(background_image, background_rect)

# Define a function to draw the game objects
def draw():
    global background_image, background_rect
    #screen.fill((255, 255, 255))
    if last_direction == "left":
        # Flip the sprite horizontally
        flipped_sprite = pygame.transform.flip(current_sprites[current_sprite_index], True, False)
        screen.blit(flipped_sprite, (player_x, player_y))
    else:
        screen.blit(current_sprites[current_sprite_index], (player_x, player_y))
    pygame.display.update()

# Start the game loop
while True:
    # Handle input events
    handle_input_events()

    # Update the game state
    update()

    # Draw the game objects
    draw()

    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

import os
import sys

import pygame
import math
import json
import random
flip_status = False
frame_count = 0
show_walkable = 0
interaction = 0
game_state = False
# Initialize Pygame
pygame.init()
# Check if quest_flags.txt exists
if os.path.isfile("quest_flags.txt"):
    # Load quest flags from file
    with open("quest_flags.txt", "r") as f:
        quest_flags = json.load(f)
else:
    # Create quest_flags.txt and initialize all flags to false
    quest_flags = {"Knight of Honor": False, "Placeholder": False, "Placeholder 2": False}
    with open("quest_flags.txt", "w") as f:
        json.dump(quest_flags, f)

if os.path.isfile("inventory.txt"):
    # Load inventory from file
    with open("inventory.txt", "r") as f:
        inventory = json.load(f)
else:
    # Create inventory.txt and initialize all items to false
    inventory = {"Excalibur": False, "Bombs": False, "Placeholder3": False}
    with open("inventory.txt", "w") as f:
        json.dump(inventory, f)
# Background Variables
current_map = 'christmas'
# Set up the screen
screen_width = 800         # 800
screen_height = 600        #600
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
background_frames2 = [pygame.image.load(f'resources/backdrop/graveyard/frame_{i}.gif') for i in range(4)]
knight_idle = [pygame.transform.scale(pygame.image.load('resources/npc/knight_idle/frame0.gif'), (250, 250)),
               pygame.transform.scale(pygame.image.load('resources/npc/knight_idle/frame1.gif'), (250, 250)),
               pygame.transform.scale(pygame.image.load('resources/npc/knight_idle/frame2.gif'), (250, 250)),
               pygame.transform.scale(pygame.image.load('resources/npc/knight_idle/frame3.gif'), (250, 250)),]



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
bunny = pygame.transform.scale(pygame.image.load('resources/npc/bunny.png'),(100,100))
# Nested list for determining walkable area in test
ROWS = 12
COLS = 12
walkable_tiles = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
try:
    with open("inventory.txt", "r") as f:
        inventory = json.load(f)
except FileNotFoundError:
    inventory = {}

try:
    with open("quest_flags.txt", "r") as f:
        quest_flags = json.load(f)
except FileNotFoundError:
    quest_flags = {}

# Define a function to handle input events
def handle_input_events():
    global move_left, move_right, move_up, move_down, last_direction, current_map, interaction, game_state
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
            elif event.key == pygame.K_SPACE:
                pass
            elif event.key == pygame.K_e and interaction == 1 and current_map == 'hub':
                rabbit_interact()
            elif event.key == pygame.K_e and interaction == 1 and current_map == 'city':
                knight_interact()
            elif event.key == pygame.K_ESCAPE:
                pause_menu()
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
def update():
    global player_x, player_y, current_sprites, current_sprite_index, frame_count, background_image, background_frame_index
    global current_map, background_frames2
    tile_size_x = int(screen_width / COLS)
    tile_size_y = int(screen_height / ROWS)
    # Update the player position based on movement keys
    move_vector = pygame.math.Vector2(0, 0)
    player_tile_x = int(player_x / tile_size_x)
    player_tile_y = int(player_y / tile_size_y)
    if player_tile_x >= 0 and player_tile_x < COLS and player_tile_y >= 0 and player_tile_y < ROWS:
        if walkable_tiles[player_tile_y][player_tile_x] == 2:
            if (current_map == 'christmas'): hub_teleport()
            elif (current_map == 'hub' and player_x > 600):graveyard_teleport()
            elif (current_map == 'hub' and player_y < 50): island_teleport()
            elif (current_map == 'hub' and player_y <200): house_teleport()
            elif (current_map == 'hub' and player_x >100): cave_teleport()
            elif (current_map == 'hub' and player_x < 70):city_teleport()
            elif(current_map == 'cave'): hub_teleport()
            elif (current_map == 'city'): hub_teleport()
            elif(current_map == 'island'): hub_teleport()
            elif(current_map == 'graveyard'): hub_teleport()
    if move_left:
        move_vector.x -= movement_speed
    if move_right:
        move_vector.x += movement_speed
    if move_up:
        move_vector.y -= movement_speed
    if move_down:
        move_vector.y += movement_speed

    if move_vector.length() > 0:
        # Normalize the vector to get a unit vector
        move_vector.normalize_ip()

        # Move the player in the x direction
        player_x += move_vector.x * movement_speed
        tile_size_x = int(screen_width / COLS)
        player_tile_x = int(player_x / tile_size_x)
        if player_tile_x < 0 or player_tile_x >= COLS or not walkable_tiles[int(player_y / tile_size_y)][player_tile_x]:
            # Player cannot move in the x direction, so revert the movement and set idle sprites
            player_x -= move_vector.x * movement_speed
            move_vector.x = 0
            current_sprites = idle_sprites

        # Move the player in the y direction
        player_y += move_vector.y * movement_speed
        tile_size_y = int(screen_height / ROWS)
        player_tile_y = int(player_y / tile_size_y)
        if player_tile_y < 0 or player_tile_y >= ROWS or not walkable_tiles[player_tile_y][int(player_x / tile_size_x)]:
            # Player cannot move in the y direction, so revert the movement and set idle sprites
            player_y -= move_vector.y * movement_speed
            move_vector.y = 0
            current_sprites = idle_sprites

        # Update the sprites based on the direction of movement
        if move_vector.x == 0 and move_vector.y == 0:
            current_sprites = idle_sprites
        else:
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
    if frame_count % 10 == 0 and current_map == 'christmas':
        background_frame_index += 1
        if background_frame_index >= len(background_frames):
            background_frame_index = 0
        background_image = pygame.transform.scale(background_frames[background_frame_index], (screen_width, screen_height))
    screen.blit(background_image, (0, 0))

    if frame_count % 10 == 0 and current_map == 'graveyard':
        background_frame_index += 1
        if background_frame_index >= len(background_frames2):
            background_frame_index = 0
        background_image = pygame.transform.scale(background_frames2[background_frame_index], (screen_width, screen_height))

    screen.blit(background_image, (0, 0))



def draw():
    global background_image, bunny, interaction, game_state, current_map,knight_idle, npc_locations
    bunny_y = 330 + 5 * math.sin(pygame.time.get_ticks() / 200)
    if current_map == 'hub':
        npc_maker(440,bunny_y,bunny)
    if current_map == 'city':
        npc_maker(50,350,knight_idle)
    if last_direction == "left":
        # Flip the sprite horizontally
        flipped_sprite = pygame.transform.flip(current_sprites[current_sprite_index], True, False)
        screen.blit(flipped_sprite, (player_x, player_y))
    else:
        screen.blit(current_sprites[current_sprite_index], (player_x, player_y))

    pygame.display.update()

def rabbit_interact():
    quit()


import pygame

def knight_interact():

    # Set up the window
    size = (800, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Knight Interact")

    # Set up the game variables
    my_score = 0
    ball_x = 400
    ball_y = 300
    ball_dx = .4
    ball_dy = .4
    paddle_y = 250
    paddle_h = 200
    hits = 0
    paddle_speed = 0

    # Game loop
    game_state = True
    while game_state:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = False
                elif event.key == pygame.K_w:
                    # Move paddle up continuously while the key is held down
                    paddle_speed = -1.5
                elif event.key == pygame.K_s:
                    # Move paddle down continuously while the key is held down
                    paddle_speed = 1.5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    # Stop moving paddle
                    paddle_speed = 0

        # Update the paddle position
        paddle_y += paddle_speed

        # Update the ball position
        ball_x += ball_dx
        ball_y += ball_dy

        # Check if the ball hit the paddle
        if ball_x <= 20 and paddle_y <= ball_y <= paddle_y + paddle_h:
            ball_dx = abs(ball_dx) * 1.1
            ball_dy = ball_dy * random.uniform(0.8, 1.2)
            hits += 1

        # Check if the ball hit the wall
        if ball_y < 0 or ball_y > 580:
            ball_dy = -ball_dy

        # Check if the ball went out of bounds
        if ball_x < 0:
            game_state = False
        elif ball_x > 780:
            ball_dx = -ball_dx

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the ball
        pygame.draw.circle(screen, (255, 255, 255), (ball_x, ball_y), 10)

        # Draw the paddle
        pygame.draw.rect(screen, (255, 255, 255), (10, paddle_y, 10, paddle_h))

        # Draw the score
        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(hits), True, (255, 255, 255))
        screen.blit(text, (50, 20))

        # Update the display
        pygame.display.flip()


def npc_maker(bunny_x, bunny_y, images):
    global background_image, interaction, player_x, player_y, flip_status, current_map

    if current_map == 'hub' or current_map == 'city':
        if isinstance(images, list):
            image_index = pygame.time.get_ticks() // 200 % len(images)  # Change image every 5 frames (200 milliseconds)
            image = images[image_index]
            if flip_status:
                image = pygame.transform.flip(image, True, False)  # Flip the image if flip_status is True
        else:
            image = images
            if flip_status:
                image = pygame.transform.flip(image, True, False)  # Flip the image if flip_status is True

        screen.blit(image, (bunny_x, bunny_y))

        # Check if player is near bunny
        if abs(player_x - bunny_x) < 50 and abs(player_y - bunny_y) < 50:
            # Draw "Press E to interact" message above player's head
            font = pygame.font.Font(None, 25)
            text = "Press E to interact"
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.center = (player_x, player_y - 50)

            # Draw a red box around the text
            box_width, box_height = text_surface.get_width() + 20, text_surface.get_height() + 10
            box_rect = pygame.Rect((0, 0), (box_width, box_height))
            box_rect.center = (player_x, player_y - 50)
            pygame.draw.rect(screen, (255, 0, 0), box_rect)

            screen.blit(text_surface, text_rect)

            # Set interaction to 1
            interaction = 1
        else:
            # Set interaction to 0
            interaction = 0

        # Flip the image randomly
        if pygame.time.get_ticks() // 1000 % 3 == 0 and random.random() < 0.01 and current_map == 'city':
            flip_status = not flip_status  # Invert the flip status

def pause_menu():
    global game_state, inventory, quest_flags

    # Set game state to paused
    game_state = False

    # Create a list of menu options
    menu_options = ["Inventory", "Save", "New Game"]
    selected_option = 0
    backdrop = pygame.image.load('resources/backdrop/loading/frame0.png')
    screen.blit(backdrop, (0, 0))
    while True:
        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Resume the game and return from the function
                    game_state = True
                    return
                elif event.key == pygame.K_w:
                    # Move the selection up
                    selected_option = (selected_option - 1) % len(menu_options)
                    screen.blit(backdrop, (0, 0))
                elif event.key == pygame.K_s:
                    # Move the selection down
                    selected_option = (selected_option + 1) % len(menu_options)
                    screen.blit(backdrop, (0, 0))
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Execute the selected option
                    if selected_option == 0:
                        print("Opening inventory...")
                    elif selected_option == 1:
                        print("Saving game...")
                        with open("inventory.txt", "w") as f:
                            json.dump(inventory, f)
                        with open("quest_flags.txt", "w") as f:
                            json.dump(quest_flags, f)
                    elif selected_option == 2:
                        print("Starting new game...")
                        quest_flags = {"Knight of Honor": False}
                        inventory = {"Excalibur": False, "Bombs": False}


        # Clear the screen
       # screen.fill((0, 0, 0))

        # Draw the menu options
        font = pygame.font.Font(None, 36)
        for i, option in enumerate(menu_options):
            text = font.render(option, True, (50, 205, 50))
            outline = font.render(option, True, (0, 0, 0))
            rect = text.get_rect(center=(400, 200 + i * 50))
            outline_rect = rect.copy()
            outline_rect.inflate_ip(4, 4)  # Make the outline slightly larger
            outline_rect.center = rect.center
            if i == selected_option:
                # Highlight the selected option
                pygame.draw.rect(screen, (255, 0, 0), rect, 3)
            screen.blit(outline, outline_rect)
            screen.blit(text, rect)

        # Update the display
        pygame.display.flip()
def teleport(new_bg_path, new_walkable_tiles, new_player_x, new_player_y):
    global background_image, walkable_tiles, player_x, player_y, current_map
    # Load the new background image
    if (current_map == 'christmas'): current_map = 'hub'
    elif (current_map == 'hub' and player_x > 600):current_map = 'graveyard'
    elif (current_map == 'hub' and player_y < 50): current_map = 'island'
    elif (current_map == 'hub' and player_y < 300): current_map = 'christmas'
    elif (current_map == 'hub' and player_x > 100): current_map = 'cave'
    elif (current_map == 'hub' and player_x < 70): current_map = 'city'
    elif (current_map == 'graveyard'): current_map = 'hub'
    elif (current_map == 'city'): current_map = 'hub'
    elif (current_map == 'cave'): current_map = 'hub'
    elif (current_map == 'island'): current_map = 'hub'
    if (current_map != 'christmas'):
        del background_image
        background_image = pygame.image.load(new_bg_path).convert()
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Update the walkable tiles and player coordinates
    walkable_tiles = new_walkable_tiles
    player_x = new_player_x
    player_y = new_player_y
def hub_teleport():
    global moving_sprites, idle_sprites, movement_speed
    if current_map == "city":
        x, y = 100, 350
    elif current_map == 'graveyard':
        x, y = 550, 1
    elif current_map == "cave":
        x, y = 150, 450
        idle_sprites.clear()
        moving_sprites.clear()
        idle_sprites = [pygame.transform.scale(pygame.image.load('resources/idle/frame0.gif'), (120, 120)),
                        pygame.transform.scale(pygame.image.load('resources/idle/frame1.gif'), (120, 120)),
                        pygame.transform.scale(pygame.image.load('resources/idle/frame2.gif'), (120, 120)),
                        pygame.transform.scale(pygame.image.load('resources/idle/frame3.gif'), (120, 120))]
        moving_sprites = [pygame.transform.scale(pygame.image.load('resources/moving/frame0.gif'), (120, 120)),
                          pygame.transform.scale(pygame.image.load('resources/moving/frame1.gif'), (120, 120)),
                          pygame.transform.scale(pygame.image.load('resources/moving/frame2.gif'), (120, 120)),
                          pygame.transform.scale(pygame.image.load('resources/moving/frame3.gif'), (120, 120))]
        movement_speed = 5
    elif current_map == "island":
        x, y = 500, 1
        idle_sprites.clear()
        moving_sprites.clear()
        idle_sprites = [pygame.transform.scale(pygame.image.load('resources/idle/frame0.gif'), (120, 120)),
                        pygame.transform.scale(pygame.image.load('resources/idle/frame1.gif'), (120, 120)),
                        pygame.transform.scale(pygame.image.load('resources/idle/frame2.gif'), (120, 120)),
                        pygame.transform.scale(pygame.image.load('resources/idle/frame3.gif'), (120, 120))]
        moving_sprites = [pygame.transform.scale(pygame.image.load('resources/moving/frame0.gif'), (120, 120)),
                          pygame.transform.scale(pygame.image.load('resources/moving/frame1.gif'), (120, 120)),
                          pygame.transform.scale(pygame.image.load('resources/moving/frame2.gif'), (120, 120)),
                          pygame.transform.scale(pygame.image.load('resources/moving/frame3.gif'), (120, 120))]
        movement_speed = 5
    else:
        x, y = 75, 110
    teleport("resources/backdrop/hub/frame0.png",
             [[1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2],
              [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
             x, y)



def house_teleport():
    teleport("resources/backdrop/christmas/frame0.png",
             [
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                 [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
                 [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                 [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                 [1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
             ],300,380)
def city_teleport():
    teleport("resources/backdrop/city/frame0.gif",[
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2]
    ],700,400)
def cave_teleport():
    global idle_sprites, moving_sprites, movement_speed
    # Clear the existing player sprites
    idle_sprites.clear()
    moving_sprites.clear()

    # Load the shrunken player sprites
    idle_sprites.append(pygame.transform.scale(pygame.image.load('resources/idle/frame0.gif'), (50, 50)))
    idle_sprites.append(pygame.transform.scale(pygame.image.load('resources/idle/frame1.gif'), (50, 50)))
    idle_sprites.append(pygame.transform.scale(pygame.image.load('resources/idle/frame2.gif'), (50, 50)))
    idle_sprites.append(pygame.transform.scale(pygame.image.load('resources/idle/frame3.gif'), (50, 50)))
    moving_sprites.append(pygame.transform.scale(pygame.image.load('resources/moving/frame0.gif'), (50, 50)))
    moving_sprites.append(pygame.transform.scale(pygame.image.load('resources/moving/frame1.gif'), (50, 50)))
    moving_sprites.append(pygame.transform.scale(pygame.image.load('resources/moving/frame2.gif'), (50, 50)))
    moving_sprites.append(pygame.transform.scale(pygame.image.load('resources/moving/frame3.gif'), (50, 50)))
    movement_speed = 2.083
    # Teleport the player
    teleport("resources/backdrop/cave/frame0.png",
             [[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
              [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0],
              [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0],
              [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
             360, 230)

def island_teleport():
    global idle_sprites, moving_sprites, movement_speed
    # Clear the existing player sprites
    idle_sprites.clear()
    moving_sprites.clear()

    # Load the shrunken player sprites
    idle_sprites.append(pygame.transform.scale(pygame.image.load('resources/idle/frame0.gif'), (60, 60)))
    idle_sprites.append(pygame.transform.scale(pygame.image.load('resources/idle/frame1.gif'), (60, 60)))
    idle_sprites.append(pygame.transform.scale(pygame.image.load('resources/idle/frame2.gif'), (60, 60)))
    idle_sprites.append(pygame.transform.scale(pygame.image.load('resources/idle/frame3.gif'), (60, 60)))
    moving_sprites.append(pygame.transform.scale(pygame.image.load('resources/moving/frame0.gif'), (60, 60)))
    moving_sprites.append(pygame.transform.scale(pygame.image.load('resources/moving/frame1.gif'), (60, 60)))
    moving_sprites.append(pygame.transform.scale(pygame.image.load('resources/moving/frame2.gif'), (60, 60)))
    moving_sprites.append(pygame.transform.scale(pygame.image.load('resources/moving/frame3.gif'), (60, 60)))
    movement_speed = 2.5
    teleport("resources/backdrop/island/frame0.png",
        [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1]],270,530)
def graveyard_teleport():
    teleport("resources/backdrop/graveyard/frame_0.gif",
             [[0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
              [0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0],
              [1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
              [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
              [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
              [2, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0],
              [0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0],
              [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
             5, 200)
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
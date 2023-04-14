import os
import sys
import time
import pygame
import math
import json
import random
from pygame import mixer
fruit_caught = 0
fail_index = 0
beam_attack = 0
beam_start = 0
stale_player_x2 = 0
stale_player_y2 = 0
x_ref = 5
y_ref = 20
Slime_location = 0
balloons_popped = 0
counter = 0
bomb_det = 0
my_score = 0
flip_status = False
frame_count = 0
show_walkable = 0
interaction = 0
game_state = False

# Starting the mixer
mixer.init()

# Loading the song
mixer.music.load("resources/music/lobby.mp3")

# Setting the volume
mixer.music.set_volume(0.5)

# Start playing the song
mixer.music.play()

# Initialize Pygame
pygame.init()
# Check if quest_flags.txt exists
if os.path.isfile("quest_flags.txt"):
    # Load quest flags from file
    with open("quest_flags.txt", "r") as f:
        quest_flags = json.load(f)
else:
    # Create quest_flags.txt and initialize all flags to false
    quest_flags = {"Knight of Honor": False, "Boulder": False, "Archery": False, "Slime": False, "holy_grail": False}
    with open("quest_flags.txt", "w") as f:
        json.dump(quest_flags, f)

if os.path.isfile("inventory.txt"):
    # Load inventory from file
    with open("inventory.txt", "r") as f:
        inventory = json.load(f)
else:
    # Create inventory.txt and initialize all items to false
    inventory = {"Bombs": False, "Bunny Bag": False, "Boat": False, "GoB": False, "Beam": False}
    with open("inventory.txt", "w") as f:
        json.dump(inventory, f)
# Background Variables
current_map = 'christmas'
# Set up the screen
screen_width = 800         # 800
screen_height = 600        # 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the clock
clock = pygame.time.Clock()

# Load the sprites
if quest_flags["holy_grail"] == False:
    idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle/frame{i}.gif'), (120, 120)) for i in
                    range(4)]
else: idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle_2/frame{i}.gif'), (120, 120)) for i in range(4)]
moving_sprites = [pygame.transform.scale(pygame.image.load(f'resources/moving/frame{i}.gif'), (120, 120)) for i in range(4)]
background_frames = [pygame.image.load(f'resources/backdrop/christmas/frame{i}.gif') for i in range(5)]
background_frames2 = [pygame.image.load(f'resources/backdrop/graveyard/frame_{i}.gif') for i in range(4)]
background_frames3 = [pygame.image.load(f'resources/backdrop/holy_grail/frame_{i:03d}_delay-0.04s.gif') for i in range(108)]
beams = [pygame.transform.scale(pygame.image.load(f'resources/inventory/beam_attack/frame{i}.png'), (300, 300)) for i in range(16)]
ghost = [pygame.transform.scale(pygame.image.load(f'resources/npc/Ghost/frame{i}.png'), (300, 300)) for i in range(16)]
knight_idle = [pygame.transform.scale(pygame.image.load(f'resources/npc/knight_idle/frame{i}.gif'), (250, 250)) for i in range(4)]
bomb_img = pygame.transform.scale(pygame.image.load('resources/inventory/bomb.png'), (75,75))
bomb_explosion = [pygame.transform.scale(pygame.image.load(f'resources/inventory/frame_{i}.png'), (75, 75)) for i in range(4)]
portal = [pygame.transform.scale(pygame.image.load(f'resources/inventory/tile{i}.png'), (150, 150)) for i in range(4)]
boulder = pygame.transform.scale(pygame.image.load('resources/map_objects/boulder.png'), (200, 200))
boating = [pygame.transform.scale(pygame.image.load(f'resources/boating/frame{i}.gif'), (120, 120)) for i in range(2)]
Slime = [pygame.transform.scale(pygame.image.load(f'resources/map_objects/frame{i}.png'), (75, 75)) for i in range(4)]
GoB = pygame.transform.scale(pygame.image.load('resources/inventory/portal_key.png'), (125, 125))
holy_grail = pygame.transform.scale(pygame.image.load('resources/map_objects/holy_grail.png'), (200, 200))
archer_frames = []
for i in range(12):
    frame = pygame.transform.scale(pygame.image.load(f"resources/npc/archer_elf/frame{i}.png"), (600, 300))
    archer_frames.append(frame)
# Set the starting sprite and position
current_sprites = idle_sprites
current_sprite_index = 0
player_x = screen_width // 2
player_y = screen_height // 2
stale_player_x = 0
stale_player_y = 0
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
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0],
    [1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 0],
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
    global move_left, move_right, move_up, move_down, last_direction, current_map, interaction, game_state, player_x, player_y, bomb_explosion, stale_player_x, stale_player_y
    global stale_player_x, stale_player_y, GoB, stale_player_x2, stale_player_y2, portal, beam_attack, quest_flags, inventory
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
            elif event.key == pygame.K_b and inventory["Bombs"] == True:
                stale_player_x = player_x
                stale_player_y = player_y
            elif stale_player_x != 0 and event.key == pygame.K_e:
                bomb_interact()
                # Load a sound effect
                sound_effect = pygame.mixer.Sound("resources/music/bomb.wav")
                # Play the sound effect over the music
                sound_effect.play()
            elif event.key == pygame.K_f and quest_flags["holy_grail"] == False and inventory["Beam"] == True and abs(player_x - 400) <= 50 and abs(player_y - 300) <= 50 and current_map == 'holygrail':
                beam_attack = 1
                quest_flags["holy_grail"] = True
                # Load a sound effect
                sound_effect = pygame.mixer.Sound("resources/music/win.wav")
                # Play the sound effect over the music
                sound_effect.play()
                end_function()
            elif event.key == pygame.K_f and inventory["Beam"] == True:
                beam_attack = 1
                # Load a sound effect
                sound_effect = pygame.mixer.Sound("resources/music/beam.wav")
                # Play the sound effect over the music
                sound_effect.play()
            elif event.key == pygame.K_e and interaction == 1 and current_map == 'hub':
                rabbit_interact()
            elif event.key == pygame.K_e and interaction == 1 and current_map == 'city':
                knight_interact()
            elif event.key == pygame.K_e and interaction == 1 and current_map == 'cave':
                elf_interact()
            elif event.key == pygame.K_e and interaction == 1 and current_map == 'graveyard':
                ghost_interact()
            elif event.key == pygame.K_e and interaction == 1 and current_map == 'island':
                inventory["GoB"] = True
                # Load a sound effect
                sound_effect = pygame.mixer.Sound("resources/music/win.wav")
                # Play the sound effect over the music
                sound_effect.play()
            elif event.key == pygame.K_e and interaction == 1 and current_map == 'holygrail' and quest_flags['holy_grail'] == False:
                holy_grail_interact()
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
    global player_x, player_y, current_sprites, current_sprite_index, frame_count, background_image, background_frame_index, boating,music_paths
    global current_map, background_frames2, background_frames3
    tile_size_x = int(screen_width / COLS)
    tile_size_y = int(screen_height / ROWS)
    # Update the player position based on movement keys
    move_vector = pygame.math.Vector2(0, 0)
    player_tile_x = int(player_x / tile_size_x)
    player_tile_y = int(player_y / tile_size_y)
    if player_tile_x >= 0 and player_tile_x < COLS and player_tile_y >= 0 and player_tile_y < ROWS:
        if walkable_tiles[player_tile_y][player_tile_x] == 2:
            if (current_map == 'christmas' and player_x < 410): hub_teleport()
            elif(current_map == 'holygrail'): alter_teleport()
            elif (current_map == 'alter' and player_y > 400): house_teleport()
            elif (current_map == 'alter' and player_y < 400): holy_grail_teleport()
            elif (current_map == 'christmas' and player_x > 410 and inventory['GoB'] == True): alter_teleport()
            elif (current_map == 'hub' and player_x > 600):graveyard_teleport()
            elif (current_map == 'hub' and player_y < 50): island_teleport()
            elif (current_map == 'hub' and player_y <200): house_teleport()
            elif (current_map == 'hub' and player_x >100 and quest_flags["Boulder"] == True): cave_teleport()
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
        if player_tile_x < 0 or player_tile_x >= COLS or not walkable_tiles[int(player_y / tile_size_y)][player_tile_x] or (walkable_tiles[player_tile_y][player_tile_x] == 3 and inventory['Boat']==False) or walkable_tiles[player_tile_y][player_tile_x] == 4 :
            # Player cannot move in the x direction, so revert the movement and set idle sprites
            player_x -= move_vector.x * movement_speed
            move_vector.x = 0
            current_sprites = idle_sprites

        # Move the player in the y direction
        player_y += move_vector.y * movement_speed
        tile_size_y = int(screen_height / ROWS)
        player_tile_y = int(player_y / tile_size_y)
        if player_tile_y < 0 or player_tile_y >= ROWS or not walkable_tiles[player_tile_y][int(player_x / tile_size_x)]or (walkable_tiles[player_tile_y][player_tile_x] == 3 and inventory['Boat']== False) or walkable_tiles[player_tile_y][player_tile_x] == 4:
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
    if player_tile_y >= 0 and player_tile_y < len(walkable_tiles) and player_tile_x >= 0 and player_tile_x < len(
            walkable_tiles[0]):
        if walkable_tiles[player_tile_y][player_tile_x] == 3:
            if inventory["Boat"] == True:
                current_sprites = boating
            else:
                current_sprites = idle_sprites
    # Update the current sprite based on the current frame
    if current_map == 'island' and walkable_tiles[player_tile_y][player_tile_x] == 4:
        current_sprites = boating
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

    if frame_count % 10 == 0 and current_map == 'holygrail':
        background_frame_index += 1
        if background_frame_index >= len(background_frames3):
            background_frame_index = 0
        background_image = pygame.transform.scale(background_frames3[background_frame_index], (screen_width, screen_height))
    screen.blit(background_image, (0, 0))



def draw():
    global background_image, bunny, interaction, game_state, current_map,knight_idle, npc_locations, stale_player_x, stale_player_y, bomb_det, counter, Slime, Slime_location
    global x_ref,y_ref, GoB, stale_player_x2, stale_player_y2, portal,beams, move_up,move_right,move_left,move_down,last_direction,beam_start, ghost, holy_grail, music_paths
    bunny_y = 330 + 5 * math.sin(pygame.time.get_ticks() / 200)
    if (current_map == 'christmas' or current_map == 'alter') and inventory["GoB"] == True:
        npc_maker(650,440,portal)
    if current_map == 'hub':
        npc_maker(440,bunny_y,bunny)
    if current_map == 'hub':
        if not quest_flags["Boulder"]:
            npc_maker(150, 450, boulder)
    if current_map == 'city':
        npc_maker(50,350,knight_idle)
    if current_map == 'graveyard':
        npc_maker(280,150,ghost)
    if current_map == 'holygrail' and quest_flags['holy_grail'] == False:
        npc_maker(320,150,holy_grail)
    if beam_attack == 1:
        beam_start = 1
        if (move_up == True and move_left == False and move_right == False):
            npc_maker(player_x- 90,player_y-250,beams)
        elif (move_left == True):
            npc_maker(player_x -250, player_y-90, beams)
        elif (move_down == True and move_left == False and move_right == False):
            npc_maker(player_x - 90, player_y + 90, beams)
        elif (move_right == True):
            npc_maker(player_x+90, player_y-90 ,beams)
        else: npc_maker(player_x- 90,player_y-250,beams)
    if current_map == 'island' and not quest_flags["Slime"]:
        if current_map == 'island' and Slime_location == 0 and \
                abs(player_x - 5) < 76 and abs(player_y - 20) < 76:
            x_ref = 300
            y_ref = 0
            Slime_location += 1
        if current_map == 'island' and Slime_location == 1 and \
                abs(player_x - 300) < 76 and abs(player_y - 0) < 76:
            x_ref = 500
            y_ref = 500
            Slime_location += 1
        if current_map == 'island'  and Slime_location == 2 and \
                abs(player_x - 500) < 76 and abs(player_y - 500) < 76:
            x_ref = 5
            y_ref = 20
            Slime_location = 0
        npc_maker(x_ref,y_ref,Slime)
    if stale_player_x != 0 and bomb_det == 0:
        npc_maker(stale_player_x,stale_player_y,bomb_img)
    if stale_player_x2 != 0:
        npc_maker(stale_player_x2, stale_player_y2, portal)
    if stale_player_x != 0 and bomb_det == 1:
        npc_maker(stale_player_x, stale_player_y, bomb_explosion)
        counter = counter + 1
        if current_map == "hub" and abs(stale_player_x - 150) < 75 and abs(stale_player_y - 450) < 75:
            quest_flags["Boulder"] = True
        if current_map == "island" and abs(stale_player_x - x_ref) < 75 and abs(stale_player_y - y_ref)<75:
            quest_flags["Slime"] = True
        if counter == 90:
            stale_player_x = 0
            stale_player_y = 0
            counter = 0
            bomb_det = 0
    if current_map == 'cave':
         npc_maker(300,260,archer_frames)
    if current_map == 'island' and inventory["GoB"] == False and quest_flags["Slime"] == True:
        npc_maker(x_ref,y_ref,GoB)
    if last_direction == "left":
        # Flip the sprite horizontally
        flipped_sprite = pygame.transform.flip(current_sprites[current_sprite_index % len(current_sprites)], True,
                                               False)
        screen.blit(flipped_sprite, (player_x, player_y))
    else:
        screen.blit(current_sprites[current_sprite_index % len(current_sprites)], (player_x, player_y))

    pygame.display.update()
def bomb_interact():
    global bomb_det
    bomb_det = 1
def end_function():
    global idle_sprites
    knight_name = "World Saved"
    knight_comment = "You have saved the world from the corrupted grail, and have protected the world from harm"
    knight_comment2 = "You have been rewarded with a new idle animation!"
    knight_comment3 = "Thank you for playing my game! (@yurippe777 on GitHub)"

    # Set up font and text objects
    font = pygame.font.SysFont("Arial", 18)
    knight_name_text = font.render(knight_name, True, (255, 255, 255))
    knight_comment_text = font.render(knight_comment, True, (255, 255, 255))
    knight_comment2_text = font.render(knight_comment2, True, (255, 255, 255))
    knight_comment3_text = font.render(knight_comment3, True, (255, 255, 255))
    screen.blit(knight_name_text, (10, 400))
    screen.blit(knight_comment_text, (10, 450))
    screen.blit(knight_comment2_text, (10, 500))
    screen.blit(knight_comment3_text, (10, 550))
    pygame.display.flip()

    # Wait a few seconds
    time.sleep(10)
    idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle_2/frame{i}.gif'), (120, 120)) for i in
                    range(4)]
def holy_grail_interact():
    pygame.init()

    # Set up screen
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Set up initial variables
    knight_name = "Holy Grail"
    knight_comment = "It is said to possess immense magical powers and the ability to grant wishes."
    knight_comment2 = "It is fully corrupted, and is a threat to all of mankind."
    knight_comment3 = "You know what you must do to protect your homeland and those who you hold dear."

    # Set up font and text objects
    font = pygame.font.SysFont("Arial", 20)
    knight_name_text = font.render(knight_name, True, (255, 255, 255))
    knight_comment_text = font.render(knight_comment, True, (255, 255, 255))
    knight_comment2_text = font.render(knight_comment2, True, (255, 255, 255))
    knight_comment3_text = font.render(knight_comment3, True, (255,255,255))
    screen.blit(knight_name_text, (10, 10))
    screen.blit(knight_comment_text, (10, 50))
    screen.blit(knight_comment2_text, (10, 100))
    screen.blit(knight_comment3_text, (10, 150))
    pygame.display.flip()

    # Wait a few seconds
    time.sleep(7)
def ghost_interact():
    global fruit_caught
    pygame.init()

    # Set up screen
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Set up initial variables
    knight_name = "Gravestone"
    knight_comment = "Ye who seek strength, try thy might in this game of the dead,"
    knight_comment2 = "you must catch 100 souls, but beware! With each collected soul"
    knight_comment3 = "your job becomes more difficult, and the amount of souls left to collect"
    knight_challenge = "becomes smaller and smaller!"

    # Set up font and text objects
    font = pygame.font.SysFont("Arial", 20)
    knight_name_text = font.render(knight_name, True, (255, 255, 255))
    knight_comment_text = font.render(knight_comment, True, (255, 255, 255))
    knight_comment2_text = font.render(knight_comment2, True, (255, 255, 255))
    knight_comment3_text = font.render(knight_comment3, True, (255,255,255))
    knight_challenge_text = font.render(knight_challenge, True, (255, 255, 255))
    if fruit_caught == 0:
        # Display text
        screen.blit(knight_name_text, (10, 10))
        screen.blit(knight_comment_text, (10, 50))
        screen.blit(knight_comment2_text, (10, 100))
        screen.blit(knight_comment3_text, (10, 150))
        screen.blit(knight_challenge_text, (10, 200))
        pygame.display.flip()

        # Wait a few seconds
        time.sleep(8)

        # Call second interaction function
        ghost_interact2()
    elif fruit_caught > 0 and fruit_caught < 100:
        balloons_popped = 0
    elif fruit_caught >= 100:
        balloons_popped = 0
        knight_name = "Gravestone"
        knight_comment = "Congrats, you have been blessed by the dead, and have gained the ability"
        knight_comment2 = "known as instant death beam, it is said to be strong enough to destroy anything in"
        knight_challenge = "its path. Use it by pressing F."
        font = pygame.font.SysFont("Arial", 24)
        knight_name_text = font.render(knight_name, True, (255, 255, 255))
        knight_comment_text = font.render(knight_comment, True, (255, 255, 255))
        knight_comment2_text = font.render(knight_comment2, True, (255, 255, 255))
        knight_challenge_text = font.render(knight_challenge, True, (255, 255, 255))
        # Display text
        screen.blit(knight_name_text, (10, 10))
        screen.blit(knight_comment_text, (10, 50))
        screen.blit(knight_comment2_text, (10, 100))
        screen.blit(knight_challenge_text, (10, 150))
        pygame.display.flip()
        time.sleep(8)
        inventory['Beam'] = True
        # Load a sound effect
        sound_effect = pygame.mixer.Sound("resources/music/win.wav")
        # Play the sound effect over the music
        sound_effect.play()
def ghost_interact2():
    global fruit_caught
    # Initialize game variables
    screen_width = 800
    screen_height = 600
    background_color = (255, 255, 255)
    fruit_color = (255, 0, 0)
    player_color = (0, 0, 255)
    player_width = 200
    player_height = 50
    player_speed = 1.2
    fruit_width = 25
    fruit_height = 25
    fruit_count = 40
    fruits_missed = 0
    fruit_caught = 0
    fruit_speed = .1 + (.005 * fruit_caught)
    font_size = 32
    font_color = (0, 0, 0)
    font_type = pygame.font.SysFont('', font_size)

    # Initialize Pygame and set up the screen
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Fruit Grab")

    # Initialize the player position
    player_x = screen_width // 2
    player_y = screen_height - player_height

    # Create a list to hold the fruit
    fruit_list = []

    # Set up the game clock
    clock = pygame.time.Clock()

    # Main game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move the player based on keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_d] and player_x < screen_width - player_width:
            player_x += player_speed

        # Spawn a new fruit at random position
        if len(fruit_list) < fruit_count:
            fruit_x = random.randint(0, screen_width - fruit_width)
            fruit_y = random.randint(-1000,0)
            fruit_list.append([fruit_x, fruit_y])

        # Move the fruit down the screen
        for i in range(len(fruit_list)):
            fruit_list[i][1] += fruit_speed

        # Check if any fruit has been caught by the player
        for fruit in fruit_list:
            fruit_rect = pygame.Rect(fruit[0], fruit[1], fruit_width, fruit_height)
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
            if player_rect.colliderect(fruit_rect):
                fruit_list.remove(fruit)
                fruit_caught += 1
                fruit_speed = .1 + (.005 * fruit_caught)

        # Clear the screen
        screen.fill(background_color)

        # Draw the player
        pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))

        # Draw the fruit
        for fruit in fruit_list:
            pygame.draw.rect(screen, fruit_color, (fruit[0], fruit[1], fruit_width, fruit_height))

        # Draw the score
        score_text = font_type.render("Score: " + str(fruit_caught), True, font_color)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Check if the game has ended
        if fruit_caught >= 100:
            game_over_text = font_type.render("You Win!", True, font_color)
            screen.blit(game_over_text, (screen_width // 2 - font_size, screen_height // 2 - font_size))
            pygame.display.flip()
            pygame.time.wait(3000)
            return
        if all(fruit[1] > 600 for fruit in fruit_list) and fruit_caught > 0:
            game_over_text = font_type.render("You Lose!", True, font_color)
            screen.blit(game_over_text, (screen_width // 2 - font_size, screen_height // 2 - font_size))
            pygame.display.flip()
            pygame.time.wait(3000)
            return

def rabbit_interact():
    pygame.init()

    # Set up screen
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Set up initial variables
    if inventory['Bunny Bag'] == False:
        knight_name = "Boating Bunny"
        knight_comment = "It's terrible! I was in the cave when all of a sudden a boulder"
        knight_comment2 = "chased me, and I dropped my bag on the way out!"
        knight_comment3 = "Do you think you can retrieve it for me? I can let you use the boat"
        knight_challenge = "if you do."
    else:
        knight_name = "Boating Bunny"
        knight_comment = "Thank you for getting my bag back to me! Water should no longer hinder you."
        knight_comment2 = "Just make sure to be careful out on the open seas for my sake, ok?"
        knight_comment3 = ""
        knight_challenge = ""
        inventory['Boat'] = True
        # Load a sound effect
        sound_effect = pygame.mixer.Sound("resources/music/win.wav")
        # Play the sound effect over the music
        sound_effect.play()
    # Set up font and text objects
    font = pygame.font.SysFont("Arial", 20)
    knight_name_text = font.render(knight_name, True, (255, 255, 255))
    knight_comment_text = font.render(knight_comment, True, (255, 255, 255))
    knight_comment2_text = font.render(knight_comment2, True, (255, 255, 255))
    knight_comment3_text = font.render(knight_comment3, True, (255, 255, 255))
    knight_challenge_text = font.render(knight_challenge, True, (255, 255, 255))

    # Display text
    screen.blit(knight_name_text, (10, 10))
    screen.blit(knight_comment_text, (10, 50))
    screen.blit(knight_comment2_text, (10, 100))
    screen.blit(knight_comment3_text, (10, 150))
    screen.blit(knight_challenge_text, (10, 200))
    pygame.display.flip()
    time.sleep(8)
def elf_interact():
    global balloons_popped
    pygame.init()

    # Set up screen
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Set up initial variables
    knight_name = "Elven Archer"
    knight_comment = "I have stumbled upon quite a treasure, a bunny bag!"
    knight_comment2 = "However, I cannot simply give it to you without you first"
    knight_comment3 = "proving to me that you are worthy of such a gift."
    knight_challenge = "If you want it, you must demonstrate your prowess with a bow."

    # Set up font and text objects
    font = pygame.font.SysFont("Arial", 20)
    knight_name_text = font.render(knight_name, True, (255, 255, 255))
    knight_comment_text = font.render(knight_comment, True, (255, 255, 255))
    knight_comment2_text = font.render(knight_comment2, True, (255, 255, 255))
    knight_comment3_text = font.render(knight_comment3, True, (255,255,255))
    knight_challenge_text = font.render(knight_challenge, True, (255, 255, 255))
    if balloons_popped == 0:
        # Display text
        screen.blit(knight_name_text, (10, 10))
        screen.blit(knight_comment_text, (10, 50))
        screen.blit(knight_comment2_text, (10, 100))
        screen.blit(knight_comment3_text, (10, 150))
        screen.blit(knight_challenge_text, (10, 200))
        pygame.display.flip()

        # Wait a few seconds
        time.sleep(8)

        # Call second interaction function
        elf_interact2()
    elif balloons_popped > 0 and balloons_popped < 10:
        balloons_popped = 0
    elif balloons_popped >= 30:
        balloons_popped = 0
        knight_name = "Elven Archer"
        knight_comment = "Well struck, traveler! Your aim is true, and your shot is unrivaled!"
        knight_comment2 = "As promised, I shall give you the bunny bag I came across in this cave."
        knight_challenge = "I will remember this display of archery prowess for some time to come."
        font = pygame.font.SysFont("Arial", 24)
        knight_name_text = font.render(knight_name, True, (255, 255, 255))
        knight_comment_text = font.render(knight_comment, True, (255, 255, 255))
        knight_comment2_text = font.render(knight_comment2, True, (255, 255, 255))
        knight_challenge_text = font.render(knight_challenge, True, (255, 255, 255))
        # Display text
        screen.blit(knight_name_text, (10, 10))
        screen.blit(knight_comment_text, (10, 50))
        screen.blit(knight_comment2_text, (10, 100))
        screen.blit(knight_challenge_text, (10, 150))
        pygame.display.flip()
        time.sleep(8)
        quest_flags['Archery'] = True
        inventory['Bunny Bag'] = True
        # Load a sound effect
        sound_effect = pygame.mixer.Sound("resources/music/win.wav")
        # Play the sound effect over the music
        sound_effect.play()
def elf_interact2():
        global balloons_popped
        # Set up the game variables
        font = pygame.font.SysFont("Arial", 24)
        balloons = []
        balloon_speed = .08
        balloon_color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        balloon_radius = 40
        balloon_count = 50
        balloons_popped = 0
        balloons_flying_off_screen = 0
        game_over = False

        # Set up the player variables
        player_x = screen_width // 2
        player_y = screen_height // 2
        player_speed = .25
        player_color = (0, 0, 255)
        player_radius = 10

        # Set up the shooting variables
        bullet_speed = 10
        bullet_color = (0, 255, 0)
        bullet_radius = 5
        bullets = []

        # Create the balloons
        for i in range(balloon_count):
            x = random.randint(balloon_radius, screen_width - balloon_radius)
            y = random.randint(screen_height + balloon_radius, (screen_height * 2)+ 1250)
            balloons.append((x, y))

        # Start the game loop
        while not game_over:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullets.append((player_x, player_y))

            # Move the player
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player_y -= player_speed
            if keys[pygame.K_s]:
                player_y += player_speed
            if keys[pygame.K_a]:
                player_x -= player_speed
            if keys[pygame.K_d]:
                player_x += player_speed

            # Keep the player on screen
            if player_x < player_radius:
                player_x = player_radius
            elif player_x > screen_width - player_radius:
                player_x = screen_width - player_radius
            if player_y < player_radius:
                player_y = player_radius
            elif player_y > screen_height - player_radius:
                player_y = screen_height - player_radius

            # Move the balloons
            for i in range(len(balloons)):
                x, y = balloons[i]
                y -= balloon_speed
                balloons[i] = (x, y)

            # Check if all balloons have reached the top
            END = 0
            if len(balloons) >= balloon_count:
                all_balloons_gone = all(y <= 0 for x, y in balloons)
                if all_balloons_gone:
                    END = 1
            # Check for collisions between bullets and balloons
            for bullet in bullets:
                for i in range(len(balloons)):
                    x, y = balloons[i]
                    if (x - bullet[0]) ** 2 + (y - bullet[1]) ** 2 <= (balloon_radius + bullet_radius) ** 2:
                        balloons[i] = (x, -300)
                        balloons_popped += 1
                        # Load a sound effect
                        sound_effect = pygame.mixer.Sound("resources/music/switch.wav")
                        # Play the sound effect over the music
                        sound_effect.play()
                        break
            # Remove bullets that are not on screen
            for i in range(len(bullets)):
                x, y = bullets[i]
                bullets.pop(i)


            # Check if the game is over
            if END ==1:
                game_over = True

            # Draw the game objects
            screen.fill((255, 255, 255))
            # Draw the balloons
            for x, y in balloons:
                pygame.draw.circle(screen, balloon_color, (x, y), balloon_radius)

            # Draw the player
            pygame.draw.circle(screen, player_color, (player_x, player_y), player_radius)

            # Draw the bullets
            for x, y in bullets:
                pygame.draw.circle(screen, bullet_color, (x, y), bullet_radius)

            # Draw the score
            score_text = font.render(f"Score: {balloons_popped}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))

            # Update the display
            pygame.display.update()

        # Game over screen
        screen.fill((255, 255, 255))
        if balloons_popped >= 40:
            game_over_text = font.render("You win!", True, (0, 0, 0))
            screen.blit(game_over_text, (
            screen_width // 2 - game_over_text.get_width() // 2,
            screen_height // 2 - game_over_text.get_height() // 2))
            pygame.display.update()
            time.sleep(3)
            return balloons_popped
        else:
            game_over_text = font.render("Game over", True, (0, 0, 0))
            screen.blit(game_over_text, (
            screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
            pygame.display.update()
            time.sleep(3)
            return balloons_popped
        # Wait for the user to close the window
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

def knight_interact():
    global my_score
    pygame.init()

    # Set up screen
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Set up initial variables
    knight_name = "Knight of Honor"
    knight_comment = "Welcome adventurer. It is a shame to see our once great city in ruins."
    knight_comment2 = "But enough lamenting, let's see what you're made of. Show me your skills!"
    knight_challenge = "I have something good for you if you can score 10 points or more."

    # Set up font and text objects
    font = pygame.font.SysFont("Arial", 24)
    knight_name_text = font.render(knight_name, True, (255, 255, 255))
    knight_comment_text = font.render(knight_comment, True, (255, 255, 255))
    knight_comment2_text = font.render(knight_comment2, True, (255,255,255))
    knight_challenge_text = font.render(knight_challenge, True, (255, 255, 255))
    if my_score == 0:
        # Display text
        screen.blit(knight_name_text, (10, 10))
        screen.blit(knight_comment_text, (10, 50))
        screen.blit(knight_comment2_text, (10,100))
        screen.blit(knight_challenge_text, (10, 150))
        pygame.display.flip()

        # Wait a few seconds
        time.sleep(6)

        # Call second interaction function
        knight_interact2()
    elif my_score >0 and my_score <10:
        my_score = 0
    elif my_score >= 10:
        my_score = 0
        knight_name = "Knight of Honor"
        knight_comment = "You have more skill then I thought adventurer."
        knight_comment2 = "Take these explosives, but use them with great caution,"
        knight_challenge = "Press B to drop one at your feet"
        font = pygame.font.SysFont("Arial", 24)
        knight_name_text = font.render(knight_name, True, (255, 255, 255))
        knight_comment_text = font.render(knight_comment, True, (255, 255, 255))
        knight_comment2_text = font.render(knight_comment2, True, (255, 255, 255))
        knight_challenge_text = font.render(knight_challenge, True, (255, 255, 255))
        # Display text
        screen.blit(knight_name_text, (10, 10))
        screen.blit(knight_comment_text, (10, 50))
        screen.blit(knight_comment2_text, (10,100))
        screen.blit(knight_challenge_text, (10, 150))
        pygame.display.flip()
        time.sleep(6)
        quest_flags['Knight of Honor'] = True
        inventory['Bombs'] = True
        # Load a sound effect
        sound_effect = pygame.mixer.Sound("resources/music/win.wav")
        # Play the sound effect over the music
        sound_effect.play()

def knight_interact2():
    global my_score
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and event.key == pygame.K_s:
                    paddle_speed = 0

        # Update the paddle position
        paddle_y += paddle_speed

        # Update the ball position
        ball_x += min(ball_dx, 1.6)
        ball_y += min(ball_dy, 1.6)

        # Check if the ball hit the paddle
        if ball_x <= 20 and paddle_y <= ball_y <= paddle_y + paddle_h:
            ball_dx = abs(ball_dx) * 1.1
            ball_dy = ball_dy * random.uniform(0.8, 1.2)
            hits += 1
            my_score +=1
            # Load a sound effect
            sound_effect = pygame.mixer.Sound("resources/music/switch.wav")
            # Play the sound effect over the music
            sound_effect.play()

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
    global background_image, interaction, player_x, player_y, flip_status, current_map, bomb_img, portal,move_left,move_up,move_down,move_right,beams,beam_attack, fail_index
    global beam_attack_started, beam_attack_frame,beam_start
    if isinstance(images, list) and images != beams:
        image_index = pygame.time.get_ticks() // 150 % len(images)  # Change image every 5 frames (150 milliseconds)
        image = images[image_index]
        if flip_status:
            image = pygame.transform.flip(image, True, False)  # Flip the image if flip_status is True
    else:
        if images != beams:
            image = images
            if flip_status:
                image = pygame.transform.flip(image, True, False)  # Flip the image if flip_status is True
    if isinstance(images, list) and images == beams:
        fail_index = (fail_index + 1) % len(images)  # Increment image_index by 1 and wrap around when it reaches the end
        image = images[fail_index]
        if fail_index == len(beams) - 1:
            beam_attack = 0  # Reset the global variable to 0 once the final frame has been displayed
            return
        if move_left:
            image = pygame.transform.rotate(image, 90)
        elif move_right:
            image = pygame.transform.rotate(image, -90)
        elif move_up:
            image = pygame.transform.rotate(image, 180)
        if flip_status:
            image = pygame.transform.flip(image, True, False)  # Flip the image if flip_status is True
    screen.blit(image, (bunny_x, bunny_y))
    interact_distance = 50
    if images == bomb_img:
        interact_distance = 500
    if images != bomb_img and current_map == 'cave':
        bunny_x = 530
        bunny_y = 500
    if images == portal or images == beams:
        interact_distance = 0
    if images != boulder and images != Slime:
        # Check if player is near bunny
        if abs(player_x - bunny_x) < interact_distance and abs(player_y - bunny_y) < interact_distance:
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
    if pygame.time.get_ticks() // 1000 % 3 == 0 and random.random() < 0.01:
        if current_map == 'city':
            flip_status = not flip_status  # Invert the flip status

def pause_menu():
    global game_state, inventory, quest_flags, current_map, player_x,player_y

    # Set game state to paused
    game_state = False

    # Create a list of menu options
    menu_options = ["Pause Menu", "Save", "New Game"]
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
                        pass
                    elif selected_option == 1:
                        with open("inventory.txt", "w") as f:
                            json.dump(inventory, f)
                        with open("quest_flags.txt", "w") as f:
                            json.dump(quest_flags, f)
                    elif selected_option == 2:
                        quest_flags = {"Knight of Honor": False, "Boulder": False,"Archery": False, "Slime": False,"holy_grail": False}
                        inventory = {"Bombs": False, "Bunny Bag": False, "Boat": False, "GoB": False, "Beam": False}
                        hub_teleport()
                        player_x = 75
                        player_y = 110

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
    global background_image, walkable_tiles, player_x, player_y, current_map,stale_player_x
    stale_player_x = 0
    # Load the new background image
    if (current_map == 'christmas' and player_x < 410): current_map = 'hub'
    elif(current_map == 'holygrail'): current_map = 'alter';mixer.music.load("resources/music/cipher.mp3");mixer.music.set_volume(0.5);mixer.music.play()
    elif(current_map == 'alter' and player_y > 400): current_map = 'christmas';mixer.music.load("resources/music/lobby.mp3");mixer.music.set_volume(0.5);mixer.music.play()
    elif(current_map == 'alter' and player_y < 400): current_map = 'holygrail';mixer.music.load("resources/music/lurking.mp3");mixer.music.set_volume(0.5);mixer.music.play()
    elif(current_map == 'christmas' and player_x > 410): current_map = 'alter';mixer.music.load("resources/music/cipher.mp3");mixer.music.set_volume(0.5);mixer.music.play()
    elif (current_map == 'hub' and player_x > 600):current_map = 'graveyard';mixer.music.load("resources/music/graveyard.mp3");mixer.music.set_volume(0.5);mixer.music.play()
    elif (current_map == 'hub' and player_y < 50): current_map = 'island';mixer.music.load("resources/music/cipher.mp3");mixer.music.set_volume(0.5);mixer.music.play()
    elif (current_map == 'hub' and player_y < 300): current_map = 'christmas'
    elif (current_map == 'hub' and player_x > 100): current_map = 'cave';mixer.music.load("resources/music/cipher.mp3");mixer.music.set_volume(0.5);mixer.music.play()
    elif (current_map == 'hub' and player_x < 70): current_map = 'city';mixer.music.load("resources/music/Glory.mp3");mixer.music.set_volume(0.5);mixer.music.play()
    elif (current_map == 'graveyard'): current_map = 'hub';mixer.music.load("resources/music/lobby.mp3");mixer.music.set_volume(0.5);mixer.music.play()
    elif (current_map == 'city'): current_map = 'hub';mixer.music.load("resources/music/lobby.mp3");mixer.music.set_volume(0.5);mixer.music.play()
    elif (current_map == 'cave'): current_map = 'hub';mixer.music.load("resources/music/lobby.mp3");mixer.music.set_volume(0.5);mixer.music.play()
    elif (current_map == 'island'): current_map = 'hub';mixer.music.load("resources/music/lobby.mp3");mixer.music.set_volume(0.5);mixer.music.play()
    if (current_map != 'christmas'):
        del background_image
        background_image = pygame.image.load(new_bg_path).convert()
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Update the walkable tiles and player coordinates
    walkable_tiles = new_walkable_tiles
    player_x = new_player_x
    player_y = new_player_y
def hub_teleport():
    global moving_sprites, idle_sprites, movement_speed, bomb_explosion,bomb_img, quest_flags
    if current_map == "city":
        x, y = 100, 350
    elif current_map == 'graveyard':
        x, y = 550, 1
    elif current_map == "cave":
        x, y = 150, 450
        idle_sprites.clear()
        moving_sprites.clear()
        if quest_flags["holy_grail"] == False:
            idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle/frame{i}.gif'), (120, 120)) for i
                            in
                            range(4)]
        else:
            idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle_2/frame{i}.gif'), (120, 120)) for
                            i in range(4)]
        moving_sprites = [pygame.transform.scale(pygame.image.load(f'resources/moving/frame{i}.gif'), (120, 120)) for i
                          in range(4)]
        bomb_img = pygame.transform.scale(pygame.image.load('resources/inventory/bomb.png'), (75, 75))
        bomb_explosion = [pygame.transform.scale(pygame.image.load(f'resources/inventory/frame_{i}.png'), (75, 75)) for
                          i in range(4)]

        movement_speed = 5
    elif current_map == "island":
        x, y = 500, 1
        idle_sprites.clear()
        moving_sprites.clear()
        if quest_flags["holy_grail"] == False:
            idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle/frame{i}.gif'), (120, 120)) for i
                            in
                            range(4)]
        else:
            idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle_2/frame{i}.gif'), (120, 120)) for
                            i in range(4)]
        moving_sprites = [pygame.transform.scale(pygame.image.load(f'resources/moving/frame{i}.gif'), (120, 120)) for i
                          in range(4)]
        bomb_img = pygame.transform.scale(pygame.image.load('resources/inventory/bomb.png'), (75, 75))
        bomb_explosion = [pygame.transform.scale(pygame.image.load(f'resources/inventory/frame_{i}.png'), (75, 75)) for
                          i in range(4)]
        movement_speed = 5
    else:
        x, y = 75, 110
    teleport("resources/backdrop/hub/frame0.png",
             [[0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 2],
              [0, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
              [0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
              [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 3, 3],
              [0, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3],
              [0, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3],
              [2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3],
              [1, 1, 1, 1, 1, 3, 3, 1, 1, 3, 3, 3],
              [0, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3],
              [0, 1, 2, 1, 3, 3, 3, 3, 3, 3, 3, 3],
              [0, 1, 2, 1, 3, 3, 3, 3, 3, 3, 3, 3]],
             x, y)



def house_teleport():
    global idle_sprites, moving_sprites, bomb_explosion, bomb_img, movement_speed
    idle_sprites.clear()
    moving_sprites.clear()
    bomb_explosion.clear()
    if quest_flags["holy_grail"] == False:
        idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle/frame{i}.gif'), (120, 120)) for i in
                        range(4)]
    else:
        idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle_2/frame{i}.gif'), (120, 120)) for i in
                        range(4)]
    moving_sprites = [pygame.transform.scale(pygame.image.load(f'resources/moving/frame{i}.gif'), (120, 120)) for i in
                      range(4)]
    bomb_img = pygame.transform.scale(pygame.image.load('resources/inventory/bomb.png'), (75, 75))
    bomb_explosion = [pygame.transform.scale(pygame.image.load(f'resources/inventory/frame_{i}.png'), (75, 75)) for i in
                      range(4)]
    movement_speed = 5
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
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0],
                 [1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 0],
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
    global idle_sprites, moving_sprites, movement_speed, bomb_img, bomb_explosion
    # Clear the existing player sprites
    idle_sprites.clear()
    moving_sprites.clear()
    bomb_explosion.clear()
    bomb_img = 0
    # Load the shrunken player sprites
    if quest_flags["holy_grail"] == False:
        idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle/frame{i}.gif'), (50, 50)) for i in
                        range(4)]
    else:
        idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle_2/frame{i}.gif'), (50, 50)) for i in
                        range(4)]
    moving_sprites = [pygame.transform.scale(pygame.image.load(f'resources/moving/frame{i}.gif'), (50, 50)) for i in
                      range(4)]
    bomb_img = pygame.transform.scale(pygame.image.load('resources/inventory/bomb.png'), (31, 31))
    bomb_explosion = [pygame.transform.scale(pygame.image.load(f'resources/inventory/frame_{i}.png'), (31, 31)) for i in
                      range(4)]
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
    global idle_sprites, moving_sprites, movement_speed, bomb_img, bomb_explosion
    # Clear the existing player sprites
    idle_sprites.clear()
    moving_sprites.clear()

    # Load the shrunken player sprites
    if quest_flags["holy_grail"] == False:
        idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle/frame{i}.gif'), (60, 60)) for i in
                        range(4)]
    else:
        idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle_2/frame{i}.gif'), (60, 60)) for i in
                        range(4)]
    moving_sprites = [pygame.transform.scale(pygame.image.load(f'resources/moving/frame{i}.gif'), (60, 60)) for i in
                      range(4)]
    bomb_img = pygame.transform.scale(pygame.image.load('resources/inventory/bomb.png'), (37.5, 37.5))
    bomb_explosion = [pygame.transform.scale(pygame.image.load(f'resources/inventory/frame_{i}.png'), (37.5, 37.5)) for i in
                      range(4)]
    movement_speed = 2.5
    teleport("resources/backdrop/island/frame0.png",
        [[3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 4, 3],
         [3, 4, 0, 0, 0, 0, 0, 1, 0, 0, 4, 3],
         [3, 4, 0, 1, 1, 0, 0, 1, 0, 0, 4, 3],
         [3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 4, 3],
         [3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 4, 3],
         [3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 4, 3],
         [3, 4, 4, 1, 4, 4, 4, 1, 1, 4, 3, 3],
         [3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3],
         [3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3],
         [3, 3, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3],
         [3, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3],
         [3, 2, 2, 2, 2, 2, 1, 3, 3, 3, 3, 1]],270,530)
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
def alter_teleport():
    global idle_sprites, moving_sprites, movement_speed, bomb_img, bomb_explosion
    # Clear the existing player sprites
    idle_sprites.clear()
    moving_sprites.clear()
    bomb_explosion.clear()
    bomb_img = 0
    # Load the shrunken player sprites
    if quest_flags["holy_grail"] == False:
        idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle/frame{i}.gif'), (50, 50)) for i in
                        range(4)]
    else:
        idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle_2/frame{i}.gif'), (50, 50)) for i in
                        range(4)]
    moving_sprites = [pygame.transform.scale(pygame.image.load(f'resources/moving/frame{i}.gif'), (50, 50)) for i in
                      range(4)]
    bomb_img = pygame.transform.scale(pygame.image.load('resources/inventory/bomb.png'), (31, 31))
    bomb_explosion = [pygame.transform.scale(pygame.image.load(f'resources/inventory/frame_{i}.png'), (31, 31)) for i in
                      range(4)]
    movement_speed = 2.083
    teleport("resources/backdrop/alter/alter.gif",
             [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
              [0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0],
              [0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0],
              [0, 1, 0, 1, 1, 2, 1, 1, 0, 0, 1, 0],
              [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
              [0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0],
              [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 2],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
             600, 460)
def holy_grail_teleport():
    global idle_sprites, moving_sprites, bomb_explosion, bomb_img, movement_speed
    idle_sprites.clear()
    moving_sprites.clear()
    bomb_explosion.clear()
    if quest_flags["holy_grail"] == False:
        idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle/frame{i}.gif'), (120, 120)) for i in
                        range(4)]
    else:
        idle_sprites = [pygame.transform.scale(pygame.image.load(f'resources/idle_2/frame{i}.gif'), (120, 120)) for i in
                        range(4)]
    moving_sprites = [pygame.transform.scale(pygame.image.load(f'resources/moving/frame{i}.gif'), (120, 120)) for i in
                      range(4)]
    bomb_img = pygame.transform.scale(pygame.image.load('resources/inventory/bomb.png'), (75, 75))
    bomb_explosion = [pygame.transform.scale(pygame.image.load(f'resources/inventory/frame_{i}.png'), (75, 75)) for i in
                      range(4)]
    movement_speed = 5
    teleport("resources/backdrop/holy_grail/frame_000_delay-0.04s.gif",
             [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0]],
             400, 500)
while True:
    # Handle input events
    handle_input_events()

    # Update the game state
    update()

    # Draw the game objects
    draw()

    # Limit the frame rate
    clock.tick(60)

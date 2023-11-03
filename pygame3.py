import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Geometry Dash')

# Background
background = pygame.image.load('pg1.webp')  # Add your background video here
background = pygame.transform.scale(background, (screen_width, screen_height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)       
blue = (0, 0, 255)
baby_blue = (137, 207, 240)  # New baby blue color

# Load sounds
jump_sound = pygame.mixer.Sound('chest-click-sfx.mp3')  # Add your jump sound file here
collision_sound = pygame.mixer.Sound('player-death-sound-effect.mp3')  # Add your collision sound file here
pygame.mixer.music.load('kentenshi-paranoia-mp3.mp3')  # Add your background music file here
pygame.mixer.music.play(-1)  # Play the background music on loop

# Game variables
ground_height = 50
player_width = 50
player_height = 50
player_image = pygame.image.load('6206317198298843900.webp')  # Add your player image here
player_image = pygame.transform.scale(player_image, (player_width, player_height))
player_x = 100
player_y = screen_height - ground_height - player_height
player_y_change = 0
player_jump = False
player_jump_speed = 40  # Increased jump speed
player_gravity = 3.9

obstacle_width = 70
obstacle_height = 50
obstacle_image = pygame.image.load('blue_block.jpg')  # Add your obstacle image here
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height))
obstacle_x = screen_width
obstacle_y = screen_height - ground_height - obstacle_height 
obstacle_speed = 10
speed_increment = 0.01  # Smaller speed increment factor

score = 0

clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)

# Define a function for the startup menu
def startup_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        screen.fill(black)
        draw_text("Geometry Dash", font, white, 260, 250)
        draw_text("Press ENTER to play", font, white, 240, 300)
        pygame.display.update()
        clock.tick(30)

# Define a function for the final score menu
def final_score_menu(score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        screen.fill(black)
        draw_text("Game Over", font, red, 350, 250)
        draw_text(f"Your score: {score}", font, white, 345, 300)
        draw_text("Press ENTER to play again", font, white, 240, 350)
        pygame.display.update()

# Functions
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_obstacles(obstacle_list):
    for obstacle in obstacle_list:
        screen.blit(obstacle_image, (obstacle['x'], obstacle['y']))


def collision_detection(obstacle_list):
    for obstacle in obstacle_list:
        if (player_x < obstacle['x'] + obstacle_width and player_x + player_width > obstacle['x'] and
                player_y < obstacle['y'] + obstacle_height and player_y + player_height > obstacle['y']):
            return True
    return False


# Startup menu
startup_menu()

# Game loop
running = True
obstacle_list = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not player_jump:
                player_y_change = -player_jump_speed  # Increased jump speed
                player_jump = True
                jump_sound.play()  # Play jump sound

    # Background     
    
    screen.blit(background, (0, 0))

    # Player
    screen.blit(player_image, (player_x, player_y))

    # Obstacles
    if len(obstacle_list) == 0:
        obstacle_list.append({'x': screen_width, 'y': screen_height - ground_height - obstacle_height})
    else:
        if obstacle_list[-1]['x'] < screen_width - 300:
            new_obstacle_y = random.randint(ground_height, screen_height - ground_height - obstacle_height)
            obstacle_list.append({'x': screen_width, 'y': new_obstacle_y})

    for obstacle in obstacle_list:
        obstacle['x'] -= obstacle_speed
        obstacle_speed += speed_increment  # Increasing the speed gradually

    draw_obstacles(obstacle_list)

    if obstacle_list[0]['x'] < -obstacle_width:
        obstacle_list.pop(0)
        score += 1

    # Collision detection
    if collision_detection(obstacle_list):
        collision_sound.play()  # Play collision sound
        running = False

    # Gravity
    if player_y < screen_height - ground_height - player_height or player_y_change < 0:
        player_y_change += player_gravity
        player_y += player_y_change
    else:
        player_jump = False
        player_y_change = 0
        player_y = screen_height - ground_height - player_height

    # Score           
    draw_text(f"Score: {score}", font, baby_blue, 10, 10)  # Use baby blue color for the score

    # Update display
    pygame.display.update()
    clock.tick(30)
    # Final score menu
final_score_menu(score)

# Quit Pygame
pygame.quit()

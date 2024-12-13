import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AGE OF CHAMPIONS")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRASS = (100, 100, 0)

# Define block attributes
block_width = 10
block_height = 15
block_speed = 1
block_health = 100


# Custom Block class
class Block(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.health = block_health

# Create player blocks
player_blocks = []
for i in range(20):
    y = random.randint(0, screen_height - block_height)
    block = Block(200, y, block_width, block_height)
    player_blocks.append(block)

# Timer for block doubling
start_time = pygame.time.get_ticks()
double_time = 5000  # 5 seconds in milliseconds



# Create enemy blocks
enemy_blocks = []
for i in range(20):
    y = random.randint(0, screen_height - block_height)
    block = Block(screen_width - 200 - block_width, y, block_width, block_height)
    enemy_blocks.append(block)

enemy_start_time = pygame.time.get_ticks()
enemy_spawn_time = 5000  # 5 seconds in milliseconds


# block cap
max_player_blocks = 50
max_enemy_blocks = 50

# FightButton attributes
button_width = 100
button_height = 50
button_color = (255, 10, 0)
button_text_color = WHITE
font = pygame.font.Font(None, 36)

# Button rectangle
button_rect = pygame.Rect(screen_width // 2 - button_width // 2, screen_height - button_height - 10, button_width, button_height)

# SummonButton attributes
summonButton_width = 40
summonButton_height = 40
summonButton_color = (0, 0, 255)  # BLUE color for the summon button
summonButton_text_color = WHITE
font = pygame.font.Font(None, 24)

summon_button_rect = pygame.Rect(10, screen_height - button_height - 10, button_width, button_height)

# Add a cooldown for the summon button
summon_cooldown = 1000  # 1 second in milliseconds
last_summon_time = pygame.time.get_ticks()
summon_limit = 3  # Set the maximum number of summons

font_Large = pygame.font.Font(None, 48)
count_display_rect = pygame.Rect(screen_width // 4, screen_height // 4, screen_width // 2, screen_height // 2)

font_small = pygame.font.Font(None, 24)
count_display_rect = pygame.Rect(screen_width // 4, screen_height // 4, screen_width // 2, screen_height // 2)
player_block_count = len(player_blocks)
enemy_block_count = len(enemy_blocks)

# Game loop
running = True
blocks_started = False  # Flag to check if the blocks have started
clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    current_enemy_time = pygame.time.get_ticks()
    elapsed_enemy_time = current_enemy_time - enemy_start_time

    player_block_count = len(player_blocks)
    enemy_block_count = len(enemy_blocks)

    if elapsed_enemy_time >= enemy_spawn_time:
        # Spawn new enemy blocks
        for i in range(10):  # Adjust the number of new enemy blocks as needed
            y = random.randint(0, screen_height - block_height)
            block = Block(screen_width - 200 - block_width, y, block_width, block_height)
            enemy_blocks.append(block)

        # Reset the enemy timer
        enemy_start_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not blocks_started:
            # Check if the mouse click is inside the button
            if button_rect.collidepoint(event.pos):
                blocks_started = True  # Start the block
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is inside the "Summon" button and if the limit is not reached
            if summon_button_rect.collidepoint(event.pos) and last_summon_time + summon_cooldown <= current_time and summon_limit > 0:
                # Summon a larger block when the button is clicked
                for i in range(1):
                    y = random.randint(0, screen_height - 2 * block_height)  # Adjusted to prevent going off-screen
                    # Increase the size of the summoned block
                    block = Block(200, y, 2 * block_width, 2 * block_height)
                    player_blocks.append(block)

                # Update the last summon time
                last_summon_time = current_time
                summon_limit -= 1  # Decrease the summon limit

    if elapsed_time >= double_time:
        # Double the number of player blocks
        for i in range(20):
            y = random.randint(0, screen_height - block_height)
            block = Block(200, y, block_width, block_height)
            player_blocks.append(block)

            # Reset the timer
            start_time = pygame.time.get_ticks()


    if blocks_started:
        # Move player blocks towards the center
        for block in player_blocks:
            # Calculate angle to move towards the center (screen_width // 2, screen_height // 2)
            angle = math.atan2(screen_height // 2 - block.y, screen_width // 2 - block.x)
            block.x += block_speed * math.cos(angle)
            block.y += block_speed * math.sin(angle)

        # Move enemy blocks towards the center
        for block in enemy_blocks:
            # Calculate angle to move towards the center (screen_width // 2, screen_height // 2)
            angle = math.atan2(screen_height // 2 - block.y, screen_width // 2 - block.x)
            block.x += block_speed * math.cos(angle)
            block.y += block_speed * math.sin(angle)

        # Check for collisions and resolve them
        for block1 in player_blocks + enemy_blocks:
            for block2 in player_blocks + enemy_blocks:
                if block1 != block2 and block1.colliderect(block2):
                    angle = math.atan2(block1.y - block2.y, block1.x - block2.x)
                    overlap = (block1.width + block2.width) // 2 - math.hypot(block1.x - block2.x, block1.y - block2.y) / 2
                    block1.x += overlap * math.cos(angle)
                    block1.y += overlap * math.sin(angle)
                    block2.x -= overlap * math.cos(angle)
                    block2.y -= overlap * math.sin(angle)

        # Check for collisions with screen boundaries
        for block in player_blocks + enemy_blocks:
            block.x = max(0, min(screen_width - block.width, block.x))
            block.y = max(0, min(screen_height - block.height, block.y))

        # Check for collisions between player and enemy blocks
        blocks_to_remove = []

        for player_block in player_blocks:
            for enemy_block in enemy_blocks:
                if player_block.colliderect(enemy_block):
                    player_block.health -= 2
                    enemy_block.health -= 1
                if player_block.health <= 0:
                    blocks_to_remove.append(player_block)
                if enemy_block.health <= 0:
                    blocks_to_remove.append(enemy_block)

        # Remove the blocks marked for removal
        for block in blocks_to_remove:
            if block in player_blocks:
                player_blocks.remove(block)
            if block in enemy_blocks:
                enemy_blocks.remove(block)

    # Clear the screen
    screen.fill(GRASS)

    # Draw player blocks
    for block in player_blocks:
        pygame.draw.rect(screen, WHITE, block)

    # Draw enemy blocks
    for block in enemy_blocks:
        pygame.draw.rect(screen, RED, block)

    # Draw the button
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = font.render("FIGHT!", True, button_text_color)
    screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2))
    
    # Draw the summon button
    if summon_limit > 0:
        pygame.draw.rect(screen, button_color, summon_button_rect)
        button_text = font.render(f"Summon ({summon_limit})", True, button_text_color)
        screen.blit(button_text, (summon_button_rect.centerx - button_text.get_width() // 4, summon_button_rect.centery - button_text.get_height() // 8))

    # Display player block count
    player_count_text = font_small.render(f"Player Blocks: {player_block_count}", True, WHITE)
    player_count_rect = player_count_text.get_rect(topleft=(10, 10))
    screen.blit(player_count_text, player_count_rect.topleft)

    # Display enemy block count
    enemy_count_text = font_small.render(f"Enemy Blocks: {enemy_block_count}", True, WHITE)
    enemy_count_rect = enemy_count_text.get_rect(topright=(500, 10))
    screen.blit(enemy_count_text, enemy_count_rect.topright)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
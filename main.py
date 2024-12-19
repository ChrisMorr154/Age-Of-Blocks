import pygame
from player import Player
from enemy import Enemy
from start_screen import start_screen
from game_over import game_over_screen  # Ensure this is imported correctly

# Initialize Pygame
pygame.init()

# Screen setup
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AGE OF CHAMPIONS")
clock = pygame.time.Clock()

# Show starting screen and get player block count
player_block_count = start_screen()

# Create player and enemy
player = Player(20, 20, player_block_count)  # Special block starts at top-left
enemy = Enemy(760, 20, 20)  # Special block starts at top-right

# Fonts for displaying block counts
font = pygame.font.Font(None, 36)

def check_collisions(blocks_a, blocks_b):
    """Handle collisions and apply damage between blocks."""
    to_remove_a = []
    to_remove_b = []
    for block_a in blocks_a:
        for block_b in blocks_b:
            if block_a.colliderect(block_b):
                to_remove_a.append(block_a)
                to_remove_b.append(block_b)
    return to_remove_a, to_remove_b

def move_to_center(block, speed=2):
    """Move a block towards the center of the screen."""
    center_x, center_y = screen_width // 2, screen_height // 2
    dx = center_x - block.x
    dy = center_y - block.y
    dist = max(abs(dx), abs(dy))
    if dist > 0:  # Avoid division by zero
        block.x += speed * (dx / dist)
        block.y += speed * (dy / dist)

# Game loop
running = True
winner = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement logic for player normal blocks
    if player.normal_blocks:
        player.move_blocks(enemy.normal_blocks)
    elif not player.normal_blocks:
        move_to_center(player.special_block)

    # Movement logic for enemy normal blocks
    if enemy.normal_blocks:
        enemy.move_blocks(player.normal_blocks)
    elif not enemy.normal_blocks:
        move_to_center(enemy.special_block)

    # Check collisions between normal blocks
    if player.normal_blocks and enemy.normal_blocks:
        player_to_remove, enemy_to_remove = check_collisions(player.normal_blocks, enemy.normal_blocks)

        # Remove player blocks safely
        for block in player_to_remove:
            if block in player.normal_blocks:
                player.normal_blocks.remove(block)

        # Remove enemy blocks safely
        for block in enemy_to_remove:
            if block in enemy.normal_blocks:
                enemy.normal_blocks.remove(block)

    # Special block combat with normal blocks
    if not player.normal_blocks and enemy.normal_blocks:
        # Player special block attacks enemy normal blocks
        player_to_remove, _ = check_collisions([player.special_block], enemy.normal_blocks)
        for block in player_to_remove:
            if block in enemy.normal_blocks:
                enemy.normal_blocks.remove(block)

    if not enemy.normal_blocks and player.normal_blocks:
        # Enemy special block attacks player normal blocks
        enemy_to_remove, _ = check_collisions([enemy.special_block], player.normal_blocks)
        for block in enemy_to_remove:
            if block in player.normal_blocks:
                player.normal_blocks.remove(block)

    # Special block combat at the center
    if not player.normal_blocks and not enemy.normal_blocks:
        if player.special_block.colliderect(enemy.special_block):
            player.special_health -= 10
            enemy.special_health -= 10

            # Determine winner when one special block's health reaches zero
            if player.special_health <= 0:
                winner = "enemy"
                running = False
            elif enemy.special_health <= 0:
                winner = "player"
                running = False

    # Drawing
    screen.fill((0, 128, 0))  # Background
    player.draw(screen)
    enemy.draw(screen)

    # Display block counts
    player_count_text = font.render(f"Player Blocks: {len(player.normal_blocks)}", True, (255, 255, 255))
    enemy_count_text = font.render(f"Enemy Blocks: {len(enemy.normal_blocks)}", True, (255, 255, 255))
    screen.blit(player_count_text, (10, 10))
    screen.blit(enemy_count_text, (screen_width - 200, 10))

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Show the game over screen
if winner:
    game_over_screen(winner)

pygame.quit()

import pygame
from player import Player
from enemy import Enemy
from start_screen import start_screen
from game_over import game_over_screen
from resources import *

pygame.init()

# Create the game screen
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AGE OF CHAMPIONS")
clock = pygame.time.Clock()


# I am adding the background battle image that I created myself
background_image = pygame.image.load('Resources/Battle_Background.png')

# I will fill the background image to fill the entire screen
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Put the player in the top left corner of the screen
player = Player(20, 20, start_screen())
# Put the Enemy in the top right of the game screen
enemy = Enemy(760, 20, 20)

# set font/size of the block count on screen
font = pygame.font.Font(None, 24)


def check_collisions(blocks_a, blocks_b):
    """Return the blocks that should be removed from each list due to collision."""
    to_remove_a = []
    to_remove_b = []
    for block_a in blocks_a:
        for block_b in blocks_b:
            if block_a.colliderect(block_b):
                to_remove_a.append(block_a)
                to_remove_b.append(block_b)
    return to_remove_a, to_remove_b

def move_block_towards(block, target, speed=2):
    """Move a block towards a target block or position using integers."""
    dx = target.x - block.x
    dy = target.y - block.y
    dist = max(abs(dx), abs(dy))
    if dist > 0:
        block.x += int(speed * (dx / dist))
        block.y += int(speed * (dy / dist))

def move_towards_first(block, targets, speed=2):
    """Move block towards the first target in the list if any exist."""
    if targets:
        target = targets[0]
        move_block_towards(block, target, speed)

running = True
winner = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Add the battle background image to the screen
    screen.blit(background_image, (0, 0))

    # get the players blocks to move toward the enemy
    if player.normal_blocks:
        if enemy.normal_blocks:
            player.move_blocks(enemy.normal_blocks)
        else:
            # If the enemy army blocks are all removed, have player blocks focus on the main enemy
            player.move_blocks([enemy.special_block])
    else:
        # If the player does not have blocks, move the player block to enemies
        if enemy.normal_blocks:
            move_towards_first(player.special_block, enemy.normal_blocks)
        else:
            # If both have no normal blocks, move special blocks towards each other
            move_block_towards(player.special_block, enemy.special_block)

    # Enemy movement, same logic as the player blocks
    if enemy.normal_blocks:
        if player.normal_blocks:
            enemy.move_blocks(player.normal_blocks)
        else:
            enemy.move_blocks([player.special_block])
    else:s
        if player.normal_blocks:
            move_towards_first(enemy.special_block, player.normal_blocks)
        else:
            move_block_towards(enemy.special_block, player.special_block)

    # Check normal block collisions and remove block if they collide and Health = 0
    if player.normal_blocks and enemy.normal_blocks:
        player_to_remove, enemy_to_remove = check_collisions(player.normal_blocks, enemy.normal_blocks)
        if player_to_remove or enemy_to_remove:
            print("Normal block collision detected!")
        for block in player_to_remove:
            if block in player.normal_blocks:
                player.normal_blocks.remove(block)
                print("Removed player normal block due to collision:", block)
        for block in enemy_to_remove:
            if block in enemy.normal_blocks:
                enemy.normal_blocks.remove(block)
                print("Removed enemy normal block due to collision:", block)

    # Player special block attacks enemy normal blocks if player has no normal blocks
    if not player.normal_blocks and enemy.normal_blocks:
        player_to_remove, enemy_to_remove = check_collisions([player.special_block], enemy.normal_blocks)
        if player_to_remove or enemy_to_remove:
            print("Player special block hit enemy normal block(s)!")
        for block in enemy_to_remove:
            if block in enemy.normal_blocks:
                enemy.normal_blocks.remove(block)
                print("Removed enemy normal block due to player special attack:", block)

    # Enemy special block attacks player normal blocks if enemy has no normal blocks
    if not enemy.normal_blocks and player.normal_blocks:
        player_to_remove, enemy_to_remove = check_collisions([enemy.special_block], player.normal_blocks)
        if player_to_remove or enemy_to_remove:
            print("Enemy special block hit player normal block(s)!")
        for block in player_to_remove:
            if block in player.normal_blocks:
                player.normal_blocks.remove(block)
                print("Removed player normal block due to enemy special attack:", block)

    # Special block combat
    if not player.normal_blocks and not enemy.normal_blocks:
        if player.special_block.colliderect(enemy.special_block):
            print("Special block collision! Both sides take damage.")
            player.special_health -= 10
            enemy.special_health -= 10
            print(f"Player special health: {player.special_health}")
            print(f"Enemy special health: {enemy.special_health}")

            # Check to see who won the game
            if player.special_health <= 0:
                winner = "enemy"
                running = False
            elif enemy.special_health <= 0:
                winner = "player"
                running = False

    player.draw(screen)
    enemy.draw(screen)

    # Show block count on the screen
    player_count_text = font.render(f"Player Blocks: {len(player.normal_blocks)}", True, (255, 255, 255))
    enemy_count_text = font.render(f"Enemy Blocks: {len(enemy.normal_blocks)}", True, (255, 255, 255))
    screen.blit(player_count_text, (10, 10))
    screen.blit(enemy_count_text, (screen_width - 200, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Show the game over screen
if winner:
    game_over_screen(winner)

pygame.quit()

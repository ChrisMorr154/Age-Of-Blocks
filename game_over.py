import pygame

def game_over_screen(winner):
    """
    Displays a game over screen showing whether the player won or lost.

    Args:
        winner (str): "player" if the player wins, "enemy" if the enemy wins.
    """
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("Game Over")
    font = pygame.font.Font(None, 72)
    small_font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    # Figure out which message to display
    if winner == "player":
        message = "YOU WIN!"
        color = (0, 255, 0)
    else:
        message = "YOU LOSE!"
        color = (255, 0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

        # Create the sceen
        screen.fill((0, 0, 0))
        text = font.render(message, True, color)
        small_text = small_font.render("Press Enter to Exit", True, (255, 255, 255))

       # put message in the middle of the screen
        text_rect = text.get_rect(center=(400, 200))
        small_text_rect = small_text.get_rect(center=(400, 300))

        # Position and add to screen
        screen.blit(text, text_rect)
        screen.blit(small_text, small_text_rect)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

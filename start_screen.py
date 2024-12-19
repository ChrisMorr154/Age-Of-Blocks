import pygame

def start_screen():
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("Game Start Screen")
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    running = True
    selected_blocks = 20  # Default player block count
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game on Enter
                    running = False
                elif event.key == pygame.K_UP:  # Increase blocks
                    selected_blocks += 5
                elif event.key == pygame.K_DOWN:  # Decrease blocks
                    selected_blocks = max(5, selected_blocks - 5)

        screen.fill((0, 0, 0))
        title_text = font.render("AGE OF CHAMPIONS", True, (255, 255, 255))
        screen.blit(title_text, (300, 100))

        start_text = font.render("Press Enter to Start", True, (255, 255, 255))
        screen.blit(start_text, (300, 150))

        block_text = font.render(f"Player Blocks: {selected_blocks}", True, (255, 255, 255))
        screen.blit(block_text, (300, 200))

        pygame.display.flip()
        clock.tick(60)

    return selected_blocks

import pygame
import random


# similar to Player.py
class Enemy:
    def __init__(self, special_x, special_y, normal_blocks):
        self.special_block = pygame.Rect(special_x, special_y, 20, 20)
        self.special_health = 150
        self.normal_blocks = [pygame.Rect(random.randint(600, 780), random.randint(0, 380), 10, 10) for _ in range(normal_blocks)]
        self.normal_health = 100

    def move_blocks(self, target_blocks, speed=1):
        for block in self.normal_blocks:
            closest_target = min(target_blocks, key=lambda b: abs(b.x - block.x) + abs(b.y - block.y), default=None)
            if closest_target:
                dx = closest_target.x - block.x
                dy = closest_target.y - block.y
                dist = max(abs(dx), abs(dy))
                if dist == 0:
                    continue
                block.x += speed * (dx / dist)
                block.y += speed * (dy / dist)

    def draw(self, screen):
        for block in self.normal_blocks:
            pygame.draw.rect(screen, (200, 0, 0), block)

        pygame.draw.rect(screen, (255, 0, 0), self.special_block)

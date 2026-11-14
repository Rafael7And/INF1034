import sys
from pathlib import Path

import pygame
from pygame.locals import QUIT, KEYDOWN

pygame.init()

BASE_DIR = Path(__file__).resolve().parent

clock = pygame.time.Clock()

curr_frame = 0
anim_time = 0
hero_x = 0
hero_speed = 250
hero_walk_list = [
    pygame.image.load(str(BASE_DIR / f"Hero_Walk_{frame:02}.png"))
    for frame in (1, 2, 5)
]


run_animation = False
curr_frame_mm = 0
anim_time_mm = 0
megaman_spritesheet = pygame.image.load(str(BASE_DIR / "megaman_spritesheet.png"))

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Hello World!')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                run_animation = True

    clock.tick(60)
    dt = clock.get_time()

    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_RIGHT]:
        hero_x += hero_speed * dt / 1000
        moving = True
    if keys[pygame.K_LEFT]:
        hero_x -= hero_speed * dt / 1000
        moving = True
    hero_x = max(0, min(hero_x, 800 - hero_walk_list[0].get_width()))

    if moving:
        anim_time += dt
        if anim_time >= 150:
            curr_frame = (curr_frame + 1) % len(hero_walk_list)
            anim_time = 0
    else:
        curr_frame = 0
        anim_time = 0
    
    if run_animation:
        anim_time_mm = anim_time_mm + dt
        anim_time_mm_sec = anim_time_mm/1000

        if anim_time_mm_sec > 0.1:
            curr_frame_mm = curr_frame_mm + 1
            # curr_frame_mm += 1
            if curr_frame_mm > 9:
                curr_frame_mm = 0
                run_animation = False
            anim_time_mm = 0

    # Desenho dos elementos na tela
    screen.fill((255,255,255))

    # screen.blit(dog_img, (0, 0))
    screen.blit(hero_walk_list[curr_frame], (int(hero_x), 0))

    # if curr_frame_mm < 5:
    #     screen.blit(megaman_spritesheet, (200, 200), (60 * curr_frame_mm, 0, 60, 60))
    # else:
    #     screen.blit(megaman_spritesheet, (200, 200), (60 * (curr_frame_mm - 5), 60, 60, 60))
    
    screen.blit(megaman_spritesheet, (200, 200), (60*(curr_frame_mm%5), 60*(curr_frame_mm//5), 60, 60))

    pygame.display.update()

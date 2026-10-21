import pygame, sys
from pygame.locals import QUIT, KEYDOWN
#criar 3 variaveis para cada uma / gandalf spritesheet ou o Hipotetico


clock = pygame.time.Clock()

dog_img = pygame.image.load("chiens-funnyanimals.gif")

megaman_spritesheet = pygame.image.load()"megaman_spritesheet.png"


hero_img = pygame.image.load("assets/assets/Hero_Walk_01.png")



hero_walk_list = [
    pygame.image.load("assets/assets/Hero_Walk_01.png"),
    pygame.image.load("assets/assets/Hero_Walk_02.png"),
    pygame.image.load("assets/assets/Hero_Walk_03.png"),
    pygame.image.load("assets/assets/Hero_Walk_04.png")
]

curr_frame = 0
anim_time = 0
hero_walk_list = []
for i in range(4):
    hero_walk_list.append(pygame.image.load(f"assets/assets/Hero_Walk_0{i+1}.png"))


run_animation = False
curr_frame_mm = 0
anim_time_mm = 0
megaman_spritesheet = pygame.image.load("megaman_spritesheet.png")

pygame.init()
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
    dt = clock.get_time() # usado como medida de tempo, apesar de nao ser

    # para fazer qlqr animação >> feito em aula

    if keys []:


    anim_time = anim_time + dt
    anim_time_sec = anim_time/1000 # dividir por 1000 para passar de milessig para seg

    hero_anim_time = hero_anim_time + dt # serve para definir o tempo de cada frame em tela
    if  hero_anim_time > 0.2:
        hero_curr_frame = hero_curr_frame +1
        if hero_curr_frame > 3:
            hero_curr_frame = 0
        hero_anim_time = 0



    if anim_time_sec > 0.15:
        curr_frame = curr_frame + 1
        # curr_frame += 1
        if curr_frame > len(hero_walk_list) -1:
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

    if hero_curr_frame < 5:
        screen.blit(megaman_spritesheet, (pos_x,0),(60*hero_curr_frame,0,60,60)) #corta a spritesheet >> eu vou passar a posição da imagem, x e y; cm meu frame ta 60, vou de 0 a 60
    else:
        screen.blit(megaman_spritesheet, (pos_x,0),(60*hero_curr_frame,-5,60,60))


    # screen.blit(dog_img, (0, 0))
        screen.blit(hero_walk_list[curr_frame], (0, 0))

    # if curr_frame_mm < 5:
    #     screen.blit(megaman_spritesheet, (200, 200), (60 * curr_frame_mm, 0, 60, 60))
    # else:
    #     screen.blit(megaman_spritesheet, (200, 200), (60 * (curr_frame_mm - 5), 60, 60, 60))
    
    screen.blit(megaman_spritesheet, (200, 200), (60*(curr_frame_mm%5), 60*(curr_frame_mm//5), 60, 60))

    pygame.display.update()

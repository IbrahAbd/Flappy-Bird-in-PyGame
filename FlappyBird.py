import pygame
import sys
import random

# Animate floor. Have 2 floors that alternate on screen to create animation like illusion.
def draw_floor():
    screen.blit(floor,(floor_x_position,900))
    screen.blit(floor,(floor_x_position + 576 ,900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos-300))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface,pipe)
        else:
            # Flip pipe, with surface pipe_surface, not flip in x, flip in y.
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True

pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()

# Game variables
gravity = 0.25
movement = 0
game_active = True

# Background surface
bg_surface = pygame.image.load('flappy-bird-assets-master/sprites/background-day.png').convert()
# Fit to scale canvas.
bg_surface = pygame.transform.scale2x(bg_surface)

floor = pygame.image.load('flappy-bird-assets-master/sprites/base.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_position = 0

bird_surface = pygame.image.load('flappy-bird-assets-master/sprites/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100, 512))

pipe_surface = pygame.image.load('flappy-bird-assets-master/sprites/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,600,800]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                movement = 0
                movement -= 10
                
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,512) 
                movement = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface,(0,0))

    if game_active == True:
        # Bird logic
        movement += gravity
        bird_rect.centery += movement
        screen.blit(bird_surface,bird_rect)
        game_active = check_collision(pipe_list)

        # Pipe logic
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    # Floor logic
    floor_x_position -= 1
    draw_floor()
    if floor_x_position <= -576:
        floor_x_position = 0


    pygame.display.update()
    # 120 fps maximum
    clock.tick(120)


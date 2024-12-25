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

def move_pipes(pipes,score):
    for pipe in pipes:
        pipe.centerx -= 2.5
        # Check if the bird has passed this pipe
        if pipe.centerx == 100:  # Bird's X position (100) when it passes the pipe
            score += 0.5

    return pipes, score

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface,pipe)
        else:
            # Flip pipe, with surface pipe_surface, not flip in x, flip in y.
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    global score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        death_sound.play()
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -movement * 3,1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == "main game":
        score_surface = font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == "game over":
        score_surface = font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = font.render(f'Highscore: {int(high_score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,850))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 256)
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()

font = pygame.font.Font("04B_19.TTF",40)

# Game variables
gravity = 0.25
movement = 0
game_active = True
score = 0
high_score = 0

# Background surface
bg_surface = pygame.image.load('flappy-bird-assets-master/sprites/background-day.png').convert()
# Fit to scale canvas.
bg_surface = pygame.transform.scale2x(bg_surface)

floor = pygame.image.load('flappy-bird-assets-master/sprites/base.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_position = 0

# Animations for bird flapping
bird_downflap = pygame.transform.scale2x(pygame.image.load('flappy-bird-assets-master/sprites/bluebird-downflap.png')).convert_alpha()
bird_midflap = pygame.transform.scale2x(pygame.image.load('flappy-bird-assets-master/sprites/bluebird-midflap.png')).convert_alpha()
bird_upflap = pygame.transform.scale2x(pygame.image.load('flappy-bird-assets-master/sprites/bluebird-upflap.png')).convert_alpha()
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

pipe_surface = pygame.image.load('flappy-bird-assets-master/sprites/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,600,800]


game_over_surface = pygame.image.load('flappy-bird-assets-master/sprites/message.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center = (288,512))


flap_sound = pygame.mixer.Sound('flappy-bird-assets-master/audio/wing.wav')
death_sound = pygame.mixer.Sound('flappy-bird-assets-master/audio/die.wav')
score_sound = pygame.mixer.Sound('flappy-bird-assets-master/audio/point.wav')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                movement = 0
                movement -= 10
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,512) 
                movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if (bird_index < 2):
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface,(0,0))

    if game_active == True:
        # Bird logic
        movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)

        # Pipe logic
        pipe_list = move_pipes(pipe_list,score)[0]
        draw_pipes(pipe_list)
        score = move_pipes(pipe_list,score)[1]
        score_display('main game')
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game over")

    # Floor logic
    floor_x_position -= 1
    draw_floor()
    if floor_x_position <= -576:
        floor_x_position = 0


    pygame.display.update()
    # 120 fps maximum
    clock.tick(120)


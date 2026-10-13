import pygame
from pygame.locals import *
import random
import time
import os
import sys

def generate_lucky_box():
    return [random.randint(0, int(column_length) - 1), random.randint(0, int(row_length) - 1)]

def generate_food():
    return [random.randint(0, int(column_length) - 1), random.randint(0, int(row_length) - 1)]

def apply_random_lucky_box_effect():
    global invincible_mode, invincible_end_time, invincible_color_change
    global speed_boost_mode, speed_boost_end_time, fps
    global score_boost_active, score_boost_end_time

    effect_type = random.randint(1, 3) 

    if effect_type == 1:
        invincible_mode = True
        invincible_end_time = pygame.time.get_ticks() + 5000 
        invincible_color_change = True

    elif effect_type == 2:
        score_boost_active = True
        score_boost_end_time = pygame.time.get_ticks() + 5000 

    elif effect_type == 3:
        speed_boost_mode = True
        speed_boost_end_time = pygame.time.get_ticks() + 5000 
        global initial_fps
        fps = initial_fps * 2 


def manage_lucky_box():
    global box_pos, is_box_visible, screen, step
    if is_box_visible and box_pos is not None:
        pygame.draw.rect(screen, [0, 0, 0], [box_pos[0] * step, box_pos[1] * step, step, step])

def get_events():
    global run_game, direction, paused, snake_color, speed_boost_mode
    
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            run_game = False
            
        if event.type == KEYDOWN:
            if event.key == K_p:
                paused = not paused
                if paused:
                    invincible_color_change = False 
                    speed_boost_mode = False 
                    global fps, initial_fps
                    fps = initial_fps 
                else:
                    if invincible_mode:
                        invincible_color_change = True
                    if speed_boost_mode:
                         fps = initial_fps * 2

            if not paused:
                if (event.key == K_d or event.key == K_RIGHT) and not direction == 'left':
                    direction = 'right'
                elif (event.key == K_a or event.key == K_LEFT) and not direction == 'right':
                    direction = 'left'
                elif (event.key == K_w or event.key == K_UP) and not direction == 'down':
                    direction = 'up'
                elif (event.key == K_s or event.key == K_DOWN) and not direction == 'up':
                    direction = 'down'

def check_events():
    global food, score, box_pos, last_box_time, is_box_visible
    global invincible_mode, invincible_end_time, invincible_color_change
    global speed_boost_mode, speed_boost_end_time, fps, initial_fps
    global score_boost_active, score_boost_end_time, snake, run_game

    rel = [0,0]
    if direction == 'right':
        rel = [1,0]
    elif direction == 'left' :
        rel = [-1, 0]
    elif direction == 'up' :
        rel = [0, -1]
    elif direction == 'down' :
        rel = [0, 1]

    head = snake[-1].copy()
    new_head = [head[0] + rel[0] , head[1] + rel[1]]

    game_over = False
    if new_head[0] < 0 or new_head[1] < 0 or new_head[0] > column_length - 1 or new_head[1] > row_length - 1:
        if not invincible_mode:
            game_over = True
    elif new_head in snake:
        if not invincible_mode:
            game_over = True
            
    if game_over:
        run_game = False
        pygame.quit()
        print("Game Over!\n\n\nPress Enter...")
        input()
        show_menu()
         

    snake.append(new_head)

    ate_food = False
    if new_head == food:
       score += 1
       pygame.display.set_caption(f"SNAKE                 SCORE : {score}")
       food = generate_food()
       ate_food = True
        
    ate_lucky_box = False
    if is_box_visible and new_head == box_pos:
        apply_random_lucky_box_effect()
        ate_lucky_box = True
        is_box_visible = False 
        box_pos = None


    if not ate_food and not score_boost_active:
        snake.pop(0)
        
    if score_boost_active and pygame.time.get_ticks() >= score_boost_end_time:
        score_boost_active = False
        if not ate_food:
            snake.pop(0)

    if speed_boost_mode and pygame.time.get_ticks() >= speed_boost_end_time:
        speed_boost_mode = False
        fps = initial_fps 
 
    if invincible_mode and pygame.time.get_ticks() >= invincible_end_time:
        invincible_mode = False
        invincible_color_change = False 

def render_and_updates():
    global screen, snake, food, box_pos, is_box_visible, snake_color
    global invincible_color_change, paused 

    screen.fill([0, 100, 180])

    for i in range(step):
        pygame.draw.line(screen , [255, 255, 255], (i * step, 0), (i * step, Y))
    for i in range(step):
        pygame.draw.line(screen , [255, 255, 255], (0, i * step), (X, i * step))

    current_snake_color = snake_color
    if invincible_color_change:
        current_snake_color = [0, 255, 0] 

    for i in snake:
        pygame.draw.rect(screen, current_snake_color, [i[0] * step, i[1] * step, step, step]) 

    if food: 
        pygame.draw.rect(screen, food_color, [food[0] * step, food[1] * step, step, step])

    manage_lucky_box()

    pygame.display.update()

X = 900
Y = 900
step = 30
column_length = X / step
row_length= Y / step
score = 0

def show_scoreboard():
    os.system("cls")
    input("Press Enter to go back to menu...")
    show_menu()

def show_menu():
    os.system("cls")
    print("                 Snake\n")
    print("-" * 40)
    print("\n[0]               Start game\n")
    print("[1]               Scoreboard\n")
    print("[2]               Exit game\n")
    print("-" * 40)
    order = int(input("Order : "))
    if order == 0:
        os.system("cls")
        username = input("Username : ")
        start_game()
    elif order == 1:
        os.system("cls")
        show_scoreboard()
    elif order == 2:
        os.system("cls")
        print("Game Exited !")
        sys.exit()
    else:
        print("Wrong order!\n Press Eneter...")
        input()
        os.system("cls")
        show_menu()
    
def start_game():
    global is_box_visible, last_box_time, box_pos, box_spawn_time, is_box_visible, screen
    global run_game, food_color, snake, snake_color, initial_fps, food, direction, invincible_color_change, invincible_end_time, invincible_mode
    global speed_boost_end_time, speed_boost_mode, score_boost_active, score_boost_end_time, score_boost_segments, paused

    os.system("cls")
    pygame.init()
    screen = pygame.display.set_mode([X, Y])
    pygame.display.set_caption(f"SNAKE                 SCORE : {score}")
    run_game = True
    paused = False
    clock = pygame.time.Clock()
    fps = 20
    initial_fps = 20 
    snake = [ [column_length // 2, row_length // 2 ] ]
    snake_color = [255, 255, 255] 
    food_color = [30,180,20]
    food = generate_food() 
    direction = "up"
    box_pos = None 
    box_spawn_time = 0 
    last_box_time = pygame.time.get_ticks() 
    is_box_visible = False 

    invincible_mode = False 
    invincible_end_time = 0 
    invincible_color_change = False 

    speed_boost_mode = False 
    speed_boost_end_time = 0 

    score_boost_active = False 
    score_boost_end_time = 0 
    score_boost_segments = 5 
    while run_game:
        get_events()
        
        if not paused:
            check_events()
            
            now = pygame.time.get_ticks()
            if not is_box_visible and (now - last_box_time >= 10000): 
                box_pos = generate_lucky_box()
                box_spawn_time = now
                is_box_visible = True
                last_box_time = now 

        render_and_updates()
        
        clock.tick(fps)

    pygame.quit()
    print("Game exited.")
    show_menu()

show_menu()
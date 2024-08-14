import pygame, sys, time
from pygame.locals import *
from pygame.math import Vector2
pygame.init()

STATE = "intro_screen"
INTRO_SCREEN = "intro_screen"
GAME_OVER = "game_over"
GAME_START = "game_start"
GAME_PLAY = "game_play"

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20
speed = 250
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 32
FONT_OBJ = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
BIGGER_FONT_OBJ = pygame.font.Font('freesansbold.ttf', FONT_SIZE + 20)

W = False
S = False
ARROW_UP = False
ARROW_DOWN = False

PLAYER1_SCORE = 0
PLAYER2_SCORE = 0
VELOCITY = 5


def main():
    global W, S, ARROW_UP, ARROW_DOWN, PLAYER1_SCORE, PLAYER2_SCORE, STATE
    background = pygame.image.load("background.png")
    CLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pong")
    PLAYER1_SCORE = 0
    PLAYER2_SCORE = 0
    speed = 250
    paddle_speed = 250

    pos = Vector2(WINDOW_WIDTH-25, WINDOW_HEIGHT//2)


    #using a vector to represent position!
    block = pygame.Rect(*pos, BLOCK_SIZE, BLOCK_SIZE) # Using * UNPACKS a tuple into 2 values
    PADDLE1_pos = Vector2(25, WINDOW_HEIGHT//2)
    PADDLE2_pos = Vector2(WINDOW_WIDTH - 50, WINDOW_HEIGHT//2)
    PADDLE1 = pygame.Rect(*PADDLE1_pos, 20, 80)
    PADDLE2 = pygame.Rect(*PADDLE2_pos, 20, 80)

    movement_vector = Vector2(5, 1)
    movement_vector = movement_vector.normalize()

    up_pressed = False
    time = CLOCK.tick() #gives us a fresh start on the time (ignores start set-up time)
    while True:
        mouse_clicked = False
        DISPLAYSURF.blit(background, (0,0))
        score_text = FONT_OBJ.render("{:.0f}:{:.0f}".format(PLAYER1_SCORE, PLAYER2_SCORE), True, WHITE)
        font_obj_rect = score_text.get_rect()
        font_obj_rect.center = (WINDOW_WIDTH/2, 52)
        DISPLAYSURF.blit(score_text, font_obj_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                up_pressed = True
                if event.key == K_UP:
                    ARROW_UP = True
                elif event.key == K_DOWN:
                    ARROW_DOWN = True
                if event.key == K_w:
                    W = True
                elif event.key == K_s:
                    S = True
            elif event.type == KEYUP:
                up_pressed = False
                if event.key == K_w:
                    W = False
                elif event.key == K_s:
                    S = False

                if event.key == K_UP:
                    ARROW_UP = False
                elif event.key == K_DOWN:
                    ARROW_DOWN = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_clicked = True

        time = CLOCK.tick()
        time_seconds = time / 1000 #how much time in seconds have elapsed

        if STATE == INTRO_SCREEN:
            score_text = FONT_OBJ.render("{:.0f}:{:.0f}".format(PLAYER1_SCORE, PLAYER2_SCORE), True, WHITE)
            font_obj_rect = score_text.get_rect()
            font_obj_rect.center = (WINDOW_WIDTH/2, 52)
            DISPLAYSURF.blit(score_text, font_obj_rect)

            intro_text = FONT_OBJ.render("Click to Start", True, WHITE)
            font_intro_text = intro_text.get_rect()
            font_intro_text.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT//2)
            DISPLAYSURF.blit(intro_text, font_intro_text)

            PLAYER1_SCORE = 0
            PLAYER2_SCORE = 0
            speed = 250
            pygame.display.update()
            if mouse_clicked == True:
                STATE = GAME_START
        elif STATE == GAME_START:
            PADDLE1_pos = Vector2(25, WINDOW_HEIGHT//2)
            PADDLE2_pos = Vector2(WINDOW_WIDTH - 50, WINDOW_HEIGHT//2)
            PADDLE1 = pygame.Rect(*PADDLE1_pos, 20, 80)
            PADDLE2 = pygame.Rect(*PADDLE2_pos, 20, 80)
            PADDLE1_movement_vector = Vector2(0, 0)
            PADDLE2_movement_vector = Vector2(0, 0)

            speed = 250
            pos = Vector2(WINDOW_WIDTH//4, WINDOW_HEIGHT//2)
            block = pygame.Rect(*pos, BLOCK_SIZE, BLOCK_SIZE) # Using * UNPACKS a tuple into 2 values

            block_movement_vector = Vector2(1, 0)
            block_movement_vector = block_movement_vector.normalize()
            STATE = GAME_PLAY
        elif STATE == GAME_PLAY:
            
            distance_moved = time_seconds * speed #calculate desired movement magnitude in that time slice
            pos += distance_moved * block_movement_vector #add that movement to my current position
            PADDLE1_pos += (time_seconds * paddle_speed) * PADDLE1_movement_vector
            PADDLE2_pos += (time_seconds * paddle_speed) * PADDLE2_movement_vector
            PADDLE1.center = tuple(PADDLE1_pos)
            PADDLE2.center = tuple(PADDLE2_pos)
            
            PADDLE1_movement_vector = Vector2(0, 0)
            PADDLE2_movement_vector = Vector2(0, 0)
            block.center = tuple(pos)
            #print(PADDLE1_movement_vector)
            #print(PADDLE2_movement_vector)
            if W:
                PADDLE1_movement_vector -= Vector2(0, 1)
            if S:
                PADDLE1_movement_vector -= Vector2(0, -1)
            if ARROW_UP:
                PADDLE2_movement_vector -= Vector2(0, 1)
            if ARROW_DOWN:
                PADDLE2_movement_vector -= Vector2(0, -1)
    
            if PADDLE1.top < 0:
                PADDLE1_pos = [25, 50]
                PADDLE1_movement_vector = Vector2(0, -1)
            elif PADDLE1.bottom > WINDOW_HEIGHT:
                PADDLE1_pos = [25, WINDOW_HEIGHT - 50]
                PADDLE1_movement_vector = Vector2(0, 0)
            if PADDLE2.top < 0:
                PADDLE2_pos = [WINDOW_WIDTH - 50, 50]
                PADDLE2_movement_vector = Vector2(0, -1)
            elif PADDLE2.bottom > WINDOW_HEIGHT:
                PADDLE2_pos = [WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50]
                PADDLE2_movement_vector = Vector2(0, 0)

            #to test bounce
                """
            if block.right >= WINDOW_WIDTH and block_movement_vector.x > 0:
                block_movement_vector.x *= -1
            elif block.left <= 0 and movement_vector.x < 0:
                block_movement_vector.x *= -1
            """
            check_end(block, block_movement_vector)
        
            if check_end(block, block_movement_vector):
                STATE = GAME_START
            if block.bottom >= WINDOW_HEIGHT and block_movement_vector.y > 0:
                block_movement_vector.y *= -1
            elif block.top <= 0 and block_movement_vector.y < 0:
                block_movement_vector.y *= -1


            if PADDLE1.colliderect(block) and block_movement_vector.x < 0:
                block_movement_vector.x *= -1
                speed += 25
                block_movement_vector = (block_movement_vector * speed + PADDLE1_movement_vector * paddle_speed).normalize()
            elif PADDLE2.colliderect(block) and block_movement_vector.x > 0:
                block_movement_vector.x *= -1
                speed += 25
                block_movement_vector = (block_movement_vector * speed + PADDLE2_movement_vector * paddle_speed).normalize()
     

            pygame.draw.rect(DISPLAYSURF, WHITE, block)
            pygame.draw.rect(DISPLAYSURF, WHITE, PADDLE1)
            pygame.draw.rect(DISPLAYSURF, WHITE, PADDLE2)

            pygame.display.update()


def check_end(block, vector):
    global PLAYER1_SCORE, PLAYER2_SCORE
    if block.left <= 0 and vector.x < 0:
        PLAYER1_SCORE += 0.5
        #time.sleep(1)
        return True
    elif block.right >= WINDOW_WIDTH and vector.x > 0:
        PLAYER2_SCORE += 0.5
        #time.sleep(1)
        return True
    return False
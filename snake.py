import pygame
import random
import time
from constants import *

head_images = [ pygame.image.load(r"Images\head1.png"),
                pygame.image.load(r"Images\head2.png"),
                pygame.image.load(r"Images\head3.png"),
                pygame.image.load(r"Images\head4.png") ]

tail_images = [ pygame.image.load(r"Images\tail1.png"),
                pygame.image.load(r"Images\tail2.png"),
                pygame.image.load(r"Images\tail3.png"),
                pygame.image.load(r"Images\tail4.png") ]

body_images = [ pygame.image.load(r"Images\body horizontal.png"),
                pygame.image.load(r"Images\body vertical.png"),
                pygame.image.load(r"Images\body1.png"),
                pygame.image.load(r"Images\body2.png"),
                pygame.image.load(r"Images\body3.png"),
                pygame.image.load(r"Images\body4.png") ]

apple_image = pygame.image.load(r"Images\apple.png")
blank_image = pygame.image.load(r"Images\blank.png")

snake = []
apple = None
screen = None
move = None
last_move = None

def validPosition(pos):
    return pos[0] >= 0 and pos[0] < DIMENSION and pos[1] >= 0 and pos[1] < DIMENSION

def position(a, b):
    if a[0] < b[0] and a[1] == b[1]:
        return 'down'
    if a[0] > b[0] and a[1] == b[1]:
        return 'up'
    if a[0] == b[0] and a[1] < b[1]:
        return 'right'
    if a[0] == b[0] and a[1] > b[1]:
        return 'left'

def body_image(prev, curr, next):
    if ((position(prev, curr) == 'left' and position(curr, next) == 'left') or
        (position(prev, curr) == 'right' and position(curr, next) == 'right')):
        return body_images[0]
        # Horizontal
    if ((position(prev, curr) == 'up' and position(curr, next) == 'up') or
        (position(prev, curr) == 'down' and position(curr, next) == 'down')):
        return body_images[1]
        # Vertical
    if ((position(prev, curr) == 'up' and position(curr, next) == 'right') or
        (position(prev, curr) == 'left' and position(curr, next) == 'down')):
        return body_images[2]
        # ---
        # |
    if ((position(prev, curr) == 'up' and position(curr, next) == 'left') or
        (position(prev, curr) == 'right' and position(curr, next) == 'down')):
        return body_images[3]
        # ---
        #   |
    if ((position(prev, curr) == 'left' and position(curr, next) == 'up') or
        (position(prev, curr) == 'down' and position(curr, next) == 'right')):
        return body_images[4]
        # |
        # ---
    if ((position(prev, curr) == 'right' and position(curr, next) == 'up') or
        (position(prev, curr) == 'down' and position(curr, next) == 'left')):
        return body_images[5]
        #   |
        # ---

def head_image(prev, curr):
    if position(prev, curr) == 'right':
        return head_images[0]
    if position(prev, curr) == 'down':
        return head_images[1]
    if position(prev, curr) == 'left':
        return head_images[2]
    if position(prev, curr) == 'up':
        return head_images[3]

def tail_image(curr, next):
    if position(curr, next) == 'right':
        return tail_images[0]
    if position(curr, next) == 'down':
        return tail_images[1]
    if position(curr, next) == 'left':
        return tail_images[2]
    if position(curr, next) == 'up':
        return tail_images[3]

def draw():
    global snake, apple, screen
    screen.fill(BACKGROUND_COLOR)

    # Draw apple
    screen.blit(apple_image, (apple[1]*SIZE, apple[0]*SIZE))

    # Draw body
    for t in range(1, len(snake) - 1):
        img = body_image(snake[t+1], snake[t], snake[t-1])
        i, j = snake[t]
        screen.blit(img, (j*SIZE, i*SIZE))

    # Draw tail
    i, j = snake[len(snake)-1]
    img = tail_image(snake[len(snake)-1], snake[len(snake)-2])
    screen.blit(img, (j*SIZE, i*SIZE))

    #Draw head
    i, j = snake[0]
    img = head_image(snake[1], snake[0])
    screen.blit(img, (j*SIZE, i*SIZE))

    pygame.display.flip()

def over():
    global snake
    if len(snake) == MAX_LENGTH:
        return "won"

    if not validPosition(snake[0]):
        return "lost"
    
    for t in range(1, len(snake)):
        if snake[0] == snake[t]:
            return "lost"
    
    return None

def initialize():
    global snake, apple, move, last_move
    move = None
    last_move = None
    snake = []
    for j in range(2, 2 + INITIAL_LENGTH):
        snake.insert(0, (DIMENSION/2, j))
    
    apple = (DIMENSION/2, 3*DIMENSION/4)

def generate():
    global snake, apple
    list = []
    for i in range(0, DIMENSION):
        for j in range(0, DIMENSION):
            list.append((i, j))

    for t in range(0, len(snake)):
        list.remove(snake[t])
    
    index = random.randint(0, len(list) - 1)
    apple = list[index]

def game():
    global snake, move, apple, last_move
    initialize()
    draw()

    timer = time.time()
    state = over()

    while state == None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] and last_move != 'down':
                    move = 'up'
                elif keys[pygame.K_s] and last_move != 'up':
                    move = 'down'
                elif keys[pygame.K_a] and last_move != 'right' and move != None:
                    move = 'left'
                elif keys[pygame.K_d] and last_move != 'left':
                    move = 'right'
        
        if move == None:
            continue

        # Move
        if time.time() - timer >= TIME:
            i, j = snake[0]
            if move == 'up':
                last_move = 'up'
                i -= 1
            elif move == 'down':
                last_move = 'down'
                i += 1
            elif move == 'right':
                last_move = 'right'
                j += 1
            elif move == 'left':
                last_move = 'left'
                j -= 1
            
            snake.insert(0, (i, j))

            # Draw head
            img = head_image(snake[1], snake[0])
            screen.blit(img, (j*SIZE, i*SIZE))
            img = body_image(snake[2], snake[1], snake[0])
            screen.blit(img, (snake[1][1]*SIZE, snake[1][0]*SIZE))

            if (i, j) == apple:
                apple = None
            else:
                i, j = snake.pop(len(snake)-1)
                if (i, j) != snake[0]:
                    # Draw blank (if head is not on the prevois tail position)
                    screen.blit(blank_image, (j*SIZE, i*SIZE))

                # Draw tail
                i, j = snake[len(snake)-1]
                img = tail_image(snake[len(snake)-1], snake[len(snake)-2])
                screen.blit(img, (j*SIZE, i*SIZE))
            
            timer = time.time()

        if apple == None:
            generate()

            # Draw apple
            screen.blit(apple_image, (apple[1]*SIZE, apple[0]*SIZE))

        pygame.display.flip()
        state = over()
    
    return True

def main():
    global screen

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    icon = pygame.image.load('icon.ico')
    pygame.display.set_icon(icon)

    run = True
    while run:
        run = game()

    pygame.quit()

main()
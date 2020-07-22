#%%
import pygame
import random
import Learner

pygame.init()

#%% CONSTANTS
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

BLOCK_SIZE = 10 
DIS_WIDTH = 600
DIS_HEIGHT = 400

QVALUES_N = 100
FRAMESPEED = 50000

#%% Game 

def GameLoop():
    global dis
    
    dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    # Starting position of snake
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2
    x1_change = 0
    y1_change = 0
    snake_list = [(x1,y1)]
    length_of_snake = 1

    # Create first food
    foodx = round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
    foody = round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    dead = False
    reason = None
    while not dead:
        # Get action from agent
        action = learner.act(snake_list, (foodx,foody))
        if action == "left":
            x1_change = -BLOCK_SIZE
            y1_change = 0
        elif action == "right":
            x1_change = BLOCK_SIZE
            y1_change = 0
        elif action == "up":
            y1_change = -BLOCK_SIZE
            x1_change = 0
        elif action == "down":
            y1_change = BLOCK_SIZE
            x1_change = 0

        # Move snake
        x1 += x1_change
        y1 += y1_change
        snake_head = (x1,y1)
        snake_list.append(snake_head)

        # Check if snake is off screen
        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            reason = 'Screen'
            dead = True

        # Check if snake hit tail
        if snake_head in snake_list[:-1]:
            reason = 'Tail'
            dead = True

        # Check if snake ate food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            foody = round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
            length_of_snake += 1

        # Delete the last cell since we just added a head for moving, unless we ate a food
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Draw food, snake and update score
        dis.fill(BLUE)
        DrawFood(foodx, foody)
        DrawSnake(snake_list)
        DrawScore(length_of_snake - 1)
        pygame.display.update()

        # Update Q Table
        learner.UpdateQValues(reason)
        
        # Next Frame
        clock.tick(FRAMESPEED)

    return length_of_snake - 1, reason

def DrawFood(foodx, foody):
    pygame.draw.rect(dis, GREEN, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])   

def DrawScore(score):
    font = pygame.font.SysFont("comicsansms", 35)
    value = font.render(f"Score: {score}", True, YELLOW)
    dis.blit(value, [0, 0])

def DrawSnake(snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, BLACK, [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])



#%%
game_count = 1

learner = Learner.Learner(DIS_WIDTH, DIS_HEIGHT, BLOCK_SIZE)

while True:
    learner.Reset()
    if game_count > 100:
        learner.epsilon = 0
    else:
        learner.epsilon = .1
    score, reason = GameLoop()
    print(f"Games: {game_count}; Score: {score}; Reason: {reason}") # Output results of each game to console to monitor as agent is training
    game_count += 1
    if game_count % QVALUES_N == 0: # Save qvalues every qvalue_dump_n games
        print("Save Qvals")
        learner.SaveQvalues()


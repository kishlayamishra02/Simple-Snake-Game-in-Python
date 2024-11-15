import pygame as pg
from random import randrange

# Initialize constants and variables
WINDOW = 1000
TILE_SIZE = 40  # Reduced size for the snake and tiles
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]
snake = pg.Rect(0, 0, TILE_SIZE - 2, TILE_SIZE - 2)
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 200
food = snake.copy()
food.center = get_random_position()

# Pygame setup
pg.init()
screen = pg.display.set_mode([WINDOW] * 2, pg.RESIZABLE)  # Resizable window
clock = pg.time.Clock()
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

# Font for score and game over text
font = pg.font.SysFont('Arial', 30)
game_over_font = pg.font.SysFont('Arial', 60)

# Score variable
score = 0

# Game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.VIDEORESIZE:  # Handle window resize
            WINDOW = min(event.w, event.h)  # Keep it square
            screen = pg.display.set_mode((WINDOW, WINDOW), pg.RESIZABLE)
            RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and dirs[pg.K_w]:
                snake_dir = (0, -TILE_SIZE)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_s and dirs[pg.K_s]:
                snake_dir = (0, TILE_SIZE)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_a and dirs[pg.K_a]:
                snake_dir = (-TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
            if event.key == pg.K_d and dirs[pg.K_d]:
                snake_dir = (TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
    
    screen.fill('black')
    
    # Check for self-eating or border collision
    self_eating = any(segment.center == snake.center for segment in segments[:-1])
    if (
        snake.left < 0 or snake.right > WINDOW
        or snake.top < 0 or snake.bottom > WINDOW
        or self_eating
    ):
        # Game Over screen
        screen.fill('black')
        game_over_text = game_over_font.render('Game Over', True, 'red')
        score_text = game_over_font.render(f'Score: {score}', True, 'white')
        screen.blit(game_over_text, (WINDOW // 2 - 150, WINDOW // 2 - 50))
        screen.blit(score_text, (WINDOW // 2 - 100, WINDOW // 2 + 20))
        pg.display.flip()
        pg.time.wait(3000)
        # Reset game
        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_dir = 1, (0, 0)
        segments = [snake.copy()]
        score = 0
        continue
    
    # Check food collision
    if snake.colliderect(food):
        food.center = get_random_position()
        while food.center in [segment.center for segment in segments]:
            food.center = get_random_position()
        length += 1
        score += 1  # Increment score
    
    # Draw food
    pg.draw.rect(screen, 'red', food)
    
    # Draw snake
    for segment in segments:
        pg.draw.rect(screen, 'green', segment)
    # Draw snake head in blue
    pg.draw.rect(screen, 'blue', segments[-1])  # Snake head
    
    # Move snake
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        if len(segments) > length:
            segments.pop(0)
    
    # Draw score
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 10))  # Top-left corner
    
    pg.display.flip()
    clock.tick(60)

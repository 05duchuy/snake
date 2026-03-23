import pygame
import random
import os

pygame.init()

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (220, 220, 220)
MEDIUM_GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
SELECTED_COLOR = (100, 200, 100)

WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

font_small = pygame.font.SysFont("Arial", 20)
font_medium = pygame.font.SysFont("Arial", 30, bold=True)
font_large = pygame.font.SysFont("Arial", 50, bold=True)

snake_block = 20

clock = pygame.time.Clock()

DIFFICULTIES = {
    "EASY": {"speed": 10, "points": 2, "color": (100, 255, 100)},
    "NORMAL": {"speed": 15, "points": 5, "color": (255, 255, 100)},
    "HARD": {"speed": 20, "points": 10, "color": (255, 100, 100)}
}

HIGH_SCORE_FILE = "highscore.txt"

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            try:
                return int(file.read())
            except:
                return 0
    return 0

def draw_button(text, x, y, width, height, color, hover_color, text_color=BLACK, is_selected=False, difficulty=None):
    mouse_pos = pygame.mouse.get_pos()
    clicked = False
    
    if is_selected and difficulty:
        color = DIFFICULTIES[difficulty]["color"]
        hover_color = color
    
    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
        if pygame.mouse.get_pressed()[0]:
            clicked = True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))
        pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
    
    text_surf = font_medium.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + width/2, y + height/2))
    screen.blit(text_surf, text_rect)
    return clicked

def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], snake_block, snake_block])
        pygame.draw.rect(screen, BLACK, [block[0], block[1], snake_block, snake_block], 1)

def show_menu(high_score, current_difficulty):
    screen.fill(BLACK)
    
    title = font_large.render("SNAKE GAME", True, GREEN)
    screen.blit(title, (WIDTH//2 - title.get_width()//2 + 3, 53))
    title_shadow = font_large.render("SNAKE GAME", True, (0, 100, 0))
    screen.blit(title_shadow, (WIDTH//2 - title.get_width()//2, 50))
    
    high_score_text = font_medium.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, 120))
    
    easy_clicked = draw_button("EASY", WIDTH//2 - 220, 200, 120, 50, 
                              LIGHT_GRAY, MEDIUM_GRAY, BLACK, 
                              current_difficulty == "EASY", "EASY")
    
    normal_clicked = draw_button("NORMAL", WIDTH//2 - 60, 200, 120, 50, 
                               LIGHT_GRAY, MEDIUM_GRAY, BLACK, 
                               current_difficulty == "NORMAL", "NORMAL")
    
    hard_clicked = draw_button("HARD", WIDTH//2 + 100, 200, 120, 50, 
                             LIGHT_GRAY, MEDIUM_GRAY, BLACK, 
                             current_difficulty == "HARD", "HARD")
    
    start_clicked = draw_button("START GAME", WIDTH//2 - 120, 300, 240, 60, 
                              BLUE, (0, 150, 255), WHITE)
    
    pygame.display.update()
    
    selected_difficulty = None
    if easy_clicked: selected_difficulty = "EASY"
    if normal_clicked: selected_difficulty = "NORMAL"
    if hard_clicked: selected_difficulty = "HARD"
    
    return start_clicked, selected_difficulty

def main():
    high_score = load_high_score()
    game_active = False
    running = True
    difficulty = "NORMAL"
    
    button_cooldown = 0
    COOLDOWN_TIME = 10
    
    while running:
        if button_cooldown > 0:
            button_cooldown -= 1
        
        if not game_active:
            start_clicked, new_difficulty = show_menu(high_score, difficulty)
            
            if button_cooldown == 0:
                if new_difficulty:
                    difficulty = new_difficulty
                    button_cooldown = COOLDOWN_TIME
                
                if start_clicked:
                    button_cooldown = COOLDOWN_TIME
                    snake_speed = DIFFICULTIES[difficulty]["speed"]
                    points_per_food = DIFFICULTIES[difficulty]["points"]
                    
                    x, y = WIDTH // 2, HEIGHT // 2
                    x_change, y_change = 0, 0
                    snake_list = []
                    length_of_snake = 1
                    score = 0
                    food_x = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
                    food_y = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block
                    game_active = True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and x_change == 0:
                        x_change = -snake_block
                        y_change = 0
                    elif event.key == pygame.K_RIGHT and x_change == 0:
                        x_change = snake_block
                        y_change = 0
                    elif event.key == pygame.K_UP and y_change == 0:
                        x_change = 0
                        y_change = -snake_block
                    elif event.key == pygame.K_DOWN and y_change == 0:
                        x_change = 0
                        y_change = snake_block
            
            x += x_change
            y += y_change
            
            if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
                game_active = False
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                continue
            
            screen.fill(BLACK)
            
            pygame.draw.rect(screen, RED, [food_x, food_y, snake_block, snake_block])
            pygame.draw.rect(screen, BLACK, [food_x, food_y, snake_block, snake_block], 1)
            
            snake_head = [x, y]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]
            
            for block in snake_list[:-1]:
                if block == snake_head:
                    game_active = False
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)
                    break
            
            draw_snake(snake_list)
            
            score_text = font_small.render(f"Score: {score} | Difficulty: {difficulty}", True, WHITE)
            screen.blit(score_text, (10, 10))
            
            if (abs(x - food_x) < snake_block and abs(y - food_y) < snake_block):
                food_x = round(random.randrange(0, WIDTH - snake_block) / snake_block) * snake_block
                food_y = round(random.randrange(0, HEIGHT - snake_block) / snake_block) * snake_block
                length_of_snake += 1
                score += points_per_food
            
            pygame.display.update()
            clock.tick(snake_speed)
    
    pygame.quit()

if __name__ == "__main__":
    main()
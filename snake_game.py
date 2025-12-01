import pygame
import random
import datetime

# Pygame'i başlat
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 800, 600
INFO_BAR_HEIGHT = 50
CELL_SIZE = 30

# Renkler
BACKGROUND_COLOR = (30, 30, 30)
INFO_BAR_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
HIGHLIGHT_COLOR = (255, 215, 0)  # Altın rengi

# Ekranı oluştur
screen = pygame.display.set_mode((WIDTH, HEIGHT + INFO_BAR_HEIGHT))
pygame.display.set_caption("Snake Game")

# Yazı tipi
font = pygame.font.Font(None, 36)

def draw_text(text, position, color=TEXT_COLOR):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Zorluk seçenekleri menüsü (ilk ekran)
def draw_difficulty_menu(selected):
    screen.fill(BACKGROUND_COLOR)
    draw_text("Select Difficulty", (WIDTH//2 - 100, HEIGHT//4), TEXT_COLOR)
    difficulties = ["Easy", "Medium", "Hard"]
    for i, diff in enumerate(difficulties):
        y = HEIGHT//2 + i * 50
        if i == selected:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, (WIDTH//2 - 100, y - 10, 200, 40))
        draw_text(diff, (WIDTH//2 - 80, y))
    pygame.display.flip()

# Elma üretimi (yılanın bulunduğu hücreler dışındaki boş hücrelerden)
def generate_apple(snake):
    empty_spaces = [(x, y) for x in range(0, WIDTH, CELL_SIZE) 
                           for y in range(0, HEIGHT, CELL_SIZE) if (x, y) not in snake]
    return random.choice(empty_spaces) if empty_spaces else None

# Zorluk menüsünde seçim yapma
selected_difficulty = 0
game_started = False
while not game_started:
    draw_difficulty_menu(selected_difficulty)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and selected_difficulty > 0:
                selected_difficulty -= 1
            elif event.key == pygame.K_DOWN and selected_difficulty < 2:
                selected_difficulty += 1
            elif event.key == pygame.K_RETURN:
                game_started = True
    pygame.display.flip()

# Zorluk ayarları (FPS olarak kullanılacak hız)
difficulty_speed = {"Easy": 8, "Medium": 10, "Hard": 12}
speeds = list(difficulty_speed.values())
speed = speeds[selected_difficulty]

clock = pygame.time.Clock()

# Ana oyun döngüsü: "running" True iken oyun yeniden başlatılır
running = True
while running:
    # Her oyuna başlarken başlangıç durumlarını sıfırla
    snake = [((WIDTH // 2) // CELL_SIZE * CELL_SIZE, (HEIGHT // 2) // CELL_SIZE * CELL_SIZE)]
    direction = (CELL_SIZE, 0)
    apple = generate_apple(snake)
    score = 0
    game_over = False

    # Oyun içi döngü (oyun oynanıyor)
    while not game_over:
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, INFO_BAR_COLOR, (0, HEIGHT, WIDTH, INFO_BAR_HEIGHT))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)
        
        # Yılanın yeni baş konumunu hesapla
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        # Kenarlara çarpma kontrolü
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            game_over = True
        # Kendine çarpma kontrolü
        if new_head in snake:
            game_over = True
        
        snake.insert(0, new_head)
        if new_head == apple:
            score += 10
            apple = generate_apple(snake)
        else:
            snake.pop()
        
        # Yılanı çiz
        for seg in snake:
            pygame.draw.rect(screen, GREEN, (seg[0], seg[1], CELL_SIZE, CELL_SIZE))
        # Elmayı çiz
        if apple:
            pygame.draw.rect(screen, RED, (apple[0], apple[1], CELL_SIZE, CELL_SIZE))
        # Bilgi çubuğuna saat ve skor ekle
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        draw_text(current_time, (20, HEIGHT + 10))
        draw_text("Skor: " + str(score), (WIDTH - 150, HEIGHT + 10))
        pygame.display.flip()
        clock.tick(speed)
    
    # Oyun bittiğinde (game over) "Game Over" ekranı: alt alta seçenekler
    options = ["Devam Et", "Bitir"]
    selected_option = 0
    menu_active = True
    while menu_active:
        screen.fill(BACKGROUND_COLOR)
        draw_text("Game Over", (WIDTH//2 - 100, HEIGHT//2 - 80), RED)
        for i, opt in enumerate(options):
            y = HEIGHT//2 + i * 50
            if i == selected_option:
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, (WIDTH//2 - 100, y - 10, 200, 40))
            draw_text(opt, (WIDTH//2 - 80, y))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_option > 0:
                    selected_option -= 1
                elif event.key == pygame.K_DOWN and selected_option < len(options) - 1:
                    selected_option += 1
                elif event.key == pygame.K_RETURN:
                    if options[selected_option] == "Devam Et":
                        menu_active = False  # Oyun yeniden başlar (outer while döngüsü yeniden çalışır)
                    elif options[selected_option] == "Bitir":
                        pygame.quit()
                        exit()
        clock.tick(speed)

pygame.quit()

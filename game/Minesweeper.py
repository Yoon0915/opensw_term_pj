import pygame
import random

pygame.init()

# 색상 및 폰트 정의
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GRAY = (128, 128, 128)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)
FONT_LARGE = pygame.font.SysFont(None, 72)
FONT_MEDIUM = pygame.font.SysFont(None, 48)
FONT_SMALL = pygame.font.SysFont(None, 36)

# 화면 크기 및 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

CELL_SIZE = 50
GRID_COLS = SCREEN_WIDTH // CELL_SIZE
GRID_ROWS = SCREEN_HEIGHT // CELL_SIZE

# 게임 초기화 함수
def initialize_game():
    global grid_data, game_status
    grid_data = [[{'mine': False, 'opened': False, 'mine_count': 0, 'flagged': False} for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    for _ in range(NUM_MINES):
        while True:
            col = random.randint(0, GRID_COLS - 1)
            row = random.randint(0, GRID_ROWS - 1)
            if not grid_data[row][col]['mine']:
                grid_data[row][col]['mine'] = True
                break
    game_status = 0

NUM_MINES = 15
initialize_game()

# 시간 설정
clock = pygame.time.Clock()

# 범위 검사 함수
def is_within_bounds(col, row):
    return 0 <= col < GRID_COLS and 0 <= row < GRID_ROWS

# 타일 열기 함수
def reveal_tile(col, row):
    if not is_within_bounds(col, row):
        return

    tile = grid_data[row][col]
    if tile['opened'] or tile['mine']:
        return

    tile['opened'] = True
    surrounding_mines = count_surrounding_mines(col, row)
    if surrounding_mines > 0:
        tile['mine_count'] = surrounding_mines
    else:
        for dcol, drow in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            reveal_tile(col + dcol, row + drow)

# 주변 지뢰 개수 세기 함수
def count_surrounding_mines(col, row):
    count = 0
    for dcol, drow in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        ncol, nrow = col + dcol, row + drow
        if is_within_bounds(ncol, nrow) and grid_data[nrow][ncol]['mine']:
            count += 1
    return count

# 게임 실행 함수
def play_game():
    global game_status
    WIN = 1
    LOSS = 2

    while True:
        clock.tick(30)
        screen.fill(COLOR_BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if game_status > 0:
                    if event.key == pygame.K_SPACE:
                        initialize_game()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
            elif event.type == pygame.MOUSEBUTTONDOWN and game_status == 0:
                mouse_col = event.pos[0] // CELL_SIZE
                mouse_row = event.pos[1] // CELL_SIZE
                if event.button == 1:
                    if is_within_bounds(mouse_col, mouse_row):
                        tile = grid_data[mouse_row][mouse_col]
                        if tile['mine']:
                            tile['opened'] = True
                            game_status = LOSS
                        else:
                            reveal_tile(mouse_col, mouse_row)
                elif event.button == 3:
                    if is_within_bounds(mouse_col, mouse_row):
                        tile = grid_data[mouse_row][mouse_col]
                        tile['flagged'] = not tile['flagged']

                    win_condition = True
                    for row in grid_data:
                        for tile in row:
                            if tile['mine'] and not tile['flagged']:
                                win_condition = False
                    if win_condition:
                        game_status = WIN

        for col in range(GRID_COLS):
            for row in range(GRID_ROWS):
                tile = grid_data[row][col]
                if tile['mine_count']:
                    mine_count_img = FONT_SMALL.render(f'{tile["mine_count"]}', True, COLOR_YELLOW)
                    screen.blit(mine_count_img, mine_count_img.get_rect(centerx=col * CELL_SIZE + CELL_SIZE // 2, centery=row * CELL_SIZE + CELL_SIZE // 2))
                if tile['mine']:
                    mine_img = FONT_SMALL.render('X', True, COLOR_RED)
                    screen.blit(mine_img, mine_img.get_rect(centerx=col * CELL_SIZE + CELL_SIZE // 2, centery=row * CELL_SIZE + CELL_SIZE // 2))
                if not tile['opened']:
                    pygame.draw.rect(screen, COLOR_GRAY, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if tile['flagged']:
                    flag_img = FONT_SMALL.render('F', True, COLOR_WHITE)
                    screen.blit(flag_img, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))
                pygame.draw.rect(screen, COLOR_WHITE, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        if game_status > 0:
            game_over_text = FONT_LARGE.render('Game Over', True, COLOR_RED)
            screen.blit(game_over_text, game_over_text.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2 - 60))

            prompt_text = FONT_MEDIUM.render('Continue   Quit', True, COLOR_RED)
            screen.blit(prompt_text, prompt_text.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))

            key_hint_text = FONT_SMALL.render('   [Space]          [Esc]', True, COLOR_WHITE)
            screen.blit(key_hint_text, key_hint_text.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2 + 40))

        pygame.display.update()

play_game()
pygame.quit()

import pygame
import random
from datetime import datetime, timedelta

pygame.init()

# 색상 정의
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)

# 화면 크기 설정
screen_size = [400, 400]
display = pygame.display.set_mode(screen_size)

game_over = False
clock = pygame.time.Clock()
last_movement_time = datetime.now()

# 방향 키 매핑
DIRECTION_KEYS = {
    pygame.K_UP: 'NORTH',
    pygame.K_DOWN: 'SOUTH',
    pygame.K_LEFT: 'WEST',
    pygame.K_RIGHT: 'EAST',
}

# 블록 그리기 함수
def draw_square(display, color, position):
    square = pygame.Rect((position[1] * 20, position[0] * 20), (20, 20))
    pygame.draw.rect(display, color, square)

# 뱀 클래스
class Snake:
    def __init__(self):
        self.body_positions = [(0, 2), (0, 1), (0, 0)]
        self.heading = ''

    def render(self):
        for position in self.body_positions:
            draw_square(display, COLOR_GREEN, position)

    def move_forward(self):
        head = self.body_positions[0]
        row, col = head
        if self.heading == 'NORTH':
            self.body_positions = [(row - 1, col)] + self.body_positions[:-1]
        elif self.heading == 'SOUTH':
            self.body_positions = [(row + 1, col)] + self.body_positions[:-1]
        elif self.heading == 'WEST':
            self.body_positions = [(row, col - 1)] + self.body_positions[:-1]
        elif self.heading == 'EAST':
            self.body_positions = [(row, col + 1)] + self.body_positions[:-1]

    def increase_length(self):
        tail = self.body_positions[-1]
        row, col = tail
        if self.heading == 'NORTH':
            self.body_positions.append((row - 1, col))
        elif self.heading == 'SOUTH':
            self.body_positions.append((row + 1, col))
        elif self.heading == 'WEST':
            self.body_positions.append((row, col - 1))
        elif self.heading == 'EAST':
            self.body_positions.append((row, col + 1))

# 사과 클래스
class Apple:
    def __init__(self, initial_position=(5, 5)):
        self.position = initial_position

    def render(self):
        draw_square(display, COLOR_RED, self.position)

# 게임 루프 함수
def play_game():
    global game_over, last_movement_time

    # 초기화
    snake = Snake()
    apple = Apple()
    apple_count = 0  # 수집한 사과 갯수 초기화
    font = pygame.font.SysFont(None, 36)

    while True:
        clock.tick(10)
        display.fill(COLOR_WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        play_game()  # 재귀 호출로 게임을 다시 시작
                        return
                    elif event.key == pygame.K_ESCAPE:
                        return
                elif event.key in DIRECTION_KEYS:
                    snake.heading = DIRECTION_KEYS[event.key]

        # 게임 진행
        if not game_over:
            if timedelta(seconds=0.1) <= datetime.now() - last_movement_time:
                snake.move_forward()
                last_movement_time = datetime.now()

            # 뱀과 사과 충돌 확인
            if snake.body_positions[0] == apple.position:
                snake.increase_length()
                apple.position = (random.randint(0, 19), random.randint(0, 19))
                apple_count += 1  # 사과 갯수 증가

            # 뱀의 자기 충돌 체크
            if snake.body_positions[0] in snake.body_positions[1:]:
                game_over = True

        # 뱀과 사과 그리기
        snake.render()
        apple.render()

        # Apple 수집 갯수 왼쪽 상단에 표시
        apple_count_text = font.render(f"Apples: {apple_count}", True, COLOR_RED)
        text_rect = apple_count_text.get_rect(topright=(screen_size[0] - 10, 10))
        display.blit(apple_count_text, text_rect)

        # 게임 종료 시 메시지 표시
        if game_over:
            game_over_text = font.render("Game Over!", True, COLOR_RED)
            restart_text = font.render("Restart   Quit", True, COLOR_RED)
            controls_text = font.render("[Space]  [ESC]", True, COLOR_RED)
            
            display.blit(game_over_text, game_over_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 - 40)))
            display.blit(restart_text, restart_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2)))
            display.blit(controls_text, controls_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 + 40)))

        pygame.display.update()

play_game()
pygame.quit()

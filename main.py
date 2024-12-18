import pygame
import subprocess
import os

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("고전 전자 오락")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER_COLOR = (0, 102, 204)

# 폰트 설정
font = pygame.font.SysFont(None, 36)

# 버튼 클래스
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BUTTON_COLOR
        self.text = text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

# 게임 실행 함수
def run_tetris():
    subprocess.Popen(["python", os.path.join("game", "Tetris.py")])

def run_minesweeper():
    subprocess.Popen(["python", os.path.join("game", "Minesweeper.py")])

def run_Brick_break():
    subprocess.Popen(["python", os.path.join("game", "Brick_break.py")])

def run_Snake():
    subprocess.Popen(["python", os.path.join("game", "Snake.py")])

# 버튼 생성
tetris_button = Button(100, 50, 200, 50, "Tetris", run_tetris)
minesweeper_button = Button(100, 120, 200, 50, "Minesweeper", run_minesweeper)
brick_break_button = Button(100, 190, 200, 50, "Brick Break", run_Brick_break)
snake_button = Button(100, 260, 200, 50, "Snake", run_Snake)

# 버튼 리스트
buttons = [tetris_button, minesweeper_button, brick_break_button, snake_button]

# 메인 루프
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for button in buttons:
                button.check_click(mouse_pos)
    
    # 버튼에 마우스 오버 효과
    mouse_pos = pygame.mouse.get_pos()
    for button in buttons:
        if button.rect.collidepoint(mouse_pos):
            button.color = BUTTON_HOVER_COLOR
        else:
            button.color = BUTTON_COLOR

    # 버튼 그리기
    for button in buttons:
        button.draw(screen)

    pygame.display.flip()

pygame.quit()

import pygame
import subprocess
import os

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("게임 실행기")

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

# 버튼 생성
tetris_button = Button(100, 80, 200, 50, "Tetris", run_tetris)
minesweeper_button = Button(100, 160, 200, 50, "Minesweeper", run_minesweeper)

# 메인 루프
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            tetris_button.check_click(mouse_pos)
            minesweeper_button.check_click(mouse_pos)
    
    # 버튼에 마우스 오버 효과
    mouse_pos = pygame.mouse.get_pos()
    if tetris_button.rect.collidepoint(mouse_pos):
        tetris_button.color = BUTTON_HOVER_COLOR
    else:
        tetris_button.color = BUTTON_COLOR

    if minesweeper_button.rect.collidepoint(mouse_pos):
        minesweeper_button.color = BUTTON_HOVER_COLOR
    else:
        minesweeper_button.color = BUTTON_COLOR

    # 버튼 그리기
    tetris_button.draw(screen)
    minesweeper_button.draw(screen)

    pygame.display.flip()

pygame.quit()

import pygame
import random
import time

pygame.init()

# 색상 정의
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)

# 폰트 설정
main_font = pygame.font.SysFont(None, 72)
sub_font = pygame.font.SysFont(None, 36)

# 화면 크기 설정
width, height = 600, 800
display = pygame.display.set_mode((width, height))

fps_clock = pygame.time.Clock()

def play_game():
    points = 0
    misses = 0
    RESULT_WIN = 1
    RESULT_LOSE = 2
    game_status = 0

    # 벽돌 생성
    brick_list = []
    num_columns = 8
    num_rows = 7
    for x in range(num_columns):
        for y in range(num_rows):
            block = pygame.Rect(x * 70 + 35, y * 21 + 35, 60, 16)
            brick_list.append(block)

    # 공 설정
    ball = pygame.Rect(width // 2 - 8, height // 2 - 8, 16, 16)
    ball_dx = 5
    ball_dy = -5

    # 패들 설정
    paddle = pygame.Rect(width // 2 - 40, height - 20, 80, 16)
    paddle_dx = 0

    while True:
        fps_clock.tick(30)
        display.fill(COLOR_BLACK)

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                return
            elif evt.type == pygame.KEYDOWN:
                if game_status == 0:
                    if evt.key == pygame.K_LEFT:
                        paddle_dx = -5
                    elif evt.key == pygame.K_RIGHT:
                        paddle_dx = 5
                else:
                    # 게임 종료 상태에서 스페이스바로 재시작, ESC로 종료
                    if evt.key == pygame.K_SPACE:
                        play_game()  # 재귀 호출로 게임 재시작
                        return
                    elif evt.key == pygame.K_ESCAPE:
                        return
            elif evt.type == pygame.KEYUP:
                if evt.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    paddle_dx = 0

        if game_status == 0:
            # 패들 이동
            paddle.left += paddle_dx

            # 공 이동
            ball.left += ball_dx
            ball.top += ball_dy

            # 벽 충돌 처리
            if ball.left <= 0 or ball.left >= width - ball.width:
                ball_dx = -ball_dx
            if ball.top < 0:
                ball_dy = -ball_dy
            elif ball.top >= height:
                misses += 1
                ball.left = width // 2 - ball.width // 2
                ball.top = height // 2 - ball.width // 2
                ball_dy = -ball_dy

            if misses >= 3:
                game_status = RESULT_LOSE

            # 패들 화면 내 유지
            if paddle.left < 0:
                paddle.left = 0
            elif paddle.left > width - paddle.width:
                paddle.left = width - paddle.width

            # 벽돌 충돌 처리
            for block in brick_list:
                if ball.colliderect(block):
                    brick_list.remove(block)
                    ball_dy = -ball_dy
                    points += 1
                    break

            # 패들과 공 충돌
            if ball.colliderect(paddle):
                ball_dy = -ball_dy
                if ball.centerx <= paddle.left or ball.centerx > paddle.right:
                    ball_dx = -ball_dx

            # 게임 승리 조건
            if len(brick_list) == 0:
                game_status = RESULT_WIN

        # 화면 그리기
        for block in brick_list:
            pygame.draw.rect(display, COLOR_GREEN, block)

        if game_status == 0:
            pygame.draw.circle(display, COLOR_WHITE, (ball.centerx, ball.centery), ball.width // 2)

        pygame.draw.rect(display, COLOR_BLUE, paddle)

        score_display = sub_font.render(f'Score: {points}', True, COLOR_YELLOW)
        display.blit(score_display, (10, 10))

        miss_display = sub_font.render(f'Balls left: {3-misses}', True, COLOR_YELLOW)
        display.blit(miss_display, miss_display.get_rect(right=width - 10, top=10))

        if game_status > 0:
            result_message = main_font.render('Victory' if game_status == RESULT_WIN else 'Defeat', True, COLOR_RED)
            display.blit(result_message, result_message.get_rect(center=(width // 2, height // 2)))

            # 재시작 안내 메시지
            restart_message = sub_font.render('Press Space to Restart or ESC to Quit', True, COLOR_YELLOW)
            display.blit(restart_message, restart_message.get_rect(center=(width // 2, height // 2 + 50)))

        pygame.display.update()

play_game()
pygame.quit()

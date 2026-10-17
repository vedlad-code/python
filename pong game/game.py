import pygame
import random

pygame.init()

screen_width = 1200
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")
font = pygame.font.Font(None, size= 40)

# -x-x-x-x-x-x-x-x-x-x-x-x-x-paddle-x-x-x-x-x-x-x-x-x-x-x-x-x-
white = "#ffffff"
player_paddle = pygame.Rect(12, 350, 7, 50)
player_paddle.centery = screen.get_rect().centery
paddle_speed = 12
opp_paddle = pygame.Rect(0, 0, 7, 50)
opp_paddle.right = screen_width - 12
opp_paddle.centery = screen_height // 2
paddle_dict = {"player": player_paddle, "opponent" : opp_paddle}
# -x-x-x-x-x-x-x-x-x-x-x-x-x-x-paddle end-x-x-x-x-x-x-x-x-x-x-x-x-x-

# -x-x-x-x-x-x-x-x-x-x-x-x-x-x-ball-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
ball = pygame.Rect(0, 0, 14, 14)
ball.center = (screen_width // 2, screen_height // 2)
start_speed_x = 7
start_speed_y = 5
ball_speed_x = 0
ball_speed_y = 0
min_speed_y = 1
max_speed_y = 12
# -x-x-x-x-x-x-x-x-x-x-x-x-x-x-ball end-x-x-x-x-x-x-x-x-x-x-x-x-x-x-

# -x-x-x-x-x-x-x-x-x-x-x-x-x-x-points-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
player_score = 0
opp_score = 0
# -x-x-x-x-x-x-x-x-x-x-x-x-x-x-points end-x-x-x-x-x-x-x-x-x-x-x-x-x-x-

clock = pygame.time.Clock()
waiting = True
running = True

while running:
    
    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-updates-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
    player_dy = 0
    keys = pygame.key.get_pressed()
    multiplier_x = random.choice([1, -1])
    multiplier_y = random.choice([1, -1])

    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-player paddle movements-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
    if keys[pygame.K_w]:
        player_dy -= paddle_speed
    if keys[pygame.K_s]:
        player_dy += paddle_speed
    player_paddle.y += player_dy
    if player_paddle.top < 0:
        player_paddle.top = 0
        player_dy = 0
    if player_paddle.bottom > screen_height:
        player_paddle.bottom = screen_height
        player_dy = 0
    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-player paddle movements end-x-x-x-x-x-x-x-x-x-x-x-x-x-x-

    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-opponet paddle movements-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
    if keys[pygame.K_UP]:
        opp_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN]:
        opp_paddle.y += paddle_speed
    if opp_paddle.top < 0:
        opp_paddle.top = 0
    if opp_paddle.bottom > screen_height:
        opp_paddle.bottom = screen_height
    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-opponent paddle movements end-x-x-x-x-x-x-x-x-x-x-x-x-x-x-

    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-ball movements-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
    if not waiting:
        ball.x += ball_speed_x
        ball.y += ball_speed_y
        if ball.right > screen_width: 
            ball_speed_x *= -1 #temp condn
            player_score += 1
            ball.center = (screen_width // 2, screen_height // 2)
            waiting = True
            print(f"player_score:{player_score}, opp_score: {opp_score}")
        elif ball.left < 0: 
            ball_speed_x *= -1 #temp condn
            opp_score += 1
            ball.center = (screen_width // 2, screen_height // 2)
            waiting = True
            print(f"player_score:{player_score}, opp_score: {opp_score}")
        elif ball.top < 0 or ball.bottom > screen_height:
            ball_speed_y *= -1
    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-ball movements end-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
    
    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-collision checks-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
    collision = ball.collidedict(paddle_dict, True)
    if collision:
        # print("hit", ball.left, player_paddle.right)
        key, rect_hit = collision
        if key == "player" or key == "opponent":
            ball_speed_x *= -1
            if player_dy * ball_speed_y > 0:              # same direction: faster
                if ball_speed_y > 0:
                    ball_speed_y = min(ball_speed_y + 1, max_speed_y)
                    # print(f"dy={player_dy} ball_y_speed={ball_speed_y}")  #temp
                else:
                    ball_speed_y = max(ball_speed_y - 1, -max_speed_y)
                    # print(f"dy={player_dy} ball_y_speed={ball_speed_y}")  #temp

            elif player_dy * ball_speed_y < 0:              # opposite direction: slower
                if ball_speed_y > 0:
                    ball_speed_y = max(ball_speed_y - 1, min_speed_y)
                    # print(f"dy={player_dy} ball_y_speed={ball_speed_y}")  #temp
                else:
                    ball_speed_y = min(ball_speed_y + 1, -min_speed_y)
                    # print(f"dy={player_dy} ball_y_speed={ball_speed_y}")  #temp
        # print(f"Collided with: {key}")
    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-collision checks end-x-x-x-x-x-x-x-x-x-x-x-x-x-x-

    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-updates end-x-x-x-x-x-x-x-x-x-x-x-x-x-x-

    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-events-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and waiting:
            waiting = False
            ball_speed_x = multiplier_x * start_speed_x
            ball_speed_y = multiplier_y * start_speed_y
    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-events end-x-x-x-x-x-x-x-x-x-x-x-x-x-x-

    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-draw-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
    screen.fill(("#101010"))
    pygame.draw.rect(screen, white, player_paddle)
    pygame.draw.rect(screen, white, opp_paddle)
    if not waiting:
        pygame.draw.ellipse(screen, white, ball)
    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-draw end-x-x-x-x-x-x-x-x-x-x-x-x-x-x-

    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-text-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
    player_text = font.render(str(player_score), True, white)
    opp_text = font.render(str(opp_score), True, white)
    screen.blit(player_text, (screen_width // 2 - 80, 30))
    screen.blit(opp_text, (screen_width // 2 + 60, 30))
    if waiting:
        waiting_text = font.render("Press Space to Start", True, white)
        screen.blit(waiting_text, (screen_width//2 - 150, screen_height//2 - 19))
    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-text end-x-x-x-x-x-x-x-x-x-x-x-x-x-x-

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

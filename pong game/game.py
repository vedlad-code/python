import pygame

pygame.init()

screen_width = 1200
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")
font = pygame.font.Font(None, size= 30)

# -x-x-x-x-x-x-x-x-x-x-x-x-x-player_paddle-x-x-x-x-x-x-x-x-x-x-x-x-x-
white = "#ffffff"
player_paddle = pygame.Rect(12, 350, 7, 50)
player_paddle.centery = screen.get_rect().centery
paddle_speed = 12
opp_paddle = pygame.Rect(0, 0, 7, 50)
opp_paddle.right = screen_width - 12
opp_paddle.centery = screen_height // 2
paddle_dict = {"player": player_paddle, "opponent" : opp_paddle}
# -x-x-x-x-x-x-x-x-x-x-x-x-x-x-player_paddle end-x-x-x-x-x-x-x-x-x-x-x-x-x-

# -x-x-x-x-x-x-x-x-x-x-x-x-x-x-ball-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
ball = pygame.Rect(0, 0, 14, 14)
ball.center = (screen_width // 2, screen_height // 2)
ball_speed_x = -7
ball_speed_y = 5
min_speed_y = 1
max_speed_y = 12
# -x-x-x-x-x-x-x-x-x-x-x-x-x-x-ball end-x-x-x-x-x-x-x-x-x-x-x-x-x-x-

# -x-x-x-x-x-x-x-x-x-x-x-x-x-x-points-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
player_score = 0
opp_score = 0
# -x-x-x-x-x-x-x-x-x-x-x-x-x-x-points end-x-x-x-x-x-x-x-x-x-x-x-x-x-x-

clock = pygame.time.Clock()
running = True

while running:
    
    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-updates-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
    player_dy = 0
    keys = pygame.key.get_pressed()
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
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.right > screen_width: 
        ball_speed_x *= -1 #temp condn
        player_score += 1
        print(f"player_score:{player_score}, opp_score: {opp_score}")
    if ball.left < 0: 
        ball_speed_x *= -1 #temp condn
        opp_score += 1
        print(f"player_score:{player_score}, opp_score: {opp_score}")
    if ball.top < 0 or ball.bottom > screen_height:
        ball_speed_y *= -1
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
    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-events end-x-x-x-x-x-x-x-x-x-x-x-x-x-x-

    # -x-x-x-x-x-x-x-x-x-x-x-x-x-x-draw-x-x-x-x-x-x-x-x-x-x-x-x-x-x-
    screen.fill(("#101010"))
    pygame.draw.rect(screen, white, player_paddle)
    pygame.draw.ellipse(screen, white, ball)
    pygame.draw.rect(screen, white, opp_paddle)
    # pygame.draw.circle(screen, white, (ball_x, ball_y), ball_radius)
    player_text = font.render(str(player_score), True, white)
    opp_text = font.render(str(opp_score), True, white)
    screen.blit(player_text, (screen_width // 2 - 80, 30))
    screen.blit(opp_text, (screen_width // 2 + 60, 30))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()

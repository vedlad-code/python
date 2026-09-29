import pygame

pygame.init()

screen_width = 1200
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# paddle
white = "#ffffff"
paddle = pygame.Rect(12, 350, 7, 50)
paddle.centery = screen.get_rect().centery
paddle_speed = 8
# paddle end

# ball
ball_x = 600
ball_y = 350
ball_radius = 7
ball_speed_x = 3.5
ball_speed_y = 3.5
# ball end

clock = pygame.time.Clock()
running = True

while running:
    # updates
    # paddle movements
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle.y -= paddle_speed
    if keys[pygame.K_s]:
        paddle.y += paddle_speed
    if paddle.top < 0:
        paddle.top = 1
    if paddle.bottom > 700:
        paddle.bottom = 699
    # paddle movements end

    # ball movements
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    if ball_x < 0:
        ball_speed_x *= -1
    if ball_x > screen_width:
        ball_speed_x *= -1
    if ball_y < 0:
        ball_speed_y *= -1
    if ball_y > screen_height:
        ball_speed_y *= -1
    # updates end

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # events end

    # draw
    screen.fill(("#101010"))
    pygame.draw.rect(screen, white, paddle)
    pygame.draw.circle(screen, white, (ball_x, ball_y), ball_radius)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()

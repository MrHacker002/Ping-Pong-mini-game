import pygame
from random import randint
pygame.init()

clock = pygame.time.Clock()
FPS = 60

font1 = pygame.font.SysFont("Tahoma", 20)

platform_img = pygame.image.load("platform.png")
platform_img = pygame.transform.rotate(platform_img, 90)

ball_img = pygame.image.load("ball.png")
restart_img = pygame.image.load("restart.png")

#створи вікно гри
window = pygame.display.set_mode((700, 600))
pygame.display.set_caption("Ping-Pong")

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, x, y, width, height, image, speed, wasd):
        super().__init__(x, y, width, height, image)
        self.speed = speed
        self.wasd = wasd
    def move(self):
        keys = pygame.key.get_pressed()
        if self.wasd:
            if keys[pygame.K_w] and self.rect.y >= 1:
                self.rect.y -= self.speed
            if keys[pygame.K_s] and self.rect.y <= 599:
                self.rect.y += self.speed
        else:
            if keys[pygame.K_UP] and self.rect.y >= 1:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.y <= 599:
                self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, x, y, width, height, image, speed_x, speed_y):
        super().__init__(x, y, width, height, image)
        self.speed_x = speed_x
        self.speed_y = speed_y

player1 = Player(20, 285, 25, 70, platform_img, 5, True)
player2 = Player(660, 285, 25, 70, platform_img, 5, False)
ball = Ball(325, 295, 50, 50, ball_img, 0, 5)
restart_btn = GameSprite(640, 5, 50, 50, restart_img)


score_left = 0
lr_sc_l = 0
score_right = 0
lr_sc_r = 0
l_win_txt = font1.render("Лівий виграв", True, (0,0,0))
r_win_txt = font1.render("Правий виграв", True, (0,0,0))
r_win = False
l_win = False
game = True
finish = False
start = True
restart = False
direction = False
mouse_pos = 0, 0
while game:
    if not(finish):
        score = font1.render(f"Рахунок: {score_left} : {score_right}", True, (0,0,0))
        window.fill((255, 255, 255))
        window.blit(score, (300, 5))
        restart_btn.reset()
        player1.reset()
        player1.move()
        player2.reset()
        player2.move()
        ball.reset()

        if not(start):
            ball.rect.x += ball.speed_x
            ball.rect.y += ball.speed_y

        if score_left == 5 or score_right == 5:
            finish = True
            if score_left == 5:
                l_win = True
            if score_right == 5:
                r_win = True
        if ball.rect.colliderect(player1.rect):
            ball.speed_x *= -1    
        if ball.rect.colliderect(player2.rect):
            ball.speed_x *= -1    
        if ball.rect.right >= 700:
            score_left += 1
            restart = True
        if ball.rect.x <= 0:
            score_right += 1
            restart = True
        if ball.rect.y <= 0:
            ball.speed_y *= -1
        if ball.rect.bottom >= 600:
            ball.speed_y *= -1
        keys = pygame.key.get_pressed()
        if start or restart:
            if keys[pygame.K_SPACE]:
                if start:
                    direct = randint(0,1)
                    if direct == 0:
                        ball.speed_x = -5
                    if direct == 1:
                        ball.speed_x = 5
                    start = False
                else:
                    if direction:
                        ball.speed_x = 5
                    else:
                        ball.speed_x = -5
                    restart = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

    if restart:
        player1.rect.y = 285 
        player2.rect.y = 285 
        ball.rect.x = 325
        ball.rect.y = 295
        if score_left > lr_sc_l:
            direction = False
        if score_right > lr_sc_r:
            direction = True
        lr_sc_l = score_left
        lr_sc_r = score_right

    if l_win:
        window.blit(l_win_txt, (300, 280))
    if r_win:
        window.blit(r_win_txt, (300, 280))
    if pygame.Rect.collidepoint(restart_btn.rect, mouse_pos):
        finish = False 
        player1.rect.y = 285 
        player2.rect.y = 285 
        ball.rect.x = 325
        ball.rect.y = 295
        score_right = 0
        score_left = 0
        lr_sc_l = 0
        lr_sc_r = 0
        start = False
        direction = False
        r_win = False
        l_win = False
        mouse_pos = 0, 0
    pygame.display.update()
    clock.tick(FPS)







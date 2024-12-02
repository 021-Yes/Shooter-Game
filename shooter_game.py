#Create your own shooter

from pygame import *
from random import randint
from time import sleep

wd_w = 700
wd_h = 500
wd = display.set_mode(
    (wd_w, wd_h)
)
display.set_caption('Shooter Game')
bg = transform.scale(
    image.load('galaxy.jpg'), (wd_w, wd_h)
)

clock = time.Clock()

game = True

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        wd.blit(self.image, (self.rect.x, self.rect.y))

class Hero(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 595:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15)
        bullets.add(bullet)
        
lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > wd_h:
            self.rect.x = randint(5, 595)
            self.rect.y = 0
            lost += 1
        
class Bullet(GameSprite):
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > wd_h:
            self.rect.y = rocket.rect.y

rocket = Hero("rocket.png", 5, 395, 7.5)

bullets = sprite.Group()

ufos = sprite.Group()
for i in range(3):
    ufo_spawn = randint(5, 595)
    ufo_speed = randint(1, 3)
    ufo = Enemy("ufo.png", ufo_spawn, 5, ufo_speed)
    ufos.add(ufo)

font.init()
font1 = font.SysFont('Arial', 70)
win = font1.render('YOU WIN!', True, (255, 215, 0))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.SysFont('Arial', 50)

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound('fire.ogg')

scored = 0

finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
                fire.play()

    if finish != True:
        wd.blit(bg, (0, 0))
        rocket.reset()
        rocket.update()
        ufos.update()
        ufos.draw(wd)
        bullets.update()
        bullets.draw(wd)

    if sprite.spritecollide(rocket, ufos, False):
        wd.blit(lose, (200, 200))
        mixer.music.stop()
        finish = True

    collides = sprite.groupcollide(ufos, bullets, True, True)
    for c in collides:
        scored += 1
        ufo_spawn = randint(5, 595)
        ufo_speed = randint(1, 3)
        ufo = Enemy("ufo.png", ufo_spawn, 5, ufo_speed)
        ufos.add(ufo)

    if lost == 3:
        mixer.music.stop()
        finish = True
        wd.blit(lose, (200, 200))

    if scored == 10:
        mixer.music.stop()
        finish = True
        wd.blit(win, (200, 200))
        

    score = font2.render('Score: ' + str(scored), True, (255, 255, 255))
    miss = font2.render('Missed: ' + str(lost), True, (255, 255, 255))
    wd.blit(score, (5, 5))
    wd.blit(miss, (5, 50))

    display.update()
    clock.tick(60)
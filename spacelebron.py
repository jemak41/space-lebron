import pygame
from pygame.locals import *
from sys import exit
import os
import random

SCREENSIZE = 480, 600

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
pygame.display.set_caption("Lebron on Space")
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("Arial", 30)
score = 0

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
snd_folder = os.path.join(game_folder, "snd")

background = pygame.image.load(os.path.join(img_folder, "stars.png"))

class Lebron(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "crying bron3.jpg")).convert()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.radius = 23
        #pygame.draw.circle(self.image, (255,0,0), self.rect.center, self.radius)
        self.rect.left = SCREENSIZE[0] / 2
        self.rect.top = SCREENSIZE[1] - 110
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rect.left -= 10
        elif keys[K_RIGHT]:
            self.rect.left += 10
        elif keys[K_UP]:
            self.rect.top -= 10
        elif keys[K_DOWN]:
            self.rect.top += 10
        elif keys[K_SPACE]:
            self.shoot()


        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.left > SCREENSIZE[0] - 50:
            self.rect.left = SCREENSIZE[0] - 50
        if self.rect.top < 10:
            self.rect.top = 10
        if self.rect.top > SCREENSIZE[1] - 90:
            self.rect.top = SCREENSIZE[1] - 90

    def shoot(self):
        #THIS BLOCK OF CODE IS USED FOR DELAY
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now


            bullet1 = Bullet1(self.rect.left, self.rect.top)
            bullet2 = Bullet2(self.rect.right, self.rect.top)
            all_sprites.add(bullet1, bullet2)
            bullets.add(bullet1, bullet2)
            shoot_sounds.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super(Mob, self).__init__()
        self.image_orig = pygame.image.load(os.path.join(img_folder, "kawhi.png")).convert()
        self.image_orig = pygame.transform.scale(self.image_orig, (50,50))
        self.image = self.image_orig.copy()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = 24
        #pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)
        self.rect.left = random.randrange(SCREENSIZE[0] - self.rect.width)
        self.rect.top = random.randrange(-100, -40)
        self.speedy = random.randrange(5,8)
        self.speedx = random.randrange(-2, 2)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)

    def update(self):
        #self.rotate()
        self.rect.top += self.speedy
        self.rect.left += self.speedx
        if self.rect.top > SCREENSIZE[1] + 10:
            self.rect.left = random.randrange(SCREENSIZE[0] - self.rect.width)
            self.rect.top = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 6)

class Bullet1(pygame.sprite.Sprite):
    def __init__(self, x1, y1):
        super(Bullet1, self).__init__()
        self.image = pygame.Surface((2, 10))
        self.image.fill((255, 0, 0))
        '''self.image = pygame.image.load(os.path.join(img_folder, "ball.png")).convert()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.image.set_colorkey((255, 255, 255))'''
        self.rect = self.image.get_rect()
        self.radius = 3
        self.rect.bottom = y1
        self.rect.centerx = x1
        self.speedy = -10

    def update(self):
        self.rect.top += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Bullet2(pygame.sprite.Sprite):
    def __init__(self, x1, y1):
        super(Bullet2, self).__init__()
        self.image = pygame.Surface((2, 10))
        self.image.fill((255,0,0))
        '''
        self.image = pygame.image.load(os.path.join(img_folder, "ball.png")).convert()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.image.set_colorkey((255, 255, 255))'''
        self.rect = self.image.get_rect()
        self.radius = 3
        self.rect.bottom = y1
        self.rect.centerx = x1
        self.speedy = -10

    def update(self):
        self.rect.top += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super(Explosion, self).__init__()
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def game_over():

    clock.tick(1)
    game = myfont.render("GAME OVER!", False,(255,255,255))
    flop = myfont.render("YOU FLOPPED", False,(255,255,255))
    background = pygame.image.load("lebron flop.jpg").convert()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        screen.fill((0,0,0))
        screen.blit(background, ((SCREENSIZE[0] - background.get_width()) / 2, 0))
        screen.blit(game, ((SCREENSIZE[0] - game.get_width()) / 2,10))
        screen.blit(flop, ((SCREENSIZE[0] - flop.get_width()) / 2, SCREENSIZE[1] - 80))
        pygame.display.flip()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

lebron = Lebron()
all_sprites.add(lebron)

#Sounds
shoot_sounds = pygame.mixer.Sound(os.path.join(snd_folder, "Laser_Shoot15.wav"))
explosion_sounds = pygame.mixer.Sound(os.path.join(snd_folder, "Explosion5.wav"))


#Images
explosion_animation = {}
explosion_animation['lg'] = []
#explosion_animation['sm'] = []

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert()
    img.set_colorkey((0,0,0))
    img_lg = pygame.transform.scale(img, (75,75))
    explosion_animation['lg'].append(img_lg)

for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()


    #Update
    all_sprites.update()

    #if bullets hit the mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        score += 1
        explosion_sounds.play()

        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)

        m = Mob()
        all_sprites.add(m)
        mobs.add(m)


    #if mob hits lebron
    hits = pygame.sprite.spritecollide(lebron, mobs, False, pygame.sprite.collide_circle)
    for hit in hits:
        explosion_sounds.play()

        game_over()



    #Draw
    screen.fill((0, 0, 0))
    screen.blit(background, (0,0))

    now = pygame.time.get_ticks()

    time = myfont.render(str(int(now * 0.001)), False, (255, 255, 255))


    scores = myfont.render(str(score), False, (255, 255, 255))


    all_sprites.draw(screen)
    screen.blit(scores, (50, 50))
    screen.blit(time, (400, 50))

    pygame.display.flip()

pygame.quit()
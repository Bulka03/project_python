from pygame import *
from random import randint
window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

clock = time.Clock()
FPS = 60

font.init()
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
 

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.y = player_y
        self.rect.x = player_x
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx-5, self.rect.top, 15, 20, -10)
        bullets.add(bullet)
lost = 0

count = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = -100
            self.rect.x = randint(0, 630)
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = -100
            self.rect.x = randint(0, 630)
            lost = lost + 1
            

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < -10:
            self.kill()




main_sprite = Player('rocket.png', 325, 400, 75, 100, 10)

monsters = sprite.Group()
for i in range(5):
    sprite2 = Enemy('ufo.png', randint(80, 635), 10, 75, 50, randint(1, 5))
    monsters.add(sprite2)

asteroids = sprite.Group()
for i in range(2):
    sprite3 = Asteroid('asteroid.png', randint(80, 635), 10, 75, 50, randint(1, 5))
    asteroids.add(sprite3)

bullets = sprite.Group()




font1 = font.Font(None, 36)
font2 = font.Font(None, 36)
font3 = font.Font(None, 90)
text_lossgame = font3.render("YOU LOSE", True, (255, 0, 0))
text_win = font3.render("YOU WIN", True, (255, 255, 255))
count_lifes = 3
game = True
finish = False
while game:
    if finish != True:
        window.blit(background,(0, 0))
        text_lose = font1.render("Пропущено:" + str(lost), True, (255, 255, 255))
        text_count = font2.render("Счет:" + str(count), True, (255, 255, 255))
        text_count_lifes = font3.render("Счетчик жизней" + str(count_lifes), True, (255, 255, 255))
        window.blit(text_lose,(0, 50))
        window.blit(text_count,(0, 25))
        main_sprite.update()
        main_sprite.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
        if sprite.spritecollide(main_sprite, monsters, True) or sprite.spritecollide(main_sprite, asteroids, True):
            count_lifes -= 1
        if count_lifes <=0 or lost > 100:
            finish = True
            window.blit(text_lossgame,(200, 200))
        sprites_list = sprite.groupcollide(bullets, monsters, True, True)
        for m in sprites_list:
            count += 1
            sprite2 = Enemy('ufo.png', randint(80, 635), 10, 75, 50, randint(1, 5))
            monsters.add(sprite2)
        if count > 100:
            finish = True
            window.blit(text_win,(200, 200))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type  == KEYDOWN:
            if e.key == K_SPACE:
                main_sprite.fire()
            if e.key == K_UP:
                for monster in monsters:
                    monster.rect.y = -60
                for asteroid in asteroids:
                    asteroid.rect.y = -60
                lost = 0
                count = 0
                finish = False        

    display.update()
    clock.tick(FPS)
#Создай собственный Шутер!
from pygame import * 
from random import randint
from time import time as timer
#класс-родитель для спрайтов 
class GameSprite(sprite.Sprite): 
 #конструктор класса 
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed): 
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение 
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) 
        self.speed = player_speed 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y 
 
    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y)) 
 
#класс-наследник для спрайта-игрока (управляется стрелками) 
class Player(GameSprite): 
    def update(self): 
 
 # Управление над игроком с помощью клавиш-стрелочек 
        keys = key.get_pressed() 
        if keys[K_LEFT] and self.rect.x > 5: 
            self.rect.x -= self.speed 
        if keys[K_RIGHT] and self.rect.x < win_width - 80: 
            self.rect.x += self.speed 
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
 
#класс-наследник для спрайта-врага (перемещается сам) 
class Enemy(GameSprite): 
    def update(self):
        self.rect.y += self.speed 
        global lost
        if self.rect.y > win_height: 
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
#класс для спрайтов-препятствий 
class Asteroid(GameSprite): 
    def update(self):
        self.rect.y += self.speed 
        global lost
        if self.rect.y > win_height: 
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
 
#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
score = 0
lost = 0
max_lost = 3
lives = 3
rel_time = 3
#Персонажи игры:
ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
Asteroids = sprite.Group()
for i in range(1, 4):
    Asteroida = Asteroid('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    Asteroids.add(Asteroida)
bullets = sprite.Group()
rel_time = False
game = True
finish = False
clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (0, 180, 0))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 30)
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    if not finish:
        window.blit(background, (0,0))
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
            score = score + 1
            
        text = font2.render('Счёт: '+ str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        if score >= 10:
            finish = True
            window.blit(win, (200, 200))
        if lost >= 20:
            finish = True
            window.blit(lose, (200, 200))
        ship.update()
        monsters.update()
        bullets.update()
        Asteroids.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        Asteroids.draw(window)



 
        display.update()
    clock.tick(FPS)
    mixer.music.play()

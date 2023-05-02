from pygame import *
from random import randint


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.SysFont('Arial Black', 36)
font1 = font.SysFont('Arial Black', 40)


img_back = "galaxy.jpg" 
img_hero = "rocket.png" 
img_enemy = "ufo.png" 
img_bullet = "bullet.png"
img_start = "start_image.jpg"


score = 0 
lost = 0 


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

       
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
   
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        
    def finishing(self):
        self.rect.y -= self.speed
 
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.x + 26, self.rect.y - 50, 30, 50, -30) # создание пули
        bullets.add(bullet)

    
 

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

                                         

win_width = 1400
win_height = 800
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
start_bg = transform.scale(image.load(img_start), (win_width, win_height))


ship = Player(img_hero, 3, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)


bullets = sprite.Group() 


start = True
game = True 
finish = False
clock = time.Clock()
FPS = 60


while game:
     
    while start:
        for e in event.get():
            if e.type == QUIT:
                start = False
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    start = False
        
        
        start_text = font1.render('Добро пожаловать в игру "Shooter"!', 1, (255, 255,255))
        start_text2 = font2.render('Чтобы продолжить нажмите "ПРОБЕЛ"!', 0, (0, 255,255))
        
        window.blit(start_bg,(0, 0))
        window.blit(start_text, (350, 390))
        window.blit(start_text2, (350, 700))

        display.update()
        clock.tick(FPS)


    text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255,255))
    text_win = font2.render("Счёт: " + str(score), 1, (255, 255 ,255))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()


    if lost >= 3:
        finish = True
        text_lose = font2.render("Вы проиграли!", 3, (255, 0, 0))
        window.blit(text_lose,(win_width // 2 - 200, win_height // 2))
    

    if score >= 10:
        finish = True
        text_win = font2.render("Поздравляем, вы прошли игру!", 3, (0, 255, 0))
        window.blit(text_win,(win_width // 2 - 300, win_height // 2))
        ship.finishing()




    if not finish:
        window.blit(background,(0, 0))
        window.blit(text_lose,(20, 50))
        window.blit(text_win,(20, 20))

        ship.update()
        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()

        ship.reset()
        monster.reset()


        collisions = sprite.groupcollide(monsters, bullets, True, True)
        for c in collisions:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)


        display.update()
        clock.tick(FPS)
    else:
        for e in event.get():
            if e.type == QUIT:
                game = False

        display.update()
        clock.tick(FPS)


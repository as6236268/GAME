import pygame
import random
import os

FPS = 60
WIDTH = 600
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
STONE = (112, 128, 144)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# 遊戲初始化&創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("腥際大戰")  # 視窗遊戲名稱
clock = pygame.time.Clock()

# 載入圖片
icon_img = pygame.image.load(os.path.join("img", "R2D2.jpg")).convert()
icon_img = pygame.transform.scale(icon_img, (25, 25))
icon_img.set_colorkey(WHITE)
pygame.display.set_icon(icon_img)
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
player_img = pygame.image.load(os.path.join("img", "spaceship.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 25))
player_mini_img.set_colorkey(BLACK)
# rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
for i in range(9):
    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
power_imgs = {}
cross_img = pygame.image.load(os.path.join("img", "cross.png")).convert()
# shield_img = pygame.image.load(os.path.join("img", "shield2.png")).convert()
# shield_img.set_colorkey(BLACK)
power_imgs['cross'] = pygame.transform.scale(cross_img, (30, 30))
power_imgs['gun'] = pygame.image.load(os.path.join("img", "gun.png")).convert()
# power_imgs['shield'] = pygame.transform.scale(shield_img, (30, 30))


# 載入音效
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
cross_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
# shield_sound = pygame.mixer.Sound(os.path.join("sound", "magic2.mp3"))
expl1 = pygame.mixer.Sound(os.path.join("sound", "expl0.wav"))
expl2 = pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
expl1.set_volume(0.5)  # 調整爆炸音效大小
expl2.set_volume(0.5)
explo_sounds = [expl1, expl2]
pygame.mixer.music.load(os.path.join("sound", "starwars.mp3"))  # 背景音樂
pygame.mixer.music.set_volume(0.5)
shoot_sound.set_volume(0.7)


font_name = os.path.join("font.ttf")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)  # 設定字型&字體大小
    text_surface = font.render(text, True, WHITE)  # 文字介面
    text_rect = text_surface.get_rect()  # 文字定位
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100) * BAR_LENGTH  # 剩餘血量%數
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    if hp < 30:
        pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i  # 調整生命值距離
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(background_img, (0, 0))  #將圖片畫上去
    draw_text(screen, '腥際大戰', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, '← →移動 空白建射擊', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '按任意建開始遊戲', 18, WIDTH/2, HEIGHT * 3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)  # 一秒鐘之內最多被執行幾次(禎數)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False

def draw_die_init():
    screen.blit(background_img, (0, 0))  # 將圖片畫上去
    draw_text(screen, "GAME OVER !", 64, WIDTH/2, HEIGHT/3)
    draw_text(screen, '請按任意鍵繼續', 22, WIDTH/2, HEIGHT* 3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)  # 一秒鐘之內最多被執行幾次(禎數)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False


# 建立類別
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # 初始函式
        self.image = player_img
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(BLACK)
        # self.image = pygame.Surface((50, 40))  # 遊戲圖標
        # self.image.fill(GREEN)  # 填滿
        self.rect = self.image.get_rect()  # 圖片定位
        self.radius = 25  # 設定圖形碰撞大小
        # pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        self.speedx = 8  # 調整移動速度
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0
        # self.shi = 0
        # self.shi_time = 0

    def update(self):
        now = pygame.time.get_ticks()
        # if self.shi > 0 and now - self.shi_time > 5000:
        #     self.shi -= 1
        #     self.shi_time = now

        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now

        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        key_pressed = pygame.key.get_pressed()  # 判斷按鍵有沒有被按下去
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        # if key_pressed[pygame.K_UP]:
        #     self.rect.y -= self.speedx
        # if key_pressed[pygame.K_DOWN]:
        #     self.rect.y += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        # if self.rect.top < 0:
        #     self.rect.top = 0
        # if self.rect.bottom > HEIGHT:
        #     self.rect.bottom = HEIGHT

    def shoot(self):
        if not (self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()



    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

    # def shield(self):
    #     self.shi += 1
    #     self.shi_time = pygame.time.get_ticks()


        # self.rect.x += 2
        # if self.rect.left > WIDTH:
        #     self.rect.right = 0

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # 初始函式
        self.image_ori = random.choice(rock_imgs)
        # self.image = pygame.transform.scale(self.image, (50, 50))
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        # self.image = pygame.Surface((30, 40))  # 遊戲圖標
        # self.image.fill(STONE)  # 填滿
        self.rect = self.image.get_rect()  # 圖片定位
        self.radius = int(self.rect.width * 0.85 / 2)  # 設定圖形碰撞大小
        # pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH-self.rect.width)
        self.rect.y = random.randrange(-200, -150)
        self.speedy = random.randrange(2, 10)  # 調整x軸速度
        self.speedx = random.randrange(-3, 3)  # 調整y軸速度
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)  # 調整x軸速度
            self.speedx = random.randrange(-3, 3)  # 調整y軸速度

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # 初始函式
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        # self.image = pygame.Surface((10, 20))  # 遊戲圖標
        # self.image.fill(YELLOW)  # 填滿
        self.rect = self.image.get_rect()  # 圖片定位
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self .rect.bottom < 0:
            self.kill()  #刪除物件

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)  # 初始函式
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()  # 圖片定位
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # 控制爆炸動畫速度

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)  # 初始函式
        self.type = random.choice(['cross', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        # self.image = pygame.Surface((10, 20))  # 遊戲圖標
        # self.image.fill(YELLOW)  # 填滿
        self.rect = self.image.get_rect()  # 圖片定位
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self .rect.top > HEIGHT:
            self.kill()  #刪除物件

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    new_rock()
score = 0
pygame.mixer.music.play(-1)

running = True

# 遊戲迴圈
show_init = True
# die_init = False
runnung = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score = 0
    clock.tick(FPS)  # 一秒鐘之內最多被執行幾次(禎數)
    # 取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()


    # 更新遊戲
    all_sprites.update()

    # 判斷石頭與子彈相撞
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        random.choice(explo_sounds).play()
        score += hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.8:  # 寶物掉落機率
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()
    # 判斷石頭與飛船相撞
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)  # 石頭撞飛船
    for hit in hits:
        player.health -= hit.radius
        new_rock()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <= 0:
            die = Explosion(player.rect.center, 'player')
            all_sprites.add(die)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()

    # 判斷寶物與飛船相撞
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'cross':
            player.health += 15
            if player.health > 100:
                player.health = 100
            cross_sound.play()
        elif hit.type == 'gun':
            player.gunup()
            gun_sound.play()
        # elif hit.type == 'shield':
        #     player.shield()
        #     shield_sound.play()

    # 生命值歸0
    if player.lives == 0 and not (die.alive()):
        down = draw_die_init()
        if down:
            break
        show_init = True

    # 畫面顯示
    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))  #將圖片畫上去
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
    pygame.display.update()


pygame.quit()
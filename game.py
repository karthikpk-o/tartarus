import pygame, os, time, sys
from pygame.locals import *
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

WIDTH = 1550 
HEIGHT = 750

clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT,1000)
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255,215,0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tartarus')

font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)
font_over = pygame.font.SysFont('Bauhaus 93',100)
text = '90'

tile_size = 30
game_over = 0
main_menu = True
level = 0
max_levels = 4
score = 0
high_score = 0
count = 0
Time = 90

restart_img = pygame.image.load(os.path.join('ASSETS','restart.png'))
pause_img = pygame.image.load(os.path.join('ASSETS','pause.png'))
pause_img = pygame.transform.scale(pause_img, (100,100))
menu_img = pygame.image.load(os.path.join('ASSETS','menu.png'))
menu_img = pygame.transform.scale(menu_img, (150,100))
playagain_img = pygame.image.load(os.path.join('ASSETS','playagain.png'))
playagain_img = pygame.transform.scale(playagain_img, (200,130))
gameover_img=pygame.image.load(os.path.join('ASSETS','game over.png'))
gameover_img=pygame.transform.scale(gameover_img, (WIDTH,HEIGHT))
gameover_rect=gameover_img.get_rect()
map_img = pygame.image.load(os.path.join('ASSETS', 'map.png'))
map_img = pygame.transform.scale(map_img, (500,750))
map_rect = map_img.get_rect()
timer_img = pygame.image.load(os.path.join('ASSETS','timer.png'))
timer_img = pygame.transform.scale(timer_img, (300,100))

pygame.mixer.music.load(os.path.join('ASSETS','music.wav'))
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound(os.path.join('ASSETS','coin.wav'))
coin_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound(os.path.join('ASSETS','game_over.wav'))
game_over_fx.set_volume(0.5)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    WIN.blit(img, (x, y))

def timer():
    global Time,text
    for e in pygame.event.get():
        if Time > 0:
            if e.type == pygame.USEREVENT:
                Time -=1
                text= str(Time)
        if Time == 0:
            break
    WIN.blit(timer_img,(WIDTH // 2 + 500,0))
    WIN.blit(font.render(text,True,(0,0,0)),(WIDTH // 2 + 600,30))

def Pause():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = False
        WIN.fill(BLACK)
        draw_text('Press Spacebar to Continue',font_score, WHITE, WIDTH // 2 -200, HEIGHT // 2)
        pygame.display.update()
        clock.tick(5)
                
class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False
		pos = pygame.mouse.get_pos()
		
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		WIN.blit(self.image, self.rect)

		return action

class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        if game_over == 0:
            # get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]:
                dy -= 4
            if key[pygame.K_DOWN]:
                dy += 4
            if key[pygame.K_LEFT]:
                dx -= 4
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 4
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    dy = 0

            if pygame.sprite.spritecollide(self, monster_group, False):
                game_over = -1
                game_over_fx.play()
            if pygame.sprite.spritecollide(self, door_group, False):
                game_over = 1
            if pygame.sprite.spritecollide(self, portal_group, False):
                player.reset(30 ,HEIGHT-210)
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

        WIN.blit(self.image, self.rect)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'ASSETS/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (28, 28))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        dead_image = pygame.image.load(os.path.join('ASSETS', 'dead.png'))
        self.dead_image = pygame.transform.scale(dead_image, (30, 30))
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.direction = 0

class World():
    def __init__(self, data):
        self.tile_list = []
        wall_img = pygame.image.load(os.path.join('ASSETS', 'cobblestone.png'))
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 'X':
                    img = pygame.transform.scale(wall_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 'E':
                    monster1 = Enemy1(col_count * tile_size, row_count * tile_size)
                    monster_group.add(monster1)
                if tile == 'e':
                    monster2 = Enemy2(col_count * tile_size, row_count * tile_size)
                    monster_group.add(monster2)
                if tile == 'D':
                    door = Exit(col_count * tile_size, row_count * tile_size)
                    door_group.add(door)
                if tile == 'P':
                    portal = Portal(col_count * tile_size, row_count * tile_size)
                    portal_group.add(portal)
                if tile == 'C':
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile =='T':
                    treasure = Treasure(col_count * tile_size, row_count * tile_size)
                    treasure_group.add(treasure)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            WIN.blit(tile[0], tile[1])


class Enemy1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join('ASSETS', 'enemy2.png'))
        self.image = pygame.transform.scale(img, (28, 28))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 300:
            self.move_direction *= -1
            self.move_counter *= -1
            self.image = pygame.transform.flip(self.image, True, False)

        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                self.move_direction *= -1
                self.image = pygame.transform.flip(self.image, True, False)

class Enemy2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join('ASSETS', 'enemy1.png'))
        self.image = pygame.transform.scale(img, (28, 28))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 300:
            self.move_direction *= -1
            self.move_counter *= -1
            self.image = pygame.transform.flip(self.image, True, False) 
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                self.move_direction *= -1
                self.image = pygame.transform.flip(self.image, True, False)

class Life(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join('ASSETS','life.png'))
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y+20)

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join('ASSETS', 'coin.png'))
        self.image = pygame.transform.scale(img, (18, 18))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Treasure(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join('ASSETS', 'treasure1.png'))
        self.image = pygame.transform.scale(img, (28, 28))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join('ASSETS', 'door.png'))
        self.image = pygame.transform.scale(img, (28, 28))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join('ASSETS', 'portal2.png'))
        self.image = pygame.transform.scale(img, (28, 28))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

world_data=[]
level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X XXXXXXXXX     E      XXXXXX",
    "X XXXXXXXXX  CXXXXXX   XXXXXX",
    "X XXXXXXXXX  CXXXXXX   XXXXXX",
    "X        XX  CXXXXT       XXX",
    "XXXXXXC  XX  CXXXX       EXXX",
    "XXXXXXC  XX   XXXXXXXXXXXXXXX",
    "XXXXXXC  XX    CCCCCC  XXXXXX",
    "XCCXXXC  XX  E         XXXXXX",
    "XCCXXXC       XXXXXX   XXXXXX",
    "XE    C          XXX     XXXX",
    "XXXXXXXX   XXX   XXXXXX    XX",
    "XXXXXXXX   XXX T    XXXX  CXX",
    "XXXXXXXX  CXXXXXXXXXXXXX  CXX",
    "XXXT XXX  CXXXXXX         CXX",
    "XXXE      CXX    CCCCC   E XX",
    "XXXXXXXXXXXX    XXXXXXXXXXXXX",
    "XXXXXXXXXXXX    XXXXXXXXXXXXX",
    "XXXXXXX     CCCCCCC  XXXXXXXX",
    "XXT  XXXXXXXXXXX        E  XX",
    "XX   XXXXXXXXXXXXX     XXXXXX",
    "XX    XXXXXXXXXXXX     XXXXXX",
    "XX          XXXX           XX",
    "XXXX E    CCCCCCCCCCC     DXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

level_2 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X     CCCC    CCCCC        EX",
    "XXX  XXXXXXX XXXXXXXXXXX    X",
    "X      EXE        CCCCC     X",
    "X  XXXXXX  XXXXX  XXXXXXXXXXX",
    "X  XXXXX  XXXXXX  XXXXXXXXXXX",
    "X     CX   CCCCX   CCCC  XXXX",
    "XXXXX CXXXXX  XXXXXXXE      X",
    "X   CCC  EXX       TXX  XXXXX",
    "X  XXXXXXXX    XXXXXXX   XXXX",
    "X   CCCCCCE     CCC        TX",
    "XXXXXX   XXXCCC     E  XXXXXX",
    "XTXXX    XXE     CCC   XXXXXX",
    "X  XXXXXX     XXXXXX  TXXXXXX",
    "XE   CCCC     CCCXXXXXXXXXXXX",
    "X XXXXXXXXX     E     CXXXXXX",
    "X XXXXXXXXX   XXXXXX  CXXXXXX",
    "X XXXXXXXXX  CXXXXXX  CXXXXXX",
    "X  CCCCC XXE CXXXX        XXX",
    "XXXXXX   XX  CXXXXT      EXXX",
    "XXXXXX   XX   XXXXXXXXXXXXXXX",
    "XXXXXX   XX    CCCCC   XXXXXX",
    "X       E   XXXXXXXX  XXXXXXX",
    "XD CCC XXXX  CCCCC         EX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

level_3=[
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X           CCCCCCCCCCC          X",
    "X  XXXXXXXXXXXXXXXXXXXXXXXXX     X",
    "XC     X       X           E     X",
    "XC XXXXXX         XX CXXXXXXXXXXXX",
    "XC XXXXXX  XXXXX     CXXXXXXXXXXXX",
    "XC    CX       XE    CCCCCCC  XXXX",
    "XXXXX CXXXXX   XXXXXXXE          X",
    "XCCC     EXXE       XXC      XXXXX",
    "X  XXXXXXXX    XXXXXXXC       XXXX",
    "XE          CXXXXXXXXXX         EX",
    "XXXXXX      CXT E    TX   CXXXXXXX",
    "XT XXXE     CX       EX   CXXXXXXX",
    "X  XXXXXX   CX        XE  CXXXXXXX",
    "X  CCCCCC   EXT E    TXX   CXXXXXX",
    "XXXXXXXXXXX  X        XXC   XXXXXX",
    "XXXXXXXXXXX  XXXXXXX   XC   XXXXXX",
    "XXXXXXXXXXXE   CCCCC   XX   XXXXXX",
    "XCCCCCC  XXC  XXXXE            XXX",
    "XXXXXXC  XXC  XXXXCCC     XX   T X",
    "XXXXXX   XXC  XXXXXXX     XXXXXXXX",
    "XXXXXX E                  E XXXXXX",
    "X          XXXXX XXXXXXX C  XXXXXX",
    "XT     XXXXXD          X CCCCCCCCX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

level_4=[
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X        CCCCCCCC           CCC  X",
    "X XXXXXXXXXXXXXXXXXXXX  XXXXXXXXXX",
    "XE  X  CCCCE            E CCCC   X",
    "XCXXX  XXXXXX  XXXXXXXXXXXXXXXXXXX",
    "XC       EX          X          TX",
    "XCCCCC      E X  E CCCCC         X",
    "XXXXXXX  XXXXXXXXXXXXXXXX  X    EX",
    "XCCCC    XD E          TX eXE    X",
    "X    EX  X        E     X  X    CX",
    "XE    Xe XE     T    E  X  X E  CX",
    "XXXXX X CX     E        Xe     CCX",
    "X     X CXT           E XXXXX XXXX",
    "XE CCCX CXE        E    X  E     X",
    "X  XXXX  XXXXXXXXXXXX  XX  XXXXXXX",
    "X    XT  X E    CCCCC   X  CCCC  X",
    "Xe XXXXXeX          CCCCXXXXXX   X",
    "X  XXX   XXXXXX     XXXXX       EX",
    "X  ECCCCCC    Xe CCCX E   CCCC   X",
    "XXXXXXXXXX  XXXC XXXXXX  XXXXXXXXX",
    "X      E    C X CXXX         E   X",
    "XXXXXXXXXXXXC X   TXXXXXXXXXXX   X",
    "XT         XC X eXXX    ECCCCC   X",
    "X    E  CCCC e  CCCCE  XXXXXXXX TX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    ]

level_5=[
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X  X        E     CCCCCC         X",
    "X  X  XXXXCCXX  XX  XXX  XXXXXXXXX",
    "X     E T XX    E  CCCC      E   X",
    "XXXXXXXXXXXX eXXXXXXXXXXX  XXXXXXX",
    "Xe      E  X  XXXX P XXXX  X   C X",
    "XC XXT X   X  X E       X  XE  C X",
    "XC XXXXX      X         X e   Xe X",
    "XC X        e X       E XXXXXXXC X",
    "XC XXXXXXXXXXXXXXXe XXXXX  E   C X",
    "X  E    CCC  XXXXX  X   E CCC    X",
    "X CCC    E   XXe    X    XXXXXXXXX",
    "XXXXXXXXXXX   X    E  CCCCCC   E X",
    "XX  E CCCC    X  XXXXXXXXXXXXXXXXX",
    "XT   XXXXXXXXXX      CCCCXXXXXXXXX",
    "XX   E CCCCCC   E  X   E  CCCC  TX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X         X   E            E     X",
    "XCCCCCC  XXC  XXXXE            XXX",
    "X XXXXC  XXC  XXXXCCCE    XX    TX",
    "X XXXX   XXC  XXXXXXX     XXXXXXXX",
    "X XXXX E   CCC    CCX    E  XXXXX",
    "X          XXXXX XXXXXXX C  XXXXXX",
    "XT XXXXXXXXXXXXXXXXXXXXX CCCCC  DX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    ]
    
    
world_data.append(level_1)
world_data.append(level_2)
world_data.append(level_3)
world_data.append(level_4)
world_data.append(level_5)
player = Player(30,30)

monster_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
treasure_group = pygame.sprite.Group()
life_group = pygame.sprite.Group()

score_coin = Coin(15,12)
coin_group.add(score_coin)

score_life1 = Life(730,-5)
score_life2 = Life(770,-5)
score_life3 = Life(810,-5)
life_group.add(score_life1, score_life2, score_life3)

world = World(world_data[level])

restart_button = Button(WIDTH // 2 - 50, HEIGHT // 2 + 100, restart_img)
pause_button = Button(WIDTH // 2 + 400, 0, pause_img)
menu_button = Button(WIDTH -200,HEIGHT - 100, menu_img)

def main_menu():
    import main_menu
    main_menu.Main_menu()

def play():
    run = True
    global game_over, level, count, score, world, Time
    
    while run:
        clock.tick(FPS)
        if main_menu == True:
            main_menu()

        else:
            WIN.fill(BLACK)
            WIN.blit(map_img,(WIDTH // 2 + 270,0))
            world.draw()
            if pause_button.draw():
                Pause()
            if menu_button.draw():
                main_menu()
            if Time == 0:
                game_over= -1
            if game_over == 0:
                monster_group.update()
                door_group.update()
                if pygame.sprite.spritecollide(player, coin_group, True):
                    score += 5
                    coin_fx.play()
                draw_text('X ' + str(score), font_score, WHITE, tile_size, 5)
                if pygame.sprite.spritecollide(player, treasure_group, True):
                    score += 20
                    coin_fx.play()
                    
            coin_group.draw(WIN)
            treasure_group.draw(WIN)                    
            monster_group.draw(WIN)
            door_group.draw(WIN)
            portal_group.draw(WIN)
            life_group.draw(WIN)
            game_over = player.update(game_over)
            if game_over == 0:
                timer()

            if game_over == -1:
                if restart_button.draw():
                    count += 1
                    if count == 1:
                        life_group.remove(score_life3)
                        player.reset(30,30)
                        Time = 90
                        game_over = 0
                    elif count == 2:
                        life_group.remove(score_life2)
                        player.reset(30,30)
                        Time = 90
                        game_over = 0
                    elif count == 3:
                        life_group.remove(score_life1)
                        player.reset(30,30)
                        Time = 90
                        game_over = 0
                if count == 4:
                    WIN.blit(gameover_img,gameover_rect)
                    draw_text('GAME OVER',font_over, YELLOW, WIDTH // 2 -250 , HEIGHT // 2-150)
                    draw_text('YOU LOSE',font_over, YELLOW, WIDTH // 2 -190 , HEIGHT // 2)
                    pygame.mixer.music.pause()
                    
            if game_over == 1:
                player.reset(30,30)
                monster_group.empty()
                door_group.empty()
                portal_group.empty()
                coin_group.empty()
                treasure_group.empty()
                Time = 90
                level += 1
                
                if level <= max_levels:
                    world = World(world_data[level])
                    game_over = 0
                else:
                     WIN.blit(gameover_img,gameover_rect)
                     draw_text('GAME OVER',font_over, YELLOW, WIDTH // 2 -250 , HEIGHT // 2-150)
                     draw_text('YOU WIN',font_over, YELLOW, WIDTH // 2 -190 , HEIGHT // 2)
                     pygame.mixer.music.pause()
                     playagain = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, playagain_img)
                     if playagain.draw():
                         coin_group.empty()
                         monster_group.empty()
                         door_group.empty()
                         portal_group.empty()
                         treasure_group.empty()
                         level = 0
                         score = 0
                         count = 0
                         world = World(world_data[level])
                         life_group.add(score_life1, score_life2, score_life3)
                         game_over = 0
                         pygame.mixer.music.play(-1, 0.0, 5000)
                         main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


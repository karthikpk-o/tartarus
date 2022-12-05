import pygame, sys, os

pygame.init()

WIDTH = 1550
HEIGHT = 750
SCREEN = pygame.display.set_mode((1550, 750))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")
BG = pygame.transform.scale(BG, (WIDTH,HEIGHT))
BG_RECT = BG.get_rect()
GUY = pygame.image.load(os.path.join('ASSETS', 'guy1.png'))
GUY = pygame.transform.scale(GUY,(30, 40))
E2 = pygame.image.load(os.path.join('ASSETS', 'enemy2.png'))
E2 = pygame.transform.scale(E2,(30, 40))
E1 = pygame.image.load(os.path.join('ASSETS', 'enemy1.png'))
E1 = pygame.transform.scale(E1,(30, 40))
COIN = pygame.image.load(os.path.join('ASSETS', 'coin.png'))
COIN = pygame.transform.scale(COIN,(30, 40))
TRS = pygame.image.load(os.path.join('ASSETS', 'treasure1.png'))
TRS = pygame.transform.scale(TRS,(30, 40))

play_img = pygame.image.load('assets/Play Rect.png')
options_img = pygame.image.load('assets/Options Rect.png')
quit_img = pygame.image.load('assets/Quit Rect.png')

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)


def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

def play():
    import game
    game.play()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill('Black')

        OPTIONS_TEXT = get_font(75).render("OPTIONS", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(750, 60))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        OPTIONS_HELP = Button(image=None,pos=(750,260),
                              text_input='HELP',font=get_font(45),base_color='Blue',
                              hovering_color='Green')
        OPTIONS_BACK = Button(image=None,pos=(750,660),
                              text_input="BACK",font=get_font(45),base_color="Orange",
                              hovering_color="Green")
        OPTIONS_INST = Button(image=None,pos=(750,460),
                              text_input='INSTRUCTIONS',font=get_font(45),base_color='Blue',
                              hovering_color='Green')
        for button in [OPTIONS_BACK, OPTIONS_INST, OPTIONS_HELP]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    Main_menu()
                if OPTIONS_INST.checkForInput(OPTIONS_MOUSE_POS):
                    instructions()
                if OPTIONS_HELP.checkForInput(OPTIONS_MOUSE_POS):
                    Help()

        pygame.display.update()
        
def Help():
    while True:
        HELP_MOUSE_POS = pygame.mouse.get_pos()
        
        SCREEN.fill('Black')
        
        HELP_TEXT = get_font(75).render("HELP", True, "#b68f40")
        HELP_RECT = HELP_TEXT.get_rect(center=(750, 60))
        SCREEN.blit(HELP_TEXT, HELP_RECT)
        
        helptext1 = get_font(21).render('We are working on new updates to give you the best experience possible',True,'Blue')
        SCREEN.blit(helptext1, (30,140))                                        
        helptext2 = get_font(21).render('we want to Thank you for the co-operation and patience,',True,'Blue')
        SCREEN.blit(helptext2, (30,180))
        helptext3 = get_font(21).render('Sorry for the inconvenience caused.',True,'Blue')
        SCREEN.blit(helptext3, (30,220))
        helptext4 = get_font(21).render('Team Tartarus',True,'Blue')
        SCREEN.blit(helptext4, (30,260))
        helptext6 = get_font(21).render('Do leave a feedback',True,'Blue')
        SCREEN.blit(helptext6, (30,350))

        HELP_BACK = Button(image=None, pos=(750, 660),text_input="BACK",font=get_font(45),base_color="Orange",hovering_color="Green")
        HELP_BACK.changeColor(HELP_MOUSE_POS)
        HELP_BACK.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HELP_BACK.checkForInput(HELP_MOUSE_POS):
                    options()
        
        pygame.display.update()
        
def instructions():
    while True:
        INST_MOUSE_POS = pygame.mouse.get_pos()
        
        SCREEN.fill('Black')
        
        INST_TEXT = get_font(75).render("INSTRUCTIONS", True, "#b68f40")
        INST_RECT = INST_TEXT.get_rect(center=(750, 60))
        SCREEN.blit(INST_TEXT, INST_RECT)
        
        INST_BACK = Button(image=None,pos=(750, 660),text_input="BACK",font=get_font(25),base_color="Orange",hovering_color="Green")
        INST_BACK.changeColor(INST_MOUSE_POS)
        INST_BACK.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INST_BACK.checkForInput(INST_MOUSE_POS):
                    options()
                    
        SCREEN.blit(GUY,(60,120))
        SCREEN.blit(E1,(60,180))
        SCREEN.blit(E2,(60,250))
        SCREEN.blit(COIN,(60,320))
        SCREEN.blit(TRS,(60,390))
        
        instext1 = get_font(21).render('--> Your Character: Can move in all 4 directions; Using ARROW keys',True, 'Blue')
        SCREEN.blit(instext1, (100, 130))
        instext2 = get_font(21).render('--> Enemy1: Can only move vertically', True, 'Blue')
        SCREEN.blit(instext2, (100, 190))
        instext3 = get_font(21).render('--> Enemy2: Can only move horizontally', True, 'Blue')
        SCREEN.blit(instext3, (100, 260))
        instext4 = get_font(21).render('--> Coin: Adds 5 points to your score', True, 'Blue')
        SCREEN.blit(instext4, (100, 330))
        instext5 = get_font(21).render('--> Treasure: Adds 20 points to your score', True, 'Blue')
        SCREEN.blit(instext5, (100, 400))
        
        instext6 = get_font(21).render('This is a single player game; The character has to move through 5 levels', True, 'Blue')
        SCREEN.blit(instext6, (20, 480))
        instext7 = get_font(21).render('collecting as many coins and treasure boxes as possible without coming', True, 'Blue')
        SCREEN.blit(instext7, (20, 520))
        instext8 = get_font(21).render('in contact with the enemy. The Player will have 4 lives to complete', True, 'Blue')
        SCREEN.blit(instext8, (20, 560))
        instext9 = get_font(21).render('the game.', True, 'Blue')
        SCREEN.blit(instext9, (20, 600))
        
        pygame.display.update()
           
def Main_menu():
    while True:
        SCREEN.blit(BG, BG_RECT)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("TARTARUS", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(750, 100))

        PLAY_BUTTON = Button(play_img,pos=(750, 250),text_input="PLAY",font=get_font(75),base_color="#d7fcd4",hovering_color="White")
        OPTIONS_BUTTON = Button(options_img,pos=(750, 400),text_input="OPTIONS",font=get_font(75),base_color="#d7fcd4",hovering_color="White")
        QUIT_BUTTON = Button(quit_img,pos=(750, 550),text_input="QUIT",font=get_font(75),base_color="#d7fcd4",hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

Main_menu()
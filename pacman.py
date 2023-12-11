import pygame
import time
import random
pygame.init()
pygame.mixer.init()

# Make the grid path
grid = ['0000000000000000000000000000',
'0000000000000000000000000000',
'0111111111111001111111111110',
'0100001000001001000001000010',
'0100001000001001000001000010',
'0100001000001001000001000010',
'0111111111111111111111111110',
'0100001001000000001001000010',
'0100001001000000001001000010',
'0111111001111001111001111110',
'0000001000001001000001000000',
'0000001000001001000001000000',
'0000001001111111111001000000',
'0000001001000110001001000000',
'0000001001001111001001000000',
'1111111001001111001001111111',
'0000001001001111001001000000',
'0000001001000000001001000000',
'0000001001111111111001000000',
'0000001001000000001001000000',
'0000001001000000001001000000',
'0111111111111001111111111110',
'0100001000001001000001000010',
'0100001000001001000001000010',
'0111001111111111111111001110',
'0001001001000000001001001000',
'0001001001000000001001001000',
'0111111001111001111001111110',
'0100000000001001000000000010',
'0100000000001001000000000010',
'0111111111111111111111111110',
'0000000000000000000000000000',
'0000000000000000000000000000']

# No. of rows and columns, height and width of grid
ROWS = len(grid)
COLS = len(grid[0])

SCRW = 812
SCRH = 820
CELLW = SCRW//COLS
CELLH = SCRH//ROWS

# Cell properties
class cell():
    def __init__(self,row,col,ispath):
        self.row = row
        self.col = col
        self.ispath = int(ispath)                      #Boolean
        self.xpos = (CELLW)*col             #Cell x-axis position
        self.ypos = (CELLH)*row             #cell y-axis position
        self.dotted = True

#Pacman properties and functions
class pacman():
    def __init__(self,row,col,direc):
        self.row = row
        self.col = col
        self.direc = direc
        self.turn = direc
        self.prevpos = (self.row,self.col)
        self.hungry = 0
        self.alive = True

    def set_turn(self):
        if self.turn == 0 and game[self.row][(self.col+1)%COLS].ispath and self.col!=(COLS-1):
            self.direc = 0
        elif self.turn == 1 and game[self.row-1][self.col].ispath:
            self.direc = 1
        elif self.turn == 2 and game[self.row][(self.col-1)%COLS].ispath and self.col!=0:
            self.direc = 2
        elif self.turn == 3 and game[self.row+1][self.col].ispath:
            self.direc = 3
    
    def move(self):
        global opencost
        global dotseaten
        global points
        if self.direc == 0 and game[self.row][(self.col+1)%COLS].ispath:
            self.col = (self.col+1)%COLS
            opencost = img0
        elif self.direc == 1 and game[self.row-1][self.col].ispath:
            self.row -= 1
            opencost = img1
        elif self.direc == 2 and game[self.row][(self.col-1)%COLS].ispath:
            self.col = (self.col-1)%COLS
            opencost = img2
        elif self.direc == 3 and game[self.row+1][self.col].ispath:
            self.row += 1
            opencost = img3
        if game[self.row][self.col].dotted == True:
            game[self.row][self.col].dotted = False
            dotseaten +=1
            points += 20


class enemy():
    def __init__(self,row,col,direc):
        self.row = row
        self.col = col
        self.direc = direc
        self.prevpos = (self.row,self.col)
        self.alive = True
        self.scared = False
        self.poss_dir = []
        self.hunting = False
    
    def move(self):
        self.poss_dir = []
        if game[self.row][(self.col+1)%COLS].ispath:
            self.poss_dir.append(0)
        if game[self.row-1][self.col].ispath:
            self.poss_dir.append(1)
        if game[self.row][(self.col-1)%COLS].ispath:
            self.poss_dir.append(2)
        if game[self.row+1][self.col].ispath:
            self.poss_dir.append(3)
        if (self.direc+2)%4 in self.poss_dir:
            self.poss_dir.remove((self.direc+2)%4)

        if self.hunting:
            if self.hunting == 'home':
                self.hunt(ROWS//2,COLS//2)
            elif self.hunting == 'pacman':
                self.hunt(p.row,p.col)
        else:
            self.direc = random.choice(self.poss_dir)

        if self.direc == 0:
            self.col = (self.col+1)%COLS
        elif self.direc == 1:
            self.row -= 1
        elif self.direc == 2:
            self.col = (self.col-1)%COLS
        elif self.direc == 3:
            self.row += 1
    
    def hunt(self,goalrow,goalcol):
        if (self.row < goalrow) and (3 in self.poss_dir):
            self.direc = 3
            # print('DOWN')
            if self.scared and (1 in self.poss_dir):
                self.direc = 1
        elif (self.row > goalrow) and (1 in self.poss_dir):
            self.direc = 1
            # print('UP')
            if self.scared and (3 in self.poss_dir):
                self.direc = 3
        elif (self.col < goalcol) and (0 in self.poss_dir):
            self.direc = 0
            # print('RIGHT')
            if self.scared and (2 in self.poss_dir):
                self.direc = 2
        elif (self.col > goalcol) and (2 in self.poss_dir):
            self.direc = 2
            # print('LEFT')
            if self.scared and (0 in self.poss_dir):
                self.direc = 0
        else:
            if len(self.poss_dir) == 0:
                self.direc = (self.direc+2)%4
            else:
                self.direc = random.choice(self.poss_dir)
            # print('NO PATH')

class cherry():
    def __init__(self,cellpos):
        self.row = cellpos[0]
        self.col = cellpos[1]
        self.edible = 75


# Create the game grid made of cell objects
game = grid.copy()
for eachrow in range(ROWS):
    game[eachrow] = list(game[eachrow])
    for eachcol in range(COLS):
        game[eachrow][eachcol] = cell(eachrow,eachcol,grid[eachrow][eachcol])

path_cells = []
for r in game:
    for c in r:
        if c.ispath:
            path_cells.append(c)

TOTALDOTS = len(path_cells)


# Screen setup
screen = pygame.display.set_mode([SCRW,SCRH])
screen.fill((30,40,110))
surf_path = pygame.Surface([CELLW,CELLH])
path_color = (0,0,0)
surf_path.fill(path_color)

img = pygame.image.load('./images/norm.png')
img0 = pygame.image.load('./images/0.png')
img1 = pygame.image.load('./images/1.png')
img2 = pygame.image.load('./images/2.png')
img3 = pygame.image.load('./images/3.png')
withdot = pygame.image.load('./images/dot.png')
nodot = pygame.image.load('./images/nodot.png')
pinkimg = pygame.image.load('./images/editing/pink.png')
redimg = pygame.image.load('./images/editing/red.png')
blueimg = pygame.image.load('./images/editing/blue.png')
yellowimg = pygame.image.load('./images/editing/yellow.png')
grave = pygame.image.load('./images/rip.png')
scared = pygame.image.load('./images/scared.png')
cherryimg = pygame.image.load('./images/cherry.png')
heartimg = pygame.image.load('./images/heart.png')
deadheartimg = pygame.image.load('./images/deadheart.png')

img = pygame.transform.scale(img,(CELLW,CELLH))
img0 = pygame.transform.scale(img0,(CELLW,CELLH))
img1 = pygame.transform.scale(img1,(CELLW,CELLH))
img2 = pygame.transform.scale(img2,(CELLW,CELLH))
img3 = pygame.transform.scale(img3,(CELLW,CELLH))
withdot = pygame.transform.scale(withdot,(CELLW,CELLH))
nodot = pygame.transform.scale(nodot,(CELLW,CELLH))
pinkimg = pygame.transform.scale(pinkimg,(CELLW,CELLH))
blueimg = pygame.transform.scale(blueimg,(CELLW,CELLH))
redimg = pygame.transform.scale(redimg,(CELLW,CELLH))
yellowimg = pygame.transform.scale(yellowimg,(CELLW,CELLH))
grave = pygame.transform.scale(grave,(CELLW,CELLH))
scared = pygame.transform.scale(scared,(CELLW,CELLH))
cherryimg = pygame.transform.scale(cherryimg,(CELLW,CELLH))
heartimg = pygame.transform.scale(heartimg,(CELLW*1.4,CELLH*1.5))
deadheartimg = pygame.transform.scale(deadheartimg,(CELLW*1.4,CELLH*1.5))


opencost = img

surf_player = pygame.Surface([CELLW,CELLH])
surf_enemy1 = pygame.Surface([CELLW,CELLH])
surf_enemy2 = pygame.Surface([CELLW,CELLH])
surf_enemy3 = pygame.Surface([CELLW,CELLH])
surf_enemy4 = pygame.Surface([CELLW,CELLH])
surf_cherry = pygame.Surface([CELLW,CELLH])
surf_enemy1.blit(pinkimg,(0,0))
surf_enemy2.blit(blueimg,(0,0))
surf_enemy3.blit(redimg,(0,0))
surf_enemy4.blit(yellowimg,(0,0))
surf_cherry.blit(cherryimg,(0,0))


pygame.mixer.music.set_volume(0.7)
scorefont = pygame.font.Font('./Andale Mono.ttf',32)
textsurf = scorefont.render('placetext',True,(100,0,0))
screen.blit(textsurf,(0,0))
textsurf2 = scorefont.render('placetext2',True,(100,0,0))
screen.blit(textsurf2,(0,0))


p = pacman(2,6,3)
pink = enemy(15,13,2)
blue = enemy(15,13,2)
red = enemy(15,13,2)
yellow = enemy(15,13,2)
ch1 = cherry((2,1))
ch2 = cherry((2,26))
ch3 = cherry((30,1))
ch4 = cherry((30,26))

ENEMIES = (pink,red,blue,yellow)

homescr = pygame.image.load('./images/homescreen3.png')
homescr = pygame.transform.scale(homescr,(SCRW,SCRH))
screen.blit(homescr,(0,0))
gameover = pygame.image.load('./images/game_over_PNG14.png')
gameover = pygame.transform.scale(gameover,(SCRW/2,SCRH/3))
gorect = gameover.get_rect()
youwin = pygame.image.load('./images/winning.png')
youwin = pygame.transform.scale(youwin,(SCRW/2,SCRH/2))

colliding = False
running = False
gamestarting = True

while gamestarting:
    screen.blit(homescr,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamestarting = False
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gamestarting = False
                running = False
            elif event.key == pygame.K_SPACE:
                gamestarting = False
                running = True
    pygame.display.flip()

screen.fill((30,40,110))
gamescr = pygame.image.load('./images/homescreen.png')
gamescr = pygame.transform.scale(gamescr,(SCRW,SCRH))
screen.blit(gamescr,(0,0))

counter = 0
dotseaten = 0
points = 0
lives = 3
safe = 30
gamewon = False

while running:
    textsurf = scorefont.render(str(points),True,(200,200,200),(20,20,200))
    screen.blit(textsurf,(SCRW-100,5))

    if safe:
        safe -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RIGHT:
                p.turn = 0
            elif event.key == pygame.K_UP:
                p.turn = 1
            elif event.key == pygame.K_LEFT:
                p.turn = 2
            elif event.key == pygame.K_DOWN:
                p.turn = 3
    
    if p.alive:

        p.set_turn()    
        for eachpath in path_cells:
            if eachpath.dotted:
                surf_path.blit(withdot,(0,0))
            else:
                surf_path.blit(nodot,(0,0))
            screen.blit(surf_path,(eachpath.xpos,eachpath.ypos))
        
        if counter%2:
            surf_player.blit(img,(0,0))
        else:
            surf_player.blit(opencost,(0,0))
            
        
        if dotseaten == TOTALDOTS:
            gamewon = True
            p.alive = False
        

        if p.hungry:
            for i in ENEMIES:
                i.scared = True
                if not i.alive:
                    screen.blit(grave,(game[i.row][i.col].xpos,game[i.row][i.col].ypos))
                else:
                    screen.blit(scared,(game[i.row][i.col].xpos,game[i.row][i.col].ypos))
        
            p.hungry -= 1
            for i in ENEMIES:
                if ((p.row,p.col) == (i.row,i.col)) or ((p.prevpos == (i.row,i.col)) and ((p.row,p.col) == i.prevpos) and i.alive == True):
                    i.alive = False
                    points += 1000
                
        else:
            for i in ENEMIES:
                i.alive = True
                i.scared = False
                if (((p.row,p.col) == (i.row,i.col)) or ((p.prevpos == (i.row,i.col)) and ((p.row,p.col) == i.prevpos))) and (safe == 0):
                    colliding = True
                    safe = 10
                    if lives>0:
                        lives-=1
                        for i in range(3-lives):
                            screen.blit(deadheartimg,((8-(i*3+1))*CELLW/2,CELLH/4))
                    if lives == 0:
                        for i in range(3-lives):
                            screen.blit(deadheartimg,((8-(i*3+1))*CELLW/2,CELLH/4))
                        p.alive = False
                        time.sleep(0.1)
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.load('./sounds/die.mp3')
                        pygame.mixer.music.play()
            
            screen.blit(surf_enemy1,(game[pink.row][pink.col].xpos,game[pink.row][pink.col].ypos))
            screen.blit(surf_enemy2,(game[blue.row][blue.col].xpos,game[blue.row][blue.col].ypos))
            screen.blit(surf_enemy3,(game[red.row][red.col].xpos,game[red.row][red.col].ypos))
            screen.blit(surf_enemy4,(game[yellow.row][yellow.col].xpos,game[yellow.row][yellow.col].ypos))

            if colliding:
                pygame.mixer.music.load('./sounds/ghost-eaten.mp3')
                pygame.mixer.music.play()
                time.sleep(0.2)
                colliding = False

        screen.blit(surf_player,(game[p.row][p.col].xpos,game[p.row][p.col].ypos))

        
        for i in range(lives):
            screen.blit(heartimg,((i*3+1)*CELLW/2,CELLH/4))


        for i in (p,red,yellow,pink,blue):
            i.prevpos = (i.row,i.col)

        for fruit in (ch1,ch2,ch3,ch4):
            if fruit.edible:
                if fruit.edible == 75:
                    if (fruit.row,fruit.col) == (p.row,p.col):
                        p.hungry = 75
                        fruit.edible -= 1
                    else:
                        screen.blit(cherryimg,(game[fruit.row][fruit.col].xpos,game[fruit.row][fruit.col].ypos))
                else:
                    fruit.edible -= 1

        pygame.display.flip()                     # WARNING!!! Flipping the screen here

        p.move()
        for i in ENEMIES:
            if i.alive:
                if safe or (counter%40)<15:
                    i.hunting = False
                else:
                    i.hunting = 'pacman'
            else:
                i.hunting = 'home'
            if i.scared and i.alive:
                if counter%3 != 0:
                    i.move()
            else:
                i.move()

        counter +=1
        if p.hungry:
            pygame.mixer.music.load('./sounds/waza2.mp3')
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.load('./sounds/eat-fruit.mp3')
            pygame.mixer.music.play()
        time.sleep(0.15)
        
    else:
        if gamewon:
            screen.blit(youwin,(SCRW/4,SCRH/4))
        else:
            screen.blit(gameover,(SCRW/4,SCRH/3))
        textsurf = scorefont.render('*** SCORE: '+str(points)+' ***',True,(200,200,200),(20,20,200))
        screen.blit(textsurf,(SCRW/4,5*SCRH/7))
        textsurf2 = scorefont.render('*** DOTS EATEN: '+str(dotseaten)+'/'+str(TOTALDOTS)+' ***',True,(200,200,200),(20,20,200))
        screen.blit(textsurf2,(SCRW/5,11*SCRH/14))
        pygame.display.flip()

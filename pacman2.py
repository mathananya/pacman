import pygame
import time
import random
pygame.init()

# Make the grid path
grid = ['0000000000000000000000000000',
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
'0000001001011111101001000000',
'1111111001011111101001111111',
'0000001001011111101001000000',
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
'0000000000000000000000000000']

# No. of rows and columns, height and width of grid
ROWS = len(grid)
COLS = len(grid[0])

SCRW = 800
SCRH = 800

# Cell properties
class cell():
    def __init__(self,row,col,ispath):
        self.row = row
        self.col = col
        self.ispath = int(ispath)                      #Boolean
        self.xpos = (SCRW//COLS)*col             #Cell x-axis position
        self.ypos = (SCRH//ROWS)*row             #cell y-axis position

class pacman():
    def __init__(self,row,col,direc):
        self.row = row
        self.col = col
        self.direc = direc
        self.turn = direc

    def set_turn(self):
        if self.turn == 0 and game[self.row][self.col+1].ispath:
            self.direc = 0
        elif self.turn == 1 and game[self.row-1][self.col].ispath:
            self.direc = 1
        elif self.turn == 2 and game[self.row][self.col-1].ispath:
            self.direc = 2
        elif self.turn == 3 and game[self.row+1][self.col].ispath:
            self.direc = 3
    
    def move(self):
        global opencost
        if self.direc == 0 and game[self.row][self.col+1].ispath:
            self.col += 1
            opencost = img0
        elif self.direc == 1 and game[self.row-1][self.col].ispath:
            self.row -= 1
            opencost = img1
        elif self.direc == 2 and game[self.row][self.col-1].ispath:
            self.col -= 1
            opencost = img2
        elif self.direc == 3 and game[self.row+1][self.col].ispath:
            self.row += 1
            opencost = img3


class enemy():
    def __init__(self,row,col,direc):
        self.row = row
        self.col = col
        self.direc = direc
    
    def move(self):
        poss_dir = []
        if game[self.row][self.col+1].ispath:
            poss_dir.append(0)
        if game[self.row-1][self.col].ispath:
            poss_dir.append(1)
        if game[self.row][self.col-1].ispath:
            poss_dir.append(2)
        if game[self.row+1][self.col].ispath:
            poss_dir.append(3)
        poss_dir.remove((self.direc+2)%4)
        self.direc = random.choice(poss_dir)

        if self.direc == 0:
            self.col += 1
        elif self.direc == 1:
            self.row -= 1
        elif self.direc == 2:
            self.col -= 1
        elif self.direc == 3:
            self.row += 1

            


# Create the game grid made of cell objects
game = grid.copy()
for eachrow in range(ROWS):
    game[eachrow] = list(game[eachrow])
    for eachcol in range(COLS):
        game[eachrow][eachcol] = cell(eachrow,eachcol,grid[eachrow][eachcol])     #HAHAHA IT WORKS!!! --- 31/10

path_cells = []
for r in game:
    for c in r:
        if c.ispath:
            path_cells.append(c)


# Screen setup
screen = pygame.display.set_mode([SCRW,SCRH])
screen.fill((255,91,255))
surf_path = pygame.Surface([SCRW/COLS,SCRH/ROWS])
path_color = (0,0,0)
surf_path.fill(path_color)

surf_player = pygame.Surface([SCRW/COLS,SCRH/ROWS])
img = pygame.image.load('./images/norm.png')
img0 = pygame.image.load('./images/0.png')
img1 = pygame.image.load('./images/1.png')
img2 = pygame.image.load('./images/2.png')
img3 = pygame.image.load('./images/3.png')

img = pygame.transform.scale(img,(SCRW/COLS,SCRH/ROWS))
img0 = pygame.transform.scale(img0,(SCRW/COLS,SCRH/ROWS))
img1 = pygame.transform.scale(img1,(SCRW/COLS,SCRH/ROWS))
img2 = pygame.transform.scale(img2,(SCRW/COLS,SCRH/ROWS))
img3 = pygame.transform.scale(img3,(SCRW/COLS,SCRH/ROWS))

opencost = img

surf_enemy = pygame.Surface([SCRW/COLS,SCRH/ROWS])
surf_enemy.fill((250,20,150))


p = pacman(1,6,3)
pink = enemy(1,4,0)
red = enemy(1,5,0)
green = enemy(1,3,2)
costume_count = 0
running = True
while running:
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
    
    p.set_turn()    
    time.sleep(0.15)
    for eachpath in path_cells:
        screen.blit(surf_path,(eachpath.xpos,eachpath.ypos))
    
    if costume_count%2:
        surf_player.blit(img,(0,0))
    else:
        surf_player.blit(opencost,(0,0))

    costume_count+=1
    
    screen.blit(surf_player,(game[p.row][p.col].xpos,game[p.row][p.col].ypos))
    screen.blit(surf_enemy,(game[pink.row][pink.col].xpos,game[pink.row][pink.col].ypos))
    screen.blit(surf_enemy,(game[green.row][green.col].xpos,game[green.row][green.col].ypos))
    screen.blit(surf_enemy,(game[red.row][red.col].xpos,game[red.row][red.col].ypos))

    
    pygame.display.flip()
    p.move()
    pink.move()
    red.move()
    green.move()

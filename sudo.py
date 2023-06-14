import pygame
import copy
import sys

import ctypes
langCode = ctypes.windll.kernel32

defaultgrid =[[0 for col in range(9)] for row in range(9)]
# defaultgrid =[
#         [5, 3, 0, 0, 7, 0, 0, 0, 0],
#         [6, 0, 0, 1, 9, 5, 0, 0, 0],
#         [0, 9, 8, 0, 0, 0, 0, 6, 0],
#         [8, 0, 0, 0, 6, 0, 0, 0, 3],
#         [4, 0, 0, 8, 0, 3, 0, 0, 1],
#         [7, 0, 0, 0, 2, 0, 0, 0, 6],
#         [0, 6, 0, 0, 0, 0, 2, 8, 0],
#         [0, 0, 0, 4, 1, 9, 0, 0, 5],
#         [0, 0, 0, 0, 8, 0, 0, 7, 9],
#     ]
origgrid=copy.deepcopy(defaultgrid)

pygame.font.init()
if langCode==1031:
    pygame.display.set_caption("Sudoku-Löser")
else:
    pygame.display.set_caption("Sudoku Solver Attempt")
pygame.init()

res=(800,800)
diff=700/9
puzzStart=(50,50)
puzzPosX=0
puzzPosY=0
buttonHeight=40
buttonWidth=200
quitButtonStartCoord=(500+50,5)
checkButtonStartCoord=(250+50,5)
solveButtonStartCoord=(0+50,5)
errMsgCoord=(800,775)

errFlag=None

screen = pygame.display.set_mode(res)

errRows=[]


black=(0,0,0)
grey=(128,128,128)
white=(255,255,255)
red=(255,0,0)
font=pygame.font.SysFont("arial",40)
font2=pygame.font.SysFont("Corbel",20)
fontErr=pygame.font.SysFont("Corbel",35,bold=True)

rectangleCoords = []
selectedRect = []
for i in range (9):
        for j in range (9):
                rectangleCoords.append(pygame.Rect(puzzStart[0]+i * diff, puzzStart[1]+j * diff, diff + 1, diff+ 1))
                
colors =[[(255,255,255) for col in range(9)] for row in range(9)]
width=screen.get_width()
height=screen.get_height()
if langCode==1031:
    solveText=font2.render('Lösen',True,black)
    quitText=font2.render('Beenden',True,black)
    checkText=font2.render('Löschen',True,black)
    errEmpty=fontErr.render('Fehler: Raster ist leer',True,red)
    errValid=fontErr.render('Fehler: Gleiche Zahl im Raster',True,red)
    errNoSol=fontErr.render('Fehler: Keine Lösung',True,red)
else:
    solveText=font2.render('Solve',True,black)
    quitText=font2.render('Quit',True,black)
    checkText=font2.render('Clear',True,black)
    errEmpty=fontErr.render('Error: Grid is Empty',True,red)
    errValid=fontErr.render(f'Error: Same Number in Grid',True,red)
    errNoSol=fontErr.render('Error: No Solution',True,red)


def buttonCond(buttCoord,mouseCoord):
    if  buttCoord[0]<=mouseCoord[0]<=buttCoord[0]+buttonWidth and \
                buttCoord[1]<=mouseCoord[1]<=buttCoord[1]+buttonHeight:
        return True
    else:
        return False
def buttonText(text,coords):
    screen.blit(text,(coords[0]+75,coords[1]+10))
def buttonHigh(disp,color,coords,width,height):
    pygame.draw.rect(disp,color,[coords[0],coords[1],width,height])
    
def squareHigh(disp,color,rect):
    pygame.draw.rect(disp,color,rect)

##########--------------------------#################
#Suduko solving functions

def possible(y,x,n):
    global defaultgrid
    #checks rows and columns if number is in there
    for i in range(0,9):
        if defaultgrid[y][i]==n:
            return False
    for i in range(0,9):
        if defaultgrid[i][x]==n:
            return False
    #checks square if number is in there
    x0=(x//3)*3
    y0=(y//3)*3
    for i in range(0,3):
        for j in range(0,3):
            if defaultgrid[y0+i][x0+j]==n:
                return False
    return True
def solve():
    global defaultgrid
    #recursive function to solve the sudoku
    for y in range(9):
        for x in range(9):
            if defaultgrid[y][x]==0:
                for n in range(1,10):
                    if possible(y,x,n):
                        defaultgrid[y][x]=n
                        if not solve():
                            #if number is not valid, it sets it to 0 and tries again
                            defaultgrid[y][x]=0
                        else:
                            return defaultgrid
                return None
    
    return defaultgrid


def validCheck():
    global errRows,defaultgrid
    for row in  range(0,9):
        for col in range(0,9):
            if defaultgrid[row][col]!=0:
                tmp=defaultgrid[row][col]
                defaultgrid[row][col]=0
                if not possible(row,col,tmp):
                    errRows.append((row,col))
                defaultgrid[row][col]=tmp
                    

##########--------------------------#################

def clearBoard():
    global defaultgrid, origgrid, colors
    defaultgrid =[[0 for col in range(9)] for row in range(9)]
    colors =[[(255,255,255) for col in range(9)] for row in range(9)]

def drawlines():
    global colors
    for i in range (9):
        for j in range (9):
            if defaultgrid[i][j]!= 0:
                if colors[i][j]==(255,255,255):
                    colors[i][j]=(255,255,0)
                pygame.draw.rect(screen, colors[i][j], (puzzStart[0]+i * diff, puzzStart[1]+j * diff, diff + 1, diff+ 1))
                text1 = font.render(str(defaultgrid[i][j]), 1, black)
                screen.blit(text1, (puzzStart[0]+i * diff + 32,puzzStart[1]+ j * diff + 17))
            else:
                pygame.draw.rect(screen, colors[i][j], (puzzStart[0]+i * diff, puzzStart[1]+j * diff, diff + 1, diff+ 1))
    for l in range(10):
        if l % 3 == 0 :
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen,black,(puzzStart[0],puzzStart[1]+l*diff),(750,puzzStart[1]+l*diff),thick) #horizontal Lines in X
        pygame.draw.line(screen,black,(l*diff+puzzStart[0],puzzStart[1]),(l*diff+puzzStart[0],750),thick) #vertical Lines in Y

def errorPrint(text):
    text_rect = text.get_rect(center=(errMsgCoord[0]/2, errMsgCoord[1]))
    screen.blit(text, text_rect)


def coordinate(pos):
    global puzzPosX, puzzPosY
    puzzPosX = pos[0]//diff
    puzzPosY = pos[1]//diff
def buttonPress(butt):
    if butt[pygame.K_1] or butt[pygame.K_KP1]:
        return 1
    elif butt[pygame.K_2] or butt[pygame.K_KP2]:
        return 2   
    elif butt[pygame.K_3] or butt[pygame.K_KP3]:
        return 3
    elif butt[pygame.K_4] or butt[pygame.K_KP4]:
        return 4
    elif butt[pygame.K_5] or butt[pygame.K_KP5]:
        return 5
    elif butt[pygame.K_6] or butt[pygame.K_KP6]:
        return 6
    elif butt[pygame.K_7] or butt[pygame.K_KP7]:
        return 7
    elif butt[pygame.K_8] or butt[pygame.K_KP8]:
        return 8
    elif butt[pygame.K_9] or butt[pygame.K_KP9]:
        return 9
    elif butt[pygame.K_RETURN] or butt[pygame.K_KP_ENTER]:
        return -1
    elif butt[pygame.K_BACKSPACE] or butt[pygame.K_DELETE]:
        return -2
    else:
        return False

def gridSqIndex(no):
    rowIndex=no//9
    colIndex=int((no/9-int(no/9))*10)
    return (rowIndex,colIndex)

def mouseClickMainButts(mouse):
    global defaultgrid,errFlag,selectedRect,colors
    if buttonCond(quitButtonStartCoord,mouse):
        pygame.quit()
        sys.exit()
    elif buttonCond(checkButtonStartCoord,mouse):
        clearBoard()
        return True
    elif buttonCond(solveButtonStartCoord,mouse):
        colors =[[(255,255,255) for col in range(9)] for row in range(9)]
        selectedRect=[]
        if not all(x == 0 for v in defaultgrid for x in v):
            validCheck()
            if len(errRows)==0:
                origgrid=copy.deepcopy(defaultgrid)
                solve()
                if(origgrid==defaultgrid):
                    errFlag='noSol'
                    return True
            else:
                errFlag='invalid'

                return True
            return True
        else:
                errFlag='empty'
                return True
    else: return False



screen.fill((255,255,255))
while True:
    
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif ev.type==pygame.MOUSEBUTTONDOWN:
            errFlag='resolved'
            coordinate(mouse)
            if mouseClickMainButts(mouse):
                pass
            else:
                for ind, rect in enumerate(rectangleCoords):
                    if (rect.collidepoint(mouse)):
                        rowInd,colInd=gridSqIndex(ind)
                        colors =[[(255,255,255) for col in range(9)] for row in range(9)]
                        if len(selectedRect)!=0:
                            if rect in selectedRect:
                                selectedRect=[]
                                break
                            else:
                                selectedRect=[]
                                colors[rowInd][colInd]=(255,0,0)
                                selectedRect.append(rect)
                                break
                        else:
                            selectedRect.append(rect)
                            colors[rowInd][colInd]=(255,0,0)
                            break
        if ev.type==pygame.KEYDOWN and len(selectedRect)!=0:
            errFlag='resolved'
            keys=pygame.key.get_pressed()

            button=buttonPress(keys)
            if button:
                if button==-1:
                    selectedRect=[]
                    colors =[[(255,255,255) for col in range(9)] for row in range(9)]
                elif button==-2:
                    defaultgrid[rowInd][colInd]=0
                else:
                    defaultgrid[rowInd][colInd]=button


    mouse=pygame.mouse.get_pos()
    if buttonCond(quitButtonStartCoord,mouse):  
        buttonHigh(screen,grey,quitButtonStartCoord,buttonWidth,buttonHeight)
    elif buttonCond(checkButtonStartCoord,mouse):
        buttonHigh(screen,grey,checkButtonStartCoord,buttonWidth,buttonHeight)
    elif buttonCond(solveButtonStartCoord,mouse):
        buttonHigh(screen,grey,solveButtonStartCoord,buttonWidth,buttonHeight)
    else:
        buttonHigh(screen,white,quitButtonStartCoord,buttonWidth,buttonHeight)
        buttonHigh(screen,white,checkButtonStartCoord,buttonWidth,buttonHeight)
        buttonHigh(screen,white,solveButtonStartCoord,buttonWidth,buttonHeight)


    
    buttonText(quitText,quitButtonStartCoord)
    buttonText(checkText,checkButtonStartCoord)
    buttonText(solveText,solveButtonStartCoord)
    drawlines()
    if errFlag=='noSol':
        errorPrint(errNoSol)
    elif errFlag=='invalid':
        for i in errRows:
            colors[i[0]][i[1]]=(255,0,0)
        errorPrint(errValid)
    elif errFlag=='empty':
        errorPrint(errEmpty)
    elif errFlag=='resolved':
        errFlag=None
        errRows=[]
        screen.fill((255,255,255))
    pygame.display.update()

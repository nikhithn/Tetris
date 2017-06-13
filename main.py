import sys, pygame
from BlockFactory import BlockFactory

pygame.init()

size = width, height = 400, 640
blockSize = int(width/10)
drop = [0, blockSize]
boardColor = (0,0,0,255)
moveRight = [blockSize,0]
moveLeft = [-blockSize,0]

screen = pygame.display.set_mode(size)
board = pygame.Surface(screen.get_size())
bFactory = BlockFactory(board, blockSize, boardColor)

block, gameOver = bFactory.generateBlock()
dropTime = pygame.time.get_ticks()

while 1:
    currTime = pygame.time.get_ticks()
    if (currTime-dropTime>=200):
        if (block.moveBlock(drop)==False):
            for i in range(0, board.get_height(), blockSize):
                clearLine = True
                for j in range(0,board.get_width(),blockSize):
                    if (board.get_at([j,i])==boardColor):
                        clearLine = False
                if(clearLine):
                    area_rect = pygame.Rect(0, 0, board.get_width(), i)
                    print("Clearing Line")
                    print(area_rect)
                    area = board.subsurface(area_rect)
                    area = area.copy()
                    board.blit(area, (0,blockSize))
            block, gameOver = bFactory.generateBlock()
            if(gameOver == True):
                break
        dropTime = currTime
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                block.moveBlock(moveLeft)
            if event.key == pygame.K_RIGHT:
                block.moveBlock(moveRight)
            if event.key == pygame.K_UP:
                block.rotateBlock()

    screen.blit(board, (0,0))
    pygame.display.update()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.display.quit()
            pygame.quit()
            sys.exit()

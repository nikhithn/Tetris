import sys, pygame
from BlockFactory import BlockFactory

pygame.init()

# This is the size of the display
size = width, height = 400, 640

#This tetris board will be 10x16 blocks (where each tetrimino consists of 4 blocks)
#In general the width of a tetris board will be 10 blocks, and the height will vary
blockSize = int(width/10)

# Drop speed is the number milliseconds before the piece drops
dropSpeed = 500

# Define piece movements
drop = [0, blockSize]
moveRight = [blockSize,0]
moveLeft = [-blockSize,0]

# The boardColor will be a solid black (for now)
boardColor = (0,0,0,255)

# Set the size of the display to the size we defined above, and store it as screen
screen = pygame.display.set_mode(size)
# The board will be the entire screen size (so no hold piece or scoreboard, for now)
board = pygame.Surface(screen.get_size())

# Initialize a blockfactory (a custom class in the BlockFactory.py file)
bFactory = BlockFactory(board, blockSize, boardColor)
# Generate a block (a custom class in the BlockFactory.py file)
block, gameOver = bFactory.generateBlock()

# We are ready to start the game!
# Here we grab the current time so that we can measure game time relative to it
# This returns time in milliseconds
dropTime = pygame.time.get_ticks()

# Cannonical game loop, run forever until game over
while 1:

    # Get current time
    currTime = pygame.time.get_ticks()

    # More than the drop speed time has passed since the last drop
    # Then drop the block!
    if (currTime-dropTime>=dropSpeed):
        # First this is the new dropTime
        dropTime = currTime

        # Now we move the block by the drop increment
        # If the block could not be dropped (because it collided with something)
        # Then the block has fallen, and we need to check if any lines are cleared
        # And generate a new block
        if (block.moveBlock(drop)==False):

            # First check if any lines were cleared by looping through each row
            for i in range(0, board.get_height(), blockSize):
                clearLine = True
                # If there is any gap (a location where the board is visible)
                # Then don't clear the line
                for j in range(0,board.get_width(),blockSize):
                    if (board.get_at([j,i])==boardColor):
                        clearLine = False

                # If we should to clear the line
                if(clearLine):
                    # Then we grab the rectangle from the top to the row above the line to clear
                    # Then we copy that rectangle one row below, overwriting the line, and moving everything down
                    area_rect = pygame.Rect(0, 0, board.get_width(), i)
                    area = board.subsurface(area_rect)
                    area = area.copy()
                    board.blit(area, (0,blockSize))

            # Once any lines are cleared, we can generate the next block
            block, gameOver = bFactory.generateBlock()
            # If the block couldn't be generated (due to a collision) then the game is over!
            if(gameOver == True):
                # We break out of the game loop
                break
    
    # Here we take user input events and evaluate them
    for event in pygame.event.get():
        # If the user quits
        if event.type == pygame.QUIT: 
            # Then close the window, pygame and the process
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        # If a key is pressed
        keys = pygame.key.get_pressed()
        elif event.type == pygame.KEYDOWN:
            # Then if it is the left arrow key, move left, else if it is the right arrow key, move right
            if event.key == pygame.K_LEFT:
                block.moveBlock(moveLeft)
            elif event.key == pygame.K_RIGHT:
                block.moveBlock(moveRight)
            # If it is the up arrow key, then rotate.
            elif event.key == pygame.K_UP:
                block.rotateBlock()
        # All other input events are ignored

    # Finally draw the board onto the display, and update the display
    screen.blit(board, (0,0))
    pygame.display.update()

# If the above loop ends (game over)
# Then leave the pygame window open until the user exits
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.display.quit()
            pygame.quit()
            sys.exit()

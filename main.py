import sys, pygame
from BlockFactory import BlockFactory

pygame.init()

# Grab a system font, in this case monospace
# TODO: Figure out what happens if the font is not available
myfont = pygame.font.SysFont("monospace", 15)

# This is the size of the display
size = width, height = 400, 640

#This tetris board will be 10x16 blocks (where each tetrimino consists of 4 blocks)
#In general the width of a tetris board will be 10 blocks, and the height will vary
blockSize = int(width/10)

# Drop speed is the number milliseconds before the piece drops
dropSpeed = 200

# Define piece movements
drop = [0, blockSize]
moveRight = [blockSize,0]
moveLeft = [-blockSize,0]

# The boardColor will be a solid black (for now)
boardColor = (0,0,0,255)

# Score is set to 0 at the beginning of the game
score = 0

# Set the size of the display to the size we defined above, and store it as screen
screen = pygame.display.set_mode(size)
# The board will be the entire screen size (so no hold piece or scoreboard, for now)
board = pygame.Surface(screen.get_size())

# Initialize a blockfactory (a custom class in the BlockFactory.py file)
bFactory = BlockFactory(board, blockSize, boardColor)
# Generate a mino (a custom class in the BlockFactory.py file)
block, gameOver = bFactory.generateMino()

# We are ready to start the game!
# Here we grab the current time so that we can measure game time relative to it
# This returns time in milliseconds
dropTime = pygame.time.get_ticks()

# Cannonical game loop, run forever until game over
while 1:

    # Get current time
    currTime = pygame.time.get_ticks()

    # More than the drop speed time has passed since the last drop
    # Then drop the mino!
    if (currTime-dropTime>=dropSpeed):
        # First this is the new dropTime
        dropTime = currTime

        # Now we move the mino by the drop increment
        # If the mino could not be dropped (because it collided with something)
        # Then the mino has fallen, and we need to check if any lines are cleared
        # And generate a new mino
        if (block.moveMino(drop)==False):

            # Track the number of lines cleared.  Initially zero
            linesCleared = 0
            
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
                    # The number of lines cleared is increased by 1
                    linesCleared += 1
                    # Each subsequent line cleared in a single drop is worth 100 points more
                    score = score + linesCleared * 100

                    # Then we grab the rectangle from the top to the row above the line to clear
                    # Then we copy that rectangle one row below, overwriting the line, and moving everything down
                    area_rect = pygame.Rect(0, 0, board.get_width(), i)
                    area = board.subsurface(area_rect)
                    area = area.copy()
                    board.blit(area, (0,blockSize))

            # Once any lines are cleared, we can generate the next mino
            block, gameOver = bFactory.generateMino()
            # If the mino couldn't be generated (due to a collision) then the game is over!
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
        if event.type == pygame.KEYDOWN:
            # Then if it is the left arrow key, move left, else if it is the right arrow key, move right
            if event.key == pygame.K_LEFT:
                block.moveMino(moveLeft)
            if event.key == pygame.K_RIGHT:
                block.moveMino(moveRight)
            # If it is the up arrow key, then rotate.
            if event.key == pygame.K_UP:
                block.rotateMino()
        # All other input events are ignored

    # Finally draw the board onto the display 
    screen.blit(board, (0,0))

    # The score is printed to the top right of the scoree.  
    # TODO: This may interfere with block movement as an edge case.
    scoreLabel = myfont.render(str(score), 1, (255,255,0))
    screen.blit(scoreLabel, (0, 0))
    
    # Update the display
    pygame.display.update()

# If the above loop ends (game over)
# Then leave the pygame window open until the user exits
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.display.quit()
            pygame.quit()
            sys.exit()

import sys, pygame, abc, random

# This class generates blocks
# This file also contains the blocks themselves
# Blocks can draw themselves and move themselves
class BlockFactory:

    # The block factory takes the board so that it can put blocks on it
    def __init__(self, board, blockSize, boardColor):
        self.board = board
        self.blockSize = blockSize
        self.boardColor = boardColor

    # Here we generate a mino
    # We create a random int between 0 and 6, and based on the number we get, we generate a specific type of mino
    # So, we are generating a random mino each time
    def generateMino(self):
        mino = random.randint(0,6)
        if (mino==0):
            return I(self.board, self.blockSize, self.boardColor).generateMino()
        elif (mino==1):
            return L(self.board, self.blockSize, self.boardColor).generateMino()
        elif (mino==2):
            return J(self.board, self.blockSize, self.boardColor).generateMino()
        elif (mino==3):
            return T(self.board, self.blockSize, self.boardColor).generateMino()
        elif (mino==4):
            return S(self.board, self.blockSize, self.boardColor).generateMino()
        elif (mino==5):
            return Z(self.board, self.blockSize, self.boardColor).generateMino()
        else:
            return O(self.board, self.blockSize, self.boardColor).generateMino()


# mino is an abstract class that the specific types of minos inherit from
class Mino(abc.ABC):

    # The mino takes the board as the input so that it can draw itself on the board
    def __init__(self, board, blockSize, boardColor):
        self.board = board
        self.blockSize = blockSize
        self.boardColor = boardColor
        # The mino is defined by its edges
        # Each type of mino has a different shape, and therefore has a different edge list
        # Each edge corresponds to a single block, each block is a rect defined by [edge[0],edge[1],edge[0]+blockSize,edge[1]+blockSize]
        self.edgeList = [[],[],[],[]]
        # Block is a list that contains the actual rectangles on the surface (so we can draw them, move them, etc.)
        self.blocks = [[],[],[],[]]
        # Each type of mino has a specific color
        self.blockColor = [0,0,0]

    # Just loop through the edgelist and draw each block
    # Store the blocks in the block list
    def drawMino(self, blockColor):
        for i in range(4):
            self.blocks[i] = pygame.draw.rect(self.board, blockColor, [self.edgeList[i][0],self.edgeList[i][1],self.blockSize, self.blockSize])

    # To generate a mino, grab the edgelist of the mino
    # if there are any blocks that are already occupied then the game is over!
    def generateMino(self):
        gameOver = False
        for edge in self.edgeList:
            if (self.board.get_at(edge)!=self.boardColor):
                gameOver = True
        self.drawMino(self.blockColor)
        return self, gameOver
    
    # To move the mino, we first clear out the initial location of the mino (and set it back to the color of the board)
    def moveMino(self, movement):
        self.drawMino(self.boardColor)
        moved = True
        # Then we check to see if the location that we will move the mino to is occupied (or is past the board edge)
        for edge in self.edgeList:
            if (edge[0]+movement[0]<0 or edge[0]+movement[0]+self.blockSize>self.board.get_width() 
                or edge[1]+movement[1]+self.blockSize>self.board.get_height() 
                or self.board.get_at([edge[0]+movement[0],edge[1]+movement[1]])!=self.boardColor):
                moved = False
        # If we can move the mino, we update the edges with the new location (otherwise we leave the mino where it originally was)
        if (moved == True):
            for i in range(4):
                self.edgeList[i] = [self.edgeList[i][0]+movement[0],self.edgeList[i][1]+movement[1]]
        # Lastly we draw the mino
        self.drawMino(self.blockColor)
        return moved

    # Rotations are by 90 degrees, so we have to swap the x and y locations of the blocks relative to some axis
    def rotateMino(self):
        # First we clear out the original location of the mino
        self.drawMino(self.boardColor)
        # Then we grab the axis (the first edge in the mino is always the axis of rotation -- we just defined it that way)
        axis = self.edgeList[0]
        diff = []
        tempList = []

        for i in range(4):
            # We grab the relative positions of the blocks with respect to the axis and store them in the "diff" array
            diff = [axis[0]-self.edgeList[i][0],axis[1]-self.edgeList[i][1]]
            # We swap the relative x/y increments from the axis
            tempList.append([axis[0]-diff[1],axis[1]+diff[0]])
            # Here's an example: 
            # Suppose we have a mino with two blocks
            # **, the rotation would be *
            #                           *
            # If the first block is the axis, then the second block is [1,0] relative to the second block
            # The rotation would be [0, 1] with respect to the first block
            # So we subtract the relative location of the y coordinate from the x axis and add the relative location of the x to the y axis 

        # Check to see if the rotation collides with anything by seeing if where the block would be is already occupied
        # If it is occupied, we just return out and don't rotate the mino
        for edge in tempList:
            if (edge[0]<0 or edge[0]+self.blockSize>self.board.get_width() 
                or edge[1]+self.blockSize>self.board.get_height() 
                or edge[1]<0
                or self.board.get_at([edge[0],edge[1]])!=self.boardColor):
                self.drawMino(self.blockColor)
                return
        # Otherwise, update the edge list and draw the rotated mino
        self.edgeList=tempList
        self.drawMino(self.blockColor)


# Each of the specific types of blocks inherits from the Mino class
# When we generate the mino, we specify the initial edge locations and the color of the mino
# The rest of the generation and methods are the same for all minos
# Except the O block doesn't rotate
class I(Mino):
    def generateMino(self):
        self.edgeList = [[4*self.blockSize,0],[5*self.blockSize,0],[6*self.blockSize,0],[3*self.blockSize,0]]
        self.blockColor = [255,0,0]
        return super(I, self).generateMino()

class T(Mino):
    def generateMino(self):
        self.edgeList = [[5*self.blockSize,0],[4*self.blockSize,0],[5*self.blockSize,self.blockSize],[6*self.blockSize,0]]
        self.blockColor = [0,255,0]
        return super(T, self).generateMino()

class J(Mino):
    def generateMino(self):
        self.edgeList = [[5*self.blockSize,0],[4*self.blockSize,0],[6*self.blockSize,0],[6*self.blockSize,self.blockSize]]
        self.blockColor = [0,0,255]
        return super(J, self).generateMino()

class L(Mino):
    def generateMino(self):
        self.edgeList = [[5*self.blockSize,0],[4*self.blockSize,0],[6*self.blockSize,0],[4*self.blockSize,self.blockSize]]
        self.blockColor = [0,255,255]
        return super(L, self).generateMino()

class S(Mino):
    def generateMino(self):
        self.edgeList = [[5*self.blockSize,0],[6*self.blockSize,0],[4*self.blockSize,self.blockSize],[5*self.blockSize,self.blockSize]]
        self.blockColor = [255,255,0]
        return super(S, self).generateMino()

class Z(Mino):
    def generateMino(self):
        self.edgeList = [[5*self.blockSize,0],[4*self.blockSize,0],[6*self.blockSize,self.blockSize],[5*self.blockSize,self.blockSize]]
        self.blockColor = [255,255,255]
        return super(Z, self).generateMino()

class O(Mino):
    def generateMino(self):
        self.edgeList = [[4*self.blockSize,self.blockSize],[4*self.blockSize,0],[5*self.blockSize,0],[5*self.blockSize,self.blockSize]]
        self.blockColor = [255,0,255]
        return super(O, self).generateMino()
    
    # Cirles look the same when rotated, so let's just not rotate them
    def rotateMino(self):
        pass


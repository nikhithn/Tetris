import sys, pygame, abc, random

class BlockFactory:

    def __init__(self, board, blockSize, boardColor):
        self.board = board
        self.blockSize = blockSize
        self.boardColor = boardColor

    def generateBlock(self):
        mino = random.randint(0,6)
        if (mino==0):
            return I(self.board, self.blockSize, self.boardColor).generateBlock()
        elif (mino==1):
            return L(self.board, self.blockSize, self.boardColor).generateBlock()
        elif (mino==2):
            return J(self.board, self.blockSize, self.boardColor).generateBlock()
        elif (mino==3):
            return T(self.board, self.blockSize, self.boardColor).generateBlock()
        elif (mino==4):
            return S(self.board, self.blockSize, self.boardColor).generateBlock()
        elif (mino==5):
            return Z(self.board, self.blockSize, self.boardColor).generateBlock()
        else:
            return O(self.board, self.blockSize, self.boardColor).generateBlock()


class Block(abc.ABC):
    def __init__(self, board, blockSize, boardColor):
        self.board = board
        self.blockSize = blockSize
        self.boardColor = boardColor
        self.edgeList = [[],[],[],[]]
        self.blocks = [[],[],[],[]]
        self.blockColor = [0,0,0]

    def drawBlock(self, blockColor):
        for i in range(4):
            self.blocks[i] = pygame.draw.rect(self.board, blockColor, [self.edgeList[i][0],self.edgeList[i][1],self.blockSize, self.blockSize])

    def generateBlock(self):
        gameOver = False
        for edge in self.edgeList:
            if (self.board.get_at(edge)!=self.boardColor):
                gameOver = True
        self.drawBlock(self.blockColor)
        return self, gameOver
    
    def moveBlock(self, movement):
        self.drawBlock(self.boardColor)
        moved = True
        for edge in self.edgeList:
            if (edge[0]+movement[0]<0 or edge[0]+movement[0]+self.blockSize>self.board.get_width() 
                or edge[1]+movement[1]+self.blockSize>self.board.get_height() 
                or self.board.get_at([edge[0]+movement[0],edge[1]+movement[1]])!=self.boardColor):
                moved = False
        if (moved == True):
            for i in range(4):
                self.edgeList[i] = [self.edgeList[i][0]+movement[0],self.edgeList[i][1]+movement[1]]
        self.drawBlock(self.blockColor)
        return moved

    def rotateBlock(self):
        self.drawBlock(self.boardColor)
        axis = self.edgeList[0]
        diff = []
        tempList = []
        for i in range(4):
            diff = [axis[0]-self.edgeList[i][0],axis[1]-self.edgeList[i][1]]
            tempList.append([axis[0]-diff[1],axis[1]+diff[0]])
        for edge in tempList:
            if (edge[0]<0 or edge[0]+self.blockSize>self.board.get_width() 
                or edge[1]+self.blockSize>self.board.get_height() 
                or edge[1]<0
                or self.board.get_at([edge[0],edge[1]])!=self.boardColor):
                self.drawBlock(self.blockColor)
                return
        self.edgeList=tempList
        self.drawBlock(self.blockColor)

class I(Block):
    def generateBlock(self):
        self.edgeList = [[4*self.blockSize,0],[5*self.blockSize,0],[6*self.blockSize,0],[3*self.blockSize,0]]
        self.blockColor = [255,0,0]
        return super(I, self).generateBlock()

class T(Block):
    def generateBlock(self):
        self.edgeList = [[5*self.blockSize,0],[4*self.blockSize,0],[5*self.blockSize,self.blockSize],[6*self.blockSize,0]]
        self.blockColor = [0,255,0]
        return super(T, self).generateBlock()

class J(Block):
    def generateBlock(self):
        self.edgeList = [[5*self.blockSize,0],[4*self.blockSize,0],[6*self.blockSize,0],[6*self.blockSize,self.blockSize]]
        self.blockColor = [0,0,255]
        return super(J, self).generateBlock()

class L(Block):
    def generateBlock(self):
        self.edgeList = [[5*self.blockSize,0],[4*self.blockSize,0],[6*self.blockSize,0],[4*self.blockSize,self.blockSize]]
        self.blockColor = [0,255,255]
        return super(L, self).generateBlock()

class S(Block):
    def generateBlock(self):
        self.edgeList = [[5*self.blockSize,0],[6*self.blockSize,0],[4*self.blockSize,self.blockSize],[5*self.blockSize,self.blockSize]]
        self.blockColor = [255,255,0]
        return super(S, self).generateBlock()

class Z(Block):
    def generateBlock(self):
        self.edgeList = [[5*self.blockSize,0],[4*self.blockSize,0],[6*self.blockSize,self.blockSize],[5*self.blockSize,self.blockSize]]
        self.blockColor = [255,255,255]
        return super(Z, self).generateBlock()

class O(Block):
    def generateBlock(self):
        self.edgeList = [[4*self.blockSize,self.blockSize],[4*self.blockSize,0],[5*self.blockSize,0],[5*self.blockSize,self.blockSize]]
        self.blockColor = [255,0,255]
        return super(O, self).generateBlock()

    def rotateBlock(self):
        pass


import random

import pygame
import math


class Vec3:
    def __init__(self,x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vec = (x,y,z)
        self.mag = math.sqrt(x**2+ y**2 + z**2)

    def normalise(self):
        if self.mag == 0:
            return self.copy()
        return Vec3(self.x/self.mag, self.y/self.mag, self.z/self.mag)

    def copy(self):
        return Vec3(self.x, self.y, self.z)

    def dot(self, otherVec3):
        return self.x*otherVec3.x+self.y*otherVec3.y+self.z*otherVec3.z

    def multiply_vec(self, otherVec3):
        return Vec3(self.x*otherVec3.x, self.y*otherVec3.y, self.z*otherVec3.z)

    def clamp(self, lowerBound = (0,0,0), upperBound = (255,255,255)):
        return Vec3(min(max(self.x, lowerBound[0]), upperBound[0]),min(max(self.y, lowerBound[1]), upperBound[1]),min(max(self.z, lowerBound[2]), upperBound[2]))

    def set(self,x=False,y=False,z=False):
        if x:
            self.x = x
        if y:
            self.y = y
        if z:
            self.z = z

    def update_val(self):
        self.vec = (self.x, self.y, self.z)
        self.mag = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)



    def __add__(self, otherVec3):
        return Vec3(self.x+otherVec3.x, self.y+otherVec3.y, self.z+otherVec3.z)

    def __sub__(self, otherVec3):
        return Vec3(self.x-otherVec3.x, self.y-otherVec3.y, self.z-otherVec3.z)

    def __mul__(self, mag):
        return Vec3(self.x * mag, self.y * mag, self.z * mag)

    def __truediv__(self, mag):
        return Vec3(self.x / mag, self.y / mag, self.z / mag)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __abs__(self):
        return Vec3(abs(self.x), abs(self.y), abs(self.z))

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"


class Vec2:
    def __init__(self,x, y):
        self.x = x
        self.y = y
        self.vec = (x,y)
        self.mag = math.sqrt(x**2+ y**2)

    def normalise(self):
        if self.mag == 0:
            return self.copy()
        return Vec2(self.x/self.mag, self.y/self.mag)

    def copy(self):
        return Vec2(self.x, self.y)

    def dot(self, otherVec3):
        return self.x*otherVec3.x+self.y*otherVec3.y

    def multiply_vec(self, otherVec3):
        return Vec2(self.x*otherVec3.x, self.y*otherVec3.y)

    def clamp(self, lowerBound = (0,0,0), upperBound = (255,255,255)):
        return Vec2(min(max(self.x, lowerBound[0]), upperBound[0]),min(max(self.y, lowerBound[1]), upperBound[1]))

    def set(self,x=False,y=False):
        if x:
            self.x = x
        if y:
            self.y = y

    def update_val(self):
        self.vec = (self.x, self.y)
        self.mag = math.sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, otherVec3):
        return Vec2(self.x+otherVec3.x, self.y+otherVec3.y)

    def __sub__(self, otherVec3):
        return Vec2(self.x-otherVec3.x, self.y-otherVec3.y)

    def __mul__(self, mag):
        return Vec2(self.x * mag, self.y * mag)

    def __truediv__(self, mag):
        return Vec2(self.x / mag, self.y / mag)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __abs__(self):
        return Vec2(abs(self.x), abs(self.y))

    def __str__(self):
        return f"{self.x} {self.y}"

    def __mod__(self, n):
        return Vec2(self.x%n, self.y%n)

    def __floordiv__(self, n):
        return Vec2(self.x//n, self.y//n)

def getRandomVec():
    theta = math.tau * random.randint(0,100) / 100


    return Vec2(math.sin(theta), math.cos(theta))

f = open("settings.txt", "r")
fileText = f.read()
f.close()

fileSettings = fileText.split("\n")
thing1 = fileSettings[0].split(",")

boardDim = Vec2(int(thing1[0]), int(thing1[1]))
blockSize = int(fileSettings[1])

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((boardDim*blockSize + Vec2(0,150)).vec)
clock = pygame.time.Clock()

pointScoreArray = (0, 100, 250, 400, 800, 2000, 3000, 4000, 5000, 6000)
colorArray = (Vec3(255,100,100),
              Vec3(100,255,100),
              Vec3(100,100,255),
              Vec3(255,255,100),
              Vec3(255,100,255),
              Vec3(100,255,255),
              )
score = 0
bestScore = 0

def drawBlock(color, pos, borderSize = 4, screen = screen):
    pygame.draw.rect(screen, color.vec, pygame.Rect(pos.x, pos.y, blockSize, blockSize))
    pygame.draw.rect(screen, (color * 0.8).vec, pygame.Rect(pos.x+borderSize, pos.y+borderSize, blockSize-borderSize*2, blockSize-borderSize*2))

def drawBackground():
    backgroundSurface = pygame.Surface((boardDim*blockSize).vec)
    for x in range(boardDim.x):
        for y in range(boardDim.y):
            drawBlock(Vec3(20,20,20), Vec2(x,y)*blockSize, screen = backgroundSurface)

    return backgroundSurface


class Particles:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.dir = getRandomVec()
        self.speed = random.randint(0,10)
        self.remove = False

    def update(self):
        self.speed /= 1.1
        self.pos += self.dir * self.speed

        self.size /= 1.2

        if self.size < 0.1:
            self.remove = True

    def draw(self):
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(self.pos.x, self.pos.y, self.size, self.size))

class ParticleContainer:
    def __init__(self):
        self.container = []

    def add(self, particle):
        self.container.append(particle)

    def update(self):
        removeParticleArray = []
        for particle in self.container:
            particle.update()
            if particle.remove:
                removeParticleArray.append(particle)

        for particle in removeParticleArray:
            self.container.remove(particle)

    def draw(self):
        for particle in self.container:
            particle.draw()

particleContainer = ParticleContainer()

class Board:
    def __init__(self, boardDimensions):
        self.dim = boardDimensions
        self.boardRep = [[0 for x in range(self.dim.x)] for y in range(self.dim.y)]
        self.boardColorRep  = [[Vec3(0,0,0) for x in range(self.dim.x)] for y in range(self.dim.y)]

    def inBounds(self, pos):
        return pos.x >= 0 and pos.x < self.dim.x and pos.y >= 0 and pos.y < self.dim.y

    def reset(self):
        self.boardRep = [[0 for x in range(self.dim.x)] for y in range(self.dim.y)]

    def canPlaceBlock(self, block, pos):

        relCoord = Vec2(0,0)
        for row in block.blockShape:

            relCoord.x = 0

            for item in row:

                globalPos = pos + relCoord

                if item == 1:
                    if not self.inBounds(globalPos):
                        return False

                    if self.boardRep[globalPos.y][globalPos.x] == 1:
                        return False

                relCoord += Vec2(1, 0)

            relCoord += Vec2(0, 1)

        return True

    def placeBlock(self, block, blockColor, pos):
        if self.canPlaceBlock(block, pos):

            for y in range(pos.y, pos.y + block.height):
                for x in range(pos.x, pos.x + block.width):
                    blockType = block.blockShape[y- pos.y][x-pos.x]

                    if blockType != 0:
                        self.boardRep[y][x] = blockType
                        self.boardColorRep[y][x] = blockColor
            return True

        return False


    def draw(self):
        screen.blit(background, (0, 0))

        for y in range(self.dim.y):
            for x in range(self.dim.x):
                if self.boardRep[y][x] == 1:
                    drawBlock(self.boardColorRep[y][x], Vec2(x, y) * blockSize)

    def clearRows(self):
        global score
        clearRowArray = []
        clearColArray = []

        # rows
        for x in range(self.dim.y):
            if sum(self.boardRep[x]) == self.dim.x:
                clearRowArray.append(x)

        for y in range(self.dim.x):

            tempSum = 0
            for x in range(self.dim.y):
                tempSum += self.boardRep[x][y]

            if tempSum == self.dim.y:
                clearColArray.append(y)

        for row in clearRowArray:
            self.boardRep[row] = [0 for i in range(self.dim.x)]
            for i in range(self.dim.x):
                particleContainer.add(Particles(Vec2(i, row)*blockSize + Vec2(blockSize, blockSize)*0.5, random.randint(0,50)))

        for col in clearColArray:
            for y in range(self.dim.y):
                self.boardRep[y][col] = 0

                particleContainer.add(Particles(Vec2(col, y) * blockSize + Vec2(blockSize, blockSize)*0.5, random.randint(0, 50)))

        score += pointScoreArray[len(clearColArray)+len(clearRowArray)]

    def isGameOver(self, possibleBlocks):
        for block in possibleBlocks:

            canPlace = False
            for i in range(self.dim.x * self.dim.y):
                x = i % self.dim.x
                y = i // self.dim.y
                if self.canPlaceBlock(block, Vec2(x, y)):
                    canPlace = True
                    break

            if canPlace:
                return False

        return True






class Block:
    def __init__(self, blockShape):
        self.blockShape = blockShape
        self.width = len(self.blockShape[0])
        self.height = len(self.blockShape)

board = Board(boardDim)

class BlockDrag:
    def __init__(self, blockShape, ogPos):
        self.blockShape = blockShape.blockShape
        self.blockObject = blockShape
        self.pos = ogPos
        self.prevValidPos = ogPos
        self.color = random.choice(colorArray)

    def draw(self, currBlock, pos):
        if currBlock != self:
            x_count = 0
            y_count = 0
            tempSurface = pygame.Surface((500,500), pygame.SRCALPHA)
            for row in self.blockShape:
                x_count = 0
                for item in row:
                    blockVec = Vec2(x_count, y_count) * blockSize
                    if item != 0:
                        drawBlock(self.color, blockVec, screen=tempSurface)
                    x_count += 1

                y_count += 1
            newSurface = pygame.transform.scale_by(tempSurface, 0.5)

            screen.blit(newSurface, self.pos.vec)
            return

        cannotFit = True
        if pos.y + (len(self.blockShape)-1)*blockSize >= boardDim.y * blockSize or board.canPlaceBlock(self.blockObject, pos//blockSize):
            self.prevValidPos = pos
            cannotFit = False

        x_count = 0
        y_count = 0
        for row in self.blockShape:
            x_count = 0
            for item in row:
                blockVec = pos + Vec2(x_count, y_count) * blockSize
                if item != 0:
                    if pos.y + (len(self.blockShape)-1)*blockSize < boardDim.y * blockSize and not cannotFit:
                        drawBlock(self.color, blockVec // blockSize * blockSize)
                    else:
                        drawBlock(self.color, blockVec)
                x_count += 1

            y_count += 1



    def isHoverOver(self, mousePos):
        scaleFactor = 0.5
        return mousePos.x > self.pos.x and mousePos.x < self.pos.x + len(self.blockShape[0]) * blockSize * scaleFactor and mousePos.y > self.pos.y and mousePos.y < self.pos.y + len(self.blockShape) * blockSize * scaleFactor

running = True
background = drawBackground()

blockTypeArray = [
    [[1, 1],
     [1, 1]],
    [[1, 1, 1],
     [1, 1, 1]],
    [[1, 1],
     [1, 1],
     [1, 1]],
    [[1, 0],
     [1, 0],
     [1, 1]],
    [[1, 1],
     [0, 1],
     [0, 1]],
    [[1, 1],
     [1, 0],
     [1, 0]],
    [[0, 1],
     [0, 1],
     [1, 1]],
    [[1, 0, 0],
     [1, 1, 1]],
    [[1, 1, 1],
     [0, 0, 1]],
    [[0, 0, 1],
     [1, 1, 1]],
    [[1, 1, 1],
     [1, 0, 0]],
    [[1, 0],
     [1, 1],
     [1, 0]],
    [[0, 1],
     [1, 1],
     [0, 1]],
    [[0, 1, 0],
     [1, 1, 1]],
    [[1, 1, 1],
     [0, 1, 0]],
    [[1,1,1,1]],
    [[1],
     [1],
     [1],
     [1]],
    [[1,1,1,1,1]],
    [[1],
     [1],
     [1],
     [1],
     [1]],
    [[1,1,1],
     [1,1,1],
     [1,1,1]],
    [[1, 0],
     [1, 1],
     [0, 1]],
    [[0, 1],
     [1, 1],
     [1, 0]],
    [[1, 1, 0],
     [0, 1, 1]],
    [[0, 1, 1],
     [1, 1, 0]],
    [[0,0,1],
     [0,0,1],
     [1,1,1]],
    [[1,1,1],
     [1,0,0],
     [1,0,0]],
    [[1,1,1],
     [0,0,1],
     [0,0,1]],
    [[1,0,0],
     [1,0,0],
     [1,1,1]],
]



blockTypes = [Block(blockType) for blockType in blockTypeArray]


currBlock = None

blockChoiceArray = [BlockDrag(random.choice(blockTypes), Vec2(boardDim.x/3*i * blockSize + 50,boardDim.y*blockSize + 50)) for i in range(3)]

font = pygame.font.Font("Poppins-Regular.ttf",25)
fontSmol = pygame.font.Font("Poppins-Regular.ttf",15)
fontFat = pygame.font.Font("Poppins-Regular.ttf",50)


lost = False

while running:
    keys = pygame.key.get_pressed()
    mousePos = Vec2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if keys[pygame.K_ESCAPE]:
        running = False



    screen.fill((30,30,30))

    if not lost:
        if pygame.mouse.get_pressed()[0]:
            for block in blockChoiceArray:
                if block.isHoverOver(mousePos):
                    currBlock = block
                    break
        else:
            if currBlock != None:
                canPlace = board.placeBlock(currBlock.blockObject, currBlock.color, currBlock.prevValidPos // blockSize)

                if canPlace:
                    blockChoiceArray.remove(currBlock)
            currBlock = None

        board.clearRows()


        if len(blockChoiceArray) == 0:
            blockChoiceArray = [
                BlockDrag(random.choice(blockTypes), Vec2(boardDim.x / 3 * i * blockSize + 50, boardDim.y * blockSize + 50))
                for i in range(3)]

        if board.isGameOver(blockChoiceArray):
            lost = True

        particleContainer.update()




    board.draw()
    for block in blockChoiceArray:
        block.draw(currBlock, mousePos)

    particleContainer.draw()

    if score > bestScore:
        bestScore = score


    fontText = font.render(f"Score:{score}", 1, (255,255,255))
    fontText2 = fontSmol.render(f"Best Score:{score}", 1, (255,255,255))

    if not lost:
        screen.blit(fontText, (0,0))
        screen.blit(fontText2, (0,25))
    else:
        fontText = fontFat.render("Imagine Losing", 1, (255, 255, 255))
        fontText2 = font.render(f"Score:{score} Best:{bestScore}", 1, (255, 255, 255))

        fontSize1 = fontText.get_size()
        fontSize2 = fontText2.get_size()

        screen.blit(fontText,
                    ((boardDim.x * blockSize - fontSize1[0]) / 2, (boardDim.y * blockSize - fontSize1[1]) / 2))
        screen.blit(fontText2,
                    ((boardDim.x * blockSize - fontSize2[0]) / 2, (boardDim.y * blockSize - fontSize2[1]) / 2 + 50))

        if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            lost = False
            blockChoiceArray = [BlockDrag(random.choice(blockTypes),
                                          Vec2(boardDim.x / 3 * i * blockSize + 50, boardDim.y * blockSize + 50)) for i
                                in range(3)]
            currBlock = None
            board.reset()
            score = 0

    pygame.display.flip()
    clock.tick(60)



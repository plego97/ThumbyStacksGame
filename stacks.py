import time
import thumby
import math

# Stacks 
# Paul Fast
# 06.03.2022


class StackedLine:
    start = 0
    end = 0
    
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Game:
    # state: 1 = menu, 2 = game, 3 = lost, 4 = paused
    state = 0
    stacknumber = 0
    # 20 = resume, 30 = new game
    selectedmenupx = 0
    
    height = 0
    currX = 0
    direction = 0 # 0 = to right, 1 = to left
    currLength = 0
    stackedLines = []
    
    # constants
    maxLines = 20 # how many lines are shown
    speed = 1 # how fast the lines move
    
    # buttons
    def A(self):
        return thumby.buttonA.pressed()
    def B(self):
        return thumby.buttonB.pressed()
    def U(self):
        return thumby.buttonU.pressed()
    def D(self):
        return thumby.buttonD.pressed()
    
    def init(self):
        self.state = 1 # start on menu
        self.selectedmenupx = 30 # start pointer on new game
        thumby.display.setFPS(60)
        
    def initGame(self):
        self.stacknumber = 0
        self.selectedmenupx = 20 # set pointer to resume
        self.stackedLines = [StackedLine(0, thumby.display.width)]
        self.height = thumby.display.height - 1
        self.currX = 10
        self.currLength = thumby.display.width - 20
    
    def drawNumber(self, number, height):
        width = 0
        if number > 9:
            width = 5
        if number > 99:
            width = 9
        thumby.display.drawText(str(number), int(thumby.display.width /2) - width, height, 1)
        
    
    def drawPrevLines(self):
        lineLength = len(self.stackedLines)
        maxLines = min(self.maxLines, lineLength)
        self.height = -1
        
        for index in range(maxLines):
            index += 1
            line = self.stackedLines[-index]
            height = thumby.display.height - maxLines + index -2
            if(self.height is -1):
                self.height = height
            thumby.display.drawLine(line.start, height, line.end, height, 1)
            
        self.height -= 1
        
    def drawGame(self):
        self.drawNumber(self.stacknumber, 0)
        
        self.drawPrevLines()
        if self.currLength < 0:
            self.state = 3 # lost game
        
        if(self.direction is 0):
            self.currX += self.speed
            if(self.currX + self.currLength) > thumby.display.width:
                self.direction = 1
                self.currX = thumby.display.width - self.currLength - 1
        elif(self.direction is 1):
            self.currX -= self.speed
            if(self.currX < 0):
                self.direction = 0
                self.currX = 0
                
        thumby.display.drawLine(self.currX, self.height, self.currLength + self.currX, self.height, 1)
        
        if(self.A()):
            if(len(self.stackedLines) > 0):
                prev = self.stackedLines[-1]
                self.currLength = min(prev.end, self.currX + self.currLength) - max(prev.start, self.currX)
                self.currX = max(prev.start, self.currX)
            
            self.stackedLines.append(StackedLine(self.currX, self.currX + self.currLength))
            self.currX = 0
            self.stacknumber +=1
            while(self.A()): 
                time.sleep_ms(20)
        
        if(self.B()):
            self.state = 4
            while(self.B()): 
                time.sleep_ms(20)
        
        #thumby.display.drawLine(10, thumby.display.height - 1, thumby.display.width - 10, thumby.display.height - 1, 1)
    
    def drawGameOver(self):
        thumby.display.drawText("YOU LOST", int(thumby.display.width /2) - 24, 0,1)
        thumby.display.drawText("SCORE:", int(thumby.display.width /2) - 18, 10,1)
        self.drawNumber(self.stacknumber, 20)
        thumby.display.drawText(">TO MENU", int(thumby.display.width /2) - 24, 30,1)
        if(self.A()):
            self.initGame()
            self.state = 1 # show menu
            while(self.A()): 
                time.sleep_ms(20)
    
    def drawMenu(self):
        thumby.display.drawText("STACKS", int(thumby.display.width /2) - 18, 0,1)
        thumby.display.drawText(">NEW GAME", int(thumby.display.width /2) - 26, 20,1)
        if(self.A()):
            self.initGame()
            self.state = 2 # start game
            while(self.A()): 
                time.sleep_ms(20)
    
    def drawPauseMenu(self):
        thumby.display.drawText("STACKS", int(thumby.display.width /2) - 18, 0,1)
        thumby.display.drawText("RESUME", int(thumby.display.width /2) - 18, 20,1)
        thumby.display.drawText("NEW GAME", int(thumby.display.width /2) - 24, 30,1)
        thumby.display.drawText(">", 5, self.selectedmenupx, 1)
        if(self.U() or self.D()):
            self.selectedmenupx += 10 if self.selectedmenupx is 20 else -10
            while(self.U() or self.D()): 
                time.sleep_ms(20)
        if(self.A()):
            if(self.selectedmenupx is 30): # new game
                self.initGame()
            self.state = 2
            while(self.A()): 
                time.sleep_ms(20)

game = Game()
game.init()
while(1):
    thumby.display.fill(0)
    if game.state is 1:
        game.drawMenu()
    elif game.state is 2:
        game.drawGame()
    elif game.state is 3:
        game.drawGameOver()
    elif game.state is 4:
        game.drawPauseMenu()

    thumby.display.update()


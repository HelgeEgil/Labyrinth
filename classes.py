import maps
from graphics import *
from random import *

class Map:
    def __init__(self, board, win, blindMode):
        self.win = win

        # read the maps.py file for information about map building
        # board is the name of the map, provided from the main function        

        self.initwallsV = maps.maps[board]["wallsV"][:]
        self.initwallsH = maps.maps[board]["wallsH"][:]
        self.map = maps.maps[board]["items"][:]
        if "centaur" in maps.maps[board].keys():
            self.centaur = maps.maps[board]["centaur"][:]
            self.centCheck = True
        else:
            self.centCheck = False
            
        self.map.reverse() # so we get (0,0) at bottom left
        
        self.gridV = [ Line(Point(k-0.5, -0.5), Point(k-.5, 4.5)) for k in [1,2,3,4] ]
        self.gridH = [ Line(Point(-0.5, k-0.5), Point(4.5, k-.5)) for k in [1,2,3,4] ]

        self.initwallsV.reverse()
        self.initwallsH.reverse()

        self.linesV = {}
        self.linesH = {}

        self.centLines = []
        self.boardname = board
        self.buttonPos = [(-0.4, 0.4), (0.6, 1.4), (1.6, 2.4),
                          (2.6, 3.4), (3.6, 4.4)]
        self.blindMode = blindMode

        # V
        for x in range(6):
            for y in range(5):
                if not self.initwallsV[y][x]:
                    self.linesV[(x,y)] = 0
                if self.initwallsV[y][x] in [1,2,3,4,6]:
                    self.linesV[(x,y)] = Line(Point(x - 0.5, y - 0.5), Point(x - 0.5, y + 0.5))
                if self.initwallsV[y][x] in (2,6):
                    self.linesV[(x,y)].setOutline("green")
                if self.initwallsV[y][x] in (1,2,4,6):
                    self.linesV[(x,y)].setWidth(2)
                if self.initwallsV[y][x] == 1:
                    self.linesV[(x,y)].setOutline("darkgrey")
                if self.initwallsV[y][x]:
                    if self.blindMode:
                        self.linesV[(x,y)].setOutline("white")
                    self.linesV[(x,y)].draw(win)

        # H
        for x in range(5):
            for y in range(6):
                if not self.initwallsH[y][x]:
                    self.linesH[(x,y)] = 0
                if self.initwallsH[y][x]:
                    self.linesH[(x,y)] = Line(Point(x - 0.5, y - 0.5), Point(x + 0.5, y - 0.5))
                if self.initwallsH[y][x] in (2,6):
                    self.linesH[(x,y)].setOutline("green")
                if self.initwallsH[y][x] in (1,2,4,6):
                    self.linesH[(x,y)].setWidth(2)
                if self.initwallsH[y][x] == 1:
                    self.linesH[(x,y)].setOutline("darkgrey")
                if self.initwallsH[y][x]:
                    if self.blindMode:
                        self.linesH[(x,y)].setOutline("white")
                    self.linesH[(x,y)].draw(win)
        
        self.teleports = [0]*5
        for x in range(5):
            for y in range(5):
                if self.map[y][x] in range(1,6):
                    if self.teleports[self.map[y][x] - 1]:
                        print "Too many teleports!"
                        raw_input("Press a key to exit.")
                        sys.exit(1)
                    self.teleports[self.map[y][x]-1] = (x,y)
        self.teleports.append(self.teleports[0]) # for cyclic effect
        
        self.mapobjects = {}
        for x in range(5):
            for y in range(5):
                if self.map[y][x]:
                        self.mapobjects[(x,y)] = Text(Point(x, y), self.map[y][x])
                        self.mapobjects[(x,y)].setSize(16)
                        if self.blindMode:
                            self.mapobjects[(x,y)].setOutline("white")
                        self.mapobjects[(x,y)].draw(win)
                else:
                    self.mapobjects[(x,y)] = False

    def displayButtons(self):
        _p = self.buttonPos[:]
        self.buttons = [Rectangle(Point(_p[0][0], -0.9), Point(_p[0][1], -0.6)),
                        Rectangle(Point(_p[1][0], -0.9), Point(_p[1][1], -0.6)),
                        Rectangle(Point(_p[2][0], -0.9), Point(_p[2][1], -0.6)),
                        Rectangle(Point(_p[3][0], -0.9), Point(_p[3][1], -0.6)),
                        Rectangle(Point(_p[4][0], -0.9), Point(_p[4][1], -0.6))]
        self.buttonText = [Text(Point((_p[0][0]+_p[0][1])/2., -0.75), "<"),
                           Text(Point((_p[1][0]+_p[1][1])/2., -0.75), "OK"),
                           Text(Point((_p[2][0]+_p[2][1])/2., -0.75), "RAND"),
                           Text(Point((_p[3][0]+_p[3][1])/2., -0.75), "NO DM"),
                           Text(Point((_p[4][0]+_p[4][1])/2., -0.75), ">")]
        self.mapName = [Text(Point(2, 4.75), self.boardname)]
        
        for item in self.buttons + self.buttonText + self.mapName:
            item.draw(self.win)

    def removeButtons(self):
        for item in self.buttons + self.buttonText + self.mapName:
            item.undraw()

    def getName():
        if self.mapName:
            return self.mapName

    def pressButtons(self):
        while 1:
            p = self.win.getMouse()
            _p = self.buttonPos[:]
            if -0.9 < p.getY() < -0.6:
                if _p[0][0] < p.getX() < _p[0][1]:
                    return -1
                elif _p[1][0] < p.getX() < _p[1][1]:
                    return 0
                elif _p[2][0] < p.getX() < _p[2][1]:
                    return 3
                elif _p[3][0] < p.getX() < _p[3][1]:
                    return 2
                elif _p[4][0] < p.getX() < _p[4][1]:
                    return 1
        

    def getCentaur(self):
        if self.centCheck:
            return self.centaur
        else:
            return False
    
    def clear(self):
        for each in self.linesH.values() + self.linesV.values() + self.mapobjects.values():
            if each:
                each.undraw()
       
    def drawWallV(self, x, y):
        """Draws a wall at x (0-5) and y (0-4)."""
        if not self.linesV[(x,y)]:
            self.linesV[(x,y)] = Line(Point(x - 0.5, y - 0.5), Point(x - 0.5, y + 0.5))
            self.linesV[(x,y)].setWidth(2)
            self.linesV[(x,y)].setOutline("darkgrey")
            self.linesV[(x,y)].draw(self.win)
            self.initwallsV[y][x] = 1

    def displayCentaurLines(self):
        if not self.centCheck:
            return False
        
        pos = self.centaur[0][:]
        moves = self.centaur[1][:]
        movediagram = {"moveUp." : [0, 1],
                       "moveDown." : [0, -1],
                       "moveLeft." : [-1, 0],
                       "moveRight." : [1, 0] }
        self.centMarker = Image(Point(pos[0], pos[1]), 'centaur2.gif')

        for i in range(len(moves)):
            nextpos = [ pos[0] + movediagram[moves[i]][0],
                        pos[1] + movediagram[moves[i]][1] ]
            
            self.centLines.append(Line(Point(pos[0], pos[1]),
                                       Point(nextpos[0], nextpos[1])))
            self.centLines[-1].setWidth(2)
            self.centLines[-1].setOutline("darkblue")
            pos = nextpos
            self.centLines[-1].draw(self.win)
        self.centMarker.draw(self.win)

    def removeCentaurLines(self):
        if not len(self.centLines):
            return False
        for line in self.centLines:
            line.undraw()
        self.centMarker.undraw()
        

    def drawWallH(self, x, y):
        """Draws a wall at x (0-4) and y (0-5)."""
        if not self.linesH[(x,y)]:
            self.linesH[(x,y)] = Line(Point(x - 0.5, y - 0.5), Point(x + 0.5, y - 0.5))
            self.linesH[(x,y)].setWidth(2)
            self.linesH[(x,y)].setOutline("darkgrey")
            self.linesH[(x,y)].draw(self.win)
            self.initwallsH[y][x] = 1

    def deleteWallV(self, x, y):
        if self.linesV[(x,y)]:
            self.linesV[(x,y)].undraw()
            self.linesV[(x,y)] = False
            self.initwallsV[y][x] = 0

    def deleteWallH(self, x, y):
        if self.linesH[(x,y)]:
            self.linesH[(x,y)].undraw()
            self.linesH[(x,y)] = False
            self.initwallsH[y][x] = 0

    def setGrid(self):
        for each in self.gridH:
            each.setOutline("darkgrey")
            each.draw(self.win)
        for each in self.gridV:
            each.setOutline("darkgrey")
            each.draw(self.win)

    def removeGrid(self):
        for each in self.gridH:
            each.undraw()
        for each in self.gridV:
            each.undraw()

    def hamsterV(self, x, y):
        if self.linesV[(x,y)]:
            self.linesV[(x,y)].setOutline("green")
            if self.initwallsV[y][x] == 1:
                self.initwallsV[y][x] = 2
            else:
                self.initwallsV[y][x] = 6

    def hamsterH(self, x, y):
        if self.linesH[(x,y)]:
            self.linesH[(x,y)].setOutline("green")
            if self.initwallsH[y][x] == 1:
                self.initwallsH[y][x] = 2
            else:
                self.initwallsH[y][x] = 6

    def unHamsterV(self, x, y):
        if self.linesV[(x,y)]:
            self.linesV[(x,y)].setOutline("darkgrey")
            if self.initwallsV[y][x] == 2:
                self.initwallsV[y][x] = 1
            else:
                self.initwallsV[y][x] = 4

    def unHamsterH(self, x, y):
        if self.linesH[(x,y)]:
            self.linesH[(x,y)].setOutline("darkgrey")
            if self.initwallsH[y][x] == 2:
                self.initwallsH[y][x] = 1
            else:
                self.initwallsH[y][x] = 4

    def removeTreasure(self, x, y):
        if self.map[y][x] == "x":
            self.mapobjects[(x,y)].undraw()
            self.mapobjects[(x,y)] = False
            self.map[y][x] = 0

    def setTreasure(self, x, y):
        if not self.map[y][x]:
            self.map[y][x] = "x"
            self.mapobjects[(x,y)] = Text(Point(x, y), "x")
            self.mapobjects[(x,y)].setSize(16)
            self.mapobjects[(x,y)].draw(self.win)
        #else:
        #    self.mapobjects[y][x].setText(self.map[y][x] + "x")

    def getWallsV(self):
        return self.initwallsV

    def getWallsH(self):
        return self.initwallsH

    def getMap(self):
        return self.map

    def getTeleports(self):
        return self.teleports
        
    def getCentInitX(self):
        return self.centaur[0][0]

    def getCentInitY(self):
        return self.centaur[0][1]

    def getRandomEmptyPosition(self):
        x = (randrange(5), randrange(5))
        while self.mapobjects[x[0],x[1]]:
            x = (randrange(5), randrange(5))
        return x
    
class Player:
    def __init__(self, human, name, color, xpos, ypos, win, centaur, blindMode):
        self.human = human

        self.ammo = 2 * human
        self.grenades = 1 * human
        self.hamsters = 0
        self.hamsterkill = 0
        self.cement = 1 * human
        self.treasure = 0
        self.points = 0
        self.alive = 1 * human
        self.direction = 1
        self.blindMode = blindMode
        
        self.win = win
        position = Point(int(xpos), int(ypos))
        self.name = name
        self.color = color

        if self.human:
            self.marker = Circle(position, 0.5)
            if not self.blindMode:
                self.marker.setOutline(self.color)
            else:
                self.marker.setOutline("white")
            self.marker.setWidth(2)
#            self.marker = Image(position, 'players\\blackplayer.gif')
        else:
##            self.marker = Circle(position, 0.2)
##            self.marker.setOutline(self.color)
##            self.marker.setFill(self.color)
            if not blindMode:
                self.marker = Image(position, 'centaur2.gif')
            else:
                self.marker = Circle(position, 0.5)
                self.marker.setOutline("white")
        self.marker.draw(win)

        if not self.human:
            if centaur:
                self.centaur = centaur
                self.moveId = 0
            else:
                print "No centaur configured for map!"
                sys.exit(1)

    def shoot(self):
        self.ammo -= 1

    def throw(self):
        self.grenades -= 1

    def hamster(self):
        self.hamsters -= 1

    def hamsterKill(self):
        self.hamsterkill -= 1

    def die(self):
        if self.human:
            self.ammo = 0
            self.grenades = 0
            self.hamsters = 0
            self.hamsterkill = 0
            self.cement = 0
            self.treasure = 0
            self.alive = 0
            self.marker.setWidth(1)

    def revive(self):
        if self.human:
            self.alive = 1
            self.marker.setWidth(2)

    def useCement(self):
        self.cement -= 1

    def getX(self):
        if self.human:
            return int(self.marker.getCenter().getX())
        else:
            return int(self.marker.getAnchor().getX())
    
    def getY(self):
        if self.human:
            return int(self.marker.getCenter().getY())
        else:
            return int(self.marker.getAnchor().getY())

    def isHuman(self):
        return self.human

    def getName(self):
        return self.name

    def getStatus(self):
        return self.alive

    def getColor(self):
        return self.color

    def getAmmo(self):
        return self.ammo

    def getGrenades(self):
        return self.grenades

    def getCement(self):
        return self.cement

    def getHamster(self):
        return self.hamsters

    def getHamsterKill(self):
        return self.hamsterkill

    def getTreasure(self):
        return self.treasure
    
    def moveUp(self):
        self.marker.move(0, 1)

    def moveDown(self):
        self.marker.move(0, -1)

    def moveLeft(self):
        self.marker.move(-1, 0)

    def moveRight(self):
        self.marker.move(1, 0)

    def moveTo(self, x, y):
        delta_x = x - self.getX()
        delta_y = y - self.getY()
        self.marker.move(delta_x, delta_y) 

    def refillAmmo(self):
        self.ammo = 4
        self.grenades = 2

    def refillCement(self):
        self.cement = 2

    def refillHamster(self):
        self.hamsters = 2
        self.hamsterkill = 2

    def findTreasure(self):
        self.treasure = 1
        self.marker.setWidth(3)

    def moveOut(self):
        if self.treasure == 1:
            self.points += 1
        self.treasure = -1
        self.marker.setWidth(2)
        self.marker.undraw()

    def goIn(self):
        self.treasure = 0
        self.marker.draw(self.win)

    def getPoints(self):
        return self.points

    def remove(self):
        self.marker.undraw()

    def getCentMove(self):
        newDir = self.centaur[1][self.moveId]
        if self.direction > 0:
            if self.moveId == len(self.centaur[1]) - 1:
                self.moveId = 0
            else:
                self.moveId += 1
        elif self.direction < 0:
            if self.moveId == 0:
                self.moveId = len(self.centaur[1]) - 1
            else:
                self.moveId -= 1
        return newDir

    def centFlip(self):
        """Reverses the direction and flips the directions about the origin."""
        if self.direction > 0:
            if self.moveId == 0:
                self.moveId = len(self.centaur[1]) - 2
            elif self.moveId == 1:
                self.moveId = len(self.centaur[1]) - 1
        elif self.direction < 0:
            if self.moveId == len(self.centaur[1]) - 2:
                self.moveId = 0
            elif self.moveId == len(self.centaur[1]) - 1:
                self.moveId = 1
        else:
            self.moveId -= 2*self.direction
            
        self.direction *= -1
        for i in range(len(self.centaur[1])):
            if self.centaur[1][i] == "moveUp.":
                self.centaur[1][i] = "moveDown."
            elif self.centaur[1][i] == "moveDown.":
                self.centaur[1][i] = "moveUp."
            elif self.centaur[1][i] == "moveLeft.":
                self.centaur[1][i] = "moveRight."
            elif self.centaur[1][i] == "moveRight.":
                self.centaur[1][i] = "moveLeft."


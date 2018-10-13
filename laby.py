from graphics import *
from random import *
import sys

# An interface for labyrinth, the game.

import maps
from classes import *

def main():
    # init

    win = GraphWin("LABYRINTH", 500, 500)
    win.setBackground("white")
    win.setCoords(-1, -1, 5, 5)

    maplist = sorted(maps.maps.keys())

    print "****************** LABYRINTH ***********************"
    print
    print "Welcome! This is a DM interface of the pen-and-paper"
    print "game 'Labyrinth'. The available maps are: \n* " + "\n* ".join(maplist)
    print "\nYou are welcome to add your own maps in maps.py."
    print "\nPlease choose a map in the GUI.",

    n = len(maplist)
    i = 0
    while 1:
        board = Map(maplist[i], win, False) # last: blind mode
        board.displayCentaurLines()
        if n == 1: # only one map
            blindMode = False
            break
        board.displayButtons()
        choice = board.pressButtons() # -1, 0 or 1
        board.removeButtons()
        if choice == 0: # user has chosen map
            blindMode = False
            break
        board.removeCentaurLines()
        board.clear()
        del(board)
        if choice == 2: # blind mode
            board = Map(maplist[randrange(n)], win, True)
            blindMode = True
            break
        if choice == 3: # random map
            newMap = randrange(n)
            while newMap == i:
                newMap = randrange(n)
            i = newMap
        if choice in (-1, 1):
            i += choice
            if i == n:
                i = 0
            if i == -1:
                i = n - 1
        
    teleports = board.getTeleports()

    if board.getCentaur():
        centaur = raw_input("\nCentaur (y/N)? ").lower() \
            in ["y","yes","please"] and True or False
    else:
        centaur = False
    if not centaur:
        board.removeCentaurLines()

    nPlayers = raw_input("\nHow many players? ")

    if not nPlayers:
        win.close()
        sys.exit()
    else:
        nPlayers = eval(nPlayers)

    nPlayers += centaur
    players = [0]*nPlayers

    if centaur:
        players[-1] = Player(0, "Centaur", "black", board.getCentInitX(),
                         board.getCentInitY(), win, board.getCentaur(), blindMode)
        
    if nPlayers < 1:
        print "The dungeon master won!"
        win.close()
        sys.exit(0)
    player_names = []
    for i in range(nPlayers - centaur):
        name = raw_input("Player %s's name: "%(i+1))
        player_names.append(name)
    if not blindMode:
        board.setGrid()
    colors = ["red", "lightblue", "darkgreen", "darkpink", "lightgreen",
              "darkblue", "DarkCyan", "coral", "chocolate", "chartreuse",
              "DarkMagenta", "forest green", "gold", "maroon",
              "magenta", "peru", "RosyBrown"]
    shuffle(colors)
    
    _poslist = []
    for i in range(len(player_names)):
        if not blindMode:
            print "Choose %s's position by clicking on the map." % player_names[i]
            _pos = win.getMouse()
        else:
            _pos  = board.getRandomEmptyPosition()
            while _pos in _poslist:
                _pos  = board.getRandomEmptyPosition()
            _poslist.append(_pos)
            _pos = Point(_pos[0], _pos[1])
        
        players[i] = Player(1, player_names[i], colors[i],
                        _pos.getX()+0.5, _pos.getY()+0.5, win, False, blindMode)
    board.removeGrid()


    if centaur:
        board.removeCentaurLines()
    
    print "? for command help."

    firstround = True
    
    while 1:
        actions = ["moveUp", "u", "moveDown", "d", "moveLeft", "l", "moveRight",
                   "r", "wait", "w", "f", "moveOut",
                   "shootUp", "shootDown", "shootLeft", "shootRight", "shootHere",
                   "su", "sd", "sl", "sr", "sh",
                   "grenadeUp", "grenadeDown", "grenadeLeft", "grenadeRight",
                   "gu", "gd", "gl", "gr",
                   "cementUp", "cementDown", "cementLeft", "cementRight",
                   "cu", "cd", "cl", "cr",
                   "hamUp", "hamDown", "hamLeft", "hamRight",
                   "hu", "hd", "hl", "hr",
                   "hamKillUp", "hamKillDown", "hamKillLeft", "hamKillRight",
                   "hku", "hkd", "hkl", "hkr", "status",
                   "?", "quit", "exit", "die", "revive", "remove", "removeCent"]
                   
        for player in players:
            hitWall = False
            quick = False
            current_map = board.getMap()
            event = current_map[player.getY()][player.getX()]
            
            if not player.getStatus() and event == "H" and player.isHuman():
                player.revive()
                print "%s found the health center! He's alive!" % player.getName()
                quick = True
            
            if player.getTreasure() < 0:
                action = "f"
            elif firstround:
                action = "f"
            else:
                if player.isHuman():
                    action = raw_input("%s's turn (%s). A: %s/4, G: %s/2. Action: " % (player.getName(), player.getColor(), player.getAmmo(), player.getGrenades()))
                else:
                    action = player.getCentMove()
                if action:
                    if len(action) > 1 and action[-1] == ".":
                        quick = True
                        action = action[:-1]
            while not action in actions:
                print "Type a legal command please. ? for help."
                if player.isHuman():
                    action = raw_input("%s's turn (%s). A: %s/4, G: %s/2. Action: " % (player.getName(), player.getColor(), player.getAmmo(), player.getGrenades()))
                else:
                    action = player.getCentMove()
                if len(action) > 1 and action[-1] == ".":
                    quick = True
                    action = action[:-1]
            if action == "?":
                print "Type an action. Append a period (.) to skip 2nd action."
                print "Below is a list of all the legal actions (many of them"
                print "are shorthand versions, slike \"moveLeft\" and \"l\"): \n"
                print ", ".join(actions)
                action = raw_input("%s's turn (%s). A: %s/4, G: %s/2. Action: " % (player.getName(), player.getColor(), player.getAmmo(), player.getGrenades()))
            if action == "remove":
                if player.getTreasure():
                    board.setTreasure(player.getX(), player.getY())
                player.remove()
                players.remove(player)
                quick = True

            if action == "removeCent":
                if centaur:
                    players[-1].remove()
                    players.pop()
            
            if player.getTreasure() < 0:
                player.goIn()
                print "%s is returning to the map." % player.getName()
                action = "f"
                quick = True
            
            if action == "status":
                print "Ammo: %d, grenades: %d, hamsters: %d, hamster spray: %d, cement: %d" % \
                      (player.getAmmo(), player.getGrenades(),
                       player.getHamster(), player.getHamsterKill(), player.getCement())
                print "Treasure: %s, Points: %s, Alive? %s" % \
                      (player.getTreasure(), player.getPoints(),
                       player.getStatus() and "yes" or "no")
                action = raw_input("%s's (%s) turn. Action: " % \
                                   (player.getName(), player.getColor()))
        
            if action in ["exit", "quit"]:
                win.close()
                sys.exit(1)

            elif action in ["moveUp", "moveDown", "u", "d"]:
                wall = board.getWallsH()
                if action in ("moveUp", "u"):
                    if wall[player.getY() + 1][player.getX()]:
                        print "Wall!"
                        hitWall = True
                        if not player.isHuman():
                            player.centFlip()
                    else:
                        if player.getY() == 4:
                            player.moveOut()
                            print "You found the exit!"
                            print "You have %d point%s!" % (player.getPoints(), player.getPoints() > 1 and "s" or "")
                            quick = True
                        else:
                            player.moveUp()
                            print "OK."
                            event = current_map[player.getY()][player.getX()]
                                    
                elif action in ("moveDown", "d"):
                    if wall[player.getY()][player.getX()]:
                        print "Wall!"
                        hitWall = True
                        if not player.isHuman():
                            player.centFlip()
                    else:
                        if player.getY() == 0:
                            player.moveOut()
                            print "You found the exit!"
                            print "You have %d point%s!" % (player.getPoints(), player.getPoints() > 1 and "s" or "")
                            quick = True
                        else:
                            player.moveDown()
                            print "OK."
                            event = current_map[player.getY()][player.getX()]
                          #  print event
                else: print "Not possible"
            elif action in ["moveLeft", "moveRight", "l", "r"]:
                wall = board.getWallsV()    
                if action in ("moveLeft", "l"):
                    if wall[player.getY()][player.getX()]: # 2,2
                        print "Wall!"
                        hitWall = True
                        if not player.isHuman():
                            player.centFlip()
                    else:
                        if player.getX() == 0:
                            player.moveOut()
                            print "You found the exit!"
                            print "You have %d point%s!" % (player.getPoints(), player.getPoints() > 1 and "s" or "")
                            quick = True
                        else:
                            player.moveLeft()
                            event = current_map[player.getY()][player.getX()]
                            print "OK."
                     #   print event
                elif action in ("moveRight", "r"):
                    if wall[player.getY()][player.getX() + 1]:
                        print "Wall!"
                        hitWall = True
                        if not player.isHuman():
                            player.centFlip()
                    else:
                        if player.getX() == 4:
                            player.moveOut()
                            print "You found the exit!"
                            print "You have %d point%s!" % (player.getPoints(), player.getPoints() > 1 and "s" or "")
                            quick = True
                        else:
                            player.moveRight()
                            print "OK."
                            event = current_map[player.getY()][player.getX()]
                        #    print event
                else: print "Not possible"


            if centaur:
                for target in players[:-1]:
                    if target.getX() == players[-1].getX() and \
                       target.getY() == players[-1].getY() and \
                       target.getStatus():
                        if target.getTreasure():
                            board.setTreasure(target.getX(), target.getY())
                        target.die()
                        print "The centaur killed %s" % target.getName()

            elif action == "die":
                if player.getTreasure(): board.setTreasure(player.getX(), player.getY())
                player.die()
            elif action == "revive":
                player.revive()
                quick = True
            elif action in ("wait", "w"):
                continue # use this to fix stuff
            elif action == "f":
                event = current_map[player.getY()][player.getX()]
            # Move action is done, the player can shoot/throw grenades

            if event == "x" and player.getStatus():
                if not player.getTreasure():
                    board.removeTreasure(player.getX(), player.getY())
                    player.findTreasure()
                    print "%s found treasure!" % player.getName()
                else:
                    print "%s is LOADED and cannot pick up more treasures" % player.getName()
            elif event == "x" and not player.getStatus() and player.isHuman():
                print "%s looks at a treasure, but is dead!" % player.getName()
            if event in range(1,6) and not hitWall and action in ("u","d","l","r","f") \
                                    and not player.getTreasure() < 0:
                newPos = teleports[teleports.index((player.getX(),
                                                   player.getY())) + 1]
                player.moveTo(newPos[0], newPos[1])
                print "%s fell down a hole!" % player.getName()
            elif event == "h" and player.isHuman():
                if player.getStatus():
                    player.refillHamster()
                    print "%s found the hamster storage!" % player.getName()
                else:
                    print "%s is dead, but the hamsters here are not." % player.getName()
            elif event == "A" and player.isHuman():
                if player.getStatus():
                    player.refillAmmo()
                    print "%s found the ammo storage!" % player.getName()
                else:
                    print "%s walked upon guns: Revenge is only a life away." % player.getName()
            elif event == "H" and player.isHuman():
                if not player.getStatus():
                    print "%s found the health center! He's alive!" % player.getName()
                    player.revive()
                    quick = True
            elif event == "c" and player.isHuman():
                if player.getStatus():
                    player.refillCement()
                    print "%s found the cement storage!" % player.getName()
                else:
                    print "What use do %s have for cement?" % player.getName()

            if (action in ("u", "d", "l", "r", "f") or "move" in action) and not \
                                       (firstround or quick or not player.getStatus()) and \
                                       (player.getAmmo() + player.getGrenades() + \
                                        player.getHamster() + player.getHamsterKill() + \
                                        player.getCement() > 0):
                action = raw_input("2nd action (grenadeDir, shootDir): ")
            if action in ["grenadeLeft", "grenadeRight", "grenadeUp", "grenadeDown",
                          "gl", "gr", "gu", "gd"]:
                
                # add test for hamsters
                if player.getGrenades() > 0:
                    if action in ("grenadeLeft", "gl"):
                        wall = board.getWallsV()
                        if wall[player.getY()][player.getX()] == 1:
                            board.deleteWallV(player.getX(), player.getY())
                            player.throw()
                            if event == "A":
                                player.refillAmmo()
                            print "Wall deleted."
                        elif wall[player.getY()][player.getX()] in (2, 6):
                            print "Hamster'd wall!"
                        elif wall[player.getY()][player.getX()] == 4:
                            player.throw()
                            if event == "A":
                                player.refillAmmo()
                            print "You hit an outer wall!"
                        else:
                            player.throw()
                            if event == "A":
                                player.refillAmmo()
                            print "The empty corridor dies a horrible death!"
                    elif action in ("grenadeRight", "gr"):
                        wall = board.getWallsV()
                        if wall[player.getY()][player.getX() + 1] == 1:
                            player.throw()
                            if event == "A":
                                player.refillAmmo()
                            board.deleteWallV(player.getX() + 1, player.getY())
                            print "Wall deleted."
                        elif wall[player.getY()][player.getX() + 1] in (2,6):
                            print "Hamster'd wall!"
                        elif wall[player.getY()][player.getX() + 1] == 4:
                            # was: player.getY() == 4:, but printed wrongly
                            player.throw()
                            if event == "A":
                                player.refillAmmo()
                            print "You hit an outer wall!"
                        else:
                            player.throw()
                            if event == "A":
                                player.refillAmmo()
                            print "The empty corridor dies a horrible death!"
                    elif action in ("grenadeUp", "gu"):
                        wall = board.getWallsH()
                        if wall[player.getY() + 1][player.getX()] == 1:
                            player.throw()
                            if event == "A":
                                player.refillAmmo()
                            print wall[player.getY()][player.getX()]
                            board.deleteWallH(player.getX(), player.getY() + 1)
                            print "Wall deleted!"
                        elif wall[player.getY() + 1][player.getX()] in (2,6):
                            print "Hamster'd wall!"
                        elif wall[player.getY() + 1][player.getX()] == 4:
                            player.throw()
                            if event == "A":
                                player.refillAmmo()
                            print "You hit an outer wall!"
                        else:
                            player.throw()
                            if event == "A":
                                player.refillAmmo()
                            print "The empty corridor dies a horrible death!"
                    elif action in ("grenadeDown", "gd"):
                        wall = board.getWallsH()
                        if wall[player.getY()][player.getX()] == 1:
                            player.throw()
                            if event == "A":
                                player.refillAmmo()
                            print wall[player.getY()][player.getX()]
                            board.deleteWallH(player.getX(), player.getY())
                            print "Wall deleted!"
                        elif wall[player.getY()][player.getX()] in (2,6):
                            print "Hamster'd wall!"
                        elif wall[player.getY()][player.getX()] == 4:
                            player.throw()
                            if event == "A":
                                player.refillAmmo()
                            print "You hit an outer wall!"
                        else:
                            player.throw()
                            if event == "A":
                                player.refillAmmo()
                            print "The empty corridor dies a horrible death!"
                    print "Grenades left:", player.getGrenades()
                else:
                    print "No grenades!"
            elif action in ["cementLeft", "cementRight", "cementUp", "cementDown",
                            "cl", "cr", "cu", "cd"]:
                if player.getCement():
                    if action in ("cementLeft", "cl"):
                        wall = board.getWallsV()
                        if not wall[player.getY()][player.getX()]:
                            board.drawWallV(player.getX(),player.getY())
                            print "Wall created."
                            player.useCement()
                            if event == "c":
                                    player.refillCement()
                        else:
                            print "Full!"
                    elif action in ("cementRight", "cr"):
                        wall = board.getWallsV()
                        if not wall[player.getY()][player.getX() + 1]:
                            board.drawWallV(player.getX() + 1, player.getY())
                            print "Wall created."
                            player.useCement()
                            if event == "c":
                                    player.refillCement()
                        else:
                            print "Full!"
                    elif action in ("cementUp", "cu"):
                        wall = board.getWallsH()
                        if not wall[player.getY() + 1][player.getX()]:
                            board.drawWallH(player.getX(), player.getY() + 1)
                            print "Wall created!"
                            player.useCement()
                            if event == "c":
                                    player.refillCement()
                        else:
                            print "Full!"
                    elif action in ("cementDown", "cd"):
                        wall = board.getWallsH()
                        if not wall[player.getY()][player.getX()]:  
                            board.drawWallH(player.getX(), player.getY())
                            print "Wall created!"
                            player.useCement()
                            if event == "c":
                                    player.refillCement()
                        else:
                            print "Full!"
                    print "Cement left:", player.getCement()
                else:
                    print "No cement!"
                        
            elif action in ["hamsterRight", "hamsterLeft", "hamsterUp",
                            "hamsterDown", "hr", "hl", "hu", "hd"]:
                if player.getHamster():
                    if action in ["hl", "hamsterLeft"]:
                        wall = board.getWallsV()
                        if wall[player.getY()][player.getX()]:
                            board.hamsterV(player.getX(),player.getY())
                            print "Hamster created."
                            player.hamster()
                            if event == "h":
                                player.refillHamster()
                                print "Free hamster!"
                        else:
                            print "Impossible!"
                    elif action in ["hamsterRight", "hr"]:
                        wall = board.getWallsV()
                        if wall[player.getY()][player.getX() + 1]:
                            board.hamsterV(player.getX() + 1, player.getY())
                            print "Hamster created."
                            player.hamster()
                            if event == "h":
                                player.refillHamster()
                                print "Free hamster!"
                        else:
                            print "Impossible!"
                    elif action in ["hu", "hamsterUp"]:
                        wall = board.getWallsH()
                        if wall[player.getY() + 1][player.getX()]:
                            board.hamsterH(player.getX(), player.getY() + 1)
                            print "Hamster created!"
                            player.hamster()
                            if event == "h":
                                player.refillHamster()
                                print "Free hamster!"
                        else:
                            print "Impossible!"
                    elif action in ["hd", "hamsterDown"]:
                        wall = board.getWallsH()
                        if wall[player.getY()][player.getX()]:
                            board.hamsterH(player.getX(), player.getY())
                            print "Hamster created!"
                            player.hamster()
                            if event == "h":
                                player.refillHamster()
                                print "Free hamster!"
                        else:
                            print "Impossible!"
                    print "Hamsters left:", player.getHamster()
                else:
                    print "No hamsters!"
            elif action in ["hamKillRight", "hamKillLeft", "hamKillUp",
                            "hamKillDown", "hkr", "hkl", "hku", "hkd"]:
                if player.getHamsterKill():
                    if action in ("hkl", "hamKillLeft"):
                        wall = board.getWallsV()
                        if wall[player.getY()][player.getX()]:
                            board.unHamsterV(player.getX(),player.getY())
                            print "Hamster sprayed."
                            player.hamsterKill()
                            if event == "h":
                                player.refillHamster()
                                print "Free hamster spray!"
                        else:
                            print "Impossible!"
                    elif action in ("hamKillRight", "hkr"):
                        wall = board.getWallsV()
                        if wall[player.getY()][player.getX() + 1]:
                            board.unHamsterV(player.getX() + 1, player.getY())
                            print "Hamster sprayed."
                            player.hamsterKill()
                            if event == "h":
                                player.refillHamster()
                                print "Free hamster spray!"
                        else:
                            print "Impossible!"
                    elif action in ("hku", "hamKillUp"):
                        wall = board.getWallsH()
                        if wall[player.getY() + 1][player.getX()]:
                            board.unHamsterH(player.getX(), player.getY() + 1)
                            print "Hamster sprayed!"
                            player.hamsterKill()
                            if event == "h":
                                player.refillHamster()
                                print "Free hamster spray!"
                        else:
                            print "Impossible!"
                    elif action in ("hkd", "hamKillDown"):
                        wall = board.getWallsH()
                        if wall[player.getY()][player.getX()]:  
                            board.unHamsterH(player.getX(), player.getY())
                            print "Hamster sprayed!"
                            player.hamsterKill()
                            if event == "h":
                                player.refillHamster()
                                print "Free hamster spray!"
                        else:
                            print "Impossible!"
                    print "Hamster spray left:", player.getHamsterKill()
                else:
                    print "No hamster spray!"
                
            elif action in ["shootLeft", "shootRight", "shootUp", "shootDown",
                            "shootHere", "sl", "sr", "su", "sd", "sh"]:
                dead_player = False
                if player.getAmmo():
                    player.shoot()
                    if event == "A":
                        player.refillAmmo()
                        print "Free shot!"
                else:
                    print "Out of ammo!"
                    action = False
                    
                if action in ("shootLeft", "sl"):
                    wall = board.getWallsV()
                    dist = {}
                    clear_path = True
                    for target in players:
                        if player.getName() == target.getName(): continue
                        if target.getY() == player.getY():
                            # right Y
                            if target.getX() < player.getX():
                                # right direction
                                for steps in range(target.getX()+1,
                                                   player.getX()+1):
                                    if wall[target.getY()][steps]:
                                        clear_path = False
                                        break
                                    else:
                                        clear_path = True
                            else:
                                clear_path = False
                                continue
                        else: continue
                        if clear_path and target.getStatus():
                            print target.getName()
                            dist[player.getX() - target.getX()] = target.getName()
                    if dist:
                        dead_player = dist[min(dist.keys())]
                        print "%s is dead" % dead_player
                        for target in players:
                            if target.getName() == dead_player:
                                if target.getTreasure():
                                    board.setTreasure(target.getX(), target.getY())
                                target.die()
                    else:
                        print "You hit the wall!"
                                
                elif action in ("shootRight", "sr"):
                    wall = board.getWallsV()
                    dist = {}
                    for target in players:
                        if player.getName() == target.getName(): continue
                        if target.getY() == player.getY():
                            # right Y
                            if target.getX() > player.getX():
                                # right direction
                                for steps in range(player.getX()+1,
                                                   target.getX()+1):
                                    if wall[target.getY()][steps]:
                                        clear_path = False
                                        break
                                    else:
                                        clear_path = True
                            else:
                                clear_path = False
                                continue
                        else: continue
                        if clear_path and target.getStatus():
                            dist[target.getX() - player.getX()] = target.getName()
                    if dist:
                        dead_player = dist[min(dist.keys())]
                        print "%s is dead" % dead_player
                        for target in players:
                            if target.getName() == dead_player:
                                if target.getTreasure():
                                    board.setTreasure(target.getX(), target.getY())
                                target.die()
                    else:
                        print "You hit the wall!"

                elif action in ("shootUp", "su"):
                    wall = board.getWallsH()
                    dist = {}
                    for target in players:
                        if player.getName() == target.getName(): continue
                        if target.getX() == player.getX():
                            # right X
                            if target.getY() > player.getY():
                                # right direction
                                for steps in range(player.getY()+1,
                                                   target.getY()+1):
                                    if wall[steps][target.getX()]:
                                        clear_path = False
                                        break
                                    else:
                                        clear_path = True
                            else:
                                clear_path = False
                                continue
                        else: continue
                        if clear_path and target.getStatus():
                            dist[target.getY() - player.getY()] = target.getName()
                    if dist:
                        dead_player = dist[min(dist.keys())]
                        print "%s is dead" % dead_player
                        for target in players:
                            if target.getName() == dead_player:
                                if target.getTreasure():
                                    board.setTreasure(target.getX(), target.getY())
                                target.die()
                    else:
                        print "You hit the wall!"

                elif action in ("shootDown", "sd"):
                    wall = board.getWallsH()
                    dist = {}
                    for target in players:
                        if player.getName() == target.getName():
                            continue
                        if target.getX() == player.getX():
                            # right X
                            if target.getY() < player.getY():
                                # right direction
                                for steps in range(target.getY()+1,
                                                   player.getY()+1):
                                    if wall[steps][target.getX()]:
                                        clear_path = False
                                        break
                                    else:
                                        clear_path = True
                            else:
                                clear_path = False
                                continue
                        else: continue
                        if clear_path and target.getStatus():
                            dist[player.getY() - target.getY()] = target.getName()
                    if dist:
                        dead_player = dist[min(dist.keys())]
                        print "%s is dead" % dead_player
                        for target in players:
                            if target.getName() == dead_player:
                                if target.getTreasure():
                                    board.setTreasure(target.getX(), target.getY())
                                target.die()
                    else:
                        print "You hit the wall!"

                if action in ("shootHere", "sh"):
                    for target in players:
                        if player.getName() == target.getName():
                            continue
                        if not target.getStatus():
                            continue
                        if target.getY() == player.getY():
                            # right Y
                            if target.getX() == player.getX():
                                dead_player = target.getName()
                    if dead_player:
                        print "%s is dead" % dead_player
                        for target in players:
                            if target.getName() == dead_player:
                                if target.getTreasure():
                                    board.setTreasure(target.getX(), target.getY())
                                target.die()
                    else:
                        print "You hit the ground!"
                                    
            elif action in ("wait", "w"):
                continue
                #event = current_map[pos[1]][pos[0]]
                #print event
            elif action in ["exit", "quit"]:
                win.close()
                del(board)
                sys.exit(1)
        if firstround: firstround = False
main()

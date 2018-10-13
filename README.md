# Labyrinth
A Dungeon Master (DM) interface for the pen & paper game Labyrinth.

A session consists of 1--4 players plus a DM.
The players compete on an (for them) unknown map for 
the five treasures put there. A point is awarded when
a player carrying a treasure exits the map. The players 
move around by  interacting with the DM: "Move Up (North)", 
"Move Left (West)"). The DM checks the map, and respons whether 
the action is possible or not. If the path is blocked by a wall, for 
example, the action is not possible and the player is told so
(and has spent his move). It is up to the players to connect
the map fragments identified by their movements to the full
map, where they are now able to navigate with grace.

The map consists of a 5x5 cell grid with the following
* Walls put between the cells
* Teleporters (five cyclic teleporters 1->2->3->4->5->1)
* Five treasures
* An exit in the outer walls
* The possibility of a secret exit, also in the outer walls
* An ammo storage cell: The player will here receive 4 shots and 2 grenades
* A cement storage: The player will here receive 2 units of cement
* A hamster storage: The player will receive two hamsters and two hamster sprays
* A health studio: Killed players will receive life here (hidden from living players)
* Some maps also have a centaur, with a preprogrammed A->B->A route

A player turn consists of (in turn)
i) the possibility of a one-cell movement or following through in a teleporter
ii) An action, such as shooting in a direction (up/down/left/right/here) where
	a player standing in the indicated direction unhindered by walls will be killed,
	throwing a grenade (UDLR) to remove a (non-hamstered) wall, applying a hamster
	in a direction (UDLR) to grenade-securing a wall (the grenade would be given back),
	applying hamster spray to remove a wall or using cement (UDLR) to construct a new wall.
	
It is also possible to omit the movement to gain a single action.
If a player is killed, he loses all his belongings (shots, grenades, hamsters, hamster sprays, 
cement and the single treasure he might be carrying). The treasure is then put on the 
ground where he died, available for later pickup by any players. 
He is a ghost, and must now wander around to find the health studio.

If a player locates the exit, he must spend a turn outside before being available in the cell
inside the door. He gains a point if he carries a treasure upon exit (and deposits it outside).

The secret exit is a cemented outer wall which must be grenaded. If a regular outer wall is
grenaded, the player is told the wall cannot be destroyed (and loses his grenade) -- identifying
the wall as an outer wall.

The player with the most points when all treasures are carried out is the winner.

PROGRAM INSTRUCTIONS:
Run "laby.py" as a DM (or in noDM mode to hide the map -- a random map will be chosen). Choose
a map and the number of players. All commands is given in the CLI, use "h" to see the available
commands.
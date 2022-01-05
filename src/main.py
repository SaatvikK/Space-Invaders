############ IMPORTS ############
# Libraries
import pygame;
import random as rand;
import json;
from glob import glob;
import time;

# Other classes
from game import game;
from MainMenu import mainMenu;
#################################

class Main():
  def __init__(self) -> None:
    return None;
  
  def main(self):
    newmenu = mainMenu();
    newmenu.menuStart();
    if(newmenu.type == "create"): 
      newgame = game(int(newmenu.Lives), newmenu.cooldowns, newmenu.difficulty);
      newgame.GameID = newgame.generateGameID();
      newgame.createSprites();
      newgame.makeAliens();
      newgame.saveGame();
      newgame.gameLoop();

    elif(newmenu.type == "load"):
      newgame = game(0, {"alien": 0, "player": 0, "AlienBulletsMax": 0}, "easy");
      newgame.createSprites();
      newgame.load(newmenu.GameID);
      newgame.makeAliens();
      newgame.saveGame();
      newgame.gameLoop();



if(__name__ == "__main__"): 
  MainObj = Main();
  MainObj.main();

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
    newgame = game(int(newmenu.Lives), newmenu.cooldowns);


if(__name__ == "__main__"): 
  MainObj = Main();
  MainObj.main();

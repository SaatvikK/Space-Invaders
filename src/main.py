############ IMPORTS ############
# Classes
from game import game;
from MainMenu import mainMenu;
from LoginMenu import loginMenu;
import sys;
#################################

class Main():
  def __init__(self, IsDev) -> None:
    self.IsDev = IsDev;
    return None;
  
  def main(self):
    if(self.IsDev == "dev"):
      self.executeGame("admin"); # If in developer mode, auto-log in as "admin".
    
    newlogin = loginMenu();
    newlogin.menu();
    if(newlogin.res["status"] == True):
      self.executeGame(newlogin.res["usrn"]);
      exit()
  
  def executeGame(self, usrn):
    newmenu = mainMenu(self.IsDev, usrn);
    newmenu.menuStart();
    if(newmenu.type == "create"): 
      newgame = game(int(newmenu.Lives), newmenu.cooldowns, newmenu.difficulty, self.IsDev, usrn);
      newgame.GameID = newgame.generateGameID();
      newgame.createSprites();
      newgame.makeAliens();
      newgame.saveGame();
      newgame.gameLoop();

    elif(newmenu.type == "load"):
      newgame = game(0, {"alien": 0, "player": 0, "AlienBulletsMax": 0}, "easy", self.IsDev, usrn);
      newgame.createSprites();
      newgame.load(newmenu.GameID);
      newgame.makeAliens();
      newgame.saveGame();
      newgame.gameLoop();

if(__name__ == "__main__"):
  IsDev = sys.argv[1];
  MainObj = Main(IsDev);
  MainObj.main();
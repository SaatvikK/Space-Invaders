############ IMPORTS ############
# Classes
from game import game;
from MainMenu_v3 import mainMenu;
from LoginMenu import loginMenu;
import sys;
#################################

# This is the main class, it handles all data transfers between the login menu, main menu, and game objects.
# It also executes the login menu, main menu, and game object when/if needed.
class Main():
  def __init__(self, IsDev) -> None:
    self.IsDev = IsDev;
    return None;
  
  def main(self):
    if(self.IsDev == "dev"): # If `IsDev` is true, the login-system is byassed and the developer logins using the `admin` account.
      self.executeGame("admin"); # If in developer mode, auto-log in as "admin".
    
    newlogin = loginMenu(); # Instantiate a new login menu.
    newlogin.menu(); # Execute the menu method to display the login menu.
    if(newlogin.res["result"] == True): # `newlogin.res` is a dictionary that holds two key-value pairs: 1. The status of the last attempted login (boolean); 2. The reason of the failed login (usrname/pwd wrong or a server error).
      self.executeGame(newlogin.res["usrn"]); # Execute the game if the login attempt was successful. We pass in the username into the game object.
      exit();
    

  
  def executeGame(self, usrn):
    newmenu = mainMenu(self.IsDev, usrn); # Instantiating a new main menu.
    newmenu.menuStart(); # Starting the menu.
    # The `newmenu.type` attribute refers to which button the user clicked ("create game" or "load game").
    if(newmenu.type == "create"):
      newgame = game(int(newmenu.Lives), newmenu.cooldowns, newmenu.difficulty, self.IsDev, usrn); # Instantiating a new game object.
      # Initializing the new game:
      newgame.GameID = newgame.generateGameID();
      newgame.createSprites();
      newgame.makeAliens();
      newgame.makeBarriers();
      newgame.saveGame();
      newgame.gameLoop();

    elif(newmenu.type == "load"):
      newgame = game(0, {"alien": 0, "player": 0, "AlienBulletsMax": 0}, "easy", self.IsDev, usrn);
      newgame.createSprites();
      newgame.load(newmenu.GameID); # Loading the game.
      newgame.makeAliens();
      newgame.makeBarriers();
      newgame.saveGame();
      newgame.gameLoop();

if(__name__ == "__main__"):
  IsDev = sys.argv[1]; # During execution via CLI (`python main.py`) the developer can pass in an arguement to signify that they are a developer.
  MainObj = Main(IsDev);
  MainObj.main();
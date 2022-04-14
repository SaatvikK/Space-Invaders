############ IMPORTS ############
# Classes
from game import game;
from LoginMenu_v2 import loginMenu;
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
    else:
      newlogin = loginMenu(); # Instantiate a new login menu.
      newlogin.menu(); # Execute the menu method to display the login menu.
      
if(__name__ == "__main__"):
  IsDev = sys.argv[1]; # During execution via CLI (`python main.py`) the developer can pass in an arguement to signify that they are a developer.
  MainObj = Main(IsDev);
  MainObj.main();
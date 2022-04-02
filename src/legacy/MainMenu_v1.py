############ IMPORTS ############
# Libraries
import tkinter as tk;
from tkinter import *;
from tkinter import font as tkFont;
import tkinter.filedialog;
import os;
import json;

# Other Modules
from mergesort import *; # Importing my merge sort algorithm
#################################

# Class for the main menu.
class mainMenu:
  def __init__(self, IsDev, usrn) -> None:
    self.usrn = usrn;
    self.IsDev = IsDev;
    self.window = tk.Tk();
    self.window.attributes("-fullscreen", True)

    # Getting the width and height of the monitor using tkinter, so that the main menu can be dynamic.
    self.ScreenWidth, self.ScreenHeight = self.window.winfo_screenwidth(), self.window.winfo_screenheight();
    print(self.ScreenWidth, "x", self.ScreenHeight)
    self.window.title("Space Invaders: Main Menu");
    self.window.iconbitmap(); #Icon for window
    self.ButtonFont = tkFont.Font(family='Georgia', size=20, weight='bold');
    return None;
  
  def backgroundDisplay(self):
    # Creating the background
    self.bg = tk.PhotoImage(file = "../assets/bg.png");
    OpenImg = tk.Label(self.window, image = self.bg);
    OpenImg.place(x = 0, y = 0, relwidth = 1, relheight = 1);
  
  def menuStart(self) -> None:
    def backgroundDisplay():
      self.bg = tk.PhotoImage(file = "../assets/bg.png");
      OpenImg = tk.Label(self.window, image = self.bg);
      OpenImg.place(x = 0, y = 0, relwidth = 1, relheight = 1);
    
    def menuButtons():
      # "New Game" Button
      NewGame = tk.Button(self.window, text = "New Game", command = lambda: self.newGame(), height = 1, width = 10, font = self.ButtonFont);
      NewGame.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 - 40);
      
      # "Load Game" Button
      LoadGame = tk.Button(self.window, text = "Load Game", command = lambda: self.loadGame(), height = 1, width = 10, font = self.ButtonFont);
      LoadGame.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 + 40);

      # "Stats Page" Button
      StatsPageButton = tk.Button(self.window, text = "Your Stats", command = lambda: self.statsPage(), height = 1, width = 10, font = self.ButtonFont);
      StatsPageButton.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 + 120)

      Exit = tk.Button(self.window, text = "Exit App", command = lambda: self.exitApp(), height = 1, width = 10, font = self.ButtonFont);
      Exit.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 + 200);

    backgroundDisplay();
    menuButtons();
    self.window.mainloop();
  
  def statsPage(self):
    # Getting the stats of each game that THIS player has played.
    def readStats(games: list) -> dict: # "games" is a list of GameIDs owned by the currently logged in user.
      stats = [];
      for i in range(len(games)): # Iterating through the list.
        with open("../database/" + str(games[i]) + "/settings/player.json", "r") as file: # Opening settings/player.json
          data = json.load(file);
          if(data["username"] == self.usrn): # Checking if the game that is currently being looked at is owned by the user.

            # If the game is owned bt the user, we grab the score and the wave number from the database:
            with open("../database/" + str(games[i]) + "/stats/score.json", "r") as statsfile1: # Opening stats/score.json
              data1 = json.load(statsfile1);

              with open("../database/" + str(games[i]) + "/stats/wave.json", "r") as statsfile2: # Opening stats/wave.json
                data2 = json.load(statsfile2);
                stats.append({ # Creating a dicttionary for THIS game and appending it to the stats[] array. 
                  "score": data1["score"], 
                  "wave": data2["wave"],
                  "id": games[i]
                });
                # The format of the stats[] array is as follows:
                # stats = [{
                #   "score":,
                #   "wave":,
                #   "id":
                #  },
                #  {
                #  ...
                #  }
                #];
      return stats;


    for widget in self.window.winfo_children(): # Destroying everything on the screen (so that it is blank).
      widget.destroy();
    
    self.backgroundDisplay();

    title = tk.Label(self.window, text = "Your Stats", font = tkFont.Font(family = "Georgia", size = 20, weight = "bold", slant = "italic"));
    title.place(x = 0, y = 0);

    games = self.checkIfGameOwnedByCurrentUser(os.listdir("../database/")); # Getting all the games owned by the user.
    stats = readStats(games);

    # Merge sorting the AllScores list. `driverMethod()` is the driver code that initialises the mergeSort algorithm.
    # A merge sort was used over a bubble sort algorithm as it can complete a sort operation in O(n log n) time (worst case performance).
    # This is far better than a bubble sort's O(n^2) time.
    stats = driverMethod(stats);
    for i in range(len(stats)): # Iterating through the newly-sorted stats list.
      # Printing out the stats for the game.
      boop = tk.Label(
        self.window, 
        text = 
          str(i + 1) + 
          ") Game: " + 
          str(stats[i]["id"]) + 
          ", Score: " + 
          str(stats[i]["score"]) + 
          ", Wave: " + 
          str(stats[i]["wave"]
        ),
        font = tkFont.Font(family = "Georgia", size = 15, weight = "bold")
      );
      if(i == 0): boop.place(x = 50, y = 100);
      else: boop.place(x = 50, y = i*150);

    return;
  
  def newGame(self): # This method is called if the user clicks the "New Game" button.
    self.window.title("Space Invaders: New Game");
    # Destroy everything on the screen (i.e. the main menu)
    for widget in self.window.winfo_children():
      widget.destroy();
    
    self.backgroundDisplay();

    ## Lives settings
    title = tk.Label(self.window, text = "Lives:", font =  tkFont.Font(family = "Georgia", size = 20, weight = "bold", slant = "italic"));
    title.place(x = 0, y = 0);

    Lives = tk.StringVar(self.window); Lives.set("Select amount of lives");
    LivesMenu = tk.OptionMenu(self.window, Lives, *["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]) 
    LivesMenu.place(x = 50, y= 100);

    ## Difficulty settings
    title = tk.Label(self.window, text = "Difficulty:", font =  tkFont.Font(family = "Georgia", size = 20, weight = "bold", slant = "italic"));
    title.place(x = 0, y = 150);

    difficulty = tk.StringVar(self.window); difficulty.set("Select difficulty.")
    DiffMenu = tk.OptionMenu(self.window, difficulty, *["Hard", "Medium", "Easy", "Casual/Normal"]);
    DiffMenu.place(x = 50, y = 200);

    def beginGame(): # Executed when the user finishes adjusting the new game's settings and clicks "Create Game".
      self.type = "create";
      print("Beginning game", Lives.get())
      self.Lives = int(Lives.get());
      print(difficulty.get())
      self.difficulty = difficulty.get();
      # Creating dictionaries of various cooldowns and thresholds for the player and aliens depending on what difficulty the user chose.
      # This dictionary will be passed into the game object when it is created in `main.py`.
      if(difficulty.get() == "Hard"): self.cooldowns = {"alien": 100, "player": 1000, "AlienBulletsMax": 20};
      elif(difficulty.get() == "Medium"): self.cooldowns = {"alien": 300, "player": 500, "AlienBulletsMax": 7};
      elif(difficulty.get() == "Easy"): self.cooldowns = {"alien": 3000, "player": 100, "AlienBulletsMax": 3};
      elif(difficulty.get() == "Casual/Normal"): self.cooldowns = {"alien": 1000, "player": 500, "AlienBulletsMax": 5};
      self.window.destroy();
      

    SubmitButton = tk.Button(self.window, text = "Create Game", command = beginGame);
    SubmitButton.place(x = 5, y = 1000);

  # This method returns all the games owned by the currently logged in user given a list of Game IDs.
  def checkIfGameOwnedByCurrentUser(self, games: list) -> list:
    OwnedGames = [];
    for i in range(len(games)):
      with open("../database/" + str(games[i]) + "/settings/user.json", "r") as file:
        data = json.load(file);
        if(data["username"] == self.usrn):
          OwnedGames.append(games[i]);
    return OwnedGames;

  def loadGame(self): # Executed if the user clicks "Load Game" in the main menu.
    # opening load-game menu
    self.window.title("Space Invaders: Load a Game");
    # Destroy everything on the screen (i.e. the main menu)
    for widget in self.window.winfo_children():
      widget.destroy();

    self.backgroundDisplay();
    # Getting all the games owned by the user so that they can be listed on the screen.
    games = self.checkIfGameOwnedByCurrentUser(os.listdir("../database/"));
    
    ## Games
    title = tk.Label(self.window, text = "Load a Game", font =  tkFont.Font(family = "Georgia", size = 20, weight = "bold", slant = "italic"));
    title.place(x = 0, y = 0);
    GamesDropDown = tk.StringVar(self.window); GamesDropDown.set("Select a game...");
    GamesMenu = tk.OptionMenu(self.window, GamesDropDown, *games);
    GamesMenu.place(x = 50, y= 100);

    def beginGame():
      self.type = "load";
      self.GameID = GamesDropDown.get();
      self.window.destroy();
    
    # Once the user chooses a game, we load it from the latest saved state.
    SubmitButton = tk.Button(self.window, text = "Create Game", command = beginGame);
    SubmitButton.place(x = 5, y = 1000);
    
  def exitApp(self): exit();

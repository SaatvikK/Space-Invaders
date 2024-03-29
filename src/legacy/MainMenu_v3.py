############ IMPORTS ############
# Libraries
#from locale import textdomain
import shutil
import tkinter as tk;
from tkinter import *;
from tkinter import font as tkFont;
import tkinter.filedialog;
import os;
import json;
import requests as req; 
from tkinter import ttk;

# Other Modules
from mergesort import *; # Importing my merge sort algorithm
#################################

# Class for the main menu.
class mainMenu:
  def __init__(self, IsDev, usrn) -> None:
    self.usrn = usrn;
    self.IsDev = IsDev;
    self.window = tk.Tk();
    self.window.attributes("-fullscreen", True);
    self.stack = [];

    # Getting the width and height of the monitor using tkinter, so that the main menu can be dynamic.
    self.ScreenWidth, self.ScreenHeight = self.window.winfo_screenwidth(), self.window.winfo_screenheight();
    print(self.ScreenWidth, "x", self.ScreenHeight)
    self.window.title("Space Invaders: Main Menu");
    self.window.iconbitmap(); #Icon for window
    self.ButtonFont = tkFont.Font(family='Georgia', size=20, weight='bold');
    return None;
  
  def goBack(self):
    print(self.stack)
    self.stack.pop(len(self.stack) - 1);
    LastPage = self.stack[len(self.stack) - 1];

    # This is a method to 
    pages = { "NewGame": self.newGame, "MainMenu": self.menuStart, "LoadGame": self.loadGame, "StatsPage": self.statsPage, "ExitApp": self.exitApp };
    pages[LastPage]();

  def backgroundDisplay(self):
    # Creating the background
    self.bg = tk.PhotoImage(file = "../assets/bg.png");
    OpenImg = tk.Label(self.window, image = self.bg);
    OpenImg.place(x = 0, y = 0, relwidth = 1, relheight = 1);
  
  def menuStart(self) -> None:
    if("MainMenu" not in self.stack): self.stack.append("MainMenu");
    def backgroundDisplay():
      self.bg = tk.PhotoImage(file = "../assets/bg.png");
      OpenImg = tk.Label(self.window, image = self.bg);
      OpenImg.place(x = 0, y = 0, relwidth = 1, relheight = 1);
    
    def menuButtons():
      # "New Game" Button
      NewGame = tk.Button(self.window, text = "New Game", command = self.newGame, height = 1, width = 10, font = self.ButtonFont);
      NewGame.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 - 40);
      
      # "Load Game" Button
      LoadGame = tk.Button(self.window, text = "Load Game", command = self.loadGame, height = 1, width = 10, font = self.ButtonFont);
      LoadGame.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 + 40);

      # "Stats Page" Button
      StatsPageButton = tk.Button(self.window, text = "Your Stats", command = self.statsPage, height = 1, width = 10, font = self.ButtonFont);
      StatsPageButton.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 + 120)

      Exit = tk.Button(self.window, text = "Exit App", command = self.exitApp, height = 1, width = 10, font = self.ButtonFont);
      Exit.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 + 200);

    backgroundDisplay();
    menuButtons();
    self.window.mainloop();
  
  def statsPage(self):
    if("StatsPage" not in self.stack): self.stack.append("StatsPage");
    # Getting the stats of each game that THIS player has played.
    def readStats(games: list) -> dict: # "games" is a list of GameIDs owned by the currently logged in user.
      stats = [];
      for i in range(len(games)): # Iterating through the list.
        with open("../database/" + str(games[i]) + "/settings/meta.json", "r") as file: # Opening settings/player.json
          data = json.load(file);
          if(data["username"] == self.usrn): # Checking if the game that is currently being looked at is owned by the user.

            # If the game is owned bt the user, we grab the score and the wave number from the database:
            with open("../database/" + str(games[i]) + "/stats/score.json", "r") as statsfile1: # Opening stats/score.json
              data1 = json.load(statsfile1);

              with open("../database/" + str(games[i]) + "/stats/wave.json", "r") as statsfile2: # Opening stats/wave.json
                data2 = json.load(statsfile2);
                stats.append([ # Creating an array for THIS game and appending it to the stats[] array. 
                  games[i], # GameID
                  data1["value"], # score
                  data2["value"], # wave
                  data["created"]["date"] + " @ " + data["created"]["time"], # Created
                  data["LastPlayed"]["date"] + " @ " + data["LastPlayed"]["time"] # Last Played
                ]); # This has to be an array (not a dictionary) because TreeView only uses arrays - not dictionaries.
      return stats;

    for widget in self.window.winfo_children(): # Destroying everything on the screen (so that it is blank).
      widget.destroy();
    
    self.backgroundDisplay();

    title = tk.Label(self.window, text = "Your Stats", font = tkFont.Font(family = "Georgia", size = 20, weight = "bold", slant = "italic"));
    title.place(x = 0, y = 0);

    ## Back Button
    BackButton = tk.Button(self.window, text = "Back", command = self.goBack, height = 1, width = 10, font = self.ButtonFont);
    BackButton.place(x = 5, y = 900);

    games = self.checkIfGameOwnedByCurrentUser(os.listdir("../database/")); # Getting all the games owned by the user.
    stats = readStats(games);

    # Merge sorting the AllScores list. `driverMethod()` is the driver code that initialises the mergeSort algorithm.
    # A merge sort was used over a bubble sort algorithm as it can complete a sort operation in O(n log n) time (worst case performance).
    # This is far better than a bubble sort's O(n^2) time.
    stats = driverMethod(stats);

    tree = ttk.Treeview(self.window, columns = ["id", "score", "wave", "created", "LastPlayed"], show = "headings");
    tree.heading("id", text = "Game ID"); tree.heading("score", text = "Score"); 
    tree.heading("wave", text = "Wave"); tree.heading("created", text = "Created"); 
    tree.heading("LastPlayed", text = "Last Played");

    for row in stats:
      print(row)
      tree.insert("", tk.END, values = row);
    
    tree.bind("<<TreeviewSelect>>")
    tree.place(x = 100, y = 200);

    return;
  
  def newGame(self): # This method is called if the user clicks the "New Game" button.
    self.window.title("Space Invaders: New Game");
    if("NewGame" not in self.stack): self.stack.append("NewGame");
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

    ## Back Button
    BackButton = tk.Button(self.window, text = "Back", command = self.goBack, height = 1, width = 10, font = self.ButtonFont);
    BackButton.place(x = 5, y = self.ScreenHeight - 500);

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
    SubmitButton.place(x = 5, y = self.ScreenHeight - 200);

  # This method returns all the games owned by the currently logged in user given a list of Game IDs.
  def checkIfGameOwnedByCurrentUser(self, games: list) -> list:
    OwnedGames = [];
    for i in range(len(games)):
      with open("../database/" + str(games[i]) + "/settings/meta.json", "r") as file:
        data = json.load(file);
        if(data["username"] == self.usrn):
          OwnedGames.append(games[i]);
    return OwnedGames;

  def loadGame(self): # Executed if the user clicks "Load Game" in the main menu.
    if("LoadGame" not in self.stack): self.stack.append("LoadGame");
    def beginGame(event):
      self.type = "load";
      for item in tree.selection():
        ThisItem = tree.item(item);
        self.GameID = ThisItem["values"][0];
      self.window.destroy();
      
    # opening load-game menu
    self.window.title("Space Invaders: Load a Game");
    # Destroy everything on the screen (i.e. the main menu)
    for widget in self.window.winfo_children():
      widget.destroy();

    self.backgroundDisplay();

    # Only display the load game option if there are any games in the database.
    if(len(os.listdir("../database/")) > 0):
      # Getting all the games owned by the user so that they can be listed on the screen.
      games = self.checkIfGameOwnedByCurrentUser(os.listdir("../database/"));

      ## Title
      title = tk.Label(self.window, text = "Load a Game", font =  tkFont.Font(family = "Georgia", size = 20, weight = "bold", slant = "italic"));
      title.place(x = 0, y = 0);
      

      DataToEnter = [];
      for i in range(len(games)):
        with open("../database/" + str(games[i]) + "/settings/meta.json") as file:
          data = json.load(file);
          created = data["created"]["date"] + " @ " + data["created"]["time"];
          LastPlayed = data["LastPlayed"]["date"] + " @ " + data["LastPlayed"]["time"];
          DataToEnter.append([games[i], created, LastPlayed, "LOAD GAME"]);

      tree = ttk.Treeview(self.window, columns = ["GameID", "Created", "Last Played", " "], show = "headings");
      tree.heading("GameID", text = "Game ID"); tree.heading("Created", text = "Created"); 
      tree.heading("Last Played", text = "Last Played"); tree.heading(" ", text = " ");

      for row in DataToEnter:
        print(row)
        tree.insert("", tk.END, values = row);
      
      tree.bind("<<TreeviewSelect>>", beginGame)
      tree.grid(row = 0, column = 0);

      ## Delete Button
      # We only display the delete button if there are any games in the DB. That way, we dont need to carry out the same check in mainMenu.deleteGame().
      DeleteButton = tk.Button(self.window, text = "Delete A Game", command = self.deleteGame, height = 1, width = 15, font = self.ButtonFont);
      DeleteButton.place(x = 5, y = self.ScreenHeight - 400);

    else: 
      text = tk.Label(self.window, text = "There are no games in the local database.", font =  tkFont.Font(family = "Georgia", size = 20, weight = "bold", slant = "italic"));
      text.place(x = self.ScreenWidth//2, y = self.ScreenHeight//2 - 100);

    ## Back Button
    BackButton = tk.Button(self.window, text = "Back", command = self.goBack, height = 1, width = 10, font = self.ButtonFont);
    BackButton.place(x = 5, y = self.ScreenHeight - 200);
    
  def deleteGame(self):
    if("DeleteGame" not in self.stack): self.stack.append("DeleteGame");
    # opening load-game menu
    self.window.title("Space Invaders: Delete a Game");
    # Destroy everything on the screen (i.e. the main menu)
    for widget in self.window.winfo_children():
      widget.destroy();

    def delete(event):
      self.type = "delete";
      game = None;
      for item in tree.selection():
        ThisItem = tree.item(item);
        game = ThisItem["values"][0];
      try: 
        shutil.rmtree("../database/" + str(game)); # Deleting the game from local db.
      except: pass;
      print("https://nea-rest-api.thesatisback.repl.co/NEA_API/v1/" + str(game))
      res = req.delete("https://nea-rest-api.thesatisback.repl.co/NEA_API/v1/" + str(game));
      print(res.json());
    self.backgroundDisplay();

    # Getting all the games owned by the user so that they can be listed on the screen.
    games = self.checkIfGameOwnedByCurrentUser(os.listdir("../database/"));

    ## Games
    title = tk.Label(self.window, text = "Delete a Game", font =  tkFont.Font(family = "Georgia", size = 20, weight = "bold", slant = "italic"));
    title.place(x = 0, y = 0);

    DataToEnter = [];
    for i in range(len(games)):
      with open("../database/" + str(games[i]) + "/settings/meta.json") as file:
        data = json.load(file);
        created = data["created"]["date"] + " @ " + data["created"]["time"];
        LastPlayed = data["LastPlayed"]["date"] + " @ " + data["LastPlayed"]["time"];
        DataToEnter.append([games[i], created, LastPlayed, "LOAD GAME"]);

    tree = ttk.Treeview(self.window, columns = ["GameID", "Created", "Last Played", " "], show = "headings");
    tree.heading("GameID", text = "Game ID"); tree.heading("Created", text = "Created"); 
    tree.heading("Last Played", text = "Last Played"); tree.heading(" ", text = " ");

    for row in DataToEnter:
      tree.insert("", tk.END, values = row);
    
    tree.bind("<<TreeviewSelect>>", delete)
    tree.grid(row = 0, column = 0);

    ## Back Button
    BackButton = tk.Button(self.window, text = "Back", command = self.goBack, height = 1, width = 10, font = self.ButtonFont);
    BackButton.place(x = 5, y = self.ScreenHeight - 200);


  def exitApp(self): exit();


n = mainMenu("dev", "admin");
n.menuStart()
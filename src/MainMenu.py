############ IMPORTS ############
# Libraries
import tkinter as tk;
from tkinter import *;
from tkinter import font as tkFont;
import tkinter.filedialog;
import os;
#################################

class mainMenu:
  def __init__(self) -> None:
    self.window = tk.Tk();
    self.ScreenWidth, self.ScreenHeight = self.window.winfo_screenwidth(), self.window.winfo_screenheight();
    self.window.title("Space Invaders: Main Menu");
    self.window.iconbitmap(); #Icon for window
    self.ButtonFont = tkFont.Font(family='Georgia', size=20, weight='bold');
    return None;
  
  def menuStart(self) -> None:
    def backgroundDisplay():
      self.bg = tk.PhotoImage(file = "../assets/bg.png");
      OpenImg = tk.Label(self.window, image = self.bg);
      OpenImg.place(x = 0, y = 0, relwidth = 1, relheight = 1);
    
    def menuButtons():
      NewGame = tk.Button(self.window, text = "New Game", command = lambda: self.newGame(), height = 1, width = 10, font = self.ButtonFont);
      NewGame.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 - 40);

      LoadGame = tk.Button(self.window, text = "Load Game", command = lambda: self.loadGame(), height = 1, width = 10, font = self.ButtonFont);
      LoadGame.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 + 40);

      Exit = tk.Button(self.window, text = "Exit App", command = lambda: self.exitApp(), height = 1, width = 10, font = self.ButtonFont);
      Exit.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 + 120);
  

    backgroundDisplay();
    menuButtons();
    self.window.mainloop();
  
  def newGame(self):
    self.window.title("Space Invaders: New Game");
    # Destroy everything on the screen (i.e. the main menu)
    for widget in self.window.winfo_children():
      widget.destroy();
    
    # Creating the background
    self.bg = tk.PhotoImage(file = "../assets/bg.png");
    OpenImg = tk.Label(self.window, image = self.bg);
    OpenImg.place(x = 0, y = 0, relwidth = 1, relheight = 1);

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

    def beginGame():
      self.type = "create";
      print("Beginning game", Lives.get())
      self.Lives = int(Lives.get());
      print(difficulty.get())
      self.difficulty = difficulty.get();
      if(difficulty.get() == "Hard"): self.cooldowns = {"alien": 100, "player": 1000, "AlienBulletsMax": 20};
      elif(difficulty.get() == "Medium"): self.cooldowns = {"alien": 300, "player": 500, "AlienBulletsMax": 7};
      elif(difficulty.get() == "Easy"): self.cooldowns = {"alien": 3000, "player": 100, "AlienBulletsMax": 3};
      elif(difficulty.get() == "Casual/Normal"): self.cooldowns = {"alien": 1000, "player": 500, "AlienBulletsMax": 5};
      self.window.destroy();
      

    SubmitButton = tk.Button(self.window, text = "Create Game", command = beginGame);
    SubmitButton.place(x = 5, y = 1000);

    #print("hihihihihi", AmountPlayers.get())
    #return int(AmountPlayers.get()[0]);

  def loadGame(self):
    # opening load-game menu
    self.window.title("Space Invaders: Load a Game");
    # Destroy everything on the screen (i.e. the main menu)
    for widget in self.window.winfo_children():
      widget.destroy();
    
    # Creating the background
    self.bg = tk.PhotoImage(file = "../assets/bg.png");
    OpenImg = tk.Label(self.window, image = self.bg);
    OpenImg.place(x = 0, y = 0, relwidth = 1, relheight = 1);

    games = os.listdir("../database");

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
      
    SubmitButton = tk.Button(self.window, text = "Create Game", command = beginGame);
    SubmitButton.place(x = 5, y = 1000);
    


  def exitApp(self): exit();
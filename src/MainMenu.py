############ IMPORTS ############
# Libraries
import tkinter as tk;
from tkinter import *;
from tkinter import font as tkFont;
import tkinter.filedialog;
import PIL as pil;
from PIL import ImageTk, Image;
import glob;
import json;

# Classes
from game import game;
#################################

class mainMenu:
  def __init__(self) -> None:
    self.window = tk.Tk();
    self.ScreenWidth, self.ScreenHeight = self.window.winfo_screenwidth(), self.window.winfo_screenheight();
    self.window.title("CATAN: Main Menu");
    self.window.iconbitmap(); #Icon for window
    self.ButtonFont = tkFont.Font(family='Georgia', size=20, weight='bold');
    self.AmountPlayers = 0;
    return None;
  
  def menuStart(self) -> None:
    def backgroundDisplay():
      self.bg = tk.PhotoImage(file = "../resources/MainMenuBG.png");
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
    self.window.title("CATAN: Create a New Game");
    # Destroy everything on the screen (i.e. the main menu)
    for widget in self.window.winfo_children():
      widget.destroy();
    
    # Creating the background
    self.bg = tk.PhotoImage(file = "../resources/NewGameSettingsBG.png");
    OpenImg = tk.Label(self.window, image = self.bg);
    OpenImg.place(x = 0, y = 0, relwidth = 1, relheight = 1);

    title = tk.Label(self.window, text = "How many players will there be?", font =  tkFont.Font(family = "Georgia", size = 20, weight = "bold", slant = "italic"));
    title.place(x = 0, y = 0);

    AmountPlayers = tk.StringVar(self.window); AmountPlayers.set("Select amount of players");

    PlayersMenu = tk.OptionMenu(self.window, AmountPlayers, *["2 Players", "3 Players", "4 Players"]) 
    PlayersMenu.place(x = 50, y= 100);

    def beginGame():
      print("Beginning game", AmountPlayers.get())
      self.AmountPlayers = int(AmountPlayers.get()[0]);
      self.window.destroy();
      

    SubmitButton = tk.Button(self.window, text = "Submit", command = beginGame);
    SubmitButton.place(x = 5, y = 110);

    #print("hihihihihi", AmountPlayers.get())
    #return int(AmountPlayers.get()[0]);

  def loadGame(self):
    # opening load-game menu
    pass;

  def exitApp(self): exit();
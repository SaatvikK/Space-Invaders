############ IMPORTS ############
# Libraries
from ast import arg
from typing import Dict
import random as rand;
import tkinter
from tkinter import *;
from tkinter import font as tkFont;
import customtkinter as ctk;
import hashlib as hashes;
import requests as req;
import sys;
import json;
import os; 
import numpy as np;
import shutil;

#from main import MainObj;
from game import game;
#################################


ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class mainMenu(ctk.CTk):
  def __init__(self, usrn) -> None:
    super().__init__();
    self.usrn = usrn;
    self.stack = [];
    self.window = ctk.CTk();
    # Getting the width and height of the monitor using tkinter, so that the main menu can be dynamic.
    self.ScreenWidth, self.ScreenHeight = self.window.winfo_screenwidth(), self.window.winfo_screenheight();
    print(self.ScreenWidth, "x", self.ScreenHeight);

    return None;
  
  def errorPopUp(self, msg: str):
    ErrorWindow = ctk.CTkToplevel(self.window);
    ErrorLabel = ctk.CTkLabel(master = ErrorWindow, text = msg);
    ErrorLabel.place(relx = 0.5, rely = 0.5, anchor = "center");       

  def goBack(self):
    print(self.stack)
    self.stack.pop(len(self.stack) - 1);
    LastPage = self.stack[len(self.stack) - 1];

    # This is a method to 
    pages = { "NewGame": self.newGame, "MainMenu": self.menuStart, "LoadGame": self.loadGame, "StatsPage": self.statsPage };
    pages[LastPage]();

  def menuStart(self):
    for widget in self.window.winfo_children():
      widget.destroy();
    if("MainMenu" not in self.stack): self.stack.append("MainMenu");
    TitleLabel = ctk.CTkLabel(master = self.window, text = "Space Invaders", text_font=("Roboto", -40, "bold"));
    TitleLabel.place(relx = 0.5, rely = 0.2, anchor = "center");
    
    def menuButtons():
      NewGameButton = ctk.CTkButton(master = self.window, text = "New Game", command = self.newGame);
      NewGameButton.place(relx = 0.5, rely = 0.3, anchor = "center");

      LoadGameButton = ctk.CTkButton(master = self.window, text = "Load Game", command = self.loadGame);
      LoadGameButton.place(relx = 0.5, rely = 0.35, anchor = "center");

      StatsPageButton = ctk.CTkButton(master = self.window, text = "Your Stats", command = self.statsPage);
      StatsPageButton.place(relx = 0.5, rely = 0.4, anchor = "center");

      ExitButton = ctk.CTkButton(master = self.window, text = "Exit App", command = lambda: exit());
      ExitButton.place(relx = 0.5, rely = 0.45, anchor = "center");

    def leftframe():
      # configure grid layout (1x2)
      self.grid_columnconfigure(1, weight=1)
      self.rowconfigure(0, weight=1)
      # configure grid layout
      self.window.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
      self.window.grid_rowconfigure(5, weight=1)  # empty row as spacing
      self.window.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
      self.window.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing
    
    leftframe()
    menuButtons();
    self.window.mainloop();

  def newGame(self):
    for widget in self.window.winfo_children():
      widget.destroy();
    if("NewGame" not in self.stack): self.stack.append("NewGame");
    self.type = "create";
    print("new game")

    TitleLabel = ctk.CTkLabel(master = self.window, text = "Game Setup Menu", text_font=("Roboto", -40, "bold"));
    TitleLabel.place(relx = 0.5, rely = 0.2, anchor = "center");

    ## DIFFICULTY
    def setDiff(diff): self.difficulty = diff;
    self.difficulty = None; # Final chosen difficulty.

    self.DiffLabel = ctk.CTkLabel(master = self.window, text = "Choose a Difficulty:", text_font = ("Roboto", -14, "bold"));
    self.DiffLabel.place(relx = 0.4, rely = 0.3, anchor = "center");
    
    self.radio_var = tkinter.IntVar(value=0)
    self.DiffEasy = ctk.CTkRadioButton(master = self.window, value = 0, command = lambda: setDiff("Easy"), text = "Easy", variable = self.radio_var);
    self.DiffEasy.place(relx = 0.385, rely = 0.35, anchor = "center");
    self.DiffCasual = ctk.CTkRadioButton(master = self.window, value = 1, command = lambda: setDiff("Casual/Normal"), text = "Casual/Normal", variable = self.radio_var);
    self.DiffCasual.place(relx = 0.4, rely = 0.4, anchor = "center");
    self.DiffMedium = ctk.CTkRadioButton(master = self.window, value = 2, command = lambda: setDiff("Medium"), text = "Medium", variable = self.radio_var);
    self.DiffMedium.place(relx = 0.39, rely = 0.45, anchor = "center");
    self.DiffHard = ctk.CTkRadioButton(master = self.window, value = 3, command = lambda: setDiff("Hard"), text = "Hard", variable = self.radio_var);
    self.DiffHard.place(relx = 0.385, rely = 0.5, anchor = "center");

    ## Lives
    self.lives = None;
    def setLives(value): self.lives = value;
    self.LivesLabel = ctk.CTkLabel(master = self.window, text = "How many lives would you like?", text_font = ("Roboto", -14, "bold"));
    self.LivesLabel.place(relx = 0.6, rely = 0.3, anchor = "center");
    self.slider = ctk.CTkSlider(master = self.window, from_ = 0, to = 10, number_of_steps = 10, command = setLives)
    self.slider.place(relx = 0.6, rely = 0.32, anchor = "center");

    ## Start Game BUtton
    def startGame():
      if(self.difficulty != None and self.lives != None):
        cooldowns = {
          "Hard":          {"alien": 100, "player": 1000, "AlienBulletsMax": 20},
          "Medium":        {"alien": 300, "player": 500, "AlienBulletsMax": 7},
          "Easy":          {"alien": 3000, "player": 100, "AlienBulletsMax": 3},
          "Casual/Normal": {"alien": 1000, "player": 500, "AlienBulletsMax": 5}
        }
        self.cooldowns = cooldowns[self.difficulty];
        self.executeGame();
      else:
        self.errorPopUp("You must choose BOTH a difficulty AND an amount of lives.");

    StartGameButton = ctk.CTkButton(master = self.window, text = "Start Game", command = startGame);
    StartGameButton.place(relx = 0.6, rely = 0.4, anchor = "center");

    ## Back Button
    BackButton = ctk.CTkButton(master = self.window, text = "Go Back", command = self.goBack);
    BackButton.place(relx = 0.6, rely = 0.45, anchor = "center");
    
  def loadGame(self):
    self.type = "load";
    for widget in self.window.winfo_children():
      widget.destroy();
    if("LoadGame" not in self.stack): self.stack.append("LoadGame"); 
    print("load game")

    ## Title
    TitleLabel = ctk.CTkLabel(master = self.window, text = "Load a Game", text_font=("Roboto", -40, "bold"));
    TitleLabel.place(relx = 0.5, rely = 0.2, anchor = "center");

    # Only display the load game option if there are any games in the database.
    DataToEnter = [];
    if(len(os.listdir("../database/")) > 0):
      # Getting all the games owned by the user so that they can be listed on the screen.
      games = self.checkIfGameOwnedByCurrentUser(os.listdir("../database/"));

      for i in range(len(games)):
        with open("../database/" + str(games[i]) + "/settings/meta.json") as file:
          data = json.load(file);
          created = data["created"]["date"] + " @ " + data["created"]["time"];
          LastPlayed = data["LastPlayed"]["date"] + " @ " + data["LastPlayed"]["time"];
          DataToEnter.append({ "ID": games[i], "created": created, "LastPlayed": LastPlayed });


    ## BUTTONS
    def sigmoid(x: int) -> float:
      denominator = 1 + np.exp(-x);
      return 1/denominator;

    self.radio_var = tkinter.IntVar(value=0);
    self.GameID = None;
    def putID(): self.GameID = DataToEnter[i]["ID"];

    for i in range(len(DataToEnter)):
      y = np.abs(sigmoid(i)) - 0.1;
      if(i != 0): y -= 0.3;
      print(DataToEnter[i])
      print(y)
      string = "Game " + str(DataToEnter[i]["ID"]) + " was CREATED on " + DataToEnter[i]["created"] + " and LAST PALYED on " + DataToEnter[i]["LastPlayed"]; 
      button = ctk.CTkRadioButton(master = self.window, value = i, command = lambda: putID(), text = string, variable = self.radio_var);
      button.place(relx = 0.5, rely = y, anchor = "center");

    def loadAGame():
      if(self.GameID != None):
        self.executeGame();
      else:
        self.errorPopUp("You must select a game to load.");    

    def deleteAGAme():
      if(self.GameID != None):
        try: 
          shutil.rmtree("../database/" + str(self.GameID)); # Deleting the game from local db.
        except: pass;
        print("https://nea-rest-api.thesatisback.repl.co/NEA_API/v1/" + str(self.GameID))
        res = req.delete("https://nea-rest-api.thesatisback.repl.co/NEA_API/v1/" + str(self.GameID));
        self.errorPopUp("Game successfully deleted.");
      else:
        self.errorPopUp("You must select a game to delete.");

    ## Load Game Button
    LoadGameButton = ctk.CTkButton(master = self.window, text = "Load This Game", command = loadAGame);
    LoadGameButton.place(relx = 0.7, rely = 0.3, anchor = "center");

    ## Delete Game Button
    DeleteGameButton = ctk.CTkButton(master = self.window, text = "Delete This Game", command = deleteAGAme);
    DeleteGameButton.place(relx = 0.7, rely = 0.35, anchor = "center");

    ## Back Button
    BackButton = ctk.CTkButton(master = self.window, text = "Go Back", command = self.goBack);
    BackButton.place(relx = 0.7, rely = 0.4, anchor = "center");

  def statsPage(self): 
    if("StatsPage" not in self.stack): self.stack.append("StatsPage");
    print("stats page")
  
  def executeGame(self):
    # The `self.type` attribute refers to which button the user clicked ("create game" or "load game").
    if(self.type == "create"):
      newgame = game(int(self.lives), self.cooldowns, self.difficulty, self.usrn); # Instantiating a new game object.
      # Initializing the new game:
      newgame.GameID = newgame.generateGameID();
      newgame.createSprites();
      newgame.makeAliens();
      newgame.makeBarriers();
      newgame.saveGame();
      newgame.gameLoop();

    elif(self.type == "load"):
      newgame = game(0, {"alien": 0, "player": 0, "AlienBulletsMax": 0}, "easy", self.usrn);
      newgame.createSprites();
      newgame.load(self.GameID); # Loading the game.
      newgame.makeAliens();
      newgame.makeBarriers();
      newgame.saveGame();
      newgame.gameLoop();

  # This method returns all the games owned by the currently logged in user given a list of Game IDs.
  def checkIfGameOwnedByCurrentUser(self, games: list) -> list:
    OwnedGames = [];
    for i in range(len(games)):
      with open("../database/" + str(games[i]) + "/settings/meta.json", "r") as file:
        data = json.load(file);
        if(data["username"] == self.usrn):
          OwnedGames.append(games[i]);
    return OwnedGames;


n = mainMenu("admin")
n.menuStart()

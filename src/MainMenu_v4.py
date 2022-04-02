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

#from main import MainObj;
from game import game;
#################################


ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class mainMenu(ctk.CTk):
  def __init__(self, usrn) -> None:
    super().__init__();
    self.usrn = usrn;
    self.window = ctk.CTk();
    # Getting the width and height of the monitor using tkinter, so that the main menu can be dynamic.
    self.ScreenWidth, self.ScreenHeight = self.window.winfo_screenwidth(), self.window.winfo_screenheight();
    print(self.ScreenWidth, "x", self.ScreenHeight);

    return None;

  def menuStart(self):
    TitleLabel = ctk.CTkLabel(master = self.window, text = "Space Invaders", text_font=("Roboto", -40, "bold"));
    TitleLabel.place(relx = 0.5, rely = 0.2, anchor = "center");

    NewGameButton = ctk.CTkButton(master = self.window, text = "New Game", command = self.newGame);
    NewGameButton.place(relx = 0.5, rely = 0.3, anchor = "center");

    LoadGameButton = ctk.CTkButton(master = self.window, text = "Load Game", command = self.loadGame);
    LoadGameButton.place(relx = 0.5, rely = 0.35, anchor = "center");

    StatsPageButton = ctk.CTkButton(master = self.window, text = "Your Stats", command = self.statsPage);
    StatsPageButton.place(relx = 0.5, rely = 0.4, anchor = "center");

    ExitButton = ctk.CTkButton(master = self.window, text = "Exit App", command = lambda: exit());
    ExitButton.place(relx = 0.5, rely = 0.45, anchor = "center");

    self.window.mainloop();

  def newGame(self): 
    print("new game")
    for widget in self.window.winfo_children():
      widget.destroy();
    TitleLabel = ctk.CTkLabel(master = self.window, text = "Game Setup Menu", text_font=("Roboto", -40, "bold"));
    TitleLabel.place(relx = 0.5, rely = 0.2, anchor = "center");

    ## DIFFICULTY
    def diffChange(value):
      diffs = ["Easy", "Casual/Normal", "Medium", "Hard"];

      if(value == 1.0): value = 3
      elif(value == 0.33333333333333337): value = 1;
      elif(value == 0.6666666666666667): value = 2;
      print(value)
      print(diffs[int(value)])
      self.DiffText.set(diffs[int(value)]);

    self.DiffText = tkinter.StringVar();
    self.DiffText.set("Current Difficulty: " + "None");
    DiffLabel = ctk.CTkLabel(master = self.window, textvariable = self.DiffText);
    DiffLabel.place(relx = 0.5, rely = 0.5, anchor = "center");

    DiffSlider = ctk.CTkSlider(master = self.window, from_=0, to=1, number_of_steps = 3, command = diffChange)
    DiffSlider.place(relx = 0.5, rely = 0.6, anchor = "center");

  def loadGame(self): 
    print("load game")
  def statsPage(self): 
    print("stats page")



n = mainMenu("admin")
n.menuStart()

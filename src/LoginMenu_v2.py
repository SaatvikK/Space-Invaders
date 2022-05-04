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
from MainMenu_v4 import mainMenu;
#################################


ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class loginMenu(ctk.CTk):
  def __init__(self) -> None:
    super().__init__();
    self.window = ctk.CTk();
    # Getting the width and height of the monitor using tkinter, so that the main menu can be dynamic.
    self.ScreenWidth, self.ScreenHeight = self.window.winfo_screenwidth(), self.window.winfo_screenheight();
    print(self.ScreenWidth, "x", self.ScreenHeight);
    return None;

  def loginRegisterPopup(self, msg):
    ErrorWindow = ctk.CTkToplevel(self.window);
    ErrorLabel = ctk.CTkLabel(master = ErrorWindow, text = msg);
    ErrorLabel.place(relx = 0.5, rely = 0.5, anchor = "center");


  def login(self, usrn: str, pwd: str) -> dict: #pwd = hashed password input
    BaseURL = "https://NEA-REST-API.thesatisback.repl.co/NEA_API/v1/"; # BaseURL of the API.
    
    self.res = req.get(BaseURL + "users/" + usrn + "/" + pwd).json(); # Making a GET request to the endpoint that identifies the resource that holds account data.
    # We can just return the result of this get request as we handle all the account verification and validation on the server side.
    # The server side checks if the two usernames and passwords are the same. If so, it responds success. Else, failure.

    if(self.res["result"] == True):
      print(self.res)
      self.loginRegisterPopup(self.res["reason"]);
      self.window.destroy();
      #MainObj.executeGame(usrn);
      self.executeMainMenu(usrn)
    else: self.loginRegisterPopup(self.res["reason"]);
    return;

  def register(self, usrn: str, pwd: str) -> dict: #pwd = hashed password input
    BaseURL = "https://NEA-REST-API.thesatisback.repl.co/NEA_API/v1/"; # BaseURL of the API.
    
    LoginAttempt = req.get(BaseURL + "users/" + usrn + "/" + pwd).json(); # Making a GET request to the endpoint that identifies the resource that holds account data.
    # We can just return the result of this get request as we handle all the account verification and validation on the server side.
    # The server side checks if the two usernames and passwords are the same. If so, it responds success. Else, failure.
    print(LoginAttempt)
    print("----------")
    if(LoginAttempt["reason"] == "Username incorrect."):
      print(usrn, pwd)
      self.res = req.post(BaseURL + "users/" + usrn + "/" + pwd).json();
      if(self.res["result"] == False): print(self.res);
      elif(self.res["result"] == True): print("Account created. Please login."); self.res["reason"] = "Account created. Please login.";
    else:
      self.res = {"result": False, "reason": "Account already exists.", "error": None, "data": None };
      print(self.res)
    
    self.loginRegisterPopup(self.res["reason"]);
    return;

  def menu(self):
    TitleLabel = ctk.CTkLabel(master = self.window, text = "Logging in or Registering?", text_font=("Roboto", -14, "bold"));
    TitleLabel.place(relx = 0.5, rely = 0.2, anchor = "center");


    UsernameEntry = ctk.CTkEntry(master = self.window, width = 120, placeholder_text = "<username>");
    PwdEntry = ctk.CTkEntry(master = self.window, width = 120, placeholder_text = "<password>");
    UsernameEntry.place(relx = 0.5, rely = 0.40, anchor = "center");
    PwdEntry.place(relx = 0.5, rely = 0.60, anchor = "center");

    
    LoginButton = ctk.CTkButton(master = self.window, text = "Login   ", height = 10, width = 5, command = lambda: self.login(UsernameEntry.get(), PwdEntry.get()));
    RegisterButton = ctk.CTkButton(master = self.window, text = "Register", height = 10, width = 5, command = lambda: self.register(UsernameEntry.get(), PwdEntry.get()));
    LoginButton.place(relx = 0.7, rely = 0.8, anchor = "center");
    RegisterButton.place(relx = 0.3, rely = 0.8, anchor = "center");
    
    self.window.mainloop();

  def executeMainMenu(self, usrn):
    newmenu = mainMenu(usrn); # Instantiating a new main menu.
    newmenu.menuStart(); # Starting the menu.

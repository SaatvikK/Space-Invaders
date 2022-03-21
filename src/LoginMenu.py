############ IMPORTS ############
# Libraries
from typing import Dict
from dotenv.main import dotenv_values
import random as rand;
import pymongo as mongo;
import dotenv as env;
import tkinter as tk;
from tkinter import *;
from tkinter import font as tkFont;
import hashlib as hashes;
import requests as req;
#################################

class loginMenu():
  def __init__(self) -> None:
    return None;

  def thisHash(self, text: str) -> str:
    SHAhash = hashes.new("sha512");
    SHAhash.update(text.encode("latin1")); # Encoding the input message into latin and then hashing it.
    return SHAhash.hexdigest(); # Returns the hexadecimal version of the hash value.

  def login(self, usrn: str, pwd: str) -> dict: #pwd = hashed password input
    BaseURL = "https://NEA-REST-API.thesatisback.repl.co/NEA_API/v1/"; # BaseURL of the API.
    
    LoginAttempt = req.get(BaseURL + "users/" + usrn + "/" + pwd).json(); # Making a GET request to the endpoint that identifies the resource that holds account data.
    # We can just return the result of this get request as we handle all the account verification and validation on the server side.
    # The server side checks if the two usernames and passwords are the same. If so, it responds success. Else, failure.
    return LoginAttempt;

  def signup(self, usrn: str, pwd: str) -> dict: #pwd = hashed password input
    BaseURL = "https://NEA-REST-API.thesatisback.repl.co/NEA_API/v1/"; # BaseURL of the API.
    
    LoginAttempt = req.post(BaseURL + "users/" + usrn + "/" + pwd).json(); # Making a GET request to the endpoint that identifies the resource that holds account data.
    # We can just return the result of this get request as we handle all the account verification and validation on the server side.
    # The server side checks if the two usernames and passwords are the same. If so, it responds success. Else, failure.
    print(LoginAttempt)
    print("----------")
    if(LoginAttempt["reason"] == "Password incorrect."):
      res = req.post(BaseURL + "/users/" + usrn + "/" + pwd).json();
      return res;
    else:
      return {"result": False, "reason": "Account already exists.", "error": None, "data": None };

  def menu(self):
    self.window = tk.Tk(); # Creating the tkinter window.
    self.ScreenWidth, self.ScreenHeight = self.window.winfo_screenwidth(), self.window.winfo_screenheight(); # Getting the monitor dimensions so that the screen can be dynamic.
    self.window.title("Space Invaders: Main Menu");
    self.window.iconbitmap(); #Icon for window
    self.ButtonFont = tkFont.Font(family='Georgia', size=20, weight='bold');

    def backgroundDisplay():
      self.bg = tk.PhotoImage(file = "../assets/bg.png");
      OpenImg = tk.Label(self.window, image = self.bg);
      OpenImg.place(x = 0, y = 0, relwidth = 1, relheight = 1);

    def execLogin():
      print("HIHIHII")
      usrn = self.UserInp.get(1.0, "end-1c"); # Getting the username from the text-box input.
      pwd = self.PwdInp.get(1.0, "end-1c"); # Getting the password from the text-box input.
      self.res = self.login(usrn, pwd);
      if(self.res["result"] == True):
        self.res["usrn"] = usrn # Adding the username to the result dictionary so that it can be read in Main.main().
        print(self.res)
        self.window.destroy();
      else:
        print(self.res);
      return;
    
    def execSignUp():
      usrn = self.UserInp.get(1.0, "end-1c");
      pwd = self.PwdInp.get(1.0, "end-1c");
      self.res = self.signup(usrn, pwd);
      if(self.res["result"] == False): print(self.res);
      elif(self.res["result"] == True): print("Account created. Please login.");
      return;
    
    def menuButtons():
      # "Login" Button
      login = tk.Button(self.window, text = "Login", command = lambda: execLogin(), height = 1, width = 10, font = self.ButtonFont);
      login.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 + 400);
      
      # "Signup" Button
      SignUp = tk.Button(self.window, text = "Sign Up", command = lambda: execSignUp(), height = 1, width = 10, font = self.ButtonFont);
      SignUp.place(x = self.ScreenWidth/2 - 400, y = self.ScreenHeight/2 + 400);
      
      #Text-boxes --------------------------------------
      # Inputs
      self.UserInp = tk.Text(self.window, height = 5, width = 20);
      self.PwdInp = tk.Text(self.window, height = 5, width = 20);

      # Label Texts
      UserText = tk.Label(self.window, text = "Username:", font = tkFont.Font(family = "Georgia", size = 20, weight = "bold", slant = "italic"));
      PwdText = tk.Label(self.window, text = "Password:", font = tkFont.Font(family = "Georgia", size = 20, weight = "bold", slant = "italic"));
      
      # Placing the labels and input boxes on the screen
      UserText.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 - 140);
      self.UserInp.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 - 100);
      PwdText.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 + 60);
      self.PwdInp.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 + 100);
    backgroundDisplay();
    menuButtons();
    self.window.mainloop();
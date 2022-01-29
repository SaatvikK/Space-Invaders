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
#################################

class loginMenu():
  def __init__(self) -> None:
    return None;

  def thisHash(self, text: str) -> str:
    SHAhash = hashes.new("sha512_256");
    SHAhash.update(text.encode("latin1")); # Encoding the input message into unicode 8 and then hashing it.
    return SHAhash.hexdigest(); # Returns the hexadecimal version of the hash value.

  def login(self, usrn: str, pwd: str) -> dict: #pwd = hashed password input
    # Login to MongoDB
    stuff = env.dotenv_values(".env"); # Getting the MongoDB login details from the .env file.
    MongoPwd = stuff["MONGO_PWD"];
    client = mongo.MongoClient("mongodb+srv://SaatvikK:" + str(MongoPwd) + "@main.l6fkh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority");
    
    # Accessing database and collection.
    db = client["login"];
    users = db.list_collection_names();
    if(usrn not in users): # Check if the inputted username is one of the collection names (collection names = usernames).
      return {"status": False, "reason": "usrn"};
    else:
      ThisCollection = db[users[users.index(usrn)]];
      RealPwd = ThisCollection.find_one({"username": usrn})["pwd"]; # Getting the actual password of the account (the one stored in the DB).

      if(pwd != RealPwd): return {"status": False, "reason": "pwd"}; # Checking it with the inputted password.
      else: return {"status": True, "usrn": usrn};

  def signup(self, usrn: str, pwd: str) -> dict: #pwd = hashed password input
    # Login to MongoDB
    stuff = env.dotenv_values(".env"); # Getting the MongoDB login details from the .env file.
    MongoPwd = stuff["MONGO_PWD"];
    client = mongo.MongoClient("mongodb+srv://SaatvikK:" + str(MongoPwd) + "@main.l6fkh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority");
    db = client["login"];
    users = db.list_collection_names();
    if(usrn in users):
      return {"status": False, "reason": "usrn_already_exists"};
    else:
      collection = db[usrn];
      collection.insert_one({"username": usrn, "pwd": pwd});
      return {"status": True};

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
      pwd = self.thisHash(self.PwdInp.get(1.0, "end-1c")); # Getting the password from the text-box input.
      self.res = self.login(usrn, pwd);
      if(self.res["status"] == True):
        print(self.res)
        self.window.destroy();

      elif(self.res["reason"] == "pwd"): print("Password was not correct."); #pwd not correct
      elif(self.res["reason"] == "usrn"): print("Username was not correct."); #usrn not correct
      return;
    
    def execSignUp():
      usrn = self.UserInp.get(1.0, "end-1c");
      pwd = self.hash(self.PwdInp.get(1.0, "end-1c"));
      self.res = self.signup(usrn, pwd);
      if(self.res["status"] == False):
        if(self.res["reason"] == "usrn_already_exists"): print("Username already exists");
      elif(self.res["status"] == True): print("Account created. Please login.");
      return;
    
    def menuButtons():
      # "Login" Button
      login = tk.Button(self.window, text = "Login", command = lambda: execLogin(), height = 1, width = 10, font = self.ButtonFont);
      login.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 + 400);
      
      # "Signup" Button
      SignUp = tk.Button(self.window, text = "Sign Up", command = lambda: execSignUp(), height = 1, width = 10, font = self.ButtonFont);
      SignUp.place(x = self.ScreenWidth/2 - 400, y = self.ScreenHeight/2 + 400);
      
      #Text-boxes
      self.UserInp = tk.Text(self.window, height = 5, width = 20);
      self.PwdInp = tk.Text(self.window, height = 5, width = 20);
      self.UserInp.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 - 100);
      self.PwdInp.place(x = self.ScreenWidth/2 - 80, y = self.ScreenHeight/2 + 100);
    backgroundDisplay();
    menuButtons();
    self.window.mainloop();

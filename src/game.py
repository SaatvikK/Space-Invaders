############ IMPORTS ############
# Libraries
from concurrent.futures import thread
import pygame;
import random as rand;
import json;
import os;
import time;
import pymongo as mongo;
import dotenv as env;
import requests as req;
import threading;
import datetime as dt;

# Other classes
from spaceship import spaceShip;
from aliens import alien;
from barrier import Barrier;
#################################

# Class for the game object.
# This object is essentially the "glue" for all the other classes that have a direct connection to the game.
# It handles all game operations and passes data to other classes.
class game():
  def __init__(self, SpaceshipLives, cooldowns, difficulty, IsDev, usrn) -> None:
    self.usrn = usrn; # The username of the currently logged in player.
    self.IsDev = IsDev;
    self.difficulty = difficulty;
    self.cooldowns = cooldowns;
    self.SpaceshipLives = SpaceshipLives;
    pygame.init();
    # Window init:
    self.WinWidth, self.WinHeight = 600, 800;
    self.screen = pygame.display.set_mode([600, 800]);
    pygame.display.set_caption("Space Invaders");
    self.background = pygame.image.load("../assets/bg.png");
    self.score, self.wave = 0, 1;
    self.rows, self.cols = 1, 5;
    self.DateCreated, self.TimeCreated = "", "";
    self.DateLastPlayed, self.TimeLastPlayed = "", "";

    pygame.font.init();
    self.font = pygame.font.SysFont("Constantia", 30);
    self.AlienBulletCooldown = {
      "time": self.cooldowns["alien"], # ms
      "TimeOfLastCooldownStart": 0
    };
    return None;
  
  def generateGameID(self): # Generating a new game id. Executed in `Main.executeGame()`` in `main.py`.
    NewGameID = None;
    try:
      # The GameID must be unique not only to all games owned by the user, but also all games owned by any user.
      # So to find all the GameIDs that exist, we must send a request to the cloud database via the API.
      response = req.get("https://nea-rest-api.thesatisback.repl.co/NEA_API/v1/list");
      response = response.json();
      print("GAME ID RES:", response)
      games = response["data"]["IDs"]; # List of current game id's.
      if(len(games) == 0): return 1; # If there are no games, just assign THIS game an ID of 1.
      NewGameID = int(max(games)) + 1; # Else increment the highest ID in games[].
    except Exception as e: NewGameID = 1; print(e)

    print("GAMEID:", NewGameID)
    return NewGameID;
  
  def clock(self):
    clock = pygame.time.Clock();
    clock.tick(60); # fps
  
  def createSprites(self): # This method creates all the sprites of the game.
    # Here, pygame's sprite groups are used. These groups are useful when controlling multiple sprites at once (such as the many aliens or bullets).
    self.SpaceshipGroup, self.BulletGroup = pygame.sprite.Group(), pygame.sprite.Group();
    self.AliensGroup = pygame.sprite.Group();
    self.AlienBulletGroup = pygame.sprite.Group();
    self.ThisSpaceship = spaceShip(self.WinWidth//2, self.WinHeight - 100, self.SpaceshipLives, self.cooldowns["player"]);
    self.SpaceshipGroup.add(self.ThisSpaceship);
    self.ExplosionGroup = pygame.sprite.Group();
    self.BarrierGroup = pygame.sprite.Group();
  
  def makeBarriers(self):
    Barrier1 = Barrier(self.WinWidth//2 - 200, self.WinHeight//2 + 50); 
    Barrier2 = Barrier(self.WinWidth//2, self.WinHeight//2 + 50);
    Barrier3 = Barrier(self.WinWidth//2 + 200, self.WinHeight//2 + 50);
    self.BarrierGroup.add(Barrier1);
    self.BarrierGroup.add(Barrier2);
    self.BarrierGroup.add(Barrier3);

  def makeAliens(self):
    if(self.wave != 1):
      if(self.wave <= 5): 
        self.rows += 1;
      elif(self.wave > 5 and self.wave <= 10): 
        self.cols += 1;

    for i in range(self.rows):
      for j in range(self.cols):
        NewAlien = alien(100 + (j*100), 100 + (i*70), self.cooldowns["AlienBulletsMax"]);
        self.AliensGroup.add(NewAlien);
  
  def scoreAndWaveCounter(self, Type: str, variable: str, y: int): # Putting the current score on the screen.
    img = self.font.render(str(Type) + ": " + str(variable), True, (255, 255, 255));
    self.screen.blit(img, (0, y));
  
  def gameOver(self): # If the player has no lives left, close the game.
    if(self.ThisSpaceship.lives <= 0 or len(self.AliensGroup.sprites()) <= 0):
      img = self.font.render("GAME OVER!", True, (255, 255, 255));
      self.screen.blit(img, (self.WinWidth/2 - 100, self.WinHeight/2 - 100));
      self.ThisSpaceship.kill(); time.sleep(4); exit();

  def waveHandler(self): # If all aliens have been killed, start the next wave (increment wave counter --> execute game.makeAliens() again).
    if(len(self.AliensGroup.sprites()) <= 0): 
      self.wave += 1;
      print("wave now updated to", self.wave)
      self.makeAliens();
      
  def gameLoop(self): # The main game loop.
    running = True;
    while(running):
      self.waveHandler();
      self.clock();
      self.screen.blit(self.background, (0, 0));

      for event in pygame.event.get():
        if(event.type == pygame.QUIT): running = False; self.saveGame(); exit(); # Saving the game before quitting.

      #self.scoreCounter();
      self.scoreAndWaveCounter("Score", self.score, 0);
      self.scoreAndWaveCounter("Wave", self.wave, 30);
      self.gameOver();
      # Sprite group(s):
      # Drawing all the sprite groups onto the screen. When pygame calls this method, it draws every single sprite in the group onto the screen.
      self.SpaceshipGroup.draw(self.screen); # .draw is not a method i made, it's an inbuilt method from pygame's sprite class.
      self.BulletGroup.draw(self.screen);
      self.AliensGroup.draw(self.screen);
      self.AlienBulletGroup.draw(self.screen);
      self.ExplosionGroup.draw(self.screen);
      self.BarrierGroup.draw(self.screen);

      # Calling the update function for every single sprite.
      self.ExplosionGroup.update();
      self.BarrierGroup.update(self.BulletGroup, self.AlienBulletGroup);
      self.BulletGroup.update(self.AliensGroup, self.score, self.ExplosionGroup);
      self.AliensGroup.update(self.WinHeight);
      self.AlienBulletGroup.update(self.WinHeight, self.SpaceshipGroup, self.ThisSpaceship, self.ExplosionGroup);

      if(pygame.key.get_pressed()[pygame.K_SPACE]):
        st = self.ThisSpaceship.move(); # We get the returned value from spaceShip.move() (which is inturn returned from spaceShip.shoot()).
        if(st == True):
          self.NewBullet = self.ThisSpaceship.NewBullet; # Create a new bullet and add it to the group.
          self.BulletGroup.add(self.ThisSpaceship.NewBullet);
      else:
        self.ThisSpaceship.move();
      
      try:
        Attacker = rand.choice(self.AliensGroup.sprites()); # Here, a random alien is chosen to shoot on for this tick.
      except: pass;
      st = Attacker.shoot(self.WinHeight, self.AlienBulletGroup.sprites(), self.AlienBulletCooldown, self.SpaceshipGroup); # Executing the shoot method.
      if(st == True):  # If the shoot was successful (i.e. if the cooldown was 0)
        self.AlienBulletGroup.add(Attacker.NewBullet); # Add the newly made bullet to the relevent group.
        self.AlienBulletCooldown["TimeOfLastCooldownStart"] = int(time.time()*1000); # milliseconds
      
      try: 
        with open("../scorestore.json", "r") as file: self.score = json.load(file)["score"];
        with open("../scorestore.json", "w") as file: os.remove("../scorestore.json");
      except: pass;

      pygame.display.update();
    pygame.quit();
  
  def load(self, GameID): # This function is executed in Main.executeGame() when a pre-existing game is being loaded.
    self.GameID = GameID;
    
    def loadStats() -> dict: # Loading the stats from the database.
      with open("../database/" + str(self.GameID) + "/stats/score.json", "r") as file:
        data = json.load(file);
        self.score = data["value"];
      
      with open("../database/" + str(self.GameID) + "/stats/wave.json", "r") as file:
        data = json.load(file);
        self.wave = data["value"];
       
    def loadSettings() -> dict: # Loading the settings (eg difficulty) from the database.
      with open("../database/" + str(self.GameID) + "/settings/difficulty.json") as file:
        data = json.load(file);
        self.difficulty = data["difficulty"];
        self.AlienBulletCooldown["time"] = data["AlienCooldown"];
        self.ThisSpaceship.BulletCooldown["time"] = data["PlayerCooldown"];
        self.cooldowns["AlienBulletsMax"] = data["AlienBulletsMax"];
      
      with open("../database/" + str(self.GameID) + "/settings/lives.json") as file:
        data = json.load(file);
        self.ThisSpaceship.lives = data["LivesRemaining"];
        self.ThisSpaceship.TotalLives = data["TotalLives"];
      
      with open("../database/" + str(self.GameID) + "/settings/meta.json") as file:
        data = json.load(file);
        self.DateCreated, self.TimeCreated = data["created"]["date"], data["created"]["time"];
        self.DateLastPlayed, self.TimeLastPlayed = data["LastPlayed"]["date"], data["LastPlayed"]["time"];
    
    loadStats(); loadSettings();
    
  def saveGame(self): # This function is executed in Main.executeGame() when a new game is being created and when the user quits a game that they are playing.
    def save(DictToSave: dict, collection: str):
      try:
        with open(self.DBLoc + collection, "w+") as file:
          json.dump(DictToSave, file);
      
      except Exception as e: print(e);
    
    def makeDB() -> str: # First, a check is done to make sure that the database folder ("../database/") exists and a database for THIS GAME ("../database/GameID/").
      x = dt.datetime.now() # Current date-time.
      self.DBLoc = "../database/" + str(self.GameID) + "/";
      if(os.path.isdir("../database/") == False): os.mkdir("../database/");
      if(os.path.isdir("../database/" + str(self.GameID)) == False):
        os.mkdir("../database/" + str(self.GameID));
        os.mkdir(self.DBLoc + "settings");
        os.mkdir(self.DBLoc + "stats");
        
        save({ # Saving the meta data as none of this can be changed after creation (other than DateTime last played).
          "username": self.usrn, 
          "created": {
            "date": str(x.day) + "/" + str(x.month) + "/" + str(x.year), 
            "time": x.strftime("%H:%M:%S")
          }, 
          "LastPlayed": {
            "date": str(x.day) + "/" + str(x.month) + "/" + str(x.year), 
            "time": x.strftime("%H:%M:%S")
          }
        }, "settings/meta.json");

      return self.DBLoc;
    
    self.DBLoc = makeDB();
    x = dt.datetime.now() # Current date-time.
    # Saving the current game state.
    save({"value": self.score}, "stats/score.json");
    save({"value": self.wave}, "stats/wave.json");
    save({"difficulty": self.difficulty, "AlienCooldown": self.AlienBulletCooldown["time"], "PlayerCooldown": self.ThisSpaceship.BulletCooldown["time"], "AlienBulletsMax": self.cooldowns["AlienBulletsMax"]}, "settings/difficulty.json");
    save({"LivesRemaining": self.ThisSpaceship.lives, "TotalLives": self.ThisSpaceship.TotalLives}, "settings/lives.json");

    # Updating the LastPlayed sub-object.
    with open("../database/" + str(self.GameID) + "/settings/meta.json") as metafile: 
      data = json.load(metafile); data["LastPlayed"]["date"] = str(x.day) + "/" + str(x.month) + "/" + str(x.year);
      data["LastPlayed"]["time"] = x.strftime("%H:%M:%S")
      save(data, "settings/meta.json");

    def backupToCloud():
      # The following subroutine replaces all white spaces in the username with `%20`. This is done as a URL cannot have white-spaces and so %20 represents a space.
      def spacesWith20(usrn):
        user = list(usrn);
        for i in range(len(user)):
          if(user[i] == " "): user[i] = "%20";
        usrn = "".join(user);
        return usrn;

      # This is where the REST API is used.
      # A REST API is used to inteface with the database server on replit.com.
      # First, the base URL is defined:
      BaseURL = "https://NEA-REST-API.thesatisback.repl.co/NEA_API/v1";

      # Next, a request is made with the GET HTTP method using the the url: `https://www.domain.com/NEA_API/v1/[GameID]`,
      DoesGameExist = req.get(BaseURL + "/" + str(self.GameID)).json();
      if(DoesGameExist["DoesGameExist"] == False): # The server will response with a JSON and a boolean value. If the value is false, the game's database DOES NOT exist in the database server.
        # Because it doesn't exist, it must first be made using a POST http method.
        
        self.usrn = spacesWith20(self.usrn);

        req.post(BaseURL + "/" + str(self.GameID) + "/" + self.usrn); # Next, a request is made using POST to `/NEA_API/v1/[GameID]/[Username]`

      # Back up stats collection using a PUT method
      req.put(BaseURL + "/" + str(self.GameID) + "/stats/score/value/" + str(self.score));
      req.put(BaseURL + "/" + str(self.GameID) + "/stats/wave/value/" + str(self.wave));
      
      # Back up settings collection using a PUT method.
      req.put(BaseURL + "/" + str(self.GameID) + "/settings/lives/TotalLives/" + str(self.ThisSpaceship.TotalLives));
      req.put(BaseURL + "/" + str(self.GameID) + "/settings/lives/LivesRemaining/" + str(self.ThisSpaceship.lives));
      if(self.difficulty == "Casual/Normal"): req.put(BaseURL + "/" + str(self.GameID) + "/settings/difficulty/difficulty/Casual");
      else: req.put(BaseURL + "/" + str(self.GameID) + "/settings/difficulty/difficulty/" + self.difficulty);
    # w/ threads = 1.52 sec, w/o = 3.50 sec
    # Threads are separate flows of execution. 
    # They are executed almost simultaneously to decrease the time of execution.
    # Here, we are creating a new thread with the target of the backupToCloud() function.

    NewThread = threading.Thread(target = backupToCloud);
    NewThread.start();

    # Because this function is querying a separate server, located in the U.S., there is a lot of latency between requests and responses.
    # Therefore, when the game is autosaving (either when it is created, or the application is closed), the program can appear, to the user,
    # to freeze. In reality, it is just waiting for the cloud database server to respond to its requests.
    # This may annoy users when they have created their game as it delays them playing the game.
    # Therefore, this function is executed in a separate thread so that the user can instantly play the game whilst the game is backed up in the
    # Background.
    

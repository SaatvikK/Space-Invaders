############ IMPORTS ############
# Libraries
import pygame;
import random as rand;
import json;
import os;
import time;
import pymongo as mongo;
import dotenv as env;

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
      games = os.listdir("../database"); # List of current game id's.
      if(len(games) == 0): return 1; # If there are no games, just assign THIS game an ID of 1.
      NewGameID = int(max(games)) + 1; # Else increment the highest ID in games[].
    except: NewGameID = 1;
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
  
  def scoreCounter(self): # Putting the current score on the screen.
    img = self.font.render("Score: " + str(self.score), True, (255, 255, 255));
    self.screen.blit(img, (0, 0));
  
  def gameOver(self): # If the player has no lives left, close the game.
    if(self.ThisSpaceship.lives <= 0 or len(self.AliensGroup.sprites()) <= 0):
      img = self.font.render("GAME OVER!", True, (255, 255, 255));
      self.screen.blit(img, (self.WinWidth/2 - 100, self.WinHeight/2 - 100));
      self.ThisSpaceship.kill(); time.sleep(2); exit();

  def waveHandler(self): # If all aliens have been killed, start the next wave (increment wave counter --> execute game.makeAliens() again).
    font = pygame.font.SysFont("Constantia", 30);
    img = font.render("Wave: " + str(self.wave), True, (255, 255, 255));
    self.screen.blit(img, (0, 50));
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

      self.scoreCounter();
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

      #try: 
      #  if(self.NewBullet.HasHitAlien == True): 
      #    print("Hit alien:", self.score)
      #    self.score += 1; self.NewBullet.HasHitAlien = False;
      #except: pass;
      
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
        self.score = data["score"];
      
      with open("../database/" + str(self.GameID) + "/stats/wave.json", "r") as file:
        data = json.load(file);
        self.wave = data["wave"];
       
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
    
    loadStats(); loadSettings();
    
  def saveGame(self): # This function is executed in Main.executeGame() when a new game is being created and when the user quits a game that they are playing.
    def makeDB() -> str: # First, a check is done to make sure that the database folder ("../database/") exists and a database for THIS GAME ("../database/GameID/").
      DBLoc = "../database/" + str(self.GameID) + "/";
      if(os.path.isdir("../database/") == False): os.mkdir("../database/");
      if(os.path.isdir("../database/" + str(self.GameID)) == False):
        os.mkdir("../database/" + str(self.GameID));
        os.mkdir(DBLoc + "settings");
        os.mkdir(DBLoc + "stats");

      return DBLoc;

    def save(DictToSave: dict, collection: str):
      try:
        with open(self.DBLoc + collection, "w+") as file:
          json.dump(DictToSave, file);
      
      except Exception as e: print("uh oh lol"); print(e);
    
    self.DBLoc = makeDB();
    # Saving the current game state.
    save({"identifier": 0, "score": self.score}, "stats/score.json");
    save({"identifier": 1, "wave": self.wave}, "stats/wave.json");
    save({"identifier": 0, "difficulty": self.difficulty, "AlienCooldown": self.AlienBulletCooldown["time"], "PlayerCooldown": self.ThisSpaceship.BulletCooldown["time"], "AlienBulletsMax": self.cooldowns["AlienBulletsMax"]}, "settings/difficulty.json");
    save({"identifier": 1, "LivesRemaining": self.ThisSpaceship.lives, "TotalLives": self.ThisSpaceship.TotalLives}, "settings/lives.json");
    save({"identifier": 2, "username": self.usrn}, "settings/player.json");

    def backupToMongo():
      # Backing up to the MongoDB Atlas server.
      # MongoDB is a cloud computing company that hosts various NoSQL database servers.
      # The local DB is being backed up to MongoDB Atlas incase the local DB is corrupted and to allow the website to get data from all the different games.
      stuff = env.dotenv_values(".env"); # Getting the MongoDB username and password.
      MongoPwd = stuff["MONGO_PWD"];
      client = mongo.MongoClient("mongodb+srv://SaatvikK:" + str(MongoPwd) + "@main.l6fkh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority");
      db = client[str(self.GameID)];
      StatsCol, SettingsCol = db["stats"], db["settings"];
      db.drop_collection("stats");
      db.drop_collection("settings");
      StatsCol.insert_one({"identifier": 0, "score": self.score});
      StatsCol.insert_one({"identifier": 1, "wave": self.wave});
      SettingsCol.insert_one({"identifier": 0, "difficulty": self.difficulty, "AlienCooldown": self.AlienBulletCooldown["time"], "PlayerCooldown": self.ThisSpaceship.BulletCooldown["time"], "AlienBulletsMax": self.cooldowns["AlienBulletsMax"]});
      SettingsCol.insert_one({"identifier": 1, "LivesRemaining": self.ThisSpaceship.lives, "TotalLives": self.ThisSpaceship.TotalLives});
      SettingsCol.insert_one({"identifier": 2, "username": self.usrn});

    backupToMongo();

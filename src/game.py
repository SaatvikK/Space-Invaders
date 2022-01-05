############ IMPORTS ############
# Libraries
from typing import Dict
from dotenv.main import dotenv_values
import pygame;
import random as rand;
import json;
import os;
import time;
import pymongo as mongo;
import dotenv as env;

# Other classes
from spaceship import spaceShip;
from bullet import bullet;
from aliens import alien;
from bullet import alienBullet;
#################################

class game():
  def __init__(self, SpaceshipLives, cooldowns, difficulty) -> None:
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

    pygame.font.init();
    self.font = pygame.font.SysFont("Constantia", 30);
    self.AlienBulletCooldown = {
      "time": self.cooldowns["alien"], # ms
      "TimeOfLastCooldownStart": 0
    };
    return None;
  
  def generateGameID(self):
    try:
      games = os.listdir("../database");
      NewGameID = rand.randint(0, 50);
      while(str(NewGameID) in games): NewGameID = rand.randint(0, 50);
      return NewGameID;
    except: return "1";
  

  def clock(self):
    clock = pygame.time.Clock();
    clock.tick(60); # fps
  
  def createSprites(self):
    self.SpaceshipGroup, self.BulletGroup = pygame.sprite.Group(), pygame.sprite.Group();
    self.AliensGroup = pygame.sprite.Group();
    self.AlienBulletGroup = pygame.sprite.Group();
    self.ThisSpaceship = spaceShip(self.WinWidth//2, self.WinHeight - 100, self.SpaceshipLives, self.cooldowns["player"]);
    self.SpaceshipGroup.add(self.ThisSpaceship);
  
  def makeAliens(self):
    rows, cols = 5, 5;
    for i in range(rows):
      for j in range(cols):
        NewAlien = alien(100 + (j*100), 100 + (i*70), self.cooldowns["AlienBulletsMax"]);
        self.AliensGroup.add(NewAlien);
  
  def scoreCounter(self):
    img = self.font.render("Score: " + str(self.score), True, (255, 255, 255));
    self.screen.blit(img, (0, 0));
  
  def gameOver(self):
    if(self.ThisSpaceship.lives <= 0 or len(self.AliensGroup.sprites()) <= 0):
      img = pygame.font.SysFont("Constantia", 40).render("GAME OVER!", True, (255, 255, 255));
      self.screen.blit(img, (self.WinWidth/2 - 100, self.WinHeight/2 - 100));


  def gameLoop(self):
    running = True;
    while(running):
      self.clock();
      self.screen.blit(self.background, (0, 0));

      for event in pygame.event.get():
        if(event.type == pygame.QUIT): self.saveGame(); running = False;

      self.scoreCounter();
      self.gameOver();
      # Sprite group(s):
      self.SpaceshipGroup.draw(self.screen); # .draw is not a method i made, it's an inbuilt method from pygame's sprite class.
      self.BulletGroup.draw(self.screen);
      self.AliensGroup.draw(self.screen);
      self.AlienBulletGroup.draw(self.screen);
      self.BulletGroup.update(self.AliensGroup, self.score);
      self.AliensGroup.update(self.WinHeight);
      self.AlienBulletGroup.update(self.WinHeight, self.SpaceshipGroup, self.ThisSpaceship);

      if(pygame.key.get_pressed()[pygame.K_SPACE]):
        st = self.ThisSpaceship.move();
        if(st == True): 
          self.NewBullet = self.ThisSpaceship.NewBullet;
          self.BulletGroup.add(self.ThisSpaceship.NewBullet);
      else:
        self.ThisSpaceship.move();
      
      Attacker = rand.choice(self.AliensGroup.sprites());
      st = Attacker.shoot(self.WinHeight, self.AlienBulletGroup.sprites(), self.AlienBulletCooldown, self.SpaceshipGroup);
      if(st == True): 
        self.AlienBulletGroup.add(Attacker.NewBullet);
        self.AlienBulletCooldown["TimeOfLastCooldownStart"] = int(time.time()*1000); # milliseconds

      try: 
        if(self.NewBullet.HasHitAlien == True): self.score += 1; self.NewBullet.HasHitAlien = False;
      except: pass;

      

      pygame.display.update();
    pygame.quit();
  
  def load(self, GameID):
    self.GameID = GameID;
    print("id", self.GameID);
    
    def loadStats():
      with open("../database/" + str(self.GameID) + "/stats/score.json", "r") as file:
        data = json.load(file);
        self.score = data["score"];
        print("score", self.score)
      
      with open("../database/" + str(self.GameID) + "/stats/wave.json", "r") as file:
        data = json.load(file);
        self.wave = data["wave"];
        print("wave", self.wave)
    
    def loadSettings():
      with open("../database/" + str(self.GameID) + "/settings/difficulty.json") as file:
        data = json.load(file);
        self.difficulty = data["difficulty"];
        print("diff", self.difficulty)
        self.AlienBulletCooldown["time"] = data["AlienCooldown"];
        print("alien cooldown", self.AlienBulletCooldown["time"])
        self.ThisSpaceship.BulletCooldown["time"] = data["PlayerCooldown"];
        print("ship cooldown", self.ThisSpaceship.BulletCooldown["time"])
        self.cooldowns["AlienBulletsMax"] = data["AlienBulletsMax"];
        print("Max bullets", self.cooldowns["AlienBulletsMax"]);
      
      with open("../database/" + str(self.GameID) + "/settings/lives.json") as file:
        data = json.load(file);
        self.ThisSpaceship.lives = data["LivesRemaining"];
        self.ThisSpaceship.TotalLives = data["TotalLives"];

    loadStats(); loadSettings();
    
  def saveGame(self):
    def makeDB() -> str:
      DBLoc = "../database/" + str(self.GameID) + "/";
      if(os.path.isdir("../database/") == False): os.mkdir("../database/");
      if(os.path.isdir("../database/" + str(self.GameID)) == False):
        os.mkdir("../database/" + str(self.GameID));
        os.mkdir(DBLoc + "settings");
        os.mkdir(DBLoc + "stats");

      return DBLoc;

    def save(DBLoc: str, DictToSave: dict, collection: str):
      try:
        with open(DBLoc + collection, "w+") as file:

          
          json.dump(DictToSave, file);
      
      except Exception as e: print("uh oh lol"); print(e);
    
    DBLoc = makeDB();
    save(DBLoc, {"identifier": 0, "score": self.score}, "stats/score.json");
    save(DBLoc, {"identifier": 1, "wave": self.wave}, "stats/wave.json");
    save(DBLoc, {"identifier": 0, "difficulty": self.difficulty, "AlienCooldown": self.AlienBulletCooldown["time"], "PlayerCooldown": self.ThisSpaceship.BulletCooldown["time"], "AlienBulletsMax": self.cooldowns["AlienBulletsMax"]}, "settings/difficulty.json");
    save(DBLoc, {"identifier": 1, "LivesRemaining": self.ThisSpaceship.lives, "TotalLives": self.ThisSpaceship.TotalLives}, "settings/lives.json");

    def backupToMongo():
      # Backing up to the MongoDB Atlas server.
      stuff = env.dotenv_values(".env");
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

    backupToMongo();
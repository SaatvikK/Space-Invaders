############ IMPORTS ############
# Libraries
from typing import Dict
import pygame;
import random as rand;
import json;
import os;
import time;
#import pymongo as db;

# Other classes
from spaceship import spaceShip;
from bullet import bullet;
from aliens import alien;
from bullet import alienBullet;
#################################

class game():
  def __init__(self) -> None:
    pygame.init();
    # Window init:
    self.WinWidth, self.WinHeight = 600, 800;
    self.screen = pygame.display.set_mode([600, 800]);
    pygame.display.set_caption("Space Invaders");
    self.background = pygame.image.load("../assets/bg.png");
    self.score, self.wave = 0, 1;

    pygame.font.init();
    self.font = pygame.font.SysFont("Constantia", 30);
    self.GameID = self.generateGameID();
    self.saveGame();
    self.createSprites();
    self.makeAliens();
    self.gameLoop();
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
    self.ThisSpaceship = spaceShip(self.WinWidth//2, self.WinHeight - 100, 3);
    self.SpaceshipGroup.add(self.ThisSpaceship);
  
  def makeAliens(self):
    rows, cols = 5, 5;
    for i in range(rows):
      for j in range(cols):
        NewAlien = alien(100 + (j*100), 100 + (i*70));
        self.AliensGroup.add(NewAlien);

    self.AlienBulletCooldown = {
      "time": 1000, # ms
      "TimeOfLastCooldownStart": 0
    };

  
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
    save(DBLoc, {"score": self.score}, "stats/score.json");
    save(DBLoc, {"wave": self.wave}, "stats/wave.json");





############ IMPORTS ############
# Libraries
import pygame;
import random as rand;
import json;
import math;
import time;

# Other classes
from bullet import bullet;
#################################

class spaceShip(pygame.sprite.Sprite):
  def __init__(self, x, y, lives, cooldown) -> None:
    print("IN SPACE SHGIP", lives)
    pygame.sprite.Sprite.__init__(self);
    self.image = pygame.image.load("../assets/spaceship.png");
    self.rect = self.image.get_rect();
    self.rect.center = (x, y);
    self.lives = lives;
    self.TotalLives = lives;
    self.BulletCooldown = {
      "time": cooldown, # ms
      "TimeOfLastCooldownStart": 0
    };

  def move(self):
    speed = 7;

    # checking for key presses:
    PressedKey = pygame.key.get_pressed();
    if(PressedKey[pygame.K_a] and self.rect.left > 0):
      self.rect.x -= speed;
    
    elif(PressedKey[pygame.K_d] and self.rect.right < 600):
      self.rect.x += speed;
    
    if(PressedKey[pygame.K_SPACE]):
      st = self.shoot();
      return st;

  def shoot(self):
    now = time.time()*1000; # milliseconds
    if((now - self.BulletCooldown["TimeOfLastCooldownStart"] >= self.BulletCooldown["time"]) or (self.BulletCooldown["TimeOfLastCooldownStart"] == 0)):
      self.NewBullet = bullet(self.rect.centerx, self.rect.top);
      #self.NewBullet.update();
      self.BulletCooldown["TimeOfLastCooldownStart"] = int(time.time()*1000); # milliseconds
      return True;
    else:
      return False;

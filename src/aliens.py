############ IMPORTS ############
# Libraries
import pygame;
import random as rand;
import json;
import math;
import time;

# Other classes
from bullet import alienBullet;
#################################

class alien(pygame.sprite.Sprite):
  def __init__(self, x, y, MaxBullets) -> None:
    self.MaxBullets = MaxBullets;
    pygame.sprite.Sprite.__init__(self);
    self.image = pygame.image.load("../assets/alien" + str(rand.randint(1, 5)) + ".png");
    self.rect = self.image.get_rect();
    self.rect.center = (x, y);
    self.speed = 5;


  def update(self, height):
    self.rect.centerx += self.speed;
    if(self.rect.right >= 600):
      self.speed = -1 * self.speed;
    elif(self.rect.left <= 0):
      self.speed = -1 * self.speed;
    
    if(self.rect.bottom < height):
      self.rect.centery += 0.8;
    else:
      # game over
      pass;

  def shoot(self, height, BulletGroup, cooldown, SpaceshipGroup):
    now = time.time()*1000; # milliseconds
    if(((now - cooldown["TimeOfLastCooldownStart"] >= cooldown["time"]) or (cooldown["TimeOfLastCooldownStart"] == 0)) and (len(BulletGroup) < self.MaxBullets and len(BulletGroup) >= 0)):
      self.NewBullet = alienBullet(self.rect.centerx, self.rect.top);
      return True;
    else:
      return False;

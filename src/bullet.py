############ IMPORTS ############
# Libraries
import pygame;
import random as rand;
import json;
import math
#################################

class bullet(pygame.sprite.Sprite):
  def __init__(self, x, y) -> None:
    pygame.sprite.Sprite.__init__(self);
    self.image = pygame.image.load("../assets/bullet.png");
    self.rect = self.image.get_rect();
    self.rect.center = (x, y);
    self.HasHitAlien = False;
  
  def update(self, AlienGroup, score):
    self.rect.y -= 5;
    if(self.rect.bottom < 0): self.kill;

    if(pygame.sprite.spritecollide(self, AlienGroup, True)): # Checking if bullet has collided with aliens using pygame method.
      self.kill();
      self.HasHitAlien = True;

class alienBullet(pygame.sprite.Sprite):
  def __init__(self, x, y) -> None:
    pygame.sprite.Sprite.__init__(self);
    self.image = pygame.image.load("../assets/AlienBullet.png");
    self.rect = self.image.get_rect();
    self.rect.center = (x, y);
  
  def update(self, height, SpaceshipGroup, ship):
    self.rect.y += 2;
    if(self.rect.top > height): self.kill();

    if(pygame.sprite.spritecollide(self, SpaceshipGroup, False)):
      self.kill();
      if(ship.lives <= 0): ship.kill();
      else:
        ship.lives -= 1;
        print("yippie!1")
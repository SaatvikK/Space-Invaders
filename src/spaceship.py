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

# Class for the player's space ship.
# Since this will be a sprite, we inherit methods and attributes from the pygame.sprite.Sprite class.
# This will make it easier to program features (such as movement) for the spaceship (and any other sprite) as Pygame will do most of the
# "heavy lifting".
class spaceShip(pygame.sprite.Sprite):
  def __init__(self, x, y, lives, cooldown) -> None:
    print("IN SPACE SHGIP", lives)
    pygame.sprite.Sprite.__init__(self);
    self.image = pygame.image.load("../assets/spaceship.png");
    self.rect = self.image.get_rect(); # This is essentially the hit-box for the spaceship.
    self.rect.center = (x, y);
    self.lives = lives;
    self.TotalLives = lives;

    # Keeps track of the spaceship's cooldown.
    self.BulletCooldown = {
      "time": cooldown, # ms
      "TimeOfLastCooldownStart": 0
    };

  def move(self):
    speed = 7;

    # checking for key presses:
    PressedKey = pygame.key.get_pressed();
    if(PressedKey[pygame.K_a] and self.rect.left > 0): # If the user pressed the "a" key and the ship isn't against the left edge...
      self.rect.x -= speed; # Move them to the left.
    
    elif(PressedKey[pygame.K_d] and self.rect.right < 600): # Else if the user pressed the "d" key and the key isn't against the right edge...
      self.rect.x += speed; # Move them to the right.
    
    if(PressedKey[pygame.K_SPACE]): # If the user pressed the spacebar...
      st = self.shoot(); # Execute the `.shoot()` method.
      return st; # The success or failure of the shot is returned to `game.py``.

  def shoot(self):
    now = time.time()*1000; # milliseconds

    # This if-statement checks if the spaceship's cooldown is over.
    if((now - self.BulletCooldown["TimeOfLastCooldownStart"] >= self.BulletCooldown["time"]) or (self.BulletCooldown["TimeOfLastCooldownStart"] == 0)):
      self.NewBullet = bullet(self.rect.centerx, self.rect.top); # Instantiate a new object of the bullet class.
      # After the bullet is fired, the cooldown clock is restarted.
      self.BulletCooldown["TimeOfLastCooldownStart"] = int(time.time()*1000); # milliseconds
      return True; # Return true, indicating that the shot was sucessful.
    else:
      return False;

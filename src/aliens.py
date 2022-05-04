############ IMPORTS ############
# Libraries
import pygame;
import random as rand;
import time;

# Other classes
from bullet import alienBullet;
#################################

# Class for the aliens.
# Since this will be a sprite, we inherit methods and attributes from the pygame.sprite.Sprite class.
# This will make it easier to program features (such as movement) for the spaceship (and any other sprite) as Pygame will do most of the
# "heavy lifting".
# Aliens are instantiated in `game.makeAliens()`.
class alien(pygame.sprite.Sprite):
  def __init__(self, x, y, MaxBullets) -> None:
    self.MaxBullets = MaxBullets; # This is the maximum amount of bullets that all aliens can fire in a certain amount of time.
    pygame.sprite.Sprite.__init__(self);
    self.image = pygame.image.load("../assets/alien" + str(rand.randint(1, 5)) + ".png"); # Giving the new alien a random sprite design.
    self.rect = self.image.get_rect(); # hit-box
    self.rect.center = (x, y);
    self.speed = 5;
    self.MoveDown = [];

  # Pygame sprites come with a pre-built update() function, however it does not include certain operations that we need, so we'll rewrite it:
  def update(self, height):
    # Moving the alien from side-to-side.
    # If the alien hits one side of the screen, move it the other way.
    self.rect.centerx += self.speed;
    if(self.rect.right >= 600):
      self.speed = -1 * self.speed;
    elif(self.rect.left <= 0):
      self.speed = -1 * self.speed;
    
    # Here the aliens are slowly moving down until they reach the bottom (game over).
    if(self.rect.bottom < height):
      sped = 10;
      lastones = self.MoveDown[-sped:];
      if((all(lastones) == True and len(lastones) >= sped) or (all(lastones) == False and len(lastones) == sped)):
        self.rect.centery += 1;
        self.MoveDown.append(True);
      else: self.MoveDown.append(False);
        
        
    else:
      print("Game over");
      exit();
      pass;

  def shoot(self, height, BulletGroup, cooldown, SpaceshipGroup):
    now = time.time()*1000; # milliseconds

    # IF the cooldown is over AND the amount of bullets currently on the screen is greater than zero AND less than the maximum amount of bullets, then:
    if(((now - cooldown["TimeOfLastCooldownStart"] >= cooldown["time"]) or (cooldown["TimeOfLastCooldownStart"] == 0)) and (len(BulletGroup) < self.MaxBullets and len(BulletGroup) >= 0)):
      self.NewBullet = alienBullet(self.rect.centerx, self.rect.top); # Create a new bullet.
      return True;
    else:
      return False;

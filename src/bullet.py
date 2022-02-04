############ IMPORTS ############
# Libraries
import pygame;
import json;

# Other Classes
from explosion import explosion;
#################################

# Classes for the spaceship and alien bullets.
# Since this will be a sprite, we inherit methods and attributes from the pygame.sprite.Sprite class.
# This will make it easier to program features (such as movement) for the spaceship (and any other sprite) as Pygame will do most of the
# "heavy lifting".
class bullet(pygame.sprite.Sprite):
  def __init__(self, x, y) -> None:
    pygame.sprite.Sprite.__init__(self);
    self.image = pygame.image.load("../assets/bullet.png");
    self.rect = self.image.get_rect();
    self.rect.center = (x, y);
    self.HasHitAlien = False;
    self.scoreBul = 0;
  
  def update(self, AlienGroup, score, ExpGroup):
    self.rect.y -= 5;
    if(self.rect.bottom < 0): self.kill;

    if(pygame.sprite.spritecollide(self, AlienGroup, True)): # Checking if bullet has collided with aliens using pygame method.
      NewExp = explosion(self.rect.centerx, self.rect.centery, 2); # Instantiating a new explosion.
      ExpGroup.add(NewExp);
      self.scoreBul = score + 1;
      self.HasHitAlien = True;
      self.kill(); # Destroying the bullet.
      with open("../scorestore.json", "w") as f:
        json.dump({"score": score + 1}, f);


# The same functionality is implemented in the alienBullet class, however the different is which direction they move in
# and what happens if there is a collision.
class alienBullet(pygame.sprite.Sprite):
  def __init__(self, x, y) -> None:
    pygame.sprite.Sprite.__init__(self);
    self.image = pygame.image.load("../assets/AlienBullet.png");
    self.rect = self.image.get_rect();
    self.rect.center = (x, y);
  
  def update(self, height, SpaceshipGroup, ship, ExpGroup):
    self.rect.y += 2;
    if(self.rect.top > height): self.kill();

    if(pygame.sprite.spritecollide(self, SpaceshipGroup, False)): # If collision, return true but dont destroy the spaceship.
      NewExp = explosion(self.rect.centerx, self.rect.centery, 1);
      ExpGroup.add(NewExp);
      self.kill();
      if(ship.lives <= 0): ship.kill(); # if the spaceship has no more lives left, kill it.
      else:
        ship.lives -= 1; # Else decrement the amount of lives that the ship has.
        print("yippie!1")
############ IMPORTS ############
# Libraries
import pygame;

# Other Classes
from explosion import explosion;
#################################

class bullet(pygame.sprite.Sprite):
  def __init__(self, x, y) -> None:
    pygame.sprite.Sprite.__init__(self);
    self.image = pygame.image.load("../assets/bullet.png");
    self.rect = self.image.get_rect();
    self.rect.center = (x, y);
    self.HasHitAlien = False;
  
  def update(self, AlienGroup, score, ExpGroup):
    self.rect.y -= 5;
    if(self.rect.bottom < 0): self.kill;

    if(pygame.sprite.spritecollide(self, AlienGroup, True)): # Checking if bullet has collided with aliens using pygame method.
      NewExp = explosion(self.rect.centerx, self.rect.centery, 2);
      ExpGroup.add(NewExp);

      self.kill();
      self.HasHitAlien = True;

class alienBullet(pygame.sprite.Sprite):
  def __init__(self, x, y) -> None:
    pygame.sprite.Sprite.__init__(self);
    self.image = pygame.image.load("../assets/AlienBullet.png");
    self.rect = self.image.get_rect();
    self.rect.center = (x, y);
  
  def update(self, height, SpaceshipGroup, ship, ExpGroup):
    self.rect.y += 2;
    if(self.rect.top > height): self.kill();

    if(pygame.sprite.spritecollide(self, SpaceshipGroup, False)):
      NewExp = explosion(self.rect.centerx, self.rect.centery, 1);
      ExpGroup.add(NewExp);
      self.kill();
      if(ship.lives <= 0): ship.kill();
      else:
        ship.lives -= 1;
        print("yippie!1")
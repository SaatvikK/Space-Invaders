############ IMPORTS ############
# Libraries
import pygame;
#################################

# Class for the barriers.
# Since this will be a sprite, we inherit methods and attributes from the pygame.sprite.Sprite class.
# This will make it easier to program features (such as movement) for the spaceship (and any other sprite) as Pygame will do most of the
# "heavy lifting".
class Barrier(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self);

    # Loading images of all stages of barriers and putting them in a list.
    self.ImgList = [
      pygame.transform.scale(pygame.image.load("../assets/Barrier1-4Health.png"), (100, 68)),
      pygame.transform.scale(pygame.image.load("../assets/Barrier2-4Health.png"), (100, 68)),
      pygame.transform.scale(pygame.image.load("../assets/Barrier3-4Health.png"), (100, 68)),
      pygame.transform.scale(pygame.image.load("../assets/BarrierFullHealth.png"), (100, 68)),
    ];
    self.image = self.ImgList[3]; # The current image.
    self.rect = self.image.get_rect(); # Hit-box of the image.
    self.rect.center = (x, y);

  def update(self, BulletGroup, AlienBulletGroup): # Bullet can be an alien bullet or a spaceship (player) bullet.
    # If either the alien bullet or player's bullet hits the barrier, then:
    if(pygame.sprite.spritecollide(self, BulletGroup, True) or pygame.sprite.spritecollide(self, AlienBulletGroup, True)):
      ImgIndex = self.ImgList.index(self.image);
      if(ImgIndex == 0): # If the barrier only has one life left, then:
        self.kill();
      else: self.image = self.ImgList[ImgIndex - 1];

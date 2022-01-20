############ IMPORTS ############
# Libraries
import pygame;
import time;
#################################

class explosion(pygame.sprite.Sprite):
  def __init__(self, x, y, size):
    pygame.sprite.Sprite.__init__(self);
    self.ImgList = [];
    for i in range(1, 6):
      img = pygame.image.load("../assets/exp" + str(i) + ".png");
      if(size == 1): img = pygame.transform.scale(img, (20, 20));
      elif(size == 2): img = pygame.transform.scale(img, (40, 40));
      elif(size == 3): img = pygame.transform.scale(img, (160, 160));

      self.ImgList.append(img);
    
    self.IndexOfImgList = 0;
    self.CurrentImg = self.ImgList[self.IndexOfImgList];
    self.image = pygame.image.load("../assets/AlienBullet.png");
    self.rect = self.image.get_rect();
    self.rect.center = (x, y);
    self.counter = 0;

  
  def update(self):
    self.threshold = 3;
    self.counter += 1;

    if(self.counter > self.threshold and self.IndexOfImgList < (len(self.ImgList) - 1)):
      self.counter = 0;
      self.IndexOfImgList += 1;
      self.image = self.ImgList[self.IndexOfImgList];
    
    if((self.IndexOfImgList > (len(self.ImgList) - 1) and self.counter > self.threshold) or self.IndexOfImgList == 4): 
      print("hiiii")
      self.kill();
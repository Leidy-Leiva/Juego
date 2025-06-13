import pygame
import configuration
class Enemy:
   def __init__(self,x,y):
        self.image=pygame.image.load("img/enemy.png")
        self.image=pygame.transform.scale(self.image,(50,50))
        self.rect=self.image.get_rect(topleft=(x,y))
        self.active = True
        self.rect=pygame.Rect(x,y,50,50)
        self.speed=2

   def follow(self,player):
        if not self.active:
            return
   
        if self.rect.x>player.x:
           self.rect.x -=self.speed
        elif self.rect.x< player.x:
           self.rect.x+= self.speed


        if self.rect.y>player.y:
           self.rect.y -=self.speed
        elif self.rect.y < player.y:
           self.rect.y+= self.speed

        self.rect.x=max(0,min(self.rect.x,configuration.WIDTH-self.rect.width))
        self.rect.y=max(0,min(self.rect.y,configuration.HEIGHT-self.rect.height))

   def draw(self,surface):
         if self.active:
            surface.blit(self.image, self.rect)
       





import pygame
import configuration
class Player:
    def __init__(self,x,y):
        self.image=pygame.image.load("img/player.png")
        self.image= pygame.transform.scale(self.image,(50,50))
        self.rect=self.image.get_rect(topleft=(x,y))
        self.speed=5
    

    def move(self,keys):
        if keys[pygame.K_LEFT]:self.rect.x -=self.speed
        if keys[pygame.K_RIGHT]:self.rect.x +=self.speed
        if keys[pygame.K_UP]:self.rect.y -=self.speed
        if keys[pygame.K_DOWN]:self.rect.y +=self.speed


    def draw(self,surface):
       surface.blit(self.image, self.rect)
# -*- coding: utf-8 -*-
"""
Created on Sun May  4 15:45:30 2014

@author: casey
"""

import pygame 
import pygame.font 
import pygame.event 
import pygame.draw

from pygame.locals import *

class weird: 
    def __init__(self, screen):
        self.screen = screen 
        
    def display_box(screen, message):
      "Print a message in a box in the middle of the screen"
      fontobject = pygame.font.Font(None,18)
      pygame.draw.rect(screen, (0,0,0),
                       ((screen.get_width() / 2) - 100,
                        (screen.get_height() / 2) - 10,
                        200,20), 0)
      pygame.draw.rect(screen, (255,255,255),
                       ((screen.get_width() / 2) - 102,
                        (screen.get_height() / 2) - 12,
                        204,24), 1)
      if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255,255,255)),
                    ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
      pygame.display.flip()
      
    def question(screen): 
    
        pygame.font.init()
        current_string = []
        display_box(screen, question + ": " + string.join(current_string,""))
        while 1:
            inkey = get_key()
            if inkey == K_BACKSPACE:
                current_string = current_string[0:-1]
            elif inkey == K_RETURN:
                break
            elif inkey == K_MINUS:
                current_string.append("_")
            elif inkey <= 127:
                current_string.append(chr(inkey))
        display_box(screen, question + ": " + string.join(current_string,""))
        print string.join(current_string,"")
        
if __name__=='__main__':
   screen = pygame.display.set_mode((640,640))
   weirdo = weird(screen)
   print weird.question(screen, "Who are you:") + " was entered"

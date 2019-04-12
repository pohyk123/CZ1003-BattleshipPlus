# CZ1003 Battleship+ [Group Project]
# This file contains useful widget classes and other widget-related functions
import sys, string
import pygame

# initialise pygame
pygame.init()

# Constant values
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
BASICFONT = pygame.font.Font('freesansbold.ttf', 25)
BIGFONT = pygame.font.Font('freesansbold.ttf', 35)
TEXTCOLOR = WHITE
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = BLUE
FONT = pygame.font.Font(None, 32)
ACCEPTED = string.ascii_letters+string.digits+string.punctuation+" "

class Button():
    def __init__(self, txt, location, action, bg=WHITE, fg=BLACK, size=(150, 30), font_name="Arial", font_size=20):
        self.color = bg  #the static (normal) color
        self.bg = bg  #actual background color, can change on mouseover
        self.fg = fg  #text color
        self.size = size

        self.font = pygame.font.SysFont(font_name, font_size)
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, 1, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center=[s//2 for s in self.size])

        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(center=location)

        self.call_back_ = action

    def draw(self,display_surface):
        self.mouseover()

        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        display_surface.blit(self.surface, self.rect)

    def mousebuttondown(self,mouse_pos,**kwargs):
        if self.rect.collidepoint(mouse_pos):
            return self.call_back(**kwargs)

    def isPressed(self,mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True

    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = GREY  #mouseover color

    def update(self):
        pass

    def call_back(self,**kwargs):
        return self.call_back_(kwargs)

class InputBox():
    def __init__(self, x, y, w, h, text='',bg=WHITE):
        self.rect = pygame.Rect(x, y, w, h)

        self.color = COLOR_INACTIVE
        self.text = text
        self.surface = pygame.surface.Surface((w,h))
        self.size = (w,h)
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.bg = bg

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode in ACCEPTED:
                    self.text += event.unicode
                # Re-render the text
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, display_surface):
        self.update()
        self.surface.fill(self.bg)
        display_surface.blit(self.surface, (self.rect.x, self.rect.y))
        display_surface.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(display_surface, self.color, self.rect, 2)

def drawText(text,font,display_surface,x,y,color):
    textobj=font.render(text,True,color)
    textrect=textobj.get_rect(topleft=(x,y))
    display_surface.blit(textobj,textrect)

def mousebuttondown():
    pos = pygame.mouse.get_pos()
    for button in buttons:
        if button.rect.collidepoint(pos):
            button.call_back()

def isPressed():
    return True

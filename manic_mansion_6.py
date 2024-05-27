# Oppgave 12 IT2-eksamen høsten 2023

import pygame
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT)
import math
import random

pygame.init()
brettbredde, bretthøyde = 800, 600
Spillebrett = pygame.display.set_mode([brettbredde, bretthøyde])
pygame.display.set_caption("Manic Mansion")
font = pygame.font.SysFont("Arial", 18)

sidelengde = 35
menneskefarge = (197, 1, 117)
sauefarge = (255,255,255)
spøkelsefarge = (159,25,254)
hindringfarge = (120,120,120)
gressfarge = (78,114,0)
tryggfarge = (193,169,142)
gameover = False
objekter = [[], [], []]  #sauer, hindringer, spøkelser

def plasserSpilleobjekter(antall):
    for n in range(antall):
      objekter[0].append(Sau(random.randint(3*brettbredde//4, brettbredde-sidelengde), random.randint(0, bretthøyde-sidelengde), sauefarge, "Sau", False))
  
    for n in range(antall):
      objekter[1].append(Hindring(random.randint(brettbredde//4, 3*brettbredde//4-sidelengde), random.randint(0, bretthøyde-sidelengde), hindringfarge, "Hin"))
  
    objekter[2].append(Spøkelse(random.randint(brettbredde//4, 3*brettbredde//4-sidelengde), random.randint(0, bretthøyde-sidelengde), spøkelsefarge, "Spø", 0.2, 0.2))
  

def main():
  global gameover
  global objekter
  global font

  menneske = Menneske(brettbredde//8-sidelengde/2, bretthøyde/2, menneskefarge, "Deg",  0.5, 0, False)
  plasserSpilleobjekter(3)
  
  run = True
  while run:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run=False
    
    frisone_venstre = pygame.Rect(0, 0, brettbredde//4, bretthøyde)
    midten = pygame.Rect(brettbredde//4, 0, brettbredde/2, bretthøyde)
    frisone_høyre = pygame.Rect(3*brettbredde//4, 0, brettbredde//4, bretthøyde)
    Spillebrett.fill(tryggfarge, frisone_venstre)
    Spillebrett.fill((0,0,0), midten)
    Spillebrett.fill(gressfarge, frisone_høyre)
    poengScore = font.render(f"Poeng: {menneske.poeng}",True, (0,0,0), tryggfarge)
    Spillebrett.blit(poengScore, (5,2))
    
    tastnå = pygame.key.get_pressed() # Henter en liste med status for alle tastatur-tasteliste
    menneske.beveg(tastnå)
    menneske.plassering()
              
    #for å hindre at de lander oppå hverandre        
    for sau1 in objekter[0]:
      for sau2 in objekter[0]:
        if sau1 != sau2:
          if sau1.sjekkKollisjon(sau2):
              sau1.xPosisjon = random.randint(3*brettbredde//4, brettbredde-sidelengde)
              sau1.yPosisjon = random.randint(0, bretthøyde-sidelengde)   
    
    for hind1 in objekter[0]:
      for hind2 in objekter[0]:
        if hind1 != hind2:
          if hind1.sjekkKollisjon(hind2):
              hind1.xPosisjon = random.randint(3*brettbredde//4, brettbredde-sidelengde)
              hind1.yPosisjon = random.randint(0, bretthøyde-sidelengde)         
                
    
    for spøk in objekter[2]: 
      spøk.flyt()
      spøk.endreRetning()
      
      if menneske.sjekkKollisjon(spøk): #treffer spøkelse
        gameover = True
    
    for liste in objekter:
      for spillobjekt in liste:
        spillobjekt.plassering()
    
    if gameover == True:
      font = pygame.font.SysFont("Arial", 50)
      gameovertekst = font.render("GAME OVER", True, (255, 255, 255), (255,0,0))
      text_rect = gameovertekst.get_rect(center=(brettbredde/2,bretthøyde/2))
      Spillebrett.blit(gameovertekst, text_rect)
      poengtekst = font.render(f"Score: {menneske.poeng}", True, (0,0,0), (242,169,255))
      poengrekt = poengtekst.get_rect(center = (brettbredde/2, 2.3*bretthøyde/3))
      Spillebrett.blit(poengtekst, poengrekt)
      
    for sau in objekter[0]:
      if menneske.sjekkKollisjon(sau):
        menneske.bærerSau = True
        menneske.bærSau()
        sau.fjernSau()

    menneske.økPoeng()

    pygame.display.update()
  pygame.quit()

class SpillObjekt:
  def __init__(self, xPosisjon:int, yPosisjon:int, farge, navn):
    self.xPosisjon = xPosisjon
    self.yPosisjon = yPosisjon
    self.farge = farge
    self.navn = navn
  
  def plassering(self):
    pygame.draw.rect(Spillebrett, self.farge, (self.xPosisjon, self.yPosisjon, sidelengde, sidelengde))
    firkant = font.render(self.navn, True, (0,0,0), self.farge)
    Spillebrett.blit(firkant, (self.xPosisjon+2, self.yPosisjon+2))
    
  def sjekkKollisjon(self, objekt): #trykk Fn + F2 for å bytte ut variablene i funksjonen
    if objekt.xPosisjon + sidelengde < self.xPosisjon: #objektet er til venstre for mennesket
      return False
    elif self.xPosisjon + sidelengde < objekt.xPosisjon: #objektet er til høyre for mennesket
      return False
    elif objekt.yPosisjon + sidelengde < self.yPosisjon: #objektet er over mennesket
      return False
    elif self.yPosisjon + sidelengde < objekt.yPosisjon: #objektet er under mennesket
      return False
    else:
      return True
  
  def flytt(self):
    pass

class Menneske(SpillObjekt):
  def __init__(self, xPosisjon:int, yPosisjon:int, farge, navn, fart:int, poeng:int, bærerSau:bool):
    super().__init__(xPosisjon, yPosisjon, farge, navn)
    self.fart = fart
    self.poeng = poeng
    self.bærerSau = bærerSau
    
  def beveg(self, tasteliste):
    if not gameover:
      
      gammelx = self.xPosisjon
      gammely = self.yPosisjon
      
      if tasteliste[K_UP]:
        self.yPosisjon -= self.fart
        if self.yPosisjon <= 0:
          self.yPosisjon=0
      if tasteliste[K_DOWN]:
        self.yPosisjon += self.fart
        if self.yPosisjon >= bretthøyde - sidelengde:
          self.yPosisjon = bretthøyde - sidelengde
      if tasteliste[K_LEFT]:
        self.xPosisjon -= self.fart
        if self.xPosisjon <= 0:
          self.xPosisjon = 0
      if tasteliste[K_RIGHT]:
        self.xPosisjon += self.fart
        if self.xPosisjon >= brettbredde - sidelengde:
          self.xPosisjon = brettbredde - sidelengde
          
      for hindring in objekter[1]:
        if self.sjekkKollisjon(hindring):
          self.xPosisjon = gammelx
          self.yPosisjon = gammely
  
  def reduserFart(self):
    self.fart -= 0.05
  
  def økPoeng(self):
    if 0 < self.xPosisjon < brettbredde/4 and self.bærerSau == True:
      self.bærerSau = False
      self.navn = "Deg"
      self.poeng += 1
      print(self.poeng)
      self.fart += 0.05
      plasserSpilleobjekter(1)
  
  def bærSau(self):
    global gameover
    if self.bærerSau:
      self.navn = "D+1"
      self.fart -= 0.05
      if len(objekter[0]) == 2:
        gameover = True
        
class Spøkelse(SpillObjekt):
  def __init__(self, xPosisjon:int, yPosisjon:int, farge, navn, xfart, yfart):
    super().__init__(xPosisjon, yPosisjon, farge, navn)
    self.xfart = xfart
    self.yfart = yfart
    
  def flyt(self):
    if not gameover:
      self.xPosisjon += self.xfart
      self.yPosisjon += self.yfart
    
  def endreRetning(self):
    if (self.xPosisjon <= brettbredde // 4 or self.xPosisjon >= 3 * brettbredde // 4 - sidelengde):
      self.xfart = -self.xfart
      self.xPosisjon += self.xfart
    if (self.yPosisjon <= 0 or self.yPosisjon >= bretthøyde - sidelengde):
      self.yfart = -self.yfart
      self.yPosisjon += self.yfart

  
class Hindring(SpillObjekt):
  def __init__(self, xPosisjon:int, yPosisjon:int, farge, navn):
    super().__init__(xPosisjon, yPosisjon, farge, navn)
  
class Sau(SpillObjekt):
  def __init__ (self, xPosisjon:int, yPosisjon:int, farge, navn, blirBåret:bool):
    super().__init__(xPosisjon, yPosisjon, farge, navn)    
    self.blirBåret = blirBåret
    
  def blirLøftet(self, menneske):
    self.xPosisjon = menneske.xPosisjon + sidelengde
    self.yPosisjon = menneske.yPosisjon
  
  def fjernSau(self):
    objekter[0].remove(self)
    
main()

        
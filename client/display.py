import os.path
import pygame
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from .initial_view import InitialView
from shared.path import getScriptDirectory



class Display(object):
  def __init__(self, width=1280, height=720):
    
    self.accessibility = False
    # initializing the loop caller
    self.loop = LoopingCall(self.process)
    self.running = True
    
    self.screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Cards Against Humanity Online')
    
    # global font (may be the original from Cards Against Humanity)
    self.font = pygame.font.Font(os.path.join(getScriptDirectory(), 'assets', 'helvetica-bold.ttf'), 20)
    
    # setting the current view
    self.view = InitialView(self)
    # loading all sounds
    self.loadSounds()
  
  
  def getFont(self):
    return self.font
  
  
  def getSize(self):
    return self.screen.get_width(), self.screen.get_height()
  
  
  def handleEvent(self, event):
    if event.type == pygame.QUIT:
      self.stop()
      return
    self.view.handleEvent(event)
  
  
  def update(self):
    self.view.update()
  
  
  def render(self):
    self.screen.fill((255, 255, 255))
    self.view.render()
    pygame.display.flip()
  
  
  def process(self):
    for event in pygame.event.get():
      self.handleEvent(event)
      if not self.running:
        return
    self.update()
    self.render()
  
  
  def stop(self):
    pygame.quit()
    reactor.stop()
    self.running = False
  
  
  def init(self, accessibility = False):
    self.accessibility = accessibility
    self.loop.start(1.0 / 30.0)
    reactor.run()

  def loadSounds(self):
    # the function which builds some sounds path for us
    def sound(name):
      return pygame.mixer.Sound(os.path.join(getScriptDirectory(), 'assets', 'sound', name+'.ogg'))

    self.tap_sound = sound('tap')
    self.tap_delete_sound = sound('tap_delete')

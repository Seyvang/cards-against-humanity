import pygame
import random
from scrolled_text_panel import ScrolledTextPanel

from shared.card import CARD_WHITE, CARD_BLACK

BORDER = 5
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
BORDER_COLOR_HOVER = (255, 0, 0)
BORDER_COLOR_CHOSEN = (0, 255, 0)

TEXT_PADDING = 10



class CardSurface(pygame.Surface):
  def __init__(self, display, x, y, width, height, card_type=CARD_WHITE):
    pygame.Surface.__init__(self, (width, height))
    
    self.callback = None
    self.display = display
    self.enabled = True
    self.label = ""
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.card_type = card_type
    self.card = None
    self.chosen = False
    
    self.border = pygame.Rect(0, 0, self.width, self.height)
    if self.card_type is CARD_WHITE:
      self.color = COLOR_WHITE
      self.text_color = COLOR_BLACK
    elif self.card_type is CARD_BLACK:
      self.color = COLOR_BLACK
      self.text_color = COLOR_WHITE
    self.border_color = COLOR_BLACK
    
    self.card_text = ScrolledTextPanel(self.display, self.x + TEXT_PADDING, self.y + TEXT_PADDING, self.width - 2 * TEXT_PADDING, self.height - 2 * TEXT_PADDING, False, self.color)
    self.rect = self.get_rect()
  
  
  def addText(self, text, color=(0, 0, 0)):
    self.card_text.addText(text, color)
  
  
  def clearText(self):
    self.card_text.clearText()
  
  
  def setLabel(self, label):
    self.label = label
  
  
  def getLabel(self):
    label = ""
    if len(self.label)>0:
      label += self.label + " "

    if self.chosen:
      label += "("+self.display.translator.translate('selected')+")"

    label += ": " + self.card_text.getLabel()

    return label

  
  def setFocus(self, value):
    self.card_text.setFocus(value)
  
  
  def setSpeakLines(self, value):
    self.card_text.setSpeakLines(value)
  
  
  def getCardText(self):
    return self.card_text
  
  
  def setCard(self, card):
    
    self.clearText()
    self.card = card
    if self.card is not None:
      if card.type is CARD_BLACK:
        self.card_text.addText(card.getCardText(), COLOR_WHITE)
        self.color = COLOR_BLACK
        self.card_text.setBackgroundColor(COLOR_BLACK)
      else:
        self.card_text.addText(card.getCardText())
        self.color = COLOR_WHITE
        self.card_text.setBackgroundColor(COLOR_WHITE)
    else:
      if self.card_type is CARD_BLACK:
        self.card_text.addText(self.display.translator.translate('No card'), COLOR_WHITE)
        self.color = COLOR_BLACK
        self.card_text.setBackgroundColor(COLOR_BLACK)
      else:
        self.card_text.addText(self.display.translator.translate('No card'))
        self.color = COLOR_WHITE
        self.card_text.setBackgroundColor(COLOR_WHITE)

  
  def getCard(self):
    return self.card
  
  
  def setFont(self, font):
    self.card_text.setFont(font)
    
  
  def handleEvent(self, event):
    # only enable hover and clicking when card is enabled
    if self.getEnable():
    # hover
      if event.type == pygame.MOUSEMOTION and not self.chosen:
        if self.rect.collidepoint(event.pos[0] - self.x, event.pos[1] - self.y):
          self.border_color = BORDER_COLOR_HOVER
        else:
          self.border_color = COLOR_BLACK
      
      # click / chose
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if self.rect.collidepoint(event.pos[0] - self.x, event.pos[1] - self.y):
          if self.callback:
            self.callback()
          else:
            self.toggleChosen()
          if not self.chosen:
            self.border_color = BORDER_COLOR_HOVER
          sound = self.getClickSound()
          sound.stop()
          sound.play()

      
    self.card_text.handleEvent(event)
  
  
  def update(self):
    pass
  
  
  def render(self):
    self.fill(self.color)
    self.card_text.render()
    self.blit(self.card_text, (TEXT_PADDING, TEXT_PADDING))
    pygame.draw.rect(self, self.border_color, self.border, BORDER)

  def setCallback(self, cb):
    self.callback = cb

  def getCallback(self):
    return self.callback


  def setEnable(self, value):
    self.enabled = value


  def getEnable(self):
    return self.card is not None and self.enabled

  def toggleChosen(self):
    if self.chosen:
      self.border_color = COLOR_BLACK
    else:
      self.border_color = BORDER_COLOR_CHOSEN

    self.chosen = not self.chosen


  def getClickSound(self):
    return self.display.game_card_sounds[random.randint(0, len(self.display.game_card_sounds)-1)]

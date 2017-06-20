import pygame

BORDER = 3
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)



class GameEntry(pygame.Surface):
  def __init__(self, display, x, y, width, height, text):
    pygame.Surface.__init__(self, (width, height))
    
    self.display = display
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.new_y = self.y
    
    self.clicked = False
    
    self.border = pygame.Rect(0, 0, self.width, self.height)
    self.border_color = COLOR_BLACK
    
    self.text = text
    self.rendered_text = self.display.getFont().render(text, 1, (0, 0, 0))
    
    self.rect = self.get_rect()
  
  
  def setNewYPos(self, y):
    self.new_y = y
  
  
  def getYPos(self):
    return self.y
  
  
  def handleEvent(self, event):
    # hover
    if not self.clicked and event.type == pygame.MOUSEMOTION:
      if self.rect.collidepoint(event.pos[0] - self.x,
                                event.pos[1] - self.new_y):
        self.border_color = COLOR_RED
      else:
        self.border_color = COLOR_BLACK
    
    # click
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      if self.rect.collidepoint(event.pos[0] - self.x,
                                event.pos[1] - self.new_y):
        self.clicked = True
        self.border_color = COLOR_GREEN
      else:
        self.clicked = False
        self.border_color = COLOR_BLACK
  
  
  def update(self):
    pass
  
  
  def render(self):
    self.fill((255, 255, 255))
    pygame.draw.rect(self, self.border_color, self.border, BORDER)
    self.blit(self.rendered_text, (10, 10))


  def getLabel(self):
    return self.text

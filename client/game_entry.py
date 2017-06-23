import pygame

BORDER = 3
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)



class GameEntry(pygame.Surface):
  def __init__(self, display, x, y, width, height, id):
    pygame.Surface.__init__(self, (width, height))
    
    self.display = display
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.new_y = self.y
    
    self.id = id
    self.text = self.display.factory.findGamename(id)
    
    self.clicked = False
    
    self.border = pygame.Rect(0, 0, self.width, self.height)
    self.border_color = COLOR_BLACK
    
    self.rendered_text = self.display.getFont().render(self.text, 1, (0, 0, 0))
    
    self.rect = self.get_rect()
    self.select_callback = None
    self.deselect_callback = None
  
  
  def setNewYPos(self, y):
    self.new_y = y
  
  
  def getYPos(self):
    return self.y
  
  
  def getId(self):
    return self.id
  
  
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
        try:
          self.select_callback(self)
        except TypeError:
          pass
      else:
        self.clicked = False
        self.border_color = COLOR_BLACK
        try:
          self.deselect_callback(self)
        except TypeError:
          pass
  
  
  def update(self):
    pass
  
  
  def render(self):
    self.fill((255, 255, 255))
    pygame.draw.rect(self, self.border_color, self.border, BORDER)
    self.blit(self.rendered_text, (10, 10))


  def getLabel(self):
    return self.text


  def getSelectCallback(self):
    return self.select_callback


  def setSelectCallback(self, cb):
    self.select_callback = cb


  def getDeselectCallback(self):
    return self.deselect_callback


  def setDeselectCallback(self, cb):
    self.deselect_callback = cb


  def setClicked(self):
    self.clicked = True
    self.border_color = COLOR_GREEN


  def getClicked(self):
    return self.clicked

import pygame

import text_input

BUTTON_PADDING = 5
BUTTON_COLOR = (128, 128, 128)
BUTTON_COLOR_HOVER = (100, 100, 100)
INPUT_PADDING = 5
MOUSE_BUTTON_LEFT = 1

textmarker = (  # sized 16x24
  "ooooo ooooo     ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "     o          ",
  "ooooo ooooo     ",
  )



class Button:
  def __init__(self, display, text, font, tcolor, (x, y), width=-1, height=-1):
    # init values
    self.display = display
    # used for accessibility purposes
    self.label = text
    self.text = font.render(text, 1, tcolor)
    self.callback = None
    self.x = x
    self.y = y
    self.width = self.w = width
    self.height = self.h = height
    self.text_x = x + BUTTON_PADDING
    self.text_y = y + BUTTON_PADDING
    self.button_rect = pygame.Rect(self.x, self.y, self.w, self.h)
    self.color = BUTTON_COLOR
    self.clicked = False
    
    # calc positions and width + height
    self.setPosition((x, y))
  
  
  def getWidth(self):
    return self.w
  
  
  def getHeight(self):
    return self.h
  
  
  def setPosition(self, (x, y)):
    self.x = x
    self.y = y
    
    # if width or height == -1 -> width and height depend on text size
    if self.width == -1:
      self.w = self.text.get_width() + 2 * BUTTON_PADDING
      self.text_x = x + BUTTON_PADDING
    else:
      self.w = self.width
      self.text_x = x + self.width / 2 - self.text.get_width() / 2
    
    if self.height == -1:
      self.h = self.text.get_height() + 2 * BUTTON_PADDING
      self.text_y = y + BUTTON_PADDING
    else:
      self.h = self.height
      self.text_y = y + self.height / 2 - self.text.get_height() / 2
    
    self.button_rect = pygame.Rect(self.x, self.y, self.w, self.h)
  
  
  def handleEvent(self, event):
    # hover over button and click events
    if event.type == pygame.MOUSEMOTION and self.button_rect.collidepoint(
            event.pos):
      self.color = BUTTON_COLOR_HOVER
    
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == \
            MOUSE_BUTTON_LEFT and self.button_rect.collidepoint(event.pos):
      self.display.button_up_sound.stop()
      self.display.button_up_sound.play()
      self.color = BUTTON_COLOR_HOVER
      self.clicked = True
    
    elif event.type == pygame.MOUSEBUTTONUP and event.button == \
            MOUSE_BUTTON_LEFT and self.button_rect.collidepoint(event.pos):
      self.display.button_down_sound.stop()
      self.display.button_down_sound.play()
      self.color = BUTTON_COLOR_HOVER
      if self.clicked:
        if self.callback:
          self.callback()
        self.clicked = False
    
    else:
      self.color = BUTTON_COLOR
      self.clicked = False
  
  
  def render(self):
    pygame.draw.rect(self.display.screen, self.color, self.button_rect, 0)
    self.display.screen.blit(self.text, (self.text_x, self.text_y))
  
  
  def setLabel(self, text):
    self.label = text
  
  
  def getLabel(self):
    return self.label + " button"
  
  
  def setCallback(self, cb):
    self.callback = cb
  
  
  def getCallback(self):
    return self.callback



# own TextInput class, which we added a rectangle
class TextInput:
  def __init__(self, display, font, (x, y), width, label=''):
    self.label = label
    self.display = display
    self.x = x + INPUT_PADDING
    self.y = y
    self.rect_color = (0, 0, 0)
    self.focus = False
    self.cursor_size = (16, 24)
    self.cursor_hotspot = (6, 12)
    self.cursor = pygame.cursors.compile(textmarker)
    self.cursor_is_textmarker = False
    self.clicked = False
    
    # to get the height of text with this font
    text_height = font.size("Dummy")[1]
    
    self.input = text_input.TextInput(self.display, font,
                                      max_width=width - 2 * INPUT_PADDING)
    self.x_end = x + width
    self.y_end = y + text_height + 2 * INPUT_PADDING
    self.input_rect = pygame.Rect(x, y - INPUT_PADDING, width,
                                  text_height + 2 * INPUT_PADDING)
  
  
  def setFocus(self, flag):
    self.focus = flag
    self.input.setFocus(flag)
  
  
  def handleEvent(self, event):
    self.input.handleEvent(event)
    
    # change cursor type when hovering over text input
    if event.type == pygame.MOUSEMOTION:
      if not self.cursor_is_textmarker and self.input_rect.collidepoint(
              event.pos):
        pygame.mouse.set_cursor(self.cursor_size, self.cursor_hotspot,
                                *self.cursor)
        self.cursor_is_textmarker = True
      
      elif self.cursor_is_textmarker and not self.input_rect.collidepoint(
              event.pos):
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        self.cursor_is_textmarker = False
    
    # set focus if clicked
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == \
            MOUSE_BUTTON_LEFT and self.input_rect.collidepoint(event.pos):
      self.clicked = True
    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and \
            self.input_rect.collidepoint(event.pos):
      if self.clicked:
        self.setFocus(True)
      self.clicked = False
      # self.rect_color = (255, 0, 0) # debug
    
    # if left mouse button clicked anywhere else, focus is gone ("dirty"
    # solution)
    elif event.type == pygame.MOUSEBUTTONUP and event.button == \
            MOUSE_BUTTON_LEFT and not self.input_rect.collidepoint(event.pos):
      self.setFocus(False)
      self.clicked = False
      # self.rect_color = (0, 0, 0)  # debug
    else:
      self.clicked = False
  
  
  def update(self):
    self.input.update()
  
  
  def render(self):
    self.display.screen.blit(self.input.render(), (self.x, self.y))
    pygame.draw.rect(self.display.screen, self.rect_color, self.input_rect, 1)
  
  
  def setLabel(self, text):
    self.label = text
  
  
  def getLabel(self):
    label = self.label + " input: "
    if self.input.get_text() == '':
      label += "empty"
    else:
      label += self.input.get_text()
    return label

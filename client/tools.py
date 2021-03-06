import pygame

import text_input

BUTTON_PADDING = 5
BUTTON_COLOR = (128, 128, 128)
BUTTON_COLOR_HOVER = (100, 100, 100)
BUTTON_COLOR_DISABLED = (192, 192, 192)
BUTTON_TEXT_COLOR = (0, 0, 0)
BUTTON_TEXT_COLOR_DISABLED = (96, 96, 96)
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
  def __init__(self, display, text, font, (x, y), width=-1, height=-1):
    # label used for accessibility purposes
    # init values
    self.enable = True
    self.focus = False
    self.display = display
    self.text = text
    self.font = font
    self.text_color = BUTTON_TEXT_COLOR
    self.callback = None
    self.x = x
    self.y = y
    self.width = self.w = width
    self.height = self.h = height
    self.text_x = x + BUTTON_PADDING
    self.text_y = y + BUTTON_PADDING
    self.button_rect = pygame.Rect(self.x, self.y, self.w, self.h)
    self.border_rect = pygame.Rect(self.x, self.y, self.w, self.h)
    self.color = BUTTON_COLOR
    self.mouse_hover = False
    self.clicked = False
    
    # calc positions and width + height
    self.setPosition((x, y), width, height)
  
  
  def getWidth(self):
    return self.w
  
  
  def getHeight(self):
    return self.h
  
  
  def setPosition(self, (x, y), width=-1, height=-1):
    self.x = x
    self.y = y
    self.setWidthHeight(width, height)
    
    
  def setWidthHeight(self, width = -1, height = -1):
    self.width = width
    self.height = height
    
    # if width or height == -1 -> width and height depend on text size
    if self.width == -1:
      self.w = self.font.size(self.text)[0] + 2 * BUTTON_PADDING
      self.text_x = self.x + BUTTON_PADDING
    else:
      self.w = self.width
      self.text_x = self.x + self.width / 2 - self.font.size(self.text)[0] / 2
    
    if self.height == -1:
      self.h = self.font.size(self.text)[1] + 2 * BUTTON_PADDING
      self.text_y = self.y + BUTTON_PADDING
    else:
      self.h = self.height
      self.text_y = self.y + self.height / 2 - self.font.size(self.text)[1] / 2
    
    self.button_rect = pygame.Rect(self.x+1, self.y+1, self.w-2, self.h-2)
    self.border_rect = pygame.Rect(self.x, self.y, self.w, self.h)
  
  
  def changeText(self, text):
    self.text = text
    self.setWidthHeight()
    
  
  def handleEvent(self, event):
    # set colors of button and text depending on whether enabled or not
    if not self.enable:
      self.color = BUTTON_COLOR_DISABLED
      self.text_color = BUTTON_TEXT_COLOR_DISABLED
      return
    else:
      self.color = BUTTON_COLOR
      self.text_color = BUTTON_TEXT_COLOR
    
    # hover over button and click events
    if event.type == pygame.MOUSEMOTION and self.button_rect.collidepoint(
            event.pos):
      self.mouse_hover = True
    
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == \
            MOUSE_BUTTON_LEFT and self.button_rect.collidepoint(event.pos):
      self.getClickSound().stop()
      self.getClickSound().play()
      self.clicked = True
    
    elif event.type == pygame.MOUSEBUTTONUP and event.button == \
            MOUSE_BUTTON_LEFT and self.button_rect.collidepoint(event.pos):
      self.display.button_down_sound.stop()
      self.display.button_down_sound.play()
      if self.clicked:
        if self.callback:
          self.callback()
        self.clicked = False
        
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == \
            MOUSE_BUTTON_LEFT and not self.button_rect.collidepoint(event.pos):
      self.focus = False
      
    else:
      self.color = BUTTON_COLOR
      self.clicked = False
      self.mouse_hover = False
  
  
  def update(self):
    if self.enable:
      if self.focus or self.mouse_hover:
        self.color = BUTTON_COLOR_HOVER
      else:
        self.color = BUTTON_COLOR
  
  
  def render(self):
    text = self.font.render(self.text, 1, self.text_color)
    pygame.draw.rect(self.display.screen, (0, 0, 0), self.border_rect, 2)
    if self.clicked:
      pygame.draw.rect(self.display.screen, self.color, (self.button_rect[0] +1, self.button_rect[1] +1, self.button_rect[2], self.button_rect[3]), 0)
      self.display.screen.blit(text, (self.text_x+1, self.text_y+1))
    else:
      pygame.draw.rect(self.display.screen, self.color, self.button_rect, 0)
      self.display.screen.blit(text, (self.text_x, self.text_y))
  
  
  def getLabel(self):
    label = self.text + " "+self.display.translator.translate("button")
    if not self.getEnable():
      label += " ("+self.display.translator.translate("disabled")+")"
    return label
  
  
  def setCallback(self, cb):
    self.callback = cb
  
  
  def getCallback(self):
    return self.callback
  
  
  def getEnable(self):
    return self.enable
  
  
  def setEnable(self, value):
    self.enable = value

  def getClickSound(self):
    return self.display.button_up_sound
  
  
  def setFocus(self, flag):
    self.focus = flag
    
    
  def getFocus(self):
    return self.focus



# own TextInput class, which we added a rectangle
class TextInput:
  def __init__(self, display, font, (x, y), width, label='', password=False, only_digits = False):
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
                                      max_width=width - 2 * INPUT_PADDING, password = password, only_digits = only_digits)
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
      self.display.view.setNewTabPosition(self.display.view.getTabOrder().index(self))
    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and \
            self.input_rect.collidepoint(event.pos):
      if self.clicked:
        self.setFocus(True)
      self.clicked = False
    
    # if left mouse button clicked anywhere else, focus is gone ("dirty"
    # solution)
    elif event.type == pygame.MOUSEBUTTONUP and event.button == \
            MOUSE_BUTTON_LEFT and not self.input_rect.collidepoint(event.pos):
      self.setFocus(False)
      self.clicked = False
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
    label = self.label + " "+self.display.translator.translate("input")+": "
    if self.input.get_text() == '':
      label += self.display.translator.translate("empty")
    else:
      label += self.input.getPrintText()
    return label


  def setText(self, text):
    self.input.input_string = text
    self.input.cursor_position = len(text)

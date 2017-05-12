from .scrolled_text_panel import ScrolledTextPanel
from .tools import *
from .view import View

PADDING_LEFT_RIGHT = 20
PADDING_TOP_BOTTOM = 20



# function for blurring a surface through smoothscaling to lower resolution
# and back to original
def blurSurf(surface, val=2.0):
  """
  Blur the given surface by the given 'amount'.  Only values 1 and greater
  are valid.  Value = 1 -> no blur.
  """
  if val < 1.0:
    raise ValueError(
      "Arg 'val' must be greater than 1.0, passed in value is %s" % val)
  scale = 1.0 / float(val)
  surf_size = surface.get_size()
  scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
  surf = pygame.transform.smoothscale(surface, scale_size)
  surf = pygame.transform.smoothscale(surf, surf_size)
  return surf



class MessageView(View):
  def __init__(self, display, width=480, height=480, maxheight=640):
    View.__init__(self, display)
    
    self.display = display
    self.width = width
    self.height = height
    self.maxheight = maxheight
    self.setHeight(height)
    self.old_screen = display.screen.copy()
    self.old_screen.set_alpha(86)
    self.old_screen = blurSurf(self.old_screen)
    self.display_size = display.getSize()
    self.hmiddle = self.display_size[0] / 2
    self.vmiddle = self.display_size[1] / 2
    self.button = None
    
    self.text = ""
    self.message_box = pygame.Surface((width, self.height))
    self.message_border = pygame.Rect(0, 0, width, self.height)
    
    self.box_x = self.hmiddle - width / 2
    self.box_y = self.vmiddle - height / 2
    
    dummy_text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, " \
                 "sed diam nonumy eirmod tempor invidunt ut labore et dolore " \
                 "magna aliquyam erat, sed diam voluptua. At vero eos et " \
                 "accusam et justo duo dolores et ea rebum. Stet clita kasd " \
                 "gubergren, no sea takimata sanctus est Lorem ipsum dolor " \
                 "sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing " \
                 "elitr, sed diam nonumy eirmod tempor invidunt ut labore et " \
                 "dolore magna aliquyam erat, sed diam voluptua. At vero eos " \
                 "et accusam et justo duo dolores et ea rebum. Stet clita " \
                 "kasd gubergren, no sea takimata sanctus est Lorem ipsum " \
                 "dolor sit amet."
    self.setText(dummy_text)
  
  
  # setting some automatically formatted and rendered text onto the screen
  def setText(self, text):
    self.text = text
    
    self.scrolled_text = ScrolledTextPanel(self.message_box, self.text,
                                           PADDING_LEFT_RIGHT,
                                           PADDING_TOP_BOTTOM,
                                           self.width - 2 * PADDING_LEFT_RIGHT,
                                           self.height - 2 * PADDING_TOP_BOTTOM)
    button_height = 0
    if self.button is not None:
      button_height = self.button.getHeight() + PADDING_TOP_BOTTOM
    # calculate new height through the text and adjust the message box
    self.setHeight(self.scrolled_text.getHeight() + button_height + 2 * \
                   PADDING_TOP_BOTTOM)
    self.message_box = pygame.Surface((self.width, self.height))
    self.message_border = pygame.Rect(0, 0, self.width, self.height)
    self.box_y = self.vmiddle - self.height / 2
    self.scrolled_text.setNewScreen(self.message_box)
  
  
  # may display a button (not needed)
  # window may also exist without any button
  # if callback is None, the button will be removed
  # otherwise it will be created
  def setButton(self, text="", callback=None):
    if callback is not None:
      self.button = Button(self.display, text, self.display.getFont(),
                           (100, 100))
      self.button.setPosition(
        (self.hmiddle + self.width / 2 - self.button.getWidth() -
         PADDING_LEFT_RIGHT,
         self.vmiddle + self.height / 2 - self.button.getHeight() -
         PADDING_TOP_BOTTOM))
      self.button.setCallback(callback)
      # need to call setText as you can call setButton from external; after that
      # we got a new height, so we need to position the buton again
      self.setText(self.text)
      self.button.setPosition(
        (self.hmiddle + self.width / 2 - self.button.getWidth() -
         PADDING_LEFT_RIGHT,
         self.vmiddle + self.height / 2 - self.button.getHeight() -
         PADDING_TOP_BOTTOM))
  
  
  # handy mehtod to check maxheight befor setting height
  def setHeight(self, new_height):
    if new_height > self.maxheight:
      self.height = self.maxheight
    else:
      self.height = new_height
  
  
  def render(self):
    self.display.screen.blit(self.old_screen, (0, 0))
    self.message_box.fill((255, 255, 255))
    pygame.draw.rect(self.message_box, (0, 0, 0), self.message_border, 3)
    self.scrolled_text.render()
    self.display.screen.blit(self.message_box, (self.box_x, self.box_y))
    if self.button is not None:
      self.button.render()
  
  
  def handleEvent(self, event):
    if self.button is not None:
      self.button.handleEvent(event)

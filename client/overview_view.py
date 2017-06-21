from .view import View
from .tools import Button, TextInput
from .scrolled_panel import ScrolledPanel
from .game_entry import GameEntry

import pygame

PADDING = 20



class OverviewView(View):
  def __init__(self, display):
    View.__init__(self, display)
    
    self.display = display
    self.screen_size = self.display.getSize()
    self.font = self.display.getFont()
    
    self.label_game_name = self.font.render("Game name:", 1, (0, 0, 0))
    self.input_game_name = TextInput(self.display, self.font, (20, 50), 300, "Game name")
    self.label_game_password = self.font.render("Game password (optional):", 1, (0, 0, 0))
    self.input_game_password = TextInput(self.display, self.font, (20, 130), 300, "Game password", True)

    self.button_create = Button(self.display, "Create Game", self.font, (20, 200))
    self.button_join = Button(self.display, "Join Game", self.font, (20, 250))
    self.button_close = Button(self.display, "Close Game Client", self.font, (20, self.screen_size[1] * 0.5))

    self.surface_overview = pygame.Surface((self.screen_size[0] - 340, self.screen_size[1] * 0.5))
    self.overview_border = pygame.Rect(0, 0, self.surface_overview.get_width(), self.surface_overview.get_height())
    self.game_overview = ScrolledPanel(self.display, 340 + PADDING, PADDING, self.surface_overview.get_width() - 2 * PADDING, self.surface_overview.get_height() - 2 * PADDING)

    self.next_surface_pos_y = self.game_overview.getPos()[1]

    #self.addGame(1)
    #self.addGame(2)
    #self.addGame(3)
    #self.addGame(4)
    #self.addGame(5)
    #self.addGame(6)
    #self.addGame(7)
    #self.addGame(8)
    #self.deleteGame(8)
    #self.deleteGame(3)
    #self.deleteGame(5)
    #self.deleteGame(6)
    #self.deleteGame(1)
    #self.deleteGame(2)
  
  
  def addGame(self, game_id):
    game_entry = GameEntry(self.display, self.game_overview.getPos()[0], self.next_surface_pos_y, self.game_overview.getAvailableWidth() - 20, 50, game_id)
    self.game_overview.addSurface(game_entry)
    self.next_surface_pos_y += game_entry.get_height() + self.game_overview.getVSpace()
  
  
  def clearGames(self):
    self.game_overview.clearSurfaces()
    self.next_surface_pos_y = self.game_overview.getPos()[1]
  
  
  def deleteGame(self, game_id):
    tmp_surfaces = self.game_overview.getSurfaces()
    self.clearGames()
    for surface in tmp_surfaces:
      if surface.getID() != game_id:
        self.addGame(surface.getID())
  
  
  def handleEvent(self, event):
    self.input_game_name.handleEvent(event)
    self.input_game_password.handleEvent(event)
    
    self.button_create.handleEvent(event)
    self.button_join.handleEvent(event)
    self.button_close.handleEvent(event)
    
    self.game_overview.handleEvent(event)
    
    
  def update(self):
    pass
  
  
  def render(self):
    self.display.screen.blit(self.label_game_name, (20, 20))
    self.input_game_name.render()
    self.display.screen.blit(self.label_game_password, (20, 100))
    self.input_game_password.render()
    
    self.button_create.render()
    self.button_join.render()
    self.button_close.render()
    
    self.surface_overview.fill((255, 255, 255))
    pygame.draw.rect(self.surface_overview, (0, 0, 0), self.overview_border, 5)
    self.display.screen.blit(self.surface_overview, (340, 0))
    self.game_overview.render()
    self.display.screen.blit(self.game_overview, self.game_overview.getPos())
#!/usr/bin/python
# -*- coding: utf-8 -*-

from card_panel import CardPanel
from cardlist_toolbar import CardListToolbar
from const import *

# from shared.card import CARD_BLACK

# elements have the border on all sides and are centered only horizontally
FLAG = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL


class CardListWindow(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent=parent,
                      name="card list panel (this is a name")

    self.toolbar = CardListToolbar(self)
    self.card_grid = ScrolledGrid(self)

    self.vbox = wx.BoxSizer(wx.VERTICAL)
    self.vbox.Add(self.toolbar, proportion=0, flag=wx.EXPAND)
    self.vbox.Add(self.card_grid, proportion=1, flag=wx.EXPAND)

    self.SetSizer(self.vbox)
    self.SetMinSize((755, -1))
    self.SetLabel("card list panel(this is a label)")
    self.SetBackgroundColour("black")


class ScrolledGrid(wx.ScrolledWindow):
  def __init__(self, parent):
    wx.ScrolledWindow.__init__(self, parent=parent,
                               name="card list grid(this is a name",
                               style=wx.FULL_REPAINT_ON_RESIZE)

    self.initialized = False

    self.SetLabel("no cards found")
    self.SetBackgroundColour("white")

    # next 2 just for initialization (don't ask about the numbers)
    self.grid = wx.GridSizer(0, 5, 0, 0)
    self.Height = 500
    self.card_count = 0

    # def buildList(self):
    # create list with dummy objects
    # for _ in itertools.repeat(None, 55):
    #  panel = wx.Panel(self, size=(ELEMENT_SIZE, ELEMENT_SIZE),
    #                                   name="Dummy")
    #  panel.SetBackgroundColour("black")
    #  self.item_list.append((panel, 0, FLAG, BORDER))

  # def BuildItemList(self, card_list):
  #   item_list = []
  #
  #   for i in range(len(card_list)):
  #     card = card_list[i]
  #     #panel = wx.Panel(parent=self, size=(ELEMENT_SIZE, ELEMENT_SIZE),
  #     #                            name=("card " + `i+1`),
  #     #                            style=wx.SIMPLE_BORDER)
  #     text = wx.TextCtrl(parent=self, id=i, size=(ELEMENT_SIZE, ELEMENT_SIZE),
  #                                   style=wx.EXPAND | wx.TE_READONLY,
  #                                   name=("text of card " + `i+1`),
  #                                   value=card.getCardText())
  #     #card_texts[i].CenterOnParent()
  #     if card.type == CARD_BLACK:
  #       #panel.SetBackgroundColour("black")
  #       text.SetBackgroundColour("black")
  #       text.SetForegroundColour("white")
  #     else:
  #       #panel.SetBackgroundColour("white")
  #       text.SetBackgroundColour("white")
  #       text.SetForegroundColour("black")
  #
  #     item_list.append((text, 0, FLAG, BORDER))
  #
  #
  #   return item_list


  def calcBestColumns(self, available_height):
    # this method calculates the number of columns depending on the existence of
    #   a scrollbar, which again depends on the number of elements that fits the
    #   available screen
    # it's kind of a mastermind-method^^ ;)

    # at first calculate columns from the available width and let the grid calc
    #   the rows
    columns = self.ClientSize.width / FULL_ELEMENT
    rows = 0
    self.grid.SetCols(columns)
    (rows, columns) = self.grid.CalcRowsCols()

    # then calculate the possible row from the available height
    possible_rows = available_height / FULL_ELEMENT

    # if rows > possible rows -> there are more rows than rows fitting the
    #   current screen -> scrollbar is needed -> width - 20px as the scrollbar
    #   takes 20 px
    if rows > possible_rows:
      columns = (self.ClientSize.width - 20) / FULL_ELEMENT

    # finally also set the number of columns and return them just to be on the
    #   safe side
    self.grid.SetCols(columns)
    return columns

  def createGrid(self, available_height=-1):
    # this method creates the actual grid with the items

    # if available_height isn't given we automatically use the top-level frame's
    # client size
    if available_height == -1:
      available_height = self.GetTopLevelParent().ClientSize.height

    self.initialized = True

    columns = self.calcBestColumns(available_height)

    # calc and set the virtual height to make the window scrollable
    self.Height = (self.card_count / columns) * FULL_ELEMENT
    self.SetVirtualSize((0, self.Height))
    self.SetScrollRate(10, 20)

    # need a horizontal box sizer to make the grid horizontal flexible; i don't
    #   know exactly why, but it works^^
    # otherwise the elements are also centered vertically
    box = wx.BoxSizer(wx.HORIZONTAL)
    box.Add(self.grid, proportion=1)
    self.SetSizer(box, True)

  def addCard(self, id, text, card_type):
    card = CardPanel(self, card_id=id, text=text, card_type=card_type)
    # box = wx.BoxSizer()
    # box.Add(card)
    self.grid.Add(card, 1,  # wx.EXPAND |
                  wx.ALL,
                  BORDER)  # if no wx.EXPAND, you only see the texts in the first column
    # however, it's fixed now

    self.card_count += 1

    return card

  def clearCards(self):
    self.card_count = 0
    for child in self.grid.GetChildren():
      self.grid.Remove(child.Window)
      child.Window.Destroy()
      del child
    self.grid.Layout()

  # retrieves the panel related to a Card object
  def getCard(self, card):

    for child in self.grid.GetChildren():
      if isinstance(child.Window,
                    CardPanel) and child.Window.card.id == card.id:
        return child.Window

    return None

  # deletes the panel related to a card object
  def deleteCard(self, card):

    panel = self.getCard(card)

    if panel is not None:
      self.grid.Remove(panel)
      panel.Destroy()
      del panel
      self.Layout()

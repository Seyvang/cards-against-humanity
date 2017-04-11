#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

APP_EXIT = 1


class CardListPanel(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent=parent)

    self.SetBackgroundColour("white")


class CurrCardPanel(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent=parent)

    self.SetBackgroundColour("white")


class MainFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, title="Card Editor",
                      size=(1280, 720))

    self.initUI()
    self.Centre()

    splitter = wx.SplitterWindow(self,
                                 style=wx.SP_LIVE_UPDATE)
    left_panel = CardListPanel(splitter)
    right_panel = CurrCardPanel(splitter)

    # split the window
    splitter.SplitVertically(left_panel, right_panel, 320)
    splitter.SetMinimumPaneSize(160)
    splitter.SetSashGravity(0.5)


  def initUI(self):
    menubar = wx.MenuBar()
    file_menu = wx.Menu()
    # menu_item = file_menu.Append(wx.ID_EXIT, 'Quit',
    #                              'Quit application')
    menu_item = wx.MenuItem(file_menu, APP_EXIT,
                            '&Quit\tCtrl+Q')
    file_menu.AppendItem(menu_item)

    self.Bind(wx.EVT_MENU, self.onQuit, id=APP_EXIT)
    menubar.Append(file_menu, '&File')
    self.SetMenuBar(menubar)

    # self.Bind(wx.EVT_MENU, self.onQuit, menu_item)

  def onQuit(self, e):
    self.Close()


def main():
  app = wx.App(False)
  frame = MainFrame()
  frame.Show()
  app.MainLoop()


if __name__ == '__main__':
  main()

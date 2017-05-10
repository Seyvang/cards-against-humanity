import sys

import pygame
from twisted.logger import globalLogBeginner, textFileLogObserver

from .display import Display
from .login_view import LoginView



def main(accessibility=False):
  pygame.mixer.pre_init(frequency=44100, buffer=1024)
  pygame.init()
  pygame.font.init()
  globalLogBeginner.beginLoggingTo([textFileLogObserver(sys.stdout)])
  
  display = Display(accessibility = accessibility)
  display.setView(LoginView)
  display.init()

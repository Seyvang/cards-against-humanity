import os.path
import sys
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from twisted.logger import globalLogBeginner, Logger, textFileLogObserver

from .factory import ServerFactory
from . import version
from shared.path import getScriptDirectory

def main():
  log = Logger()
  globalLogBeginner.beginLoggingTo([textFileLogObserver(sys.stdout)])

  log.info("Starting cards-against-humanity server version {major}.{minor}.{revision}", major=version.MAJOR, minor=version.MINOR, revision=version.REVISION)

  if not os.path.exists(os.path.join(getScriptDirectory(), "cards.db")):
    log.error("No card database found. Please consider getting one of the card databases available online or create your own using the cards-against-humanity card manager")
    sys.exit()

  endpoint = TCP4ServerEndpoint(reactor, 11337)
  endpoint.listen(ServerFactory())
  reactor.run()

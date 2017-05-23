from .user import User
from . import version
from shared.messages import *
from shared.protocol import JSONReceiver

class ServerProtocol(JSONReceiver):

  def __init__(self,factory):
    JSONReceiver.__init__(self, factory)
    self.addCallback(MODE_CLIENT_AUTHENTIFICATION, MSG_CLIENT_AUTHENTIFICATION, self.clientAuthentification)
    self.addCallback(MODE_USER_AUTHENTIFICATION, MSG_USER_AUTHENTIFICATION, self.userAuthentification)
    self.addCallback(MODE_INITIAL_SYNC, MSG_DATABASE_QUERY, self.databaseQuery)
    self.addCallback(MODE_INITIAL_SYNC, MSG_DATABASE_PULL, self.databasePull)
    self.addCallback(MODE_INITIAL_SYNC, MSG_DATABASE_KNOWN, self.databaseKnown)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_CREATE_GAME, self.createGame)
    self.addCallback(MODE_FREE_TO_JOIN, MSG_JOIN_GAME, self.joinGame)
    self.setMode(MODE_CLIENT_AUTHENTIFICATION)
    self.user = User(self)

  def connectionMade(self):
    self.identification = self.transport.getPeer().host
    self.log.info("{log_source.identification!r} established connection")

  def userAuthentification(self, username, password):
    if len(username)<6 or len(username)>30 or len(password)!=128:
      self.log.warn('{log_source.identification!r} username or password with incorrect length specified')
      self.sendMessage(MSG_USER_LOGIN, success=False, message='invalid username or password specified')
      return
    if not self.user.exists(username):
      registration = True
      result = self.user.register(username, password)
      self.log.info('{log_source.identification!r} {message}', message=result['message'])
      self.sendMessage(MSG_USER_REGISTRATION, **result)
      if not result['success']:
        self.transport.loseConnection()
        return
    result = self.user.login(username, password)
    if result['success']:
      self.identification = self.user.name
      self.setMode(MODE_INITIAL_SYNC)
    self.log.info('{log_source.identification!r} {message}', message=result['message'])
    self.sendMessage(MSG_USER_LOGIN, **result)
    if not result['success']:
      self.transport.loseConnection()
 
  def clientAuthentification(self, major, minor, revision):
    self.log.info('{log_source.identification!r} using client version {major}.{minor}.{revision}', major=major, minor=minor, revision=revision)
    if major < version.MAJOR or minor < version.MINOR:
      self.log.info('incompatible client version, connection refused')
      self.sendMessage(MSG_CLIENT_REFUSED, reason='incompatible client and server versions')
      self.transport.loseConnection()
    else:
      self.sendMessage(MSG_CLIENT_ACCEPTED)
      self.setMode(MODE_USER_AUTHENTIFICATION)

  def databaseQuery(self):
    self.sendMessage(MSG_DATABASE_QUERY, hash=self.factory.card_database.hash)

  def databasePull(self):
    self.log.info("{log_source.identification!r} requests card database")
    self.sendMessage(MSG_DATABASE_PUSH, size=self.factory.card_database.size)
    self.sendRawData(self.factory.card_database.data)

  def databaseKnown(self):
    self.log.info("{log_source.identification!r} knows current card database")
    self.sendMessage(MSG_SYNC_FINISHED)
    self.setMode(MODE_FREE_TO_JOIN)

  def createGame(self, name, password = None):
    if len(name)==0 or len(name)>30 or (password is not None and len(password)!=128):
      self.sendMessage(MSG_CREATE_GAME, success=False, message='invalid name or password')
      self.log.warn("{log_source.identification!r} tried to create game with invalid name {name} or password", name=name)
      return
    if self.factory.card_database.max_players_per_game < 3:
      self.sendMessage(MSG_CREATE_GAME, success=False, message='not enough cards available to create a game')
      self.log.warn("{log_source.identification!r} tried to create a game, but not enough cards available")
      return
    game = self.factory.createGame(name, password)
    self.sendMessage(MSG_CREATE_GAME, success=True, id=game.id)
    self.log.info("{log_source.identification!r} created new game {name} with id {id}", name=name, id = game.id)

  def joinGame(self, id, password = None):
    game = self.factory.findGame(id)
    if not game:
      self.sendMessage(MSG_JOIN_GAME, success = False, message='game not found')
      self.log.warn("{log_source.identification!r} tried to join non-existant game")
      return
    result = game.join(self.user, password)
    if not result['success']:
      self.log.info("{log_source.identification!r} failed to join game {id}: {message}", id = game.id, message = result['message'])
    else:
      self.log.info("{log_source.identification!r} joined game {id}", id = game.id)
      self.setMode(MODE_IN_GAME)
    self.sendMessage(MSG_JOIN_GAME, **result)

  def connectionLost(self, reason):
    self.log.info('{log_source.identification!r} lost connection')
    self.log.debug(reason.getErrorMessage())
    self.user.unlink()

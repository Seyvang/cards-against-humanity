import copy
import json
import random
import uuid

from twisted.logger import Logger

from . import version

class Game(object):
  log = Logger()

  def __init__(self, factory):
    self.factory = factory
    self.black_cards = []
    self.database_hash = None
    self.name = ''
    self.open = True
    self.password_hash = None
    self.running = False
    self.uuid = None
    self.users = []
    self.white_cards = []

  @classmethod
  def create(cls, factory, name, password_hash = None):
    game = cls(factory)
    game.database_hash = factory.card_database.hash
    game.name = name
    game.password_hash = password_hash
    game.uuid = uuid.uuid4()
    game.loadCards()
    return game

  @classmethod
  def load(cls, factory, **data):
    game = cls(factory)
    game.name = data['name']
    game.password_hash = data['password_hash'] if len(data['password_hash']) else None
    game.open = False
    game.database_hash = data['database_hash']
    game.uuid = uuid.UUID(data['id'])

    game.users = json.loads(data['users'])
    for user in game.users:
      user['joined'] = False
      user['white_cards'] = [factory.card_database.getCard(c) for c in user['white_cards']]

    game.white_cards = [factory.card_database.getCard(c) for c in json.loads(data['cards'])['white_cards']]
    game.black_cards = [factory.card_database.getCard(c) for c in json.loads(data['cards'])['black_cards']]

    return game

  def loadCards(self):

    self.black_cards = self.factory.card_database.getBlackCards()
    random.shuffle(self.black_cards)

    self.white_cards = self.factory.card_database.getWhiteCards()
    random.shuffle(self.white_cards)

  def mayJoin(self, user):
    if user.getGame() is not None:
      return self.formatted(join = False, message = 'already in another game')
    if self.running:
      return self.formatted(join = False, message = 'game already running')
    if self.open:
      if len(self.users) + 1 > self.factory.card_database.max_players_per_game:
        return self.formatted(join=False, message='no more players allowed')
      return self.formatted(join=True)
    else:
      possible_users = [u for u in self.users if u['user'] == user.id]

      if len(possible_users) != 1:
        return self.formatted(join = False, message = 'you are no member of this paused game')

      if possible_users[0]['joined']:
        return self.formatted(join = False, message = 'already joined this game')

      return self.formatted(join = True)

  def join(self, user, password):
    joinable = self.mayJoin(user)
    if not joinable['join']:
      return self.formatted(success=False, message=joinable['message'])
    if self.protected and password != self.password_hash:
      return self.formatted(success=False, message='wrong password supplied')

    if self.open:
      self.users.append(self.userdict(user))
      user.setGame(self)
    else:
      possible_users = [u for u in self.users if u['user'] == user.id and not u['joined']]
      possible_users[0]['joined'] = True
      user.setGame(self)

    return self.formatted(success=True, game_id = self.id)

  def getAllUsers(self):
    return [self.factory.findUser(u['user']) for u in self.users if u['joined']]

  def start(self):
    if len(self.getAllUsers())<3:
      return self.formatted(success=False, message='not enough players in this game')

    if self.running:
      return self.formatted(success=False, message='already running')

    # if the game is currently open, we need to shuffle the users
    if self.open:
      random.shuffle(self.users)
      self.open = False

    self.open = False
    self.running = True

    # all users need to get 10 cards
    for i in range(len(self.users)*10):
      self.users[i/10]['white_cards'].append(self.white_cards[i])
    self.white_cards=self.white_cards[len(self.users)*10:]

    # determine the one with the black card
    # index at 0 will always be the czar
    # and black_cards 0 will always be the current black card

    return self.formatted(success=True)

  def getCurrentBlackCard(self):
    return self.black_cards[0]

  def getAllWhiteCardsForUsers(self):
    return [(self.factory.findUser(self.users[i]['user']), self.users[i]['white_cards']) for i in range(len(self.users))]

  def disconnect(self, user):

    self.pause()

    if user.getGame() is not self:
      self.log.warn('user {user} not in game {game}', user = user.id, game = self.id)
      return

    possible_users = [u for u in self.users if u['user'] == user.id and u['joined']]
    if len(possible_users) != 1:
      self.log.warn('found {count} users in game {game} while disconnecting user {user}', count = len(possible_users), game = self.id, user = user.id)
    else:
      possible_users[0]['joined'] = False
      user.setGame(None)
      self.log.info('user {user} disconnected from game {game}', user = user.id, game = self.id)

  def leave(self, user):
    # forces the user to leave

    if user.getGame() is not self:
      return self.formatted(success = False, message = 'user is not in this game')

    users = self.getAllUsers()
    if len(users) == 0:
      self.log.warn('no users in this game, {user} tried to leave', user = user.id)
      return self.formatted(success = False, message = 'no users found in this game')

    # users which are the current czar in this running game can't leave
    if users[0] == user and self.running:
      self.log.info('czar {user} tried to leave the game, but this is not possible', user = user.id)
      return self.formatted(success = False, message = 'the czar cannot leave the game')

    possible_users = [u for u in self.users if u['user'] == user.id and u['joined']]

    if len(possible_users) != 1:
      self.log.warn('{user} tried to leave game {game}, but found {count} possible users', user = user.id, game = self.id, count = len(possible_users))
      return self.formatted(success = False, message = 'unable to find user in this game')

    del self.users[self.users.index(possible_users[0])]
    user.setGame(None)
    self.log.info('user {user} left game {game}', user = user.id, game = self.id)

    return self.formatted(success = True, unlinked = self.unlink())

  def pause(self):
    self.running = False
    self.log.info('game {game} paused', game = self.id)

  def unlink(self):
    # can only unlink if no users are left
    if len(self.users)>0:
      return False

    self.factory.unlinkGame(self)
    self.log.info('game {game} deleted', game = self.id)
    return True

  def pack(self):
    # saves the current game into the database
    # at first we construct the sql arguments dict

    args = {}

    args['id'] = self.uuid.hex
    args['name'] = self.name

    users = copy.deepcopy(self.users)
    for user in users:
      del user['joined']
      user['white_cards'] = [c.id for c in user['white_cards']]

    args['users'] = json.dumps(users)

    black_cards = [c.id for c in self.black_cards]
    white_cards = [c.id for c in self.white_cards]

    args['cards'] = json.dumps({'white_cards': white_cards, 'black_cards': black_cards})

    args['password_hash'] = self.password_hash if self.protected else ''
    args['database_hash'] = self.database_hash
    args['server_version_major'] = version.MAJOR
    args['server_version_minor'] = version.MINOR
    args['server_version_revision'] = version.REVISION

    return args

  @staticmethod
  def userdict(user):
    return {
            'user': user.id,
            'joined': True,
            'black_cards': 0,
            'white_cards': []
           }

  @staticmethod
  def formatted(**kwargs):
    return kwargs

  @property
  def protected(self):
    return self.password_hash != None

  @property
  def id(self):
    return self.uuid.int

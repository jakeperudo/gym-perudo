import random
from math import floor
from math import ceil
from random import randrange


class BetException(Exception):
	pass

class InvalidBetException(BetException):
	#Raised when a bet does not have either a higher quantity or a higher value
	pass


class Bet(object):

	def __init__(self, bet):
		self.current_bet = bet

	def __repr__(self):
		return 'bet'



def create_bet(proposed_bet, last_bet, player, game):
	#Checks validity of current bet for bots

	if last_bet:
		if proposed_bet <= last_bet:
			raise InvalidBetException()
		return proposed_bet
	else:
		return proposed_bet




class Die(object):

	def __init__(self):
		self.roll()

	def roll(self):
		self.value = randrange(1,7)




class Player(object):

	def __init__(self, name, dice_number, game):
		self.name = name
		self.game = game
		self.dice = []
		for i in range(0, dice_number):
			self.dice.append(Die())

	def make_bet(self, current_bet, action):
		pass

	def roll_dice(self):
		for die in self.dice:
			die.roll()
		# Sort dice into value order e.g. 4 2 5 -> 2 4 5
		self.dice = sorted(self.dice, key=lambda die: die.value)

	def count_dice(self, value):
		number = 0
		for die in self.dice:
			if die.value == value:
				number += 1
		return number

class BotPlayer(Player):

##Need to change to return value between 0 and 151 instead of bet strings##
	def make_bet(self, current_bet, action):
		total_dice_estimate = self.game.remaining_dice

		if current_bet == 0:
			value = random.choice(self.dice).value
			print('val0 = ' + str(value))
			quantity_limit = (total_dice_estimate - len(self.dice))//6
			quantity = self.count_dice(value) + random.randrange(0, quantity_limit + 1)
			print('quan0 = ' + str(quantity))
			bet = 6*(quantity-1) + value
			bet = create_bet(bet, current_bet, self, self.game)
			##print('bet0 = ' + str(bet))

		else:
			value = (current_bet % 6) + 1
			#print('val = ' + str(value))
			quantity = (current_bet - value)//6
			#print('quan = ' + str(quantity))
			limit = ceil(total_dice_estimate/6.0) * 2 + random.randrange(0, ceil(total_dice_estimate/4.0))
			#print('lim = ' + str(limit))
			if quantity >= limit:
				bet = 0
			else:
				bet = None
				while bet is None:
					value = random.choice(self.dice).value
					#print('val_loop = ' + str(value))
					quantity = (current_bet - value)//6
					quantity = quantity + random.randrange(0, 2)
					#print('quan_loop = ' + str(quantity))
					bet = 6*quantity + value
					try:
						bet = create_bet(bet, current_bet, self, self.game)
					except BetException:
						bet = None
				value = (bet % 6) + 1
				print('val = ' + str(value))
				quantity = (bet - value)//6
				print('quan = ' + str(quantity))
			#print('bet = ' + str(bet))
		return bet


class AIPlayer(Player):

	def make_bet(self, current_bet, action):
		###print('ai = ' + str(action))
		value = (action % 6) + 1
		###print('val = ' + str(value))
		quantity = (action - value)//6
		###print('quan = ' + str(quantity))

		##AI needs to learn valid moves
		##Maybe should only allow it to have valid moves in first place
		return action

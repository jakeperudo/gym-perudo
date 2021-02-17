import gym
from gym.spaces import Discrete
import random
import numpy as np

from gym_perudo.envs.player import BotPlayer
from gym_perudo.envs.player import AIPlayer

# 5 players, 5 6-sided dice each



class PerudoEnv(gym.Env):

    def __init__(self):
        self.number_of_players = 0
        #self.dice_number = 0 #num of dice per player
        self.players = []
        self.round = 0
        self.current_bet = 0
        self.reward = 0
        self.remaining_dice = 0
        self.action_space = Discrete(151) #up to 25x6 +1 for Dudo (0, 1, ... 150)
        self.observation_space = Discrete(151) #up to 25x6 +1 None (0, 1, ... 150)
        #observation will be the previous bet, which starts at 0=no bet
        #maybe include tupple of dice remaining and current dice and values?
        self.observation = 0
        self.done = False
        self.current_player = None

#How does the action space translate into an action?
#The action line of 151 breaks down into multiples of 6, with 0 as dudo
# 0 is dudo, 1 is 1x1, 2 is 2x1, ..., 7 is 2x1, ..., 150 is 25x6

#The observation line of 151 breaks down into multiples of 6, with 0 as no current bet
# 0 is no current bet, 1 is 1x1, 2 is 2x1, ..., 7 is 2x1, ..., 150 is 25x6

#The step is taking a single

    def step(self, action):

        self.reward = 0 #each action starts with 0 reward

        if len(self.players)==1:  #when last person loses dice,
            #if self.players[0].name == 'Bob':      possible reward??
            #    self.reward = 10 #plus 10 if AI wins game
            self.done = True
            #can return the name of the winner

        else:
            if action <= self.current_bet: #first check if action is valid given current bet
                self.reward = -1

            else:
                self.round +=1
                self.current_player = self.get_next_player(self.current_player)
                self.current_bet = self.current_player.make_bet(self.current_bet, action)
                name_list = []
                for player in self.players:
                    name_list.append(player.name)
                    print(name_list)
                if self.current_bet == 0: #if dudo is called
                    self.run_dudo(self.current_player, self.current_bet)
                #else:
                #    if self.current_player.name == 'Bob': #possible reward for AI
                #        self.reward +=0


            #returns observation, reward, done and winner's name
        return self.current_bet, self.reward, self.done, {}


    def reset(self):
        self.done = False

        self.players = [AIPlayer(name = 'Bob',
                                dice_number = 5,
                                game = self),
                        BotPlayer(
                            name = 'Chris',
                            dice_number = 5,
                            game = self),
                        BotPlayer(
                            name = 'Chenyu',
                            dice_number = 5,
                            game = self),
                        BotPlayer(
                            name = 'Kexin',
                            dice_number = 5,
                            game = self),
                        BotPlayer(
                            name = 'Jake',
                            dice_number = 5,
                            game = self)]

        for player in self.players:
            player.roll_dice()

        self.remaining_dice = len(self.players)*5

        return self.current_bet




##game functions##


    def get_next_player(self, player):
        if self.current_player == None: #Starts the game with a random player
            return self.players[random.randint(0,4)]
        else:
            return self.players[(self.players.index(player) + 1) % len(self.players)]


    def get_previous_player(self, player):
        return self.players[(self.players.index(player) - 1) % len(self.players)]


    def run_dudo(self, player, bet):
        print(' ')
        value = (self.current_bet + 1) % 6
        dice_count = self.count_dice(value)
        ##print(value)
        quantity = (self.current_bet - value)//6
        if dice_count >= quantity:
            self.current_player = player
            self.remove_die(player)
        else:
            previous_player = self.get_previous_player(player)
            self.current_player = previous_player
            self.remove_die(previous_player)


    def remove_die(self, player):
        player.dice.pop()
        self.remaining_dice -=1
        ##print(str(player.name))
        #if player.name == 'Bob':   possible reward?
        #    self.reward -= 1
        #else:
            #self.reward +=1
        if len(player.dice) == 0:
            #if player.name == 'Bob':   possible reward?
            #    self.reward -=3

            self.current_player = self.get_next_player(player)
            self.players.remove(player)


    def count_dice(self, value):
        number = 0
        for player in self.players:
            number += player.count_dice(value)
        return number

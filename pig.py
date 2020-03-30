#!/usr/bin/env python
# coding: utf-8

# In[18]:


import argparse
import random
from threading import Timer

import adts


class TimedGameProxy(object):
    def __init__(self, players):
        self.pig = Pig(players)
        self.time_up = Timer(60.0, self.pig.quit)

    def start_game(self):
        self.time_up.start()
        self.pig.start_game()


class Pig(object):

    def __init__(self, players=['Human', 'Computer']):
        self.players = adts.Queue()
        for num in xrange(len(players)):
            player = PlayerFactory(players[num] + ' ' + str(num)).get_player()
            self.players.enqueue(player)
        self.current_player = self.players.dequeue()
        print '\nFirst player: {}'.format(self.current_player.name)
        self.die = Die()

    def next_player(self):
        self.current_player.turn = False
        self.players.enqueue(self.current_player)
        self.current_player = self.players.dequeue()
        print '\nNext player is {}'.format(self.current_player.name)
        self.current_player.turn = True

    def start_game(self):
        self.current_player.turn = True
        ask_player = self.current_player.next_action()
        while ask_player and self.current_player.turn:
            if ask_player.upper()[0] == 'Q':
                self.quit()
                break

            if ask_player.upper()[0] == 'R':
                self.play()

            elif ask_player.upper()[0] == 'H':
                print '\n{} Holds. Score: {}'                     .format(self.current_player.name,
                            self.current_player.get_score())
                self.next_player()

            score = self.current_player.get_score()

            if score >= 100:
                print '\n{} wins. Score: {}'.format(self.current_player.name, score)
                break

            print '\nPlayer: ', self.current_player.name
            print '\nScore: ', self.current_player.get_score()
            ask_player = self.current_player.next_action()
            if not ask_player:
                self.quit()

    def play(self):
        num = self.current_player.play(self.die)
        if num == 1:
            self.current_player.points = []
            print '\n{} loses turn. Score set to {}'                 .format(self.current_player.name,
                        self.current_player.get_score())
            self.next_player()
        else:
            self.current_player.points.append(num)

    def quit(self):
        print 'Quitting game...'
        self.players.enqueue(self.current_player)
        while self.players.size() > 0:
            player = self.players.dequeue()
            print '\nPlayer {}: {}'.format(player.name, player.score)
        self.current_player.turn = False


class Die(object):
    faces = (1, 2, 3, 4, 5, 6)

    def roll(self):
        face = random.choice(self.faces)
        print 'Die face: {}'.format(face)
        return face


class Player(object):
    def __init__(self, name):
        self.name = name
        self.turn = False
        self.points = []
        self.score = 0
        self.plays = 0
        self.die = Die()

    def hold(self):
        self.turn = False

    def play(self, die):
        if self.turn:
            print 'Rolling the die...'
            return die.roll()

    def get_score(self):
        self.score = sum(self.points)
        return self.score

    def next_action(self):
        ask = 'Roll (R) Hold (H) or Quit (Q)?'
        return raw_input(ask)


class ComputerPlayer(Player):
    def next_action(self):
        score = self.get_score()
        if score == 25 or (100 - score) < 25:
            return 'Hold'
        else:
            return 'Roll'


class PlayerFactory(object):
    def __init__(self, player):
        if player[0] == 'H':
            self.player = Player(player)
        elif player[0] == 'C':
            self.player = ComputerPlayer(player)

    def get_player(self):
        return self.player


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--PLAYER1', required=False, type=str, default='Computer')
    PARSER.add_argument('--PLAYER2', required=False, type=str, default='Computer')
    PARSER.add_argument('--TIMED', required=False, type=int, default=1)
    PARSER.add_argument("-f", "--fff", help="an argument to fool anaconda jupyter notebook", default="1")

    ARGS = PARSER.parse_args()
    PLAYER1 = str(ARGS.PLAYER1).title()
    PLAYER2 = str(ARGS.PLAYER2).title()
    TIMED = ARGS.TIMED
    if PLAYER1 and PLAYER2:
        if TIMED == 1:
            Pig = TimedGameProxy([PLAYER1, PLAYER2])
        else:
            Pig = Pig([PLAYER1, PLAYER2])
        Pig.start_game()
    else:
        print 'You need at least two players for this game.'


# In[ ]:





# In[ ]:





# In[ ]:





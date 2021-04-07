import random


class Game:
    def __init__(self, acc):
        self.acc = acc
    def gameProcess(self, name, bet, result):
        if result == 0:
            self.acc.updateMoney(name, -int(bet))
            self.acc.updateMoney("bot", int(bet))
        elif result == 1:
            self.acc.updateMoney(name, int(bet))

from agarnet.client import Client
from agarnet.utils import special_names, get_party_address, find_server

from subscriber import Subscriber

import random
import threading


class Bot(Subscriber):
    def __init__(self):
        self.client = Client(self)
        self.finished_event = threading.Event()
        self.games_left = 1

        self.max_mass = -1
        self.mass = -1

    def main(self):
        nick = random.choice(special_names)
        self.client.player.nick = nick
        address, token = find_server()

        try:
            self.client.connect(address, token)
        except ConnectionResetError:
            # sometimes connection gets closed on first attempt
            print('Connection got closed on first attempt, retrying')
            self.client.connect(address, token)

        player = self.client.player

        self.client.send_respawn()
        self.client.send_target(*player.center)

        print('Connected, players name is {}, coords are {}.'.format(player.nick, player.center))


        self.finished_event.wait()

    def on_world_update_post(self):
        # Main bot logic
        player = self.client.player

        if player.total_mass <= self.mass:
            self.mass = player.total_mass
            print(self.mass)
            if self.mass < self.max_mass:
                self.max_mass = self.mass

    def on_cell_eaten(self, eater_id, eaten_id):
        cells = self.client.world.cells

        if eaten_id in cells and eater_id in cells:
            print('{} ate {}'.format(cells[eater_id].name, cells[eaten_id].name))

        player = self.client.player
        if eaten_id in player.own_ids:
            if len(player.own_ids) <= 1:
                self.games_left -= 1
                if self.games_left < 1:
                    self.client.disconnect()
                    self.finished_event.set()
                #~ self.client.send_respawn()

mybot = Bot()
mybot.main()

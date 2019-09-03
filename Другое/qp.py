import time
import random
import curses

class QPGame:
    def __init__(self, game_len=30, stdscr=None):
        self.game_len = game_len
        self.keep_alive = True

        if stdscr:
            self.stdscr = stdscr
        else:
            self.stdscr = curses.initscr()

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

    def destructor(self):
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()
        print('Thanks for playing, bye!')

    def addstr(self, string):
        cursor_y, cursor_x = self.stdscr.getyx()
        max_y, max_x = self.stdscr.getmaxyx()

        if cursor_y + 2 > max_y:
            self.stdscr.clear()
            self.stdscr.move(0, 0)

        self.stdscr.addstr(string)

    def getkey(self, allowed=None):
        while True:
            key = self.stdscr.getkey()
            if allowed != None:
                if key in allowed:
                    return key
            else:
                return key

    def main(self):
        while self.keep_alive:
            self.stdscr.clear()
            self.addstr('Press Q on "***" and P on "___***". You have {} seconds. You can quit with C.\n'.format(self.game_len))
            self.score = 0

            move_result = self.move()
            if move_result == False:
                self.addstr('You made a mistake.')
                self.getkey(allowed='\n')
                continue
            elif move_result == None:
                break

            start_time = time.perf_counter()

            while True:

                move_result = self.move()
                if move_result == False:
                    game_time = time.perf_counter() - start_time

                    if game_time > self.game_len / 2:
                        per_second = self.score / game_time
                        prediction = int(per_second * self.game_len)
                        self.addstr('You made a mistake. You would have probably scored {}.'.format(prediction))
                    else:
                        self.addstr('You made a mistake.')

                    self.getkey(allowed='\n')
                    break
                elif move_result == None:
                    self.addstr('Thanks for playing, bye!')
                    break

                if time.perf_counter() > start_time + self.game_len:
                    self.addstr('You scored {}. Congartulations!'.format(self.score))
                    self.getkey(allowed='\n')
                    break
        self.destructor()

    def move(self):
        if random.randint(0, 1):
            self.addstr('***\n')
            right_key = 'q'
        else:
            self.addstr('   ***\n')
            right_key = 'p'

        key = self.getkey(allowed='qpc')

        if key == 'c':
            self.keep_alive = False
        else:
            if key == right_key:
                self.score += 1
                return True
            else:
                return False

if __name__ == '__main__':
    game = QPGame()
    game.main()

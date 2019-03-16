import curses
from contextlib import contextmanager
import traceback


from reddit import stories_for_sub

SPLASH = '''
   _____                        _
  / ____|                      | |
 | |    _   _ _ __ ___  ___  __| |
 | |   | | | | '__/ __|/ _ \/ _` |
 | |___| |_| | |  \__ \  __/ (_| |
  \_____\__,_|_|  |___/\___|\__,_|    _
 |_   _|     | |                     | |
   | |  _ __ | |_ ___ _ __ _ __   ___| |_
   | | | '_ \| __/ _ \ '__| '_ \ / _ \ __|
  _| |_| | | | ||  __/ |  | | | |  __/ |_
 |_____|_| |_|\__\___|_|  |_| |_|\___|\__|

'''

@contextmanager
def logger(logfile="log.txt"):
    output = open(logfile, 'w')
    try:
        yield output
    except Exception as e:
        output.write("Exception encountered: {}".format(type(e).__name__))
        output.write(traceback.format_exc())
    finally:
        output.flush()


class UserInterface:
    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        self.height, self.width = self.screen.getmaxyx()
    def __del__(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def display_list(self, lines):
        for line in lines:
            self.screen.addstr(line)
            y, x = self.screen.getyx()
            x = 0
            y = y + 1
            if y >= self.height:
                break
            self.screen.move(y, x)
        self.screen.refresh()

if __name__ == "__main__":
    with logger() as logfile:
        ui = UserInterface()
        ui.screen.addstr(SPLASH)
        ui.screen.refresh()
        posts = stories_for_sub('linux') 
        ui.screen.getch()
        ui.screen.erase()
        ui.screen.move(0,0)
        ui.display_list(posts)
        ui.screen.getch()

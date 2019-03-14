import curses

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

class UserInterface:
    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
    def __del__(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

if __name__ == "__main__":
    ui = UserInterface()
    ui.screen.addstr(SPLASH)
    ui.screen.getch()


import curses
from contextlib import contextmanager
import traceback
import json


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

class VerticalMenu:
    def __init__(self, ui, options, log):
        self.ui = ui
        self.options = options
        self.selection = 0
        self.log = log

    def main(self):
        self.ui.display_list(self.options)
        self.log.write("entered menu")
        while True:
            input = self.ui.screen.getch()
            if input == curses.KEY_DOWN:
                self.sel_down()
            if input == curses.KEY_UP:
                self.sel_up()
            if input in (ord('q'), curses.KEY_EXIT):
                break
            if input in (ord('\n'), ord('\r'), curses.KEY_ENTER):
                self.log.write("selection picked: {}\n".format(self.options[self.selection][0]))
                self.log.flush()
                self.options[self.selection][1]()
                # TODO: hang data off to determine what to do here

    def sel_up(self):
        self.selection = (self.selection + 1) % len(self.options)
        self.update_sel()
    def sel_down(self):
        self.selection = (self.selection - 1) % len(self.options)
        self.update_sel()
    def update_sel(self):
        self.log.write("Selected: {}\n".format(self.options[self.selection][0]))
        self.log.flush()


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
        for line, _ in lines:
            self.screen.addstr(line)
            y, x = self.screen.getyx()
            x = 0
            y = y + 1
            if y >= self.height:
                break
            self.screen.move(y, x)
        self.screen.refresh()

def load_config():
    config = json.loads(open("cursedrc.json").read())
    return config["subreddits"]

def menu_for_story(ui, story, logfile):
    logfile.write("TODO: Implement showing story comments")

def menu_for_sub(ui, sub, logfile):
    ui.screen.erase()
    ui.screen.move(0,0)

    menu = VerticalMenu(
        ui,
        [
            (story, lambda: menu_for_story(ui, story, logfile))
            for story in 
            stories_for_sub(sub)
        ],
        logfile
    )

    menu.main()

if __name__ == "__main__":
    with logger() as logfile:
        subreddits = load_config()

        ui = UserInterface()
        ui.screen.addstr(SPLASH)
        ui.screen.refresh()
        ui.screen.getch()
        ui.screen.erase()
        ui.screen.move(0,0)
        menu = VerticalMenu(ui, [
            (sub, lambda: menu_for_sub(ui, sub, logfile).main())
            for sub in subreddits
        ], logfile)
        menu.main()
        ui.screen.getch()

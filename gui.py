import sys
import eel
import env


@eel.expose
def get_version():
    return env.VERSION


@eel.expose
def handle_exit():
    sys.exit(0)


def gui():
    eel.init('gui')
    eel.start('index.html', size=(800, 600))


if __name__ == '__main__':
    gui()
import sys
import eel
import env

from screeninfo import get_monitors

main_monitor = get_monitors()[0]
width, height = main_monitor.width, main_monitor.height


window_width = 800
window_height = 600
x = (width / 2) - (window_width / 2)
y = (height / 2) - (window_height / 2)

print(x, y)


@eel.expose
def get_version():
    return env.VERSION


@eel.expose
def handle_exit():
    sys.exit(0)


def gui():
    eel.init('gui')
    eel.start('index.html', size=(window_width, window_height), position=(x, y))


if __name__ == '__main__':
    gui()
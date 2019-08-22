import utime
import display
import leds
import ledfx
import buttons
import light_sensor
import ujson
import os

FILENAME = 'boreq.json'

WIDTH = 160
HEIGHT = 80

BLACK = [0, 0, 0]


class Flag:

    BI = [
        [214, 2, 112],
        [155, 79, 150],
        [0, 56, 168]
    ]

    RAINBOW = [
        [255, 0, 24],
        [255, 165, 44],
        [255, 255, 65],
        [0, 128, 24],
        [0, 0, 249],
        [134, 0, 125]
    ]


class Manager:

    def __init__(self, nickname, debug):
        self.nickname = nickname
        self.dt = 0.3
        self.renderers = []
        self.clear()
        self.load_nickname_renderer()

    def clear(self):
        leds.clear()
        leds.set_powersave(True)
        with display.open() as disp:
            disp.clear().update()
            disp.close()

    def load_nickname_renderer(self):
        self.renderers.clear()
        self.renderers.append(NicknameRenderer(self.nickname))
        #self.renderers.append(CyberpunkRenderer())

    def run(self):
        while True:
            with display.open() as disp:
                for renderer in self.renderers:
                    renderer.render(disp, self.dt)
                disp.update()
                disp.close()
            utime.sleep(self.dt)


class Renderer:

    def render(self, disp, dt):
        render_error('not', 'implemented')


class NicknameRenderer(Renderer):

    change_every = 1

    def __init__(self, nickname):
        self.nickname = nickname
        self.color_index = 0
        self.counter = 0
        self.rocket = [True, False, False]

    def render(self, disp, dt):
        self.counter += dt
        if self.counter > self.change_every:
            self.counter = 0

            self.color_index += 1
            if self.color_index >= len(Flag.RAINBOW):
                self.color_index = 0

            rocket_state = self.rocket.pop(0)
            self.rocket.append(rocket_state)

        col = Flag.RAINBOW[self.color_index]
        disp.rect(0, 0, WIDTH, HEIGHT, col=col, filled=True)
        disp.print(self.nickname, posx=HEIGHT - round(len(self.nickname) / 2 * 14), posy=30, bg=col)

        for i, state in enumerate(self.rocket):
            leds.set_rocket(i, 15 if state else 0)

class CyberpunkRenderer(Renderer):

    BLUE = [0, 184, 255]
    PINK = [214, 0, 255]

    def render(self, disp, dt):
        dark = 0
        if light_sensor.get_reading() < 30:
            dark = 1

        for i in range(10):
            leds.prep(i, self.PINK)
        for i in range(11, 15):
            leds.prep(i, self.BLUE)
        leds.update()

def render_error(err1, err2):
    with display.open() as disp:
        disp.clear()
        disp.print(err1, posx=80 - round(len(err1) / 2 * 14), posy=18)
        disp.print(err2, posx=80 - round(len(err2) / 2 * 14), posy=42)
        disp.update()
        disp.close()


#def render_nickname(title, sub, fg, bg, fg_sub, bg_sub, main_bg):
#    while True:
#        with display.open() as disp:
#            disp.update()
#            disp.close()
#        utime.sleep(0.3)


def get_key(json, key, default):
    try:
        return json[key]
    except KeyError:
        return default


if FILENAME in os.listdir('.'):
    f = open(FILENAME, 'r')
    try:
        c = ujson.loads(f.read())
        f.close()

        nickname = get_key(c, 'nickname', 'no nick')
        debug = get_key(c, 'debug', False)

        manager = Manager(nickname, debug)
        manager.run()
    except ValueError:
        render_error('invalid', 'json')
else:
    render_error('file not', 'found')

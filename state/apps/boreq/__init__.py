import utime
import display
import leds
import ledfx
import buttons
import light_sensor
import ujson
import os
import pride

FILENAME = 'boreq.json'

WIDTH = 160
HEIGHT = 80

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]


def leds_top():
    return range(11)


def leds_ambient():
    return range(11, 15)


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


class Mode:

    NICK = 'nick'
    RAINBOW = 'rainbow'
    FLASHLIGHT = 'flashlight'


class Buttons:

    def __init__(self):
        self.right_bottom = False
        self.right_bottom_once = False

        self.right_top = False
        self.right_top_once = False

    def update(self):
      now_right_bottom = buttons.read(buttons.BOTTOM_RIGHT)

      self.right_bottom_once = not self.right_bottom and now_right_bottom
      self.right_bottom = now_right_bottom

      now_right_top = buttons.read(buttons.TOP_RIGHT)

      self.right_top_once = not self.right_top and now_right_top
      self.right_top = now_right_top


class Manager:

    def __init__(self, nickname, debug):
        self.nickname = nickname
        self.debug = debug

        self.set_mode(Mode.NICK)
        self.renderers = self.get_renderers()

        self.buttons = Buttons()

        self.dt = 0.2

    def cleanup(self):
        leds.clear()
        leds.set_powersave(True)

        leds.dim_top(1)
        leds.dim_bottom(1)

        for i in range(3):
            leds.set_rocket(i, 0)

        leds.update()

        with display.open() as disp:
            disp.clear().update()
            disp.close()

    def get_renderers(self):
        nickname = NicknameRenderer(self.nickname)
        rainbow = RainbowRenderer()
        flashlight = FlashlightRenderer()
        battery = BatteryRenderer()
        debug = DebugRenderer()

        renderers = {
            Mode.NICK: [nickname, battery],
            Mode.RAINBOW: [rainbow],
            Mode.FLASHLIGHT: [flashlight],
        }

        if self.debug:
            renderers[Mode.NICK].append(debug)

        return renderers

    def get_sensors(self):
        light_level = light_sensor.get_reading()
        battery_voltage = os.read_battery()
        return Sensors(light_level, battery_voltage)

    def set_mode(self, mode):
        self.cleanup()
        self.modes = [mode]

    def process_mode_changes(self):
        if self.buttons.right_bottom_once:
            if Mode.NICK in self.modes:
                self.set_mode(Mode.RAINBOW)
            else:
                self.set_mode(Mode.NICK)

        if self.buttons.right_top_once:
            if Mode.FLASHLIGHT in self.modes:
                self.set_mode(Mode.NICK)
            else:
                self.set_mode(Mode.FLASHLIGHT)

    def run(self):
        while True:
            self.buttons.update()
            self.process_mode_changes()
            sensors = self.get_sensors()
            with display.open() as disp:
                for mode in self.modes:
                    for renderer in self.renderers[mode]:
                        renderer.render(disp, self.dt, sensors)
                disp.update()
                disp.close()
            utime.sleep(self.dt)


class Sensors:

    def __init__(self, light_level, battery_voltage):
        self.light_level = light_level
        self.battery_voltage = battery_voltage

    def is_dark(self):
        return self.light_level < 50

    def is_low(self):
        return self.battery_voltage < 3.5


class Renderer:

    def render(self, disp, dt, sensors):
        render_error('not', 'implemented')


class BatteryRenderer(Renderer):

    change_every = 0.1

    def __init__(self):
        self.enabled = False
        self.counter = 0

    def render(self, disp, dt, sensors):
        if sensors.is_low():
            self.counter += dt
            if self.counter > self.change_every:
                self.counter = 0
                self.enabled = not self.enabled

            col = [255, 0, 0] if self.enabled else BLACK
            for i in leds_top():
                leds.prep(i, col)

            leds.update()


class NicknameRenderer(Renderer):

    change_every = 1

    def __init__(self, nickname):
        self.nickname = nickname
        self.color_index = 0
        self.counter = 0
        self.rocket = [True, False, False]

    def render(self, disp, dt, sensors):
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

        if sensors.is_dark():
            for i, state in enumerate(self.rocket):
                leds.set_rocket(i, 31 if state else 0)

            for i in leds_top():
                leds.prep(i, col)

            for i in leds_ambient():
                leds.prep(i, col)
        else:
            for i in range(3):
                leds.set_rocket(i, 0)

            for i in leds_top():
                leds.prep(i, BLACK)

            for i in leds_ambient():
                leds.prep(i, BLACK)

        leds.update()


class DebugRenderer(Renderer):

    def render(self, disp, dt, sensors):
        s = '{0:>3} {1:>3}'.format(sensors.light_level, sensors.battery_voltage)
        disp.print(s, posx=0, posy=0)


class FlashlightRenderer(Renderer):

    def __init__(self):
        pass

    def render(self, disp, dt, sensors):
        for i in leds_top():
            leds.prep(i, WHITE)

        for i in leds_ambient():
            leds.prep(i, WHITE)

        leds.dim_top(8)
        leds.dim_bottom(8)

        leds.update()

        disp.rect(0, 0, WIDTH, HEIGHT, col=WHITE, filled=True)


class RainbowRenderer(Renderer):

    change_every = 0.1

    def __init__(self):
        self.color_index = 0
        self.counter = 0

    def render(self, disp, dt, sensors):
        self.counter += dt
        if self.counter > self.change_every:
            self.counter = 0

            self.color_index += 1
            if self.color_index >= len(Flag.RAINBOW):
                self.color_index = 0

        for i in range(6):
            end_y = (i + 1) * 13 if i < 5 else HEIGHT
            col_index = i if self.color_index % 2 == 0 else len(Flag.RAINBOW) - 1 - i
            disp.rect(0, i * 13, WIDTH, end_y, col=Flag.RAINBOW[col_index], filled=True)

        col = Flag.RAINBOW[self.color_index]
        for i in leds_top():
            leds.prep(i, col)
        for i in leds_ambient():
            leds.prep(i, col)
        leds.update()


def render_error(err1, err2):
    with display.open() as disp:
        disp.clear()
        disp.print(err1, posx=80 - round(len(err1) / 2 * 14), posy=18)
        disp.print(err2, posx=80 - round(len(err2) / 2 * 14), posy=42)
        disp.update()
        disp.close()


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

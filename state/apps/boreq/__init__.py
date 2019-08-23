import utime
import display
import leds
import ledfx
import buttons
import light_sensor
import ujson
import os


glenda_image = [
    [
        None, None, None, None, None, None, [210, 177, 199], None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
    ],
    [
        None, None, None, None, None, [219, 191, 210], [216, 186, 206], [226, 191, 214], None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
    ],
    [
        None, None, None, None, None, [222, 195, 213], [204, 177, 193], [137, 98, 107], [215, 183, 203], None, None, None, None, None, None, None, None, None, None, None, None, None, None
    ],
    [
        None, [195, 174, 188], [213, 190, 205], None, None, None, [241, 213, 232], [164, 130, 141], [158, 121, 132], [195, 170, 187], None, None, None, None, None, None, None, None, None, None, None, None, None
    ],
    [
        [206, 185, 199], [244, 219, 236], [212, 189, 205], [220, 197, 213], [184, 164, 178], None, [194, 171, 186], [226, 198, 216], [114, 66, 70], [168, 137, 149], [185, 163, 178], None, None, None, None, None, None, None, None, None, None, None, None
    ],
    [
        [186, 168, 180], [244, 220, 236], [120, 96, 103], [187, 157, 168], [231, 206, 222], [181, 162, 175], None, [213, 191, 212], [109, 120, 174], [62, 120, 200], [52, 129, 216], [55, 140, 233], [60, 149, 245], [55, 136, 225], [57, 140, 230], [52, 131, 216], [26, 91, 190], [24, 103, 241], None, None, None, None, None
    ],
    [
        None, [237, 214, 230], [229, 203, 218], [150, 104, 111], [170, 131, 140], [231, 205, 220], [189, 172, 192], [77, 139, 224], [53, 143, 241], [54, 144, 242], [55, 145, 244], [57, 147, 245], [58, 148, 246], [60, 149, 247], [61, 150, 248], [63, 152, 249], [60, 150, 247], [44, 127, 234], [31, 106, 194], None, None, None, None
    ],
    [
        None, None, [232, 210, 225], [227, 203, 217], [117, 75, 80], [119, 75, 79], [167, 150, 168], [112, 158, 240], [36, 108, 191], [52, 142, 241], [53, 143, 242], [55, 144, 243], [56, 146, 244], [57, 147, 245], [59, 148, 246], [60, 150, 247], [62, 151, 248], [63, 152, 249], [57, 146, 244], [43, 129, 224], None, None, None
    ],
    [
        None, None, None, [236, 214, 229], [224, 199, 214], [129, 91, 97], [106, 142, 215], [102, 147, 230], [33, 108, 209], [49, 140, 239], [51, 141, 240], [52, 142, 241], [95, 150, 236], [86, 144, 235], [57, 146, 244], [58, 148, 246], [59, 149, 247], [61, 150, 248], [62, 152, 249], [61, 151, 248], [50, 133, 223], None, None
    ],
    [
        None, None, None, None, [180, 177, 215], [143, 154, 205], [115, 164, 251], [54, 104, 211], [44, 134, 235], [47, 138, 237], [49, 139, 238], [50, 140, 240], [65, 136, 226], [52, 123, 210], [131, 158, 194], [146, 156, 152], [156, 148, 123], [175, 160, 134], [146, 142, 142], [131, 146, 156], [92, 138, 199], None, None
    ],
    [
        None, None, None, None, [80, 123, 193], [80, 123, 210], [36, 98, 202], [38, 123, 219], [43, 134, 235], [45, 136, 236], [46, 137, 237], [48, 138, 238], [100, 145, 210], [171, 164, 114], [212, 191, 188], [236, 209, 226], [243, 215, 233], [243, 215, 232], [243, 214, 231], [235, 208, 224], [179, 160, 160], [142, 141, 102], None
    ],
    [
        None, None, None, None, [35, 126, 226], [37, 128, 230], [38, 130, 231], [40, 131, 232], [41, 132, 233], [42, 133, 234], [44, 135, 235], [83, 128, 194], [170, 157, 122], [236, 212, 223], [245, 219, 235], [245, 218, 234], [244, 217, 234], [244, 216, 233], [243, 215, 232], [243, 214, 232], [229, 202, 218], None, None
    ],
    [
        None, None, None, [20, 89, 165], [33, 125, 227], [34, 126, 228], [36, 127, 229], [37, 129, 230], [39, 130, 231], [40, 131, 232], [91, 134, 200], [181, 169, 126], [238, 215, 229], [245, 220, 235], [245, 220, 235], [245, 219, 235], [245, 219, 235], [244, 218, 234], [244, 217, 233], [244, 216, 233], [237, 210, 227], None, None
    ],
    [
        None, None, None, [14, 84, 161], [27, 119, 222], [31, 123, 225], [34, 125, 227], [35, 127, 228], [36, 128, 229], [36, 126, 224], [156, 150, 109], [237, 215, 224], [246, 223, 237], [246, 222, 236], [245, 221, 236], [245, 220, 235], [245, 220, 235], [245, 219, 235], [245, 218, 234], [215, 191, 206], [229, 203, 219], [165, 145, 156], None
    ],
    [
        None, None, None, None, [18, 112, 216], [24, 117, 220], [29, 121, 224], [32, 124, 226], [34, 126, 228], [95, 124, 173], [201, 185, 179], [247, 225, 238], [247, 224, 238], [246, 223, 237], [191, 173, 184], [196, 176, 188], [245, 221, 236], [245, 220, 235], [245, 219, 235], [222, 199, 213], [231, 206, 221], [156, 137, 147], None
    ],
    [
        None, None, None, [19, 88, 208], [10, 105, 210], [15, 109, 214], [21, 114, 218], [26, 119, 222], [31, 123, 225], [145, 149, 134], [233, 214, 226], [247, 227, 239], [247, 226, 239], [247, 225, 238], [240, 218, 231], [239, 217, 231], [246, 222, 237], [246, 221, 236], [245, 221, 236], [245, 220, 235], [245, 219, 235], None, None
    ],
    [
        None, None, None, [24, 102, 241], [10, 95, 208], [7, 102, 208], [12, 106, 212], [17, 111, 215], [23, 116, 219], [164, 164, 133], [248, 228, 240], [248, 228, 241], [247, 227, 240], [247, 227, 239], [247, 226, 239], [247, 225, 238], [246, 223, 236], [207, 181, 191], [188, 151, 158], [216, 195, 208], [245, 220, 235], None, None
    ],
    [
        None, None, None, None, [0, 70, 152], [0, 96, 203], [4, 99, 206], [9, 104, 209], [14, 108, 213], [159, 159, 132], [240, 216, 231], [247, 226, 239], [248, 228, 241], [248, 228, 240], [247, 227, 240], [247, 226, 239], [186, 170, 180], [186, 169, 179], [145, 129, 137], [164, 148, 158], [246, 222, 236], None, None
    ],
    [
        None, None, None, None, None, [0, 88, 188], [0, 96, 203], [1, 97, 204], [6, 101, 207], [121, 136, 169], [220, 197, 194], [246, 219, 236], [247, 222, 238], [247, 226, 239], [248, 228, 241], [248, 228, 240], [213, 196, 207], [170, 156, 165], [192, 189, 191], [207, 188, 199], [233, 211, 224], None, None
    ],
    [
        None, None, None, None, None, [0, 77, 164], [0, 93, 197], [0, 96, 203], [0, 96, 203], [8, 96, 199], [189, 174, 146], [243, 212, 232], [245, 215, 234], [246, 219, 236], [247, 223, 238], [247, 227, 240], [248, 228, 241], [240, 225, 234], [238, 233, 236], [247, 226, 239], [197, 180, 190], None, None
    ],
    [
        None, None, None, None, None, [0, 66, 141], [0, 71, 152], [0, 79, 168], [0, 87, 185], [0, 96, 203], [120, 130, 156], [219, 190, 197], [242, 209, 230], [244, 213, 232], [245, 216, 234], [246, 220, 236], [247, 224, 238], [248, 227, 240], [248, 228, 241], [241, 221, 233], [155, 157, 187], [50, 88, 146], None
    ],
    [
        None, None, None, None, None, [81, 88, 152], [60, 80, 149], [0, 74, 157], [0, 77, 162], [0, 73, 156], [0, 72, 153], [134, 128, 107], [166, 158, 191], [187, 163, 183], [222, 204, 232], [225, 210, 239], [226, 213, 240], [203, 189, 218], [176, 169, 205], [94, 115, 163], [0, 68, 145], [0, 64, 138], None
    ],
    [
        None, None, None, None, None, None, [212, 170, 199], [197, 160, 197], [146, 128, 178], [67, 85, 154], [0, 74, 156], [0, 79, 167], [0, 79, 167], [0, 79, 167], [0, 77, 163], [0, 77, 163], [0, 75, 160], [0, 72, 154], [0, 75, 159], [0, 79, 167], [0, 63, 136], None, None
    ],
    [
        None, None, None, None, None, [189, 151, 178], [235, 188, 221], [235, 188, 221], [235, 188, 221], [233, 187, 220], [214, 171, 201], [209, 167, 197], [179, 146, 182], [171, 141, 179], [165, 139, 175], [170, 144, 180], [165, 146, 186], [151, 134, 171], [184, 163, 193], [193, 169, 188], [159, 140, 153], None, None
    ],
    [
        None, None, None, None, None, [117, 90, 106], [232, 184, 216], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 189, 221], [236, 192, 223], [237, 195, 225], [239, 199, 227], [240, 203, 229], [226, 194, 216], None, None, None
    ],
    [
        None, None, None, None, [58, 22, 22], [72, 36, 39], [187, 146, 171], [234, 187, 220], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 189, 222], [236, 192, 223], [228, 188, 216], [196, 164, 187], None, None, None
    ],
    [
        None, None, None, None, [58, 23, 23], [79, 32, 32], [60, 32, 35], [214, 169, 198], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [234, 187, 220], [230, 184, 216], [206, 165, 194], None, None, None, None
    ],
    [
        None, None, None, None, None, [48, 19, 19], [43, 16, 16], [75, 58, 69], [203, 162, 191], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [235, 188, 221], [231, 185, 217], [226, 181, 213], [187, 149, 175], [235, 188, 221], None, None, None, None
    ],
    [
        None, None, None, None, None, None, None, None, None, None, [205, 164, 192], [210, 168, 197], [235, 188, 221], [223, 178, 210], [185, 148, 174], [226, 181, 212], [233, 186, 219], [200, 159, 188], [205, 164, 193], None, None, None, None
    ],
    [
        None, None, None, None, None, None, None, None, None, None, None, None, None, [197, 157, 185], [179, 143, 168], [171, 136, 160], [203, 162, 191], None, None, None, None, None, None
    ]
]

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


class Counter:

    def __init__(self, every):
        self.counter = 0
        self.every = every

    def update(self, dt):
        self.counter += dt
        if self.counter >= self.every:
            self.counter = 0
            return True
        return False


class Manager:

    def __init__(self, nickname, debug):
        self.nickname = nickname
        self.debug = debug

        self.set_mode(Mode.NICK)
        self.renderers = self.get_renderers()

        self.buttons = Buttons()

        self.dt = 0.033

        self.update_sensors()
        self.sensors_counter = Counter(1)

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
            Mode.NICK: [nickname],
            Mode.RAINBOW: [rainbow],
            Mode.FLASHLIGHT: [flashlight],
        }

        if self.debug:
            renderers[Mode.NICK].append(debug)

        return renderers

    def update_sensors(self):
        light_level = light_sensor.get_reading()
        battery_voltage = os.read_battery()
        self.sensors = Sensors(light_level, battery_voltage)

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
            if self.sensors_counter.update(self.dt):
                self.update_sensors()

            with display.open() as disp:
                for mode in self.modes:
                    for renderer in self.renderers[mode]:
                        renderer.render(disp, self.dt, self.sensors)
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


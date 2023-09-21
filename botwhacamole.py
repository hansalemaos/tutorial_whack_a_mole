# Bot para Whack a Mole: https://www.classicgame.com/game/Whack+a+Mole
# pip install mousekey locate-pixelcolor-cpppragma fast_ctypes_screenshots whacamolefinder

import keyboard
from locate_pixelcolor_cpppragma import search_colors
from whacamolefinder import WhacAMoleFinder
from fast_ctypes_screenshots import (
    ScreenshotOfOneMonitor,
)
from mousekey import MouseKey

mkey = MouseKey()
mkey.enable_failsafekill('ctrl+e')
import numpy as np

ativo = False


def on_off():
    global ativo
    ativo = not ativo


keyboard.add_hotkey('ctrl+alt+s', on_off)


def crop_image(image, start_y, start_x, height, width):
    return image[start_y: start_y + height, start_x: start_x + width]


y_min = 234
y_max = 930
x_min = 420
x_max = 1480
start = 243, 154, 132
end = 250, 161, 139
allcolors = []
for r in range(start[0], end[0] + 1):
    for g in range(start[1], end[1] + 1):
        for b in range(start[2], end[2] + 1):
            allcolors.append([b, g, r])

bgrcolors = np.array(allcolors, dtype=np.uint8)


def screenshot_iter_function():
    while True:
        with ScreenshotOfOneMonitor(
                monitor=0, ascontiguousarray=False
        ) as screenshots_monitor:
            yield screenshots_monitor.screenshot_one_monitor()


piit = WhacAMoleFinder(screenshot_iter_function)  # pass the function without calling it!
for ini, dims in enumerate(
        piit.start_comparing(
            percent_resize=10,
            draw_output=False,
            draw_color=(255, 0, 255),
            thickness=20,
            thresh=3,
            maxval=255,
            draw_on_1_or_2=2,
            break_key="q",
        )
):
    if ativo:
        for di in dims:
            if (di.area > 10000 and di.area < 100000
                    and di.start_x > x_min and di.start_x < x_max
                    and di.start_y > y_min and di.start_y < y_max
            ):
                piccrop = crop_image(piit.last_screenshot,
                                     di.start_y, di.start_x,
                                     di.height, di.width)
                bichinho = search_colors(pic=piccrop,
                                         colors=bgrcolors, cpus=5)
                if not np.any(bichinho):
                    continue
                mkey.left_click_xy(di.center_x, di.center_y)

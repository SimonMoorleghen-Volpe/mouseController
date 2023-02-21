import pyautogui
import pygame
import numpy as np
from time import sleep
from enum import IntEnum

pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
if len(joysticks) == 0:
    raise Exception("No controller found")

can_move = True
pygame.event.set_blocked(pygame.JOYAXISMOTION)
pyautogui.FAILSAFE = False
wait = False


# Enumerate the controllers mapping so they can be used
class PS5Controller(IntEnum):
    lClick = 0
    rClick = 1
    hold = 2
    zoomIn = 10
    zoomOut = 9
    close = 6
    stop = 3
    mouseLeftRight = 0
    mouseUpDown = 1
    scroll = 3


class Xbox360Controller(IntEnum):
    lClick = 0
    rClick = 1
    hold = 2
    zoomIn = 5
    zoomOut = 4
    close = 7
    stop = 3
    mouseLeftRight = 0
    mouseUpDown = 1
    scroll = 4


class ProController(IntEnum):
    lClick = 1
    rClick = 0
    hold = 3
    zoomIn = 9
    zoomOut = 10
    close = 6
    stop = 2
    mouseLeftRight = 0
    mouseUpDown = 1
    scroll = 3


# Get the first
match joysticks[0].get_name():
    case "PS5 Controller":
        controller = PS5Controller
    case 'Nintendo Switch Pro Controller':
        controller = ProController
    case 'Xbox 360 Controller':
        controller = Xbox360Controller
    case _:
        print("Not recognized controller, defaulting to PS5 mapping")
        controller = PS5Controller

# active loop
while True:

    # go through events and see if they match any button mappings
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.JOYBUTTONDOWN:
            match event.__getattribute__('button'):
                case controller.lClick:
                    pyautogui.leftClick()
                case controller.rClick:
                    pyautogui.rightClick()
                case controller.hold:
                    pyautogui.mouseDown()
                case controller.zoomIn:
                    with pyautogui.hold('ctrl'):
                        pyautogui.press('+')
                case controller.zoomOut:
                    with pyautogui.hold('ctrl'):
                        pyautogui.press('-')
                case controller.close:
                    quit()
                case controller.stop:
                    can_move = not can_move
                case _:
                    print(event.__getattribute__('button'))
            continue
        elif event.type == pygame.JOYBUTTONUP:
            match event.__getattribute__('button'):
                case controller.hold:
                    pyautogui.mouseUp()
    # every loop, move mouse as needed
    if can_move:

        # get the values for the x-axis and y-axis, if below the margin, set to 0
        # this is to prevent slightly misaligned stick from constantly moving
        x_move = pygame.joystick.Joystick(0).get_axis(controller.mouseLeftRight)
        y_move = pygame.joystick.Joystick(0).get_axis(controller.mouseUpDown)
        if abs(x_move) < 0.05:
            x_move = 0
        if abs(y_move) < 0.05:
            y_move = 0

        if x_move != 0 or y_move != 0:
            pyautogui.moveRel(np.sign(x_move) * x_move ** 2 * 100, np.sign(y_move) * y_move ** 2 * 100,
                              duration=0, _pause=False)
            wait = True
        y_scroll = round(-pygame.joystick.Joystick(0).get_axis(controller.scroll) * 50)
        if abs(y_scroll) < 2:
            y_scroll = 0
        if y_scroll != 0:
            pyautogui.vscroll(y_scroll, _pause=False)
            wait = True
        # wait a very small amount of time as to maintain control of mouse and scroll,
        # while still hopefully feeling smooth
        if wait:
            wait = False
            sleep(0.02)

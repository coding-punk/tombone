import time

import pygame


def main():
    pygame.init()
    pygame.display.init()
    js_count = pygame.joystick.get_count()
    while js_count == 0:
        time.sleep(5)
        print("waiting for joystick count to go past 0, currently {0}".format(js_count))
        init_pygame()
        js_count = pygame.joystick.get_count()


def init_pygame():
    pygame.display.quit()
    pygame.quit()
    pygame.init()
    pygame.display.init()


if __name__ == "__main__":
    main()

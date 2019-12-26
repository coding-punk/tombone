import time

import pygame


def main():
    pygame.init()
    pygame.display.init()
    js_count = pygame.joystick.get_count()
    while js_count == 0:
        print("waiting for joystick count to go past 0, currently {0}".format(js_count))
        time.sleep(5)
        js_count = pygame.joystick.get_count()


if __name__ == "__main__":
    main()

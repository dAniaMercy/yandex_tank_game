import threading

import pygame
import sys
import logging
import datetime
import screeninfo
from pygame import *
from pygame.time import delay
from queue import Queue
from threading import *


class Settings:
    def __init__(self, WinWidth, WinHeight):
        self.WinWidth = WinWidth
        self.WinHeight = WinHeight
        self.WinRatio = 1920 * 1080 / (WinWidth * WinHeight)


class HelloGamer:
    def __init__(self, settings):
        self.settings = settings
        self.game = None

    def Main(self):
        pygame.init()
        self.game = pygame.display.set_mode([self.settings.WinWidth, self.settings.WinHeight])

        fontForHellpText = pygame.font.Font('ttf/pixel.ttf', 152)
        fontForHellpTextSmall = pygame.font.Font('ttf/pixel.ttf', 102)

        GameName = fontForHellpText.render("Tanks Game", True, (0, 178, 92))
        ProgName = fontForHellpTextSmall.render("by dAnya", True, (33, 133, 85))

        GameName_rect = GameName.get_rect(center=(self.settings.WinWidth / 2, self.settings.WinHeight / 2))
        ProgName_rect = ProgName.get_rect(
            center=(self.settings.WinWidth / 2, self.settings.WinHeight / 2 + 125 * self.settings.WinRatio))

        self.game.blit(GameName, GameName_rect)
        self.game.blit(ProgName, ProgName_rect)
        pygame.display.update()

        delay(5000)

        menu = GameMenu(self.settings, self.game)
        menu.Main()


class Menu:
    def __init__(self, settings, game):
        self.settings = settings
        self.game = game
        self.mainText = pygame.font.Font('ttf/pixel.ttf', 72)
        self.surfaces = []
        self.callbacks = []
        self.index = 0

    def AddOptions(self, options, callback):
        self.surfaces.append(self.mainText.render(options, True, (0, 178, 92)))
        self.callbacks.append(callback)

    def Switch(self, direction):
        self.index = max(0, min(self.index + direction, len(self.surfaces) - 1))

    def Select(self):
        if self.callbacks:
            self.callbacks[self.index]()

    def Draw(self, x, y, padding):
        self.game.fill((0, 0, 0))
        for i, option in enumerate(self.surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * padding * self.settings.WinRatio)
            if i == self.index:
                pygame.draw.rect(self.game, (0, 100, 0), option_rect)
            self.game.blit(option, option_rect)
        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()

class GameMenu:
    def __init__(self, settings, game):
        self.settings = settings
        self.game = game


    def Main(self):
        menu = Menu(self.settings, self.game)
        menu.AddOptions("Start", lambda: MainGame(self.game, self.settings).Main())
        menu.AddOptions("Quit", menu.quit_game)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu.quit_game()
                elif event.type == KEYDOWN:
                    if event.key == K_w:
                        menu.Switch(-1)
                    elif event.key == K_s:
                        menu.Switch(1)
                    elif event.key == K_SPACE:
                        menu.Select()

            menu.Draw(100, 100, 75)

class MainGame:
    def __init__(self, game, settings):
        self.mainText = pygame.font.Font('ttf/pixel.ttf', 72)
        self.game = game
        self.settings = settings
        self.MapWidth = 5
        self.MapHeight = 5
        self.CountEnemy = 2

    def Draw(self, x, y, padding):
        self.MapWidthText = self.mainText.render(f"Map Width: {self.MapWidth}", True, 0, 178, 92)
        self.MapHeightText = self.mainText.render(f"Map Width: {self.MapHeight}", True, 0, 178, 92)

        self.game.blit(self.MapWidthText, self.MapWidthText.get_rect())
        self.game.blit(self.MapHeightText, self.MapHeightText.get_rect())

        pygame.display.flip()

    def Main(self):
        menu = Menu(self.settings, self.game)
        menu.AddOptions("Plus 1 MapWidth", self.increase_map_width)
        menu.AddOptions("Remove 1 MapWidth", self.decrease_map_width)
        menu.AddOptions("Plus 1 MapHeight", self.increase_map_height)
        menu.AddOptions("Remove 1 MapHeight", self.decrease_map_height)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu.quit_game()
                    tMenu.join()
                    tMapSettings.join()
                elif event.type == KEYDOWN:
                    if event.key == K_w:
                        menu.Switch(-1)
                    elif event.key == K_s:
                        menu.Switch(1)
                    elif event.key == K_SPACE:
                        menu.Select()

            tMenu = threading.Thread(target=menu.Draw, args=(100, 100, 75))
            tMapSettings = threading.Thread(target=self.Draw(300,300,75))


    def increase_map_width(self):
        self.MapWidth += 1

    def decrease_map_width(self):
        self.MapWidth -= 1

    def increase_map_height(self):
        self.MapHeight += 1

    def decrease_map_height(self):
        self.MapHeight -= 1


if __name__ == '__main__':
    settings = Settings(screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height)
    HelloGamer(settings).Main()

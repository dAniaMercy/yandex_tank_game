import builtins
import threading
from collections import deque
from random import random

import pygame
import sys
import logging
import datetime
import screeninfo
from pygame import *
from pygame.time import delay
import random


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
        for i, option in builtins.enumerate(self.surfaces):
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
        menu.AddOptions("Start", lambda: MainGameMenu(self.game, self.settings).Main())
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


class MainGameMenu:
    def __init__(self, game, settings):
        self.mainText = pygame.font.Font('ttf/pixel.ttf', 72)
        self.game = game
        self.settings = settings
        self.MapWidth = 5
        self.MapHeight = 5
        self.CountEnemy = 2

    def Draw(self, x, y, padding):
        self.MapWidthText = self.mainText.render(f"Map Width: {self.MapWidth}", True, (0, 178, 92))
        self.MapHeightText = self.mainText.render(f"Map Height: {self.MapHeight}", True, (0, 178, 92))

        self.MapWidthText_rect = self.MapWidthText.get_rect().topleft = (x, y + 1 * padding * self.settings.WinRatio)
        self.MapHeightText_rect = self.MapHeightText.get_rect().topleft = (x, y + 2 * padding * self.settings.WinRatio)

        self.game.blit(self.MapWidthText, self.MapWidthText_rect)
        self.game.blit(self.MapHeightText, self.MapHeightText_rect)

        pygame.display.flip()

    def Main(self):
        self.game.fill((0, 0, 0))
        menu = Menu(self.settings, self.game)
        menu.AddOptions("Start",
                        lambda: MainGame(self.game, self.settings, self.MapWidth, self.MapHeight,
                                         self.CountEnemy).Main())
        menu.AddOptions("Plus 1 MapWidth", self.increase_map_width)
        menu.AddOptions("Remove 1 MapWidth", self.decrease_map_width)
        menu.AddOptions("Plus 1 MapHeight", self.increase_map_height)
        menu.AddOptions("Remove 1 MapHeight", self.decrease_map_height)
        menu.AddOptions("Exit", lambda: GameMenu(self.settings, self.game).Main())

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tMenu.join()
                    tMapSettings.join()
                    menu.quit_game()
                elif event.type == KEYDOWN:
                    if event.key == K_w:
                        menu.Switch(-1)
                    elif event.key == K_s:
                        menu.Switch(1)
                    elif event.key == K_SPACE:
                        menu.Select()
            tMenu = threading.Thread(target=menu.Draw, args=(100, 100, 75))
            tMapSettings = threading.Thread(target=self.Draw, args=(100, 500, 75))
            tMenu.start()
            tMapSettings.start()
            tMenu.join()
            tMapSettings.join()
            pygame.display.flip()

    def increase_map_width(self):
        self.MapWidth += 1

    def decrease_map_width(self):
        self.MapWidth -= 1

    def increase_map_height(self):
        self.MapHeight += 1

    def decrease_map_height(self):
        self.MapHeight -= 1


class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = 0.05

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class MainGame:
    def __init__(self, game, settings, MapHeight, MapWidth, CountEnemy):
        self.mainText = pygame.font.Font('ttf/pixel.ttf', 72)
        self.game = game
        self.settings = settings
        self.MapHeight = MapHeight
        self.MapWidth = MapWidth
        self.CountEnemy = CountEnemy
        self.Map = self.GenerateMap()
        self.TileSize = 128 * self.settings.WinRatio

        self.enemies = []  # Список врагов
        self.load_enemies(CountEnemy)

        self.player_x, self.player_y = 1, 1
        self.player_dx, self.player_dy = 0, -1
        self.bullets = []
        self.enemy_positions = [(x, y) for x in range(self.MapWidth) for y in range(self.MapHeight) if
                                self.Map[x][y] == 3]
        self.last_shot_time = pygame.time.get_ticks()
        self.last_enemy_move_time = pygame.time.get_ticks()
        self.last_enemy_shot_time = pygame.time.get_ticks()

        self.wall_sprite = pygame.image.load("sprites/wall.png")
        self.wall_sprite = pygame.transform.scale(self.wall_sprite, (self.TileSize, self.TileSize))

        self.tank_sprite_original = pygame.image.load("sprites/tank.png")
        self.tank_sprite_original = pygame.transform.scale(self.tank_sprite_original, (self.TileSize, self.TileSize))

        self.tank_enemy_sprite_original = pygame.image.load("sprites/enemy.png")
        self.tank_enemy_sprite_original = pygame.transform.scale(self.tank_enemy_sprite_original,
                                                                 (self.TileSize, self.TileSize))

        self.bullet_sprite = pygame.image.load("sprites/bullet.png")
        self.bullet_sprite = pygame.transform.scale(self.bullet_sprite, (self.TileSize // 4, self.TileSize // 4))

        self.player_x, self.player_y = 1, 1
        self.player_angle = 0
        self.tank_sprite = self.rotate_player_sprite()
        self.tank_enemy_sprite = self.rotate_enemy_sprite()

    def is_hit(self, bullet, target_x, target_y):
        """Проверяет, попала ли пуля в цель (игрока или врага)."""
        return int(bullet.x) == target_x and int(bullet.y) == target_y

    def update(self):
        """Обновляет позиции пуль и проверяет попадания."""
        for bullet in self.bullets[:]:
            bullet.move()

            # Проверка попадания в игрока
            if self.is_hit(bullet, self.player_x, self.player_y):
                print("💀 Игрок уничтожен!")
                pygame.quit()
                exit()

            # Проверка попадания в врагов
            for enemy in self.enemies[:]:
                if self.is_hit(bullet, enemy.x, enemy.y):
                    print("💥 Враг уничтожен!")
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    break  # Выходим, так как пуля исчезла

    def Draw(self):
        self.game.fill((0, 0, 0))

        for x in range(self.MapWidth):
            for y in range(self.MapHeight):
                screen_x, screen_y = x * self.TileSize, y * self.TileSize
                if self.Map[x][y] == 1:
                    self.game.blit(self.wall_sprite, (screen_x, screen_y))
                elif self.Map[x][y] == 2:
                    self.game.blit(self.tank_sprite, (screen_x, screen_y))

        # Отрисовка врагов
        for enemy in self.enemies:
            enemy_x, enemy_y = enemy.x * self.TileSize, enemy.y * self.TileSize
            self.game.blit(self.tank_enemy_sprite_original, (enemy_x, enemy_y))

        # Отрисовка пуль
        for bullet in self.bullets:
            bullet_x, bullet_y = bullet.x * self.TileSize, bullet.y * self.TileSize
            self.game.blit(self.bullet_sprite, (bullet_x, bullet_y))

        pygame.display.flip()

    def GenerateMap(self):
        Map = [[0 for _ in range(self.MapHeight)] for _ in range(self.MapWidth)]

        for x in range(self.MapWidth):
            Map[x][0] = Map[x][self.MapHeight - 1] = 1
        for y in range(self.MapHeight):
            Map[0][y] = Map[self.MapWidth - 1][y] = 1

        player_x, player_y = 1, 1
        Map[player_x][player_y] = 2

        enemy_positions = []
        while len(enemy_positions) < self.CountEnemy:
            x, y = random.randint(1, self.MapWidth - 2), random.randint(1, self.MapHeight - 2)
            if Map[x][y] == 0:
                Map[x][y] = 3
                enemy_positions.append((x, y))

        num_walls = (self.MapWidth * self.MapHeight) // 4
        for _ in range(num_walls):
            x, y = random.randint(1, self.MapWidth - 2), random.randint(1, self.MapHeight - 2)
            if Map[x][y] == 0 and self.can_place_wall(Map, x, y):
                Map[x][y] = 1
                if not self.is_map_fully_accessible(Map, player_x, player_y, enemy_positions):
                    Map[x][y] = 0

        return Map

    def rotate_player_sprite(self):
        return pygame.transform.rotate(self.tank_sprite_original, self.player_angle)

    def load_enemies(self, count):
        """Создает врагов в случайных местах."""
        for _ in range(count):
            x, y = random.randint(0, self.MapWidth - 1), random.randint(0, self.MapHeight - 1)
            self.enemies.append(Enemy(x, y))

    def rotate_enemy_sprite(self):
        return pygame.transform.rotate(self.tank_enemy_sprite_original, self.player_angle)

    def move_player(self, dx, dy):
        new_x, new_y = self.player_x + dx, self.player_y + dy
        if 0 <= new_x < self.MapWidth and 0 <= new_y < self.MapHeight and self.Map[new_x][new_y] != 1:
            self.Map[self.player_x][self.player_y] = 0
            self.player_x, self.player_y = new_x, new_y
            self.Map[self.player_x][self.player_y] = 2

            if dx == 1:  # Вправо
                self.player_angle = 270
            elif dx == -1:  # Влево
                self.player_angle = 90
            elif dy == 1:  # Вниз
                self.player_angle = 180
            elif dy == -1:  # Вверх
                self.player_angle = 0

            self.tank_sprite = self.rotate_player_sprite()

    def move_enemies(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_move_time >= 2000:
            self.last_enemy_move_time = current_time
            new_positions = []
            for x, y in self.enemy_positions:
                dx = 1 if self.player_x > x else -1 if self.player_x < x else 0
                dy = 1 if self.player_y > y else -1 if self.player_y < y else 0
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.MapWidth and 0 <= new_y < self.MapHeight and self.Map[new_x][new_y] == 0:
                    self.Map[x][y] = 0
                    self.Map[new_x][new_y] = 3
                    new_positions.append((new_x, new_y))
                else:
                    new_positions.append((x, y))
            self.tank_enemy_sprite_original = self.rotate_enemy_sprite()
            self.enemy_positions = new_positions

    '''def Draw(self):
        self.game.fill((0, 0, 0))

        for x in range(self.MapWidth):
            for y in range(self.MapHeight):
                screen_x, screen_y = x * self.TileSize, y * self.TileSize

                if self.Map[x][y] == 1:
                    self.game.blit(self.wall_sprite, (screen_x, screen_y))

                elif self.Map[x][y] == 2:
                    rotated_rect = self.tank_sprite.get_rect(
                        center=(screen_x + self.TileSize // 2, screen_y + self.TileSize // 2))
                    self.game.blit(self.tank_sprite, rotated_rect.topleft)

                elif self.Map[x][y] == 3:
                    pygame.draw.rect(self.game, (255, 0, 0), (screen_x, screen_y, self.TileSize, self.TileSize))

        pygame.display.flip()'''

    def DrawInConsole(self):
        for row in self.Map:
            print(" ".join(str(cell) for cell in row))

    def can_place_wall(self, Map, x, y):
        if Map[x][y] != 0:
            return False

        wall_neighbors = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.MapWidth and 0 <= ny < self.MapHeight and Map[nx][ny] == 1:
                wall_neighbors += 1

        return wall_neighbors < 2

    def is_map_fully_accessible(self, Map, player_x, player_y, enemy_positions):
        queue = deque([(player_x, player_y)])
        visited = set(queue)

        while queue:
            x, y = queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.MapWidth and 0 <= ny < self.MapHeight and
                        (nx, ny) not in visited and Map[nx][ny] != 1):
                    queue.append((nx, ny))
                    visited.add((nx, ny))

        return all((ex, ey) in visited for ex, ey in enemy_positions)

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 3000:
            self.last_shot_time = current_time
            self.bullets.append(Bullet(self.player_x, self.player_y, self.player_dx, self.player_dy))

    def enemy_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_shot_time >= 3000:
            self.last_enemy_shot_time = current_time
            for x, y in self.enemy_positions:
                dx = 1 if self.player_x > x else -1 if self.player_x < x else 0
                dy = 1 if self.player_y > y else -1 if self.player_y < y else 0
                if dx != 0 or dy != 0:
                    self.bullets.append(Bullet(x, y, dx, dy))

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.move()

    def Main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.move_player(0, -1)
                    elif event.key == pygame.K_s:
                        self.move_player(0, 1)
                    elif event.key == pygame.K_a:
                        self.move_player(-1, 0)
                    elif event.key == pygame.K_d:
                        self.move_player(1, 0)
                    elif event.key == pygame.K_SPACE:
                        self.shoot()
            self.Draw()
            self.update()
            self.move_enemies()
            self.enemy_shoot()
            self.update_bullets()
        pygame.quit()


if __name__ == '__main__':
    settings = Settings(screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height)
    HelloGamer(settings).Main()

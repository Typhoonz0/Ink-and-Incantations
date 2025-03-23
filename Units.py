"""A file containing all the summonable units"""
import pygame
import random
import os

class Unit:
    def __init__(self):
        self.hp = 1
        self.attack = 1
        self.cost = 1
        self.speed = 1
        self.x = 0
        self.y = 0
        self.target = [0, 0]
        self.lifetime = 0
        self.spawn_timer = 0
        self.move_timer = 0  # Initialize move timer for all units
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Footman.png"))

    def __str__(self):
        return "A Unit was summoned"

    def move(self, dt: float, team: list):
        """
        Move the troop towards its target, adjusted for delta time.
        Ensures movement is in whole-pixel increments.
        """
        self.move_timer += dt
        if self.move_timer >= 0.25:
            self.move_timer = 0
            if self.__class__.__name__ != "Generator":
                new_x = self.x
                new_y = self.y

                # Adjust movement speed based on delta time
                if self.target[0] > self.x:
                    new_x += round(self.speed)
                elif self.target[0] < self.x:
                    new_x -= round(self.speed)

                if self.target[1] > self.y:
                    new_y += round(self.speed)
                elif self.target[1] < self.y:
                    new_y -= round(self.speed)

                # Check for collisions with other units in the team
                collision = False
                for t in team:
                    if t.x == new_x and t.y == new_y:
                        collision = True
                        break

                # Update position if no collision
                if not collision:
                    self.x = new_x
                    self.y = new_y

                # Ensure the unit stays within bounds
                if self.x > 1322:
                    self.x = 1322
                elif self.x < 598:
                    self.x = 598
                if self.y > 876:
                    self.y = 876
                elif self.y < 154:
                    self.y = 154


class Footman(Unit):
    """The Footman Unit type (!:1/1/1)"""
    def __init__(self, xy: list):
        """
        Create Troop Footman at xy:(x, y) coordinates
        """
        super().__init__()
        self.hp = 1
        self.attack = 1
        self.cost = 1
        self.speed = 1
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Footman.png"))


class Horse(Unit):
    """The Horse Unit type (#:2/2/3)"""
    def __init__(self, xy: list):
        """
        Create Troop Horse at xy:(x, y) coordinates
        """
        super().__init__()
        self.hp = 2
        self.attack = 2
        self.cost = 3
        self.speed = 3
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Horse.png"))


class Soldier(Unit):
    """The Soldier Unit type (@:3/3/2)"""
    def __init__(self, xy: list):
        """
        Create Troop Soldier at xy:(x, y) coordinates
        """
        super().__init__()
        self.hp = 3
        self.attack = 3
        self.cost = 3
        self.speed = 2
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Soldier.png"))


class Summoner(Unit):
    """The Summoner Unit type ($:1/0/6)"""
    def __init__(self, xy: list):
        """
        Create Troop Summoner at xy:(x, y) coordinates
        """
        super().__init__()
        self.hp = 1
        self.attack = 0
        self.cost = 6
        self.speed = 3
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Summoner.png"))


class Minion(Unit):
    """The Minion Unit type (%:1/2/0)"""
    def __init__(self, xy: list):
        """
        Create Troop Minion at xy:(x, y) coordinates
        """
        super().__init__()
        self.hp = 1
        self.attack = 2
        self.cost = 0
        self.speed = 2
        self.x = xy[0]
        self.y = xy[1]
        self.lifetime = 0
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Minion.png"))


class Generator(Unit):
    """The Generator Unit type (^:4/0/0)"""
    def __init__(self, xy: list):
        """
        Control Troop Generator at xy:(x, y) coordinates
        """
        super().__init__()
        self.hp = 4
        self.attack = 0
        self.cost = 0
        self.speed = 0
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "Generator.png"))


class Runner(Unit):
    """The Runner Unit type (&:3/3/8)"""
    def __init__(self, xy: list):
        """
        Create Troop Runner at xy:(x, y) coordinates
        """
        super().__init__()
        self.hp = 3
        self.attack = 3
        self.cost = 8
        self.speed = 10
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Runner.png"))


class Tank(Unit):
    """The Tank Unit type (*:10/10/8)"""
    def __init__(self, xy: list):
        """
        Create Troop Tank at xy:(x, y) coordinates
        """
        super().__init__()
        self.hp = 10
        self.attack = 10
        self.cost = 8
        self.speed = 3
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Tank.png"))
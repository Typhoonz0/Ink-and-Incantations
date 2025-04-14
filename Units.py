"""A file containing all the summonable units"""
import pygame
import random
import os

class Unit:
    def __init__(self):
        self.hp = 1
        self.attack = 1
        self.cost = 1  # Default cost for a unit
        self.speed = 1
        self.x = 0
        self.y = 0
        self.true_x = self.x
        self.true_y = self.x
        self.target = [0, 0]
        self.lifetime = 0
        self.spawn_timer = 0
        self.move_timer = 0  # Initialize move timer for all units
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Footman.png"))

    def __str__(self):
        return "A Unit was summoned"
    
    def getCost(self) -> int:
        """
        Returns the cost of the unit.
        """
        return self.cost

    def move(self, dt: float, team: list, boundaries: list) -> None:
        """
        Move the troop towards its target, adjusted for delta time.
        Ensures movement is in whole-pixel increments.
        """
        if self.__class__.__name__ != "Generator":
            new_x = self.true_x
            new_y = self.true_y

            # Adjust movement speed based on delta time
            if self.target[0] >= self.x:
                new_x += abs(self.speed * (dt * 4))
            elif self.target[0] < self.x:
                new_x -= abs(self.speed * (dt * 4))

            if self.target[1] >= self.y:
                new_y += abs(self.speed * (dt * 4))
            elif self.target[1] < self.y:
                new_y -= abs(self.speed * (dt * 4))

            # Check for collisions with other units in the team
            collision = False
            for t in team:
                if t is self:
                    continue
                if t.x == int(new_x) and t.y == int(new_y):
                    collision = True
                    break
            # Update position if no collision
            if not collision:
                self.true_x = new_x
                self.true_y = new_y

            # Ensure the unit stays within bounds
            if self.true_x > boundaries["right"]:
                self.true_x = boundaries["right"]
            elif self.true_x < boundaries["left"]:
                self.true_x = boundaries["left"]
            if self.true_y > boundaries["bottom"]:
                self.true_y = boundaries["bottom"]
            elif self.true_y < boundaries["top"]:
                self.true_y = boundaries["top"]
                
            self.x = int(self.true_x)
            self.y = int(self.true_y)


# Subclasses with specific costs
class Footman(Unit):
    cost = 1  # Cost for Footman
    """The Footman Unit type (!:1/1/1)"""
    def __init__(self, xy: list):
        super().__init__()
        self.hp = 1
        self.attack = 1
        self.cost = 1  # Cost for Footman
        self.speed = 1
        self.x = xy[0]
        self.y = xy[1]
        self.true_x, self.true_y = xy
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Footman.png"))

class Horse(Unit):
    """The Horse Unit type (#:2/2/3)"""
    cost = 3  # Cost for Horse
    def __init__(self, xy: list):
        super().__init__()
        self.hp = 2
        self.attack = 2
        
        self.speed = 3
        self.x = xy[0]
        self.y = xy[1]
        self.true_x, self.true_y = xy
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Horse.png"))

class Soldier(Unit):
    """The Soldier Unit type (@:3/3/2)"""
    cost = 3  # Cost for Horse
    def __init__(self, xy: list):
        super().__init__()
        self.hp = 3
        self.attack = 3
        self.speed = 2
        self.x = xy[0]
        self.y = xy[1]
        self.true_x, self.true_y = xy
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Soldier.png"))

class Summoner(Unit):
    """The Summoner Unit type ($:1/0/6)"""
    cost = 6  # Cost for Summoner
    def __init__(self, xy: list):
        super().__init__()
        self.hp = 1
        self.attack = 0
        self.speed = 3
        self.x = xy[0]
        self.y = xy[1]
        self.true_x, self.true_y = xy
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Summoner.png"))

class Minion(Unit):
    """The Minion Unit type (%:1/2/0)"""
    cost = 0  # Cost for Minion
    def __init__(self, xy: list):
        super().__init__()
        self.hp = 1
        self.attack = 2
        self.speed = 2
        self.x = xy[0]
        self.y = xy[1]
        self.true_x, self.true_y = xy
        self.lifetime = 0
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Minion.png"))

class Generator(Unit):
    """The Generator Unit type (^:4/0/0)"""
    cost = 0  # Cost for Generator
    def __init__(self, xy: list):
        super().__init__()
        self.hp = 4
        self.attack = 0
        self.speed = 0
        self.x = xy[0]
        self.y = xy[1]
        self.true_x, self.true_y = xy
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "Generator.png"))

class Runner(Unit):
    """The Runner Unit type (&:3/3/8)"""
    cost = 8  # Cost for Runner
    def __init__(self, xy: list):
        super().__init__()
        self.hp = 3
        self.attack = 3
        self.speed = 10
        self.x = xy[0]
        self.y = xy[1]
        self.true_x, self.true_y = xy
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Runner.png"))

class Tank(Unit):
    """The Tank Unit type (*:10/10/8)"""
    cost = 8  # Cost for Tank
    def __init__(self, xy: list):
        super().__init__()
        self.hp = 10
        self.attack = 10

        self.speed = 3
        self.x = xy[0]
        self.y = xy[1]
        self.true_x, self.true_y = xy
        self.target = [0, 0]
        self.Asset = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Tank.png"))
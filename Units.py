"""A file containing all the summonable units"""
import pygame  
class Unit:
    def __init__(self):
        self.hp = 1
        self.attack = 1
        self.cost = 1
        self.speed = 1
        self.x = 0
        self.y = 0
        self.target = [0,0]
        self.Asset = pygame.image.load('')
    def __str__(self):
        return "A Unit was summoned"
    
    def move(self):
        if self.target[0] > self.x:
            self.x += self.speed
        else:
            self.x -= self.speed
        if self.target[1] > self.y:
            self.y += self.speed
        else:
            self.y -= self.speed
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
    def __init__(self, xy=list):
        self.hp = 1
        self.attack = 1
        self.cost = 1
        self.speed = 1
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('')

class Horse(Unit):
    """The Horse Unit type (#:2/2/3)"""
    def __init__(self, xy=list):
        self.hp = 2
        self.attack = 2
        self.cost = 3
        self.speed = 3
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('')

class Soldier(Unit):
    """The Soldier Unit type (@:3/3/2)"""
    def __init__(self, xy=list):
        self.hp = 3
        self.attack = 3
        self.cost = 3
        self.speed = 2
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('')

class Summoner(Unit):
    """The Summoner Unit type ($:1/0/6)"""
    def __init__(self, xy=list):
        self.hp = 1
        self.attack = 0
        self.cost = 6
        self.speed = 2
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('')

class Minion(Unit):
    """The Minion Unit type (%:1/2/0)"""
    def __init__(self, xy=list):
        self.hp = 1
        self.attack = 2
        self.cost = 0
        self.speed = 2
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('')

class Generator(Unit):
    """The Generator Unit type (^:4/0/0)"""
    def __init__(self, xy=list):
        self.hp = 4
        self.attack = 0
        self.cost = 0
        self.speed = 0
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('Assets\Sprites\Generator.png')

class Runner(Unit):
    """The Runner Unit type (&:3/3/8)"""
    def __init__(self, xy=list):
        self.hp = 3
        self.attack = 3
        self.cost = 8
        self.speed = 10
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('')

class Tank(Unit):
    """The Tank Unit type (*:10/10/8)"""
    def __init__(self, xy=list):
        self.hp = 10
        self.attack = 10
        self.cost = 8
        self.speed = 3
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('')

"""A file containing all the summonable units"""
import pygame  


class Unit:
    def __init__(self):
        self.hp = 1
        self.attack = 1
        self.cost = 1
        self.speed = 1
        self.team = None
        self.x = 0
        self.y = 0
        self.target = [0,0]
        self.Asset = pygame.image.load('')
    def __str__(self):
        return "A Unit was summoned"
    
class Footman(Unit):
    """The Footman Unit type (!:1/1/1)"""
    def __init__(self, team=bool, xy=list):
        self.hp = 1
        self.attack = 1
        self.cost = 1
        self.speed = 1
        self.team = team
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('')

class Horse(Unit):
    """The Horse Unit type (#:1/1/1)"""
    def __init__(self, team=bool, xy=list):
        self.hp = 2
        self.attack = 2
        self.cost = 3
        self.speed = 3
        self.team = team
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('')

class Soldier(Unit):
    """The Soldier Unit type (@:3/1/1)"""
    def __init__(self, team=bool, xy=list):
        self.hp = 3
        self.attack = 3
        self.cost = 3
        self.speed = 2
        self.team = team
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('')

class Summoner(Unit):
    """The Footman Unit type (!:1/1/1)"""
    def __init__(self, team=bool, xy=list):
        self.hp = 1
        self.attack = 0
        self.cost = 6
        self.speed = 2
        self.team = team
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('')

class Minion(Unit):
    """The Footman Unit type (!:1/1/1)"""
    def __init__(self, team=bool, xy=list):
        self.hp = 1
        self.attack = 2
        self.cost = 0
        self.speed = 2
        self.team = team
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('')

class Generator(Unit):
    """The Footman Unit type (!:1/1/1)"""
    def __init__(self, team=bool, xy=list):
        self.hp = 4
        self.attack = 0
        self.cost = 0
        self.speed = 0
        self.team = team
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('')

class Runner(Unit):
    """The Footman Unit type (!:1/1/1)"""
    def __init__(self, team=bool, xy=list):
        self.hp = 3
        self.attack = 3
        self.cost = 8
        self.speed = 10
        self.team = team
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('')


class Tank(Unit):
    """The Footman Unit type (!:1/1/1)"""
    def __init__(self, team=bool, xy=list):
        self.hp = 10
        self.attack = 10
        self.cost = 8
        self.speed = 3
        self.team = team
        self.x = xy[0]
        self.y = xy[1]
        self.target = [0,0]
        self.Asset = pygame.image.load('')
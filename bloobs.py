#!/usr/bin/python
# -*- coding: utf-8 -*-

# Written for Python 2.7.6

import pyglet
from pyglet.window import mouse
import random
from math import sin
from math import cos
from math import radians
from math import pi
from math import sqrt
from settings import settings


class Score(object):
    def __init__(self, N, M, S):
        pass


class Bloob(object):
    def __init__(self, x, y):
        bloob = random.choice(settings.bloobs[0:6])
        image = pyglet.resource.image(bloob[0])
        # Set image's anchor point
        image.anchor_x, image.anchor_y = image.width/2., image.height/2.
        self.sprite = pyglet.sprite.Sprite(image, x=x, y=y, batch=batch,
                                            group=foreground)
        self.color = bloob[1]

    def distance(self, another_bloob):
        dx = self.sprite.x - another_bloob.sprite.x
        dy = self.sprite.y - another_bloob.sprite.y
        return sqrt(dx**2 + dy**2)

    def move(self, dt, game):
        # Bloob shooted from cannon:
        if self.movement == 'shot':
            # Check if the bloob hits the edge of the wall:
            if self.sprite.x - game.wall.bloobImageSize/2. <= game.wall.leftEdge:
                self.radians = pi - self.radians
            elif self.sprite.x + game.wall.bloobImageSize/2. >= game.wall.rightEdge:
                self.radians = pi - self.radians
            # Find neighboring bloobs in the wall:
            line, spot, spot_x, spot_y = self.gridPosition(game)
            neighbors = set()
            if line%2 == 0:
                neighborPositions = ((line - 1, spot - 1),
                                     (line - 1, spot),
                                     (line,     spot - 1),
                                     (line,     spot + 1),
                                     (line + 1, spot - 1),
                                     (line + 1, spot))
            else:
                neighborPositions = ((line - 1, spot),
                                     (line - 1, spot + 1),
                                     (line,     spot - 1),
                                     (line,     spot + 1),
                                     (line + 1, spot),
                                     (line + 1, spot + 1))
            for position in neighborPositions:
                try:
                    l = position[0]
                    s = position[1]
                    wallBloob = game.wall.lines[l][s]
                    if wallBloob != None:
                        neighbors.add((wallBloob, l, s))
                except IndexError:
                    pass
            # Check the distance between neighboring bloobs:
            to_remove = set()
            for b in neighbors:
                d = self.distance(b[0])
                if d >= game.wall.bloobImageSize:
                    to_remove.add(b)
            for element in to_remove:
                neighbors.remove(element)
            #neighbors.difference(to_remove)    # THIS DOESN'T WORK, WHY???
            # When the bloob hits other bloobs in the wall:
            if len(neighbors) > 0:
                # Check whether there are bloobs of the same color:
                sameColorNeighbors = set()
                while len(neighbors) > 0:
                    b = neighbors.pop()
                    if b[0].color == self.color:
                        sameColorNeighbors.add(b)
                # When there isn't bloob with the same color as shooted bloob:
                """
                if len(sameColorNeighbors) == 0:
                    self.movement = None
                    line, spot, spot_x, spot_y = self.gridPosition(game)
                    game.wall.addBloobToWall(self, line, spot, spot_x, spot_y)
                """
                self.movement = None
                line, spot, spot_x, spot_y = self.gridPosition(game)
                game.wall.addBloobToWall(self, line, spot, spot_x, spot_y)
                """
                while len(hit) > 0:
                    bloob, line, spot = hit.pop()
                    game.wall.deleteBloob(bloob, line, spot, game)
                """
                return
            # Update bloob coordinates:
            self.sprite.x += shot_velocity * cos(self.radians) * dt
            self.sprite.y += shot_velocity * sin(self.radians) * dt
        if self.movement == 'fall':
            pass

    def gridPosition(self, game):
        y = game.window.height + game.wall.upperEdge - self.sprite.y
        line = int(y)/game.wall.lineHeight
        spot_y = game.window.height + game.wall.upperEdge - (line + 1/2.)*game.wall.lineHeight
        x = self.sprite.x - game.wall.leftEdge - game.wall.bloobSpotWidth/2.*(line%2)
        spot = int(x)/game.wall.bloobSpotWidth
        spot_x = game.wall.leftEdge + game.wall.bloobSpotWidth/2.*(2*spot + 1 + (line%2))
        return line, spot, spot_x, spot_y


class Wall(object):
    def __init__(self, game):
        self.NB = 17    # Number of Bloobs in Line 0, 2, 4, ...
        self.bloobImageSize = 36
        self.lineHeight = self.bloobImageSize - 1    # Height of bloobs line
        self.bloobSpotWidth = self.bloobImageSize + 1
        self.upperEdge = -2
        self.leftEdge = 1
        self.rightEdge = self.leftEdge + (self.NB - 1)*self.bloobSpotWidth + self.bloobImageSize
        self.firstLine_y = game.window.height + self.upperEdge - self.bloobImageSize/2.
        self.lines = []
        y = self.firstLine_y
        for line in range(game.maxLines):
            nb = self.NB - line%2
            if line < game.numberOfLines:
                x = self.leftEdge + self.bloobImageSize/2.*((line%2) + 1)
                self.lines.append(self.generateBloobsLine(nb, x, y))
                y = y - self.lineHeight
            else:
                self.lines.append([None for i in range(nb)])

    def generateBloobsLine(self, nb, x, y):
        line = []
        for b in range(nb):
            line.append(Bloob(x, y))
            x += self.bloobSpotWidth
        return line

    def deleteBloob(self, bloob, line, spot, game):
        game.wall.lines[line][spot] = None
        bloob.sprite.delete()
        pass
        #posle signal ze ma spadnut, vymaze ho z self.lines
        #a az bude dole, zmaze uplne

    def addBloobToWall(self, bloob, line, spot, spot_x, spot_y):
        try:
            self.lines[line][spot] = bloob
            bloob.sprite.x = spot_x
            bloob.sprite.y = spot_y
        except IndexError:
            pass
            #game.gameOver()


class Cannon(object):
    def __init__(self):
        # Set image's anchor point
        image = pyglet.resource.image(settings.cannon)
        image.anchor_x, image.anchor_y = image.width/2., 42
        x, y = settings.cannonPosition
        self.sprite = pyglet.sprite.Sprite(image, x=x, y=y, batch=batch,
                                            group=foreground)
        self.enabled = True

    def load(self, dt, game):
        game.bloobsInCannon[0].sprite.position = settings.bloobInCannonPosition
        x, y = settings.nextBloobPosition
        game.bloobsInCannon.append(Bloob(x, y))

    def enable(self, dt):
        self.enabled = True

    def shoot(self, game):
        # Shoot the bloob:
        if self.enabled == True:
            self.enabled = False
            game.bloobsUsed += 1
            game.bloobsUsedLabel.text = str(game.bloobsUsed)
            pyglet.clock.schedule_once(self.enable, 1)
            rad = pi/2 - radians(self.sprite.rotation)
            shootedBloob = game.bloobsInCannon.pop(0)
            shootedBloob.movement = 'shot'
            shootedBloob.radians = rad
            game.movingBloobs.append(shootedBloob)
            pressed_keys.clear()
            # Load the cannon:
            pyglet.clock.schedule_once(self.load, 1, game)

    def tick(self, dt, game):
        # Moving the cannon with arrow keys:
        delta_rotation = 1
        if 'RIGHT' in pressed_keys:
            self.sprite.rotation += delta_rotation
        if 'LEFT' in pressed_keys:
            self.sprite.rotation -= delta_rotation
        # Moving the cannon with mouse:
        if game.mouseMovement != None:
            self.sprite.rotation += game.mouseMovement
            game.mouseMovement = None
        if self.sprite.rotation > 75:
            self.sprite.rotation = 75
        if self.sprite.rotation < -75:
            self.sprite.rotation = -75
        # Shooting the bloob from cannon:
        if 'SHOOT' in pressed_keys or 'SHOOT' in pressed_mouse:
            self.shoot(game)



class DangerBar(object):
    def __init__(self, game):
        pass


class Game(object):
    def __init__(self):
        self.window = pyglet.window.Window(800, 600)
        self.window.push_handlers(keys)
        self.mouseMovement = None
        self.cannon = Cannon()
        self.movingBloobs = []
        self.initialSettings()
        self.showLabels()
        self.tnt = DangerBar(self)

    def initialSettings(self):
        self.level = 1
        self.lives = 3
        self.score = 0
        self.bloobsUsed = 0
        self.lastShot = 0
        self.maxLines = 14
        self.numberOfLines = 9
        self.start()

    def start(self):
        x1, y1 = settings.bloobInCannonPosition
        x2, y2 = settings.nextBloobPosition
        self.bloobsInCannon = [Bloob(x1, y1), Bloob(x2, y2)]
        self.wall = Wall(self)

    def showLabels(self):
        self.bloobsUsedLabel = pyglet.text.Label(text=str(self.bloobsUsed),
                            font_size=24, x=775, y=233, color=(0, 0, 0, 200),
                            anchor_x='right', anchor_y='center', batch=batch)
        self.lastShotLabel = pyglet.text.Label(text=str(self.lastShot),
                            font_size=24, x=775, y=147, color=(0, 0, 0, 200),
                            anchor_x='right', anchor_y='center', batch=batch)
        self.scoreLabel = pyglet.text.Label(text=str(self.score),
                            font_size=24, x=775, y=63, color=(0, 0, 0, 200),
                            anchor_x='right', anchor_y='center', batch=batch)
        self.levelLabel = pyglet.text.Label(text='level: '+ str(self.level),
                            font_size=20, x=95, y=50, color=(0, 0, 0, 200),
                            anchor_x='center', anchor_y='center', batch=batch)

    def update(self, dt):
        # Update the positions of all objects:
        self.cannon.tick(dt, self)
        for b in self.movingBloobs:
            b.move(dt, self)

# Setup our keyboard handler and mouse
key = pyglet.window.key
keys = key.KeyStateHandler()
pressed_keys = set()
key_control = {key.UP:    'SHOOT',
               key.RIGHT: 'RIGHT',
               key.LEFT:  'LEFT'}
pressed_mouse = set()
mouse_control = {mouse.LEFT:    'SHOOT',
                 mouse.MIDDLE:  'SHOOT'}

# Ordered groups
batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

img = pyglet.resource.image(settings.background)
Background = pyglet.sprite.Sprite(img=img, batch=batch, group=background)
game = Game()
shot_velocity = settings.velocity
pyglet.clock.schedule_interval(game.update, 1./60)


@game.window.event()
def on_draw():
    game.window.clear()
    batch.draw()

@game.window.event()
def on_key_press(symbol, modifiers):
    if symbol in key_control:
        pressed_keys.add(key_control[symbol])

@game.window.event()
def on_key_release(symbol, modifiers):
    if symbol in key_control:
        pressed_keys.discard(key_control[symbol])

@game.window.event()
def on_mouse_motion(x, y, dx, dy):
    game.mouseMovement = dx

@game.window.event()
def on_mouse_press(x, y, button, modifiers):
    pressed_mouse.add(mouse_control[button])

@game.window.event()
def on_mouse_release(x, y, button, modifiers):
    pressed_mouse.discard(mouse_control[button])


pyglet.app.run()

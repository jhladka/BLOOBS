#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyglet
from pyglet.window import mouse
import random
from math import sin
from math import cos
from math import radians
from math import pi
from settings import settings


class Bloob(object):
    def __init__(self, x, y):
        bloob = random.choice(settings.bloobs[0:6])
        image = pyglet.resource.image(bloob[0])
        # Set image's anchor point
        image.anchor_x, image.anchor_y = image.width/2, image.height/2
        self.sprite = pyglet.sprite.Sprite(image, x=x, y=y, batch=batch,
                                            group=foreground)
        self.color = bloob[1]
        """
    def tick_wall(self, dt, game):
        pass
        #self.sprite.x += 2
        #self.sprite.y += 3
        """

    def move(self, dt):
        if self.movement == 'shot':
            self.sprite.x += shot_velocity * cos(self.radians) * dt
            self.sprite.y += shot_velocity * sin(self.radians) * dt
        if self.movement == 'fall':
            pass


class Wall(object):
    def __init__(self, game):
        self.NB = 17    # Number of Bloobs in Line 0, 2, 4, ...
        self.lines = []
        y = game.firstLine_y
        for line in range(game.numberOfLines):
            nb = self.NB - line%2
            x = 19 + 18*(line%2)
            self.lines.append(self.generateBloobsLine(nb, x, y))
            y = y - 36

    def generateBloobsLine(self, nb, x, y):
        line = []
        for b in range(nb):
            line.append(Bloob(x, y))
            x += 37
        return line

    def deleteBloob(self, bloob, game):
        pass
        #posle signal ze ma spadnut, vymaze ho z self.lines
        #a az bude dole, zmaze uplne


class Cannon(object):
    def __init__(self):
        # Set image's anchor point
        image = pyglet.resource.image(settings.cannon)
        image.anchor_x, image.anchor_y = image.width/2, 42
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
        self.numberOfLines = 9
        self.firstLine_y = self.window.height - 18 # it's half size of bloob image
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
        self.cannon.tick(dt, game)
        for b in self.movingBloobs:
            b.move(dt)

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

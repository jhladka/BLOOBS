#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyglet
from settings import settings


class Bloob(object):
    def __init__(self, image, x, y):
        # Set image's anchor point
        image.anchor_x, image.anchor_y = image.width/2, image.height/2
        self.sprite = pyglet.sprite.Sprite(image, x=y, y=y, batch=batch,
                                            group=foreground)



class Cannon(object):
    def __init__(self, image):
        # Set image's anchor point
        image.anchor_x, image.anchor_y = image.width/2, 40
        self.sprite = pyglet.sprite.Sprite(image, x=315, y=50, batch=batch,
                                            group=foreground)

    def tick(self, dt):
        delta_rotation = 1
        if 'RIGHT' in pressed_keys:
            self.sprite.rotation += delta_rotation
            if self.sprite.rotation > 90:
                self.sprite.rotation = 90
        if 'LEFT' in pressed_keys:
            self.sprite.rotation -= delta_rotation
            if self.sprite.rotation < -90:
                self.sprite.rotation = -90
        #if 'FIRE' in pressed_keys:


class DangerBar(object):
    def __init__(self, game):
        pass


class Game(object):
    def __init__(self):
        self.window = pyglet.window.Window(800, 600)
        self.window.push_handlers(keys)
        img = pyglet.resource.image(settings.cannon)
        self.Objects = [Cannon(img)]
        self.initialSettings()
        self.showLabels()
        self.tnt = DangerBar(self)

    def initialSettings(self):
        self.level = 1
        self.lives = 3
        self.score = 0
        #self.start()

    def showLabels(self):
        self.scoreLabel = pyglet.text.Label(text=str(self.score),
                            font_size=30, x=760, y=63, color=(0, 0, 0, 200),
                            anchor_x='center', anchor_y='center', batch=batch)
        self.levelLabel = pyglet.text.Label(text='level: '+ str(self.level),
                            font_size=20, x=100, y=50, color=(0, 0, 0, 200),
                            anchor_x='center', anchor_y='center', batch=batch)

    def update(self, dt):
        # Update the positions of all objects:
        for obj in self.Objects:
            obj.tick(dt)


# Setup our keyboard handler
key = pyglet.window.key
keys = key.KeyStateHandler()
pressed_keys = set()
key_control = {key.UP:    'SHOOT',
               key.RIGHT: 'RIGHT',
               key.LEFT:  'LEFT'}

# Ordered groups
batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

### GAME ###

img = pyglet.resource.image(settings.background)
Background = pyglet.sprite.Sprite(img=img, batch=batch, group=background)
game = Game()
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

pyglet.app.run()

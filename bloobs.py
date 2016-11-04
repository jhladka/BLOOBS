#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyglet
from settings import settings


class Bloob(object):
    def __init__(self):
        pass


class Cannon(object):
    def __init__(self, image):
        # Set image's anchor point
        image.anchor_x, image.anchor_y = image.width/2, 35
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


class Game(object):
    def __init__(self):
        self.window = pyglet.window.Window(800, 600)
        self.window.push_handlers(keys)
        img = pyglet.resource.image(settings.cannon)
        self.Objects = [Cannon(img)]
        #self.initialSettings()

    def initialSettings(self):
        self.level = 0
        self.lives = 3
        self.score = 0
        #self.start()

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

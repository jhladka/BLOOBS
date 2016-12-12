# -*- coding: utf-8 *-*

import pyglet

# Resource paths. Resources folder must be on same level as this file.
pyglet.resource.path = ['PNG']
pyglet.resource.reindex()

background  = 'background.png'
wallBar     = 'wallBar.png'
cannon      = 'cannon.png'
tnt         = 'tnt.png'
bloobs      = [('blue.png', 'blue'),
               ('red.png', 'red'),
               ('green.png', 'green'),
               ('yellow.png', 'yellow'),
               ('purple.png', 'purple'),
               ('pink.png', 'pink'),
               ('black.png', 'black')]
highestScore = 'highestScore.png'

cannonPosition        = (315, 50)
bloobInCannonPosition = (315, 52)
nextBloobPosition     = (562, 47)
tntPosition           = (649, 298)

velocity = 600

layer_background    = pyglet.graphics.OrderedGroup(0)    # background
layer_wall          = pyglet.graphics.OrderedGroup(0.1)  # wall bloobs
layer_cannon        = pyglet.graphics.OrderedGroup(0.2)  # cannon
layer_cannonBloob   = pyglet.graphics.OrderedGroup(0.3)  # bloobs in cannon
layer_score         = pyglet.graphics.OrderedGroup(0.4)  # window with highest score
layer_scoreTable    = pyglet.graphics.OrderedGroup(0.5)  # window with highest score-text

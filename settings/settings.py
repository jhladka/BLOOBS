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

cannonPosition        = (315, 50)
bloobInCannonPosition = (315, 52)
nextBloobPosition     = (562, 47)
tntPosition           = (649, 298)   

velocity = 600

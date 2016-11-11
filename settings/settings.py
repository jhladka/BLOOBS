# -*- coding: utf-8 *-*

import pyglet

# Resource paths. Resources folder must be on same level as this file.
pyglet.resource.path = ['PNG']
pyglet.resource.reindex()

background  = 'background.png'
cannon      = 'cannon.png'
bloobs      = (('blue.png', 'blue'),
               ('red.png', 'red'),
               ('green.png', 'green'),
               ('yellow.png', 'yellow'),
               ('purple.png', 'purple'),
               ('pink.png', 'pink'))

cannonPosition          = (315, 50)
bloobInCannonPosition = (315, 52)
nextBloobPosition      = (562, 47)

velocity = 600

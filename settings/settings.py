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

cannon_coordinates  = (315, 50)

velocity = 10

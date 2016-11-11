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


class Bloob(object):
    def __init__(self, x, y, colors):
        while 1:
            bloob = random.choice(settings.bloobs[0:6])
            if bloob[1] in colors:
                break
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

    def gridPosition(self, game):
        y = game.wall.upperEdge - self.sprite.y
        line = int(y)/game.wall.lineHeight
        if line == -1:
            line = 0
        spot_y = game.wall.upperEdge - (line + 1/2.)*game.wall.lineHeight
        x = self.sprite.x - game.wall.leftEdge - game.wall.bloobSpotWidth/2.*(line%2)
        spot = int(x)/game.wall.bloobSpotWidth
        spot_x = game.wall.leftEdge + game.wall.bloobSpotWidth/2.*(2*spot + 1 + (line%2))
        return line, spot, spot_x, spot_y

    def reflection(self, game):
        if self.sprite.x - game.wall.bloobImageSize/2. <= game.wall.leftEdge:
            self.radians = pi - self.radians
        elif self.sprite.x + game.wall.bloobImageSize/2. >= game.wall.rightEdge:
            self.radians = pi - self.radians

    def hitTop(self, game):
        line, spot, spot_x, spot_y = self.gridPosition(game)
        game.movingBloobs.remove(self)
        game.wall.addBloobToWall(self, line, spot, spot_x, spot_y, game)
        game.scoreCount(0, 0)

    def collision(self, neighbors, game):
        collision = 0
        for b in neighbors:
            d = self.distance(b[0])
            if d < game.wall.bloobImageSize - 3:
                collision = 1
                break
        return collision

    def positionUpdate(self, dt):
        self.sprite.x += shot_velocity * cos(self.radians) * dt
        self.sprite.y += shot_velocity * sin(self.radians) * dt
        return self.sprite.x, self.sprite.y

    def selectSameColor(self, neighbors):
        sameColorNeighbors = set()
        while len(neighbors) > 0:
            b = neighbors.pop()
            if b[0].color == self.color:
                sameColorNeighbors.add(b)
        return sameColorNeighbors

    def findNeighborPositions(self, line, spot, game):
        if line%2 == 0:
            positions = [(line - 1, spot - 1), (line - 1, spot    ),
                         (line,     spot - 1), (line,     spot + 1),
                         (line + 1, spot - 1), (line + 1, spot    )]
        else:
            positions = [(line - 1, spot    ), (line - 1, spot + 1),
                         (line,     spot - 1), (line,     spot + 1),
                         (line + 1, spot    ), (line + 1, spot + 1)]
        neighborPositions = []
        for pos in positions:
            if pos[0] >= 0 and pos[0] < game.maxLines:
                if pos[1] >= 0 and pos[1] + pos[0]%2 < game.NB:
                    neighborPositions.append(pos)
        return neighborPositions

    def findNeighbors(self, neighborPositions, game):
        neighbors = set()
        for position in neighborPositions:
            line, spot = position[0], position[1]
            wallBloob = game.wall.lines[line][spot]
            if wallBloob != None:
                neighbors.add((wallBloob, line, spot))
        return neighbors

    def bloobsInWall(self, game):
        # Find all joined bloobs that are connected to wall top:
        bloobsInWall = []
        colors = set()
        I = 0
        for spot in range(len(game.wall.lines[0])):
            bloob = game.wall.lines[0][spot]
            if bloob != None and (bloob, 0, spot) not in bloobsInWall:
                bloobsInWall.append((bloob, 0, spot))
                colors.add(bloob.color)
                while I < len(bloobsInWall):
                    pos = self.findNeighborPositions(bloobsInWall[I][1], bloobsInWall[I][2], game)
                    neighbors = self.findNeighbors(pos, game)
                    I += 1
                    for N in neighbors:
                        if N[0] != None and N not in bloobsInWall:
                            bloobsInWall.append(N)
                            colors.add(N[0].color)
        return bloobsInWall, colors

    def move(self, dt, game):
        # Update bloob position:
        if self.sprite.y < game.wall.upperEdge - 500:
            # If bloob is under the window:
            self.sprite.position = self.positionUpdate(dt)
        else:
            # Find neighboring bloobs in the wall:
            line, spot, spot_x, spot_y = self.gridPosition(game)
            neighborPositions = self.findNeighborPositions(line, spot, game)
            neighbors = self.findNeighbors(neighborPositions, game)
            # Check for collision with neighboring bloobs:
            collision = self.collision(neighbors, game)
            # If bloob hits the top of the wall:
            top = 0
            if self.sprite.y + game.wall.bloobImageSize/2. >= game.wall.upperEdge:
                top = 1
            # When the bloob hits other bloobs in the wall or the top:
            if collision or top:
                # Find bloobs of the same color:
                sameColorNeighbors = self.selectSameColor(neighbors)
                # If there isn't bloob of the same color, add bloob to wall:
                if len(sameColorNeighbors) == 0:
                    game.wall.addBloobToWall(self, line, spot, spot_x, spot_y, game)
                    return
                # When there are bloobs with the same color:
                else:
                    checklist = list(sameColorNeighbors)
                    el = 0
                    while el < len(checklist):
                        b = checklist[el]
                        el += 1
                        neighborsOfNeighbor = self.findNeighborPositions(b[1], b[2], game)
                        for b1 in neighborsOfNeighbor:
                            l = b1[0]
                            s = b1[1]
                            bloob = game.wall.lines[l][s]
                            if bloob != None and bloob.color == self.color:
                                if (bloob, l, s) not in checklist:
                                    checklist.append((bloob, l, s))
                                    sameColorNeighbors.add((bloob, l, s))
                    S = len(sameColorNeighbors)
                    # Max one bloob of same color:
                    if S < 2:
                        game.wall.addBloobToWall(self, line, spot, spot_x, spot_y, game)
                    # At least two bloobs of same color:
                    else:
                        # Delete bloobs of same color:
                        while sameColorNeighbors:
                            b, l, s = sameColorNeighbors.pop()
                            game.wall.deleteBloobFromWall(b, l, s, game)
                        # Find bloobs in continuous wall:
                        bloobsInWall, game.wall.colors = self.bloobsInWall(game)
                        # Find all bloobs in the wall:
                        allBloobs = set()
                        for l in range(len(game.wall.lines)):
                            for s in range(len(game.wall.lines[l])):
                                if game.wall.lines[l][s] != None:
                                    allBloobs.add((game.wall.lines[l][s], l, s))
                        # Delete bloobs in fallingBloobs:
                        fallingBloobs = allBloobs.difference(bloobsInWall)
                        O = len(fallingBloobs)
                        while fallingBloobs:
                            b, l, s = fallingBloobs.pop()
                            game.wall.deleteBloobFromWall(b, l, s, game)
                        # Delete the shooted bloob:
                        self.sprite.delete()
                        game.movingBloobs.remove(self)
                        game.cannon.enable()
                        game.scoreCount(S, O)
                        if game.wall.emptyWall == False:
                            game.cannon.load(game)
                    return
            # If the bloob hits the edge of the wall it reflects back:
            self.reflection(game)
            # Update bloob coordinates:
            self.sprite.position = self.positionUpdate(dt)


class Wall(object):
    def __init__(self, game):
        self.bloobImageSize = 36
        self.lineHeight = self.bloobImageSize - 1    # Height of bloobs line
        self.bloobSpotWidth = self.bloobImageSize + 1
        self.upperEdge = game.window.height - 2
        self.leftEdge = 1
        self.rightEdge = self.leftEdge + (game.NB - 1)*self.bloobSpotWidth + self.bloobImageSize
        self.firstLine_y = self.upperEdge - self.bloobImageSize/2.
        self.colors = set()
        self.emptyWall = False
        for image in settings.bloobs:
            self.colors.add(image[1])
        self.lines = []
        y = self.firstLine_y
        for line in range(game.maxLines):
            nb = game.NB - line%2
            if line < game.numberOfLines:
                x = self.leftEdge + self.bloobImageSize/2.*((line%2) + 1)
                self.lines.append(self.generateBloobsLine(nb, x, y))
                y = y - self.lineHeight
            else:
                self.lines.append([None for i in range(nb)])

    def generateBloobsLine(self, nb, x, y):
        line = []
        for b in range(nb):
            line.append(Bloob(x, y, self.colors))
            x += self.bloobSpotWidth
        return line

    def checkEmpty(self):
        empty = True
        for spot in self.lines[0]:
            if spot != None:
                empty = False
        return empty or False

    def deleteBloobFromWall(self, bloob, line, spot, game):
        game.wall.lines[line][spot] = None
        bloob.sprite.delete()
        self.emptyWall = self.checkEmpty()
        #posle signal ze ma spadnut, vymaze ho z self.lines
        #a az bude dole, zmaze uplne

    def addBloobToWall(self, bloob, line, spot, spot_x, spot_y, game):
        game.movingBloobs.remove(bloob)
        self.lines[line][spot] = bloob
        bloob.sprite.x = spot_x
        bloob.sprite.y = spot_y
        bloob.sprite.group = foreground
        game.cannon.enable()
        game.cannon.load(game)
        game.scoreCount(0, 0)


class Cannon(object):
    def __init__(self):
        # Set image's anchor point
        image = pyglet.resource.image(settings.cannon)
        image.anchor_x, image.anchor_y = image.width/2., 42
        x, y = settings.cannonPosition
        self.sprite = pyglet.sprite.Sprite(image, x=x, y=y, batch=batch,
                                            group=top1)
        self.enabled = True

    def load(self, game):
        game.bloobsInCannon[0].sprite.position = settings.bloobInCannonPosition
        x, y = settings.nextBloobPosition
        game.bloobsInCannon.append(Bloob(x, y, game.wall.colors))
        game.bloobsInCannon[1].sprite.group = top2

    def enable(self):
        self.enabled = True

    def shoot(self, game):
        # Shoot the bloob:
        if self.enabled == True:
            self.enabled = False
            game.bloobsUsed += 1
            game.bloobsUsedLabel.text = str(game.bloobsUsed)
            rad = pi/2 - radians(self.sprite.rotation)
            shootedBloob = game.bloobsInCannon.pop(0)
            shootedBloob.radians = rad
            game.movingBloobs.append(shootedBloob)
            pressed_keys.clear()

    def tick(self, dt, game):
        # Moving the cannon with arrow keys:
        delta_rotation = 1
        if 'RIGHT' in pressed_keys:
            self.sprite.rotation += delta_rotation
        if 'LEFT' in pressed_keys:
            self.sprite.rotation -= delta_rotation
            self.score += self.lastShot
            self.lastShotLabel.text = str(self.lastShot)
            self.scoreLabel.text = str(self.score)

        # Moving the cannon with mouse:
        if game.mouseMovement != None:
            self.sprite.rotation += game.mouseMovement
            game.mouseMovement = None
        self.sprite.rotation = min(self.sprite.rotation, 75)
        self.sprite.rotation = max(self.sprite.rotation, -75)
        # Shooting the bloob from cannon:
        if 'SHOOT' in pressed_keys or 'SHOOT' in pressed_mouse:
            self.shoot(game)


class DangerBar(object):
    def __init__(self, game):
        pass


class Game(object):
    def __init__(self):
        self.window = pyglet.window.Window(800, 600)
        self.window.set_mouse_visible(False)
        self.window.push_handlers(keys)
        self.mouseMovement = None
        self.cannon = Cannon()
        self.movingBloobs = []
        self.initialSettings()
        self.showLabels()
        self.tnt = DangerBar(self)

    def initialSettings(self):
        self.level = 1
        self.score = 0
        self.bloobsUsed = 0
        self.lastShot = 0
        self.NB = 17    # number of bloobs' spots in line 0, 2, 4, ...
        self.maxLines = 14
        self.numberOfLines = 2  # 9
        self.start()

    def deleteLabel(self, dt, label):
        label.delete()

    def nextLevel(self):
        self.bonusLabel = pyglet.text.Label(text='Fullscreen bonus = 1000',
                            font_size=30, x=350, y=300, color=(0, 0, 0, 200),
                            anchor_x='center', anchor_y='center', batch=batch)
        pyglet.clock.schedule_once(self.deleteLabel, 2, self.bonusLabel)
        self.level += 1
        self.levelLabel.text = 'level: '+ str(self.level)
        self.score += 1000
        self.scoreLabel.text = str(self.score)
        self.maxLines -= 1
        self.numberOfLines -= 1
        self.start()

    def start(self):
        self.wall = Wall(self)
        x1, y1 = settings.bloobInCannonPosition
        x2, y2 = settings.nextBloobPosition
        self.bloobsInCannon = [Bloob(x1, y1, self.wall.colors),
                               Bloob(x2, y2, self.wall.colors)]
        for bloob in self.bloobsInCannon:
            bloob.sprite.group = top2

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

    def scoreCount(self, S, O):
        if S > 1:
            self.lastShot = 10 + (S - 2)*(S + 4) + 10*O**2
        else:
            self.lastShot = 0
        self.score += self.lastShot
        self.lastShotLabel.text = str(self.lastShot)
        self.scoreLabel.text = str(self.score)

    def update(self, dt):
        if self.wall.emptyWall == True:
            self.nextLevel()
            return
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
foreground = pyglet.graphics.OrderedGroup(0.5)
top1       = pyglet.graphics.OrderedGroup(0.8)
top2       = pyglet.graphics.OrderedGroup(1)


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

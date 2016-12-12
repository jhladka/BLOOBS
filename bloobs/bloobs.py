#!/usr/bin/python
# -*- coding: utf-8 -*-

# Written for Python 2.7.6

import pyglet
from pyglet.window import mouse
import settings
from bloob import Bloob
from wall import Wall
from cannon import Cannon
from danger_bar import DangerBar
from score_window import ScoreWindow


class Game(object):

    """
    Represents game.
    """

    def __init__(self, batch):
        self.batch = batch
        self.applause = pyglet.media.load('SOUNDS/yeah.wav', streaming=False)
        self.nextlevel = pyglet.media.load('SOUNDS/nextlevel.wav', streaming=False)
        self.gameover = pyglet.media.load('SOUNDS/gameover.wav', streaming=False)
        self.writeName = False
        self.control = None
        self.window = pyglet.window.Window(800, 600, caption='BLOOBS', vsync=0)
        self.bloobImageSize = 36
        self.NB = 17    # number of bloobs' spots in line 0, 2, 4, ...
        self.lineHeight = self.bloobImageSize - 1    # Height of bloobs line
        self.spotWidth = self.bloobImageSize + 1
        self.leftEdge = 1
        self.rightEdge = self.leftEdge + (self.NB - 1)*self.spotWidth + self.bloobImageSize
        self.window.set_mouse_visible(False)
        self.window.push_handlers(keys)
        self.mouseMovement = None
        self.cannon = Cannon(self.batch)
        self.newGameSettings()
        self.showLabels()

    def newGameSettings(self):
        """
        Sets initial settings.
        """
        self.level = 1
        self.score = 0
        self.bloobsUsed = 0
        self.lastShot = 0
        self.dangerBar = DangerBar(self)
        self.upperEdge = self.window.height - 2
        self.maxLines = 14
        self.numberOfLines = 9  # 9
        self.movingBloobs = []
        self.start()

    def deleteLabel(self, dt, label):
        """
        Deletes label.
        """
        label.delete()

    def nextLevelSettings(self):
        """
        Sets the options for next level.
        """
        self.bonusLabel = pyglet.text.Label(text='Fullscreen bonus = 1000',
                        font_size=34, x=300, y=400, color=(0, 0, 0, 200),
                        anchor_x='center', anchor_y='center', batch=self.batch)
        pyglet.clock.schedule_once(self.deleteLabel, 2, self.bonusLabel)
        self.level += 1
        self.levelLabel.text = 'level: '+ str(self.level)
        self.score += 1000
        self.scoreLabel.text = str(self.score)
        self.dangerBar = DangerBar(self)
        self.maxLines -= 1
        self.upperEdge -= self.lineHeight
        self.start()

    def start(self):
        """
        Starts the game.
        """
        self.wall = Wall(self)
        x1, y1 = settings.bloobInCannonPosition
        x2, y2 = settings.nextBloobPosition
        self.bloobsInCannon = [Bloob(x1, y1, self.wall.images[:6],
                                self.wall.colors[:6], self.batch),
                               Bloob(x2, y2, self.wall.images[:6],
                               self.wall.colors[:6], self.batch)]
        for bloob in self.bloobsInCannon:
            bloob.sprite.group = settings.layer_cannonBloob
        pyglet.clock.schedule(self.update)

    def showLabels(self):
        """
        Shows labels.
        """
        self.bloobsUsedLabel = pyglet.text.Label(text=str(self.bloobsUsed),
                        font_size=24, x=775, y=233, color=(0, 0, 0, 200),
                        anchor_x='right', anchor_y='center', batch=self.batch)
        self.lastShotLabel = pyglet.text.Label(text=str(self.lastShot),
                        font_size=24, x=775, y=147, color=(0, 0, 0, 200),
                        anchor_x='right', anchor_y='center', batch=self.batch)
        self.scoreLabel = pyglet.text.Label(text=str(self.score),
                        font_size=24, x=775, y=63, color=(0, 0, 0, 200),
                        anchor_x='right', anchor_y='center', batch=self.batch)
        self.levelLabel = pyglet.text.Label(text='level: '+ str(self.level),
                        font_size=20, x=95, y=50, color=(0, 0, 0, 200),
                        anchor_x='center', anchor_y='center', batch=self.batch)

    def scoreCount(self, S, O):
        """
        Counts score.
        """
        if S > 1:
            self.lastShot = 10 + (S - 2)*(S + 4) + 10*O**2
        else:
            self.lastShot = 0
        self.score += self.lastShot
        if self.lastShot > 100:
            self.applause.play()
        self.lastShotLabel.text = str(self.lastShot)
        self.scoreLabel.text = str(self.score)

    def gameOver(self):
        """
        Ends the game.
        """
        pyglet.clock.unschedule(self.update)
        self.control ='gameOver'
        self.gameover.play()
        self.gameOverLabels = []
        self.gameOverLabel = pyglet.text.Label(text='GAME OVER!!!', bold=True,
                    font_size=34, x=340, y=550, color=(0, 0, 50, 250),
                    anchor_x='center', anchor_y='center', batch=self.batch,
                    group=settings.layer_score)
        self.yourScore = pyglet.text.Label(text='Your score: ' + str(self.score),
                    bold=True, font_size=24, x=340, y=500, color=(0, 50, 0, 250),
                    anchor_x='center', anchor_y='center',
                    batch=self.batch, group=settings.layer_score)
        self.helpLabel = pyglet.text.Label(text='', color=(50, 0, 0, 250),
                    bold=True, font_size=16, x=340, y=190, anchor_x='center',
                    anchor_y='center', batch=self.batch,
                    group=settings.layer_scoreTable)
        self.gameOverLabels = [self.gameOverLabel, self.yourScore, self.helpLabel]
        self.highestScore = ScoreWindow(self, 340, 330)
        if self.writeName == False:
            self.helpLabel.text = 'Press space to restart.'

    def newGame(self):
        """
        Play new game.
        """
        self.control = None
        for label in self.gameOverLabels:
            label.delete()
        self.highestScore.sprite.delete()
        while self.highestScore.scoreTable:
            label = self.highestScore.scoreTable.pop()
            label.delete()
        pressed_keys.clear()
        self.cannon.enable()
        self.newGameSettings()
        self.levelLabel.text = 'level: '+ str(self.level)
        self.bloobsUsedLabel.text = str(self.bloobsUsed)
        self.lastShotLabel.text = str(self.lastShot)
        self.scoreLabel.text = str(self.score)

    def updateName(self, text):
        if self.writeName:
            if text == 'DELETE':
                self.highestScore.nameLabel.text = self.highestScore.nameLabel.text[:-1]
            else:
                self.highestScore.nameLabel.text += text

    def saveName(self):
        self.helpLabel.delete()
        self.highestScore.saveScore()

    def update(self, dt):
        """
        Updates the game.
        """
        if self.wall.emptyWall == True:
            self.nextlevel.play()
            pyglet.clock.unschedule(self.update)
            self.nextLevelSettings()
            return
        # Update the positions of all objects:
        if dt > 18./shot_velocity:  # 18 = bloobImageSize/2
            dt = 0.95*18./shot_velocity
        self.cannon.tick(dt, self, pressed_keys, pressed_mouse)
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

img = pyglet.resource.image(settings.background)
Background = pyglet.sprite.Sprite(img=img, batch=batch,
                        group=settings.layer_background)
game = Game(batch)
shot_velocity = settings.velocity

pyglet.clock.set_fps_limit(120)
fps_display = pyglet.clock.ClockDisplay()

@game.window.event
def on_text(text):
    game.updateName(text)

@game.window.event
def on_draw():
    game.window.clear()
    game.batch.draw()
    #fps_display.draw()

@game.window.event
def on_key_press(symbol, modifiers):
    if game.writeName == True:
        if symbol == key.BACKSPACE:
            game.updateName('DELETE')
        elif symbol == key.ENTER:
            game.saveName()
            game.writeName = False
            game.helpLabel.text = 'Press space to restart.'
    elif game.control == 'gameOver':
        if symbol == key.SPACE:
            game.newGame()
    elif symbol in key_control:
        pressed_keys.add(key_control[symbol])

@game.window.event
def on_key_release(symbol, modifiers):
    if symbol in key_control:
        pressed_keys.discard(key_control[symbol])

@game.window.event
def on_mouse_motion(x, y, dx, dy):
    game.mouseMovement = dx

@game.window.event
def on_mouse_press(x, y, button, modifiers):
    pressed_mouse.add(mouse_control[button])

@game.window.event
def on_mouse_release(x, y, button, modifiers):
    pressed_mouse.discard(mouse_control[button])


pyglet.app.run()

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
import os.path

class Game(object):

    """
    Represent game.
    """

    def __init__(self, keys):

        # Ordered groups:
        self.batch = pyglet.graphics.Batch()

        # Setup our keyboard handler and mouse:
        self.pressed_keys = set()
        self.pressed_mouse = set()

        # Set sounds and images path:
        self.my_path = os.path.abspath(os.path.dirname(__file__))
        self.sounds_path = os.path.join(self.my_path, 'SOUNDS/')
        #self.images_path = os.path.join(self.my_path, 'PNG/')

        # Background picture:
        img = pyglet.resource.image(settings.background)
        self.Background = pyglet.sprite.Sprite(img=img, batch=self.batch,
                                group=settings.layer_background)

        # Set sounds:
        self.applause = pyglet.media.load(self.sounds_path + 'yeah.wav', streaming=False)
        self.nextlevel = pyglet.media.load(self.sounds_path + 'nextlevel.wav', streaming=False)
        self.gameover = pyglet.media.load(self.sounds_path + 'gameover.wav', streaming=False)

        # Set control parameters:
        self.writeName = False
        self.control = None

        # Window:
        self.window = pyglet.window.Window(800, 600, caption='BLOOBS', vsync=0)
        self.window.set_mouse_visible(False)
        self.window.push_handlers(keys)
        self.mouseMovement = None

        # Wall settings:
        self.NB = 17        # number of bloobs' spots in line 0, 2, 4, ...
        self.bloobImageSize = 36
        self.lineHeight = self.bloobImageSize - 1   # height of bloobs line
        self.spotWidth = self.bloobImageSize + 1
        self.leftEdge = 1
        self.rightEdge = self.leftEdge + (self.NB - 1)*self.spotWidth + self.bloobImageSize

        # Generate cannon:
        self.cannon = Cannon(self)

        # Set shot velocity:
        self.shot_velocity = settings.velocity

        self.newGameSettings()
        self.showLabels()

    def newGameSettings(self):
        """
        Set initial settings.
        """

        self.level = 1
        self.score = 0
        self.bloobsUsed = 0
        self.lastShot = 0

        # Generate danger bar:
        self.dangerBar = DangerBar(self)

        # Set the wall:
        self.upperEdge = self.window.height - 2
        self.maxLines = 14
        self.numberOfLines = 9  # 9

        self.movingBloobs = []
        self.start()

    def deleteLabel(self, dt, label):
        """
        Delete label.
        """

        label.delete()

    def nextLevelSettings(self):
        """
        Set the options for next level.
        """

        self.level += 1
        self.levelLabel.text = 'level: '+ str(self.level)

        # Add 1000 points bonus for emptying the wall:
        self.score += 1000
        self.scoreLabel.text = str(self.score)
        self.bonusLabel = pyglet.text.Label(text='Fullscreen bonus = 1000',
                        font_size=34, x=300, y=400, color=(0, 0, 0, 200),
                        anchor_x='center', anchor_y='center', batch=self.batch)
        pyglet.clock.schedule_once(self.deleteLabel, 2, self.bonusLabel)

        # Reset danger bar:
        self.dangerBar = DangerBar(self)

        # Move wall one line down in next level:
        self.maxLines -= 1
        self.upperEdge -= self.lineHeight

        self.start()

    def start(self):
        """
        Start the game.
        """

        # Generate the wall of bloobs:
        self.wall = Wall(self)

        # Generate bloobs in cannon:
        x1, y1 = settings.bloobInCannonPosition
        x2, y2 = settings.nextBloobPosition
        self.bloobsInCannon = [Bloob(x1, y1, self.wall.images[:6],
                                self.wall.colors[:6], self.batch,
                                self.sounds_path),
                               Bloob(x2, y2, self.wall.images[:6],
                               self.wall.colors[:6], self.batch,
                               self.sounds_path)]
        for bloob in self.bloobsInCannon:
            bloob.sprite.group = settings.layer_cannonBloob

        # Set regular update of the screen:
        pyglet.clock.schedule(self.update)

    def showLabels(self):
        """
        Show labels.
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
        Count score.
        """

        if S > 1:
            self.lastShot = 10 + (S - 2)*(S + 4) + 10*O**2
        else:
            self.lastShot = 0
        self.score += self.lastShot

        # Play applause:
        if self.lastShot > 100:
            self.applause.play()

        # Refresh score labels:
        self.lastShotLabel.text = str(self.lastShot)
        self.scoreLabel.text = str(self.score)

    def gameOver(self):
        """
        Ends the game.
        """

        # Stop updating screen:
        pyglet.clock.unschedule(self.update)


        self.control ='gameOver'
        self.gameover.play()

        # Show labels for the end of the game:
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

        # Show instruction for restart:
        if self.writeName == False:
            self.helpLabel.text = 'Press space to restart.'

    def newGame(self):
        """
        Play new game.
        """

        # Reset control parameter:
        self.control = None

        # Delete labels and highest score table:
        for label in self.gameOverLabels:
            label.delete()
        self.highestScore.sprite.delete()
        while self.highestScore.scoreTable:
            label = self.highestScore.scoreTable.pop()
            label.delete()

        # Reset cannon control:
        self.pressed_keys.clear()
        self.cannon.enable()

        self.newGameSettings()

        # Show labels:
        self.levelLabel.text = 'level: '+ str(self.level)
        self.bloobsUsedLabel.text = str(self.bloobsUsed)
        self.lastShotLabel.text = str(self.lastShot)
        self.scoreLabel.text = str(self.score)

    def updateName(self, text):
        """
        Show player's name on the screen
        """

        if self.writeName:
            if text == 'DELETE':
                self.highestScore.nameLabel.text = self.highestScore.nameLabel.text[:-1]
            else:
                self.highestScore.nameLabel.text += text

    def saveName(self):
        """
        Save player's name
        """

        self.helpLabel.delete()
        self.highestScore.saveScore(self.my_path)

    def update(self, dt):
        """
        Update the game.
        """

        # Go to next level after emptying the wall:
        if self.wall.emptyWall == True:
            self.nextlevel.play()
            pyglet.clock.unschedule(self.update)
            self.nextLevelSettings()
            return

        # Correction so that bloob can move at most a distance of bloob's radius
        # in each frame (in case CPU is slow or busy):
        if dt > self.bloobImageSize/2./self.shot_velocity:
            dt = 0.95*18./self.shot_velocity

        # Update the positions of cannon:
        self.cannon.tick(dt, self, self.pressed_keys, self.pressed_mouse)

        # Update the positions of moving bloob:
        for b in self.movingBloobs:
            b.move(dt, self)


def main():

    key = pyglet.window.key
    keys = key.KeyStateHandler()
    key_control = {
            key.UP:    'SHOOT',
            key.RIGHT: 'RIGHT',
            key.LEFT:  'LEFT',
            }
    mouse_control = {
            mouse.LEFT:     'SHOOT',
            mouse.MIDDLE:   'SHOOT',
            }

    # Game object:
    game = Game(keys)

    # Set frames per second:
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

        # Writing player's name:
        if game.writeName == True:
            if symbol == key.BACKSPACE:
                game.updateName('DELETE')
            elif symbol == key.ENTER:
                game.saveName()
                game.writeName = False
                game.helpLabel.text = 'Press space to restart.'

        # Setting new game:
        elif game.control == 'gameOver':
            if symbol == key.SPACE:
                game.newGame()

        # Setting game action:
        elif symbol in key_control:
            game.pressed_keys.add(key_control[symbol])

    @game.window.event
    def on_key_release(symbol, modifiers):
        if symbol in key_control:
            game.pressed_keys.discard(key_control[symbol])

    @game.window.event
    def on_mouse_motion(x, y, dx, dy):
        game.mouseMovement = dx

    @game.window.event
    def on_mouse_press(x, y, button, modifiers):
        game.pressed_mouse.add(mouse_control[button])

    @game.window.event
    def on_mouse_release(x, y, button, modifiers):
        game.pressed_mouse.discard(mouse_control[button])


    pyglet.app.run()

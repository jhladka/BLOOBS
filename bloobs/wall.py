from random import choice
import settings
import pyglet
from bloob import Bloob

class Wall(object):

    """
    Represent the wall of bloobs.
    """

    def __init__(self, game):
        """
        Initial settings
        """

        # Wall position:
        self.top = game.upperEdge
        self.levelMaxLines = game.maxLines
        self.firstLine_y = game.upperEdge - game.bloobImageSize/2.

        # Set wall (brick) bars:
        nbBars = int((game.window.height - game.upperEdge)/game.lineHeight)
        self.wallBar = []
        x, y = game.leftEdge, game.window.height
        image = pyglet.resource.image(settings.wallBar)
        for n in range(nbBars):
            image.anchor_x, image.anchor_y = 0, image.height
            self.wallBar.append(pyglet.sprite.Sprite(image, x=x, y=y,
                            batch=game.batch, group=settings.layer_wall))
            y -= game.lineHeight

        # Wall parameters:
        self.emptyWall = False
        self.images = settings.bloobs
        self.colors = []
        for image in self.images:
            self.colors.append(image[1])

        # Fill the wall using random bloobs:
        self.lines = self.fillWallRandomly(game)

    def fillWallRandomly(self, game):
        """
        Fill the wall with random bloobs.
        """

        # Choose number of bloobs in the wall:
        B = 0
        for line in range(game.numberOfLines):
            for spot in range(game.NB - line%2):
                B += 1
        skullNumber = int((game.level - 1)*15/game.level)

        # Make a list of B random bloobs:

        # If level=1 do not draw skulls in the wall, choose only first 6 images:
        if game.level == 1:
            Max = 6
        else:
            Max = 7

        bloobs = []
        nbSkull = 0
        while len(bloobs) < B:
            if nbSkull < skullNumber:
                bloobs.append(Bloob(0, 0, self.images[:Max], self.colors[:Max],
                                    game.batch, game.sounds_path))
                if bloobs[-1].color == 'black':
                    nbSkull += 1
            else:
                bloobs.append(Bloob(0, 0, self.images[:6], self.colors[:6],
                                    game.batch, game.sounds_path))

        # Fill the wall with bloobs:
        lines = []
        y = self.firstLine_y
        for line in range(game.maxLines):
            nbSpots = game.NB - line%2
            if line < game.numberOfLines:
                lines.append([])
                x = game.leftEdge + game.bloobImageSize/2.*((line%2) + 1)
                while len(lines[-1]) < nbSpots:
                    bloob = choice(bloobs)
                    if line == 0:
                        if bloob.color == 'black':
                            continue
                    bloobs.remove(bloob)
                    bloob.sprite.x, bloob.sprite.y = x, y
                    lines[-1].append(bloob)
                    x += game.spotWidth
                y = y - game.lineHeight
            else:
                lines.append([None for i in range(nbSpots)])
        return lines

    def checkEmpty(self):
        """
        Check if the wall is empty.
        """

        empty = True
        for spot in self.lines[0]:
            if spot != None:
                empty = False
        return empty or False

    def deleteBloobFromWall(self, bloob, line, spot, game):
        """
        Delete particular bloob from the wall.
        """

        game.wall.lines[line][spot] = None
        bloob.sprite.delete()
        self.emptyWall = self.checkEmpty()

    def addBloobToWall(self, bloob, line, spot, spot_x, spot_y, game, dt):
        """
        Add shooted bloob to the wall.
        """

        # Change bloob's status from 'shooted' to 'wall bloob':
        game.movingBloobs.remove(bloob)
        self.lines[line][spot] = bloob
        bloob.sprite.x = spot_x
        bloob.sprite.y = spot_y
        bloob.sprite.group = settings.layer_wall

        # Reset the cannon, load it and enable shooting:
        game.cannon.enable()
        game.cannon.load(game)
        game.scoreCount(0, 0)

        # Add danger bar:
        game.dangerBar.moveDanger(1, game)

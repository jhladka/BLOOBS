import settings
import pyglet
from bloob import Bloob

class DangerBar(object):

    """
    Represent the danger bar.
    """

    def __init__(self, game):
        """
        Initial settings: crash sound, image, position
        """

        self.crash = pyglet.media.load(game.sounds_path + "crash.wav", streaming=False)
        self.image = pyglet.resource.image(settings.tnt)
        self.x, self.y = settings.tntPosition
        self.dy = 36.5
        self.danger = []
        self.max_danger = 7

    def moveDanger(self, addDanger, game):
        """
        Add or delete danger according to the last shot.
        """

        y = self.y + len(self.danger)*self.dy

        # Add danger:
        for i in range(addDanger):

            # Break if danger is already maximal:
            if len(self.danger) == self.max_danger:
                break

            self.danger.append(pyglet.sprite.Sprite(self.image, x=self.x, y=y,
                                batch=game.batch, group=settings.layer_cannon))
            y += self.dy

        # Delete danger:
        for i in range(-addDanger):

            # Break if danger is already minimal:
            if len(self.danger) == 0:
                break

            self.danger.pop()

        # Maximum danger:
        if len(self.danger) == self.max_danger:

            # Redraw wall, all bloobs fall one line down:
            self.crash.play()
            game.wall.top -= game.lineHeight
            game.wall.firstLine_y -= game.lineHeight
            for line in game.wall.lines:
                for spot in line:
                    if isinstance(spot, Bloob):
                        spot.sprite.y -= game.lineHeight
            game.batch.draw()

            # Check if bloob out of wall, if so -> game over:
            game.wall.levelMaxLines -= 1
            for spot in game.wall.lines[game.wall.levelMaxLines]:
                if isinstance(spot, Bloob):
                    game.gameOver()
                    return

            # Add another wall bar:
            image = pyglet.resource.image(settings.wallBar)
            image.anchor_x, image.anchor_y = 0, image.height
            x = game.leftEdge
            y = game.window.height - len(game.wall.wallBar)*game.lineHeight
            game.wall.wallBar.append(pyglet.sprite.Sprite(image, x=x, y=y,
                            batch=game.batch, group=settings.layer_wall))

            # Clear danger bar:
            self.danger = []

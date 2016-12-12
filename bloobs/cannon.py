from math import pi
from math import radians
from bloob import Bloob
import settings
import pyglet


class Cannon(object):

    """
    Represents tha cannon.
    """

    def __init__(self, batch):
        self.shot = pyglet.media.load('SOUNDS/shot.wav', streaming=False)
        # Set image's anchor point
        image = pyglet.resource.image(settings.cannon)
        image.anchor_x, image.anchor_y = image.width/2., 42
        x, y = settings.cannonPosition
        self.sprite = pyglet.sprite.Sprite(image, x=x, y=y, batch=batch,
                                            group=settings.layer_cannon)
        self.enabled = True
        self.bloobs = settings.bloobs[:6]

    def load(self, game):
        """
        Loads cannon with next bloob.
        """
        game.bloobsInCannon[0].sprite.position = settings.bloobInCannonPosition
        x, y = settings.nextBloobPosition
        game.bloobsInCannon.append(Bloob(x, y, self.bloobs,
                                game.wall.colors[:6], game.batch))
        game.bloobsInCannon[1].sprite.group = settings.layer_cannonBloob

    def enable(self):
        """
        Sets cannon to be able to shoot (after shooted bloob stops flying).
        """
        self.enabled = True

    def shoot(self, game, pressed_keys, pressed_mouse):
        """
        Shoots the bloob.
        """
        if self.enabled == True:
            self.enabled = False
            self.shot.play()
            game.bloobsUsed += 1
            game.bloobsUsedLabel.text = str(game.bloobsUsed)
            rad = pi/2 - radians(self.sprite.rotation)
            shootedBloob = game.bloobsInCannon.pop(0)
            shootedBloob.radians = rad
            game.movingBloobs.append(shootedBloob)
            pressed_keys.clear()
            pressed_mouse.clear()

    def tick(self, dt, game, pressed_keys, pressed_mouse):
        """
        Moves the cannon with arrow keys or mouse and shoots the bloob.
        """
        delta_rotation = 1
        # Mouse:
        if game.mouseMovement != None:
            self.sprite.rotation += 1.5*game.mouseMovement
            game.mouseMovement = None
        # Arrow keys:
        if 'RIGHT' in pressed_keys:
            self.sprite.rotation += delta_rotation
        elif 'LEFT' in pressed_keys:
            self.sprite.rotation -= delta_rotation
        self.sprite.rotation = min(self.sprite.rotation, 75)
        self.sprite.rotation = max(self.sprite.rotation, -75)
        # Shooting the bloob from cannon:
        if 'SHOOT' in pressed_keys or 'SHOOT' in pressed_mouse:
            self.shoot(game, pressed_keys, pressed_mouse)

from math import sin
from math import cos
from math import pi
from math import sqrt
from math import radians
from random import choice
import pyglet
import settings

class Bloob(object):

    """
    Represents the bloob.
    """

    def __init__(self, x, y, images, colors, batch):
        self.hit = pyglet.media.load('SOUNDS/hit.wav', streaming=False)
        while 1:
            bloob = choice(images)
            if bloob[1] in colors:
                break
        image = pyglet.resource.image(bloob[0])
        # Set image's anchor point
        image.anchor_x, image.anchor_y = image.width/2., image.height/2.
        self.sprite = pyglet.sprite.Sprite(image, x=x, y=y, batch=batch,
                                            group=settings.layer_wall)
        self.color = bloob[1]

    def distance(self, another_bloob):
        """
        Calculates distance between two bloobs.
        """
        dx = self.sprite.x - another_bloob.sprite.x
        dy = self.sprite.y - another_bloob.sprite.y
        return sqrt(dx**2 + dy**2)

    def reflection(self, game):
        """
        Change the movement direction of the bloob when it hits the edge.
        """
        if self.sprite.x - game.bloobImageSize/2. <= game.leftEdge:
            self.sprite.x = game.leftEdge + game.bloobImageSize/2.
            self.radians = pi - self.radians
            self.hit.play()
        elif self.sprite.x + game.bloobImageSize/2. >= game.rightEdge:
            self.sprite.x = game.rightEdge - game.bloobImageSize/2.
            self.radians = pi - self.radians
            self.hit.play()

    def collision(self, neighbors, game):
        """
        Check if there's collision with neighboring bloobs.
        """
        collision = 0
        for b in neighbors:
            d = self.distance(b[0])
            if d < game.bloobImageSize - 3:
                collision = 1
                break
        return collision

    def positionUpdate(self, dt):
        """
        Update fired bloob's position.
        """
        trajectory = settings.velocity * dt
        self.sprite.x += trajectory * cos(self.radians)
        self.sprite.y += trajectory * sin(self.radians)
        return self.sprite.x, self.sprite.y

    def selectSameColor(self, neighbors):
        """
        Returns set of direct neighboring bloobs of the same color as bloob(self).
        """
        sameColorNeighbors = set()
        while len(neighbors) > 0:
            b = neighbors.pop()
            if b[0].color == self.color:
                sameColorNeighbors.add(b)
        return sameColorNeighbors

    def gridPosition(self, x, y, game):
        """
        Calculates bloob's position in wall grid according to its current position.
        """
        Y = game.wall.top - y
        line = int(Y)/game.lineHeight
        spot_y = game.wall.top - (line + 1/2.)*game.lineHeight
        remainder = line%2
        X = x - game.leftEdge - game.spotWidth/2.*remainder
        spot = int(X)/game.spotWidth
        if spot == -1:
            spot = 0
        if spot == game.NB - remainder:
            spot -= 1
        spot_x = game.leftEdge + game.spotWidth/2.*(2*spot + 1 + remainder)
        return line, spot, spot_x, spot_y

    def findNeighborPositions(self, line, spot, game):
        """
        Returns valid grid positions of direct neighboring bloobs.
        """
        k, l, m = line - 1, line, line + 1
        r, s, t = spot - 1, spot, spot + 1
        if line%2 == 0:
            positions = [(k, r), (k, s), (l, r), (l, t), (m, r), (m, s)]
        else:
            positions = [(k, s), (k, t), (l, r), (l, t), (m, s), (m, t)]
        neighborPositions = []
        for pos in positions:
            if pos[0] >= 0 and pos[0] < game.maxLines:
                if pos[1] >= 0 and pos[1] + pos[0]%2 < game.NB:
                    neighborPositions.append(pos)
        return neighborPositions

    def findNeighbors(self, neighborPositions, game):
        """
        Return set of direct neighboring bloobs.
        """
        neighbors = set()
        for position in neighborPositions:
            line, spot = position[0], position[1]
            wallBloob = game.wall.lines[line][spot]
            if wallBloob != None:
                neighbors.add((wallBloob, line, spot))
        return neighbors

    def bloobsInWall(self, game):
        """
        Finds all joined bloobs connected to wall top.
        """
        bloobsInWall = []
        colors = []
        I = 0
        for spot in range(len(game.wall.lines[0])):
            bloob = game.wall.lines[0][spot]
            if bloob != None and (bloob, 0, spot) not in bloobsInWall:
                bloobsInWall.append((bloob, 0, spot))
                if bloob.color != 'black' and bloob.color not in colors:
                    colors.append(bloob.color)
                while I < len(bloobsInWall):
                    pos = self.findNeighborPositions(bloobsInWall[I][1],
                                                bloobsInWall[I][2], game)
                    neighbors = self.findNeighbors(pos, game)
                    I += 1
                    for N in neighbors:
                        if N[0] != None and N not in bloobsInWall:
                            bloobsInWall.append(N)
                            if N[0].color not in colors:
                                colors.append(N[0].color)
        return bloobsInWall, colors

    def deleteBunch(self, sameColorNeighbors, S, game):
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
            danger = -(game.lastShot - 19)/120
            game.dangerBar.moveDanger(danger, game)

    def move(self, dt, game):
        """
        Update bloob position.
        """
        # While bloob is under the window:
        if self.sprite.y < game.upperEdge - 500:
            self.sprite.position = self.positionUpdate(dt)
        else:
            # If bloob hits the top of the wall:
            hitTop = False
            if self.sprite.y + game.bloobImageSize/2. >= game.wall.top:
                hitTop = True
            # If the bloob hits the edge of the wall it reflects back:
            self.reflection(game)
            # Find neighboring bloobs in the wall:
            x, y = self.sprite.x, self.sprite.y
            line, spot, spot_x, spot_y = self.gridPosition(x, y, game)
            neighborPositions = self.findNeighborPositions(line, spot, game)
            neighbors = self.findNeighbors(neighborPositions, game)
            # Check for collision with neighboring bloobs:
            collision = self.collision(neighbors, game)
            # Update bloob coordinates:
            if not collision and not hitTop:
                self.sprite.position = self.positionUpdate(dt)
            # When the bloob hits the top or other bloobs in the wall:
            else:
                # Check if bloob out of wall:
                if line == game.wall.levelMaxLines:
                    game.gameOver()
                    return
                # Find bloobs of the same color:
                sameColorNeighbors = self.selectSameColor(neighbors)
                # If there isn't bloob of the same color, add bloob to wall:
                if len(sameColorNeighbors) == 0:
                    game.wall.addBloobToWall(self, line, spot, spot_x, spot_y,
                                    game, dt)
                    return
                # When there are direct neighboring bloobs with the same color,
                # find another joined bloobs of the same color:
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
                        game.wall.addBloobToWall(self, line, spot, spot_x, spot_y, game, dt)
                    # At least two bloobs of same color:
                    else:
                        # Delete bloobs of same color:
                        self.deleteBunch(sameColorNeighbors, S, game)

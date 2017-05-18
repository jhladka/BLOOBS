import settings
import pyglet
import io

class ScoreWindow(object):

    """
    Table with 10 highest score.
    """

    def __init__(self, game, x, y):
        image = pyglet.resource.image(settings.highestScore)
        image.anchor_x = image.width/2.
        image.anchor_y = image.height/2.
        self.sprite = pyglet.sprite.Sprite(image, x=x, y=y, batch=game.batch,
                                    group=settings.layer_score)
        self.playerScore = (game.score, game.level, game.bloobsUsed, '')
        self.displayTable(game)

    def displayTable(self, game):
        """
        Read highest score from file, display it and if player had one of
        10 best scores -> revise table.
        """

        with io.open(game.my_path + '/.highest_score.txt', 'r', encoding='utf8') as f:
            self.score = []
            for line in f:
                line = line.split()
                score = int(line[1]), int(line[2]), int(line[3]), ' '.join(line[4:])
                self.score.append((score))
        self.rank = self.findRank(game)
        self.showTable(game)

    def findRank(self, game):
        """
        Calculate player's rank.
        """

        from bisect import bisect_left
        self.score.sort()
        return len(self.score) - bisect_left(self.score, self.playerScore)

    def showTable(self, game):
        """
        Display table with highest score.
        """

        caption = pyglet.text.Label(text='HIGHEST SCORE:', bold=True,
                    font_size=16, x=340, y=437, anchor_x='center',
                    anchor_y='center', batch=game.batch,
                    group=settings.layer_scoreTable)
        self.scoreTable = [caption]

        # Columns' position and name:
        columns = [210, 280, 320, 370, 490]
        labels = ['rank', 'score', 'level', 'bloobs', 'player']

        for i in range(5):
            label = pyglet.text.Label(text=labels[i],
                    font_size=10, x=columns[i], y=410, anchor_x='right',
                    anchor_y='center', batch=game.batch,
                    group=settings.layer_scoreTable)
            self.scoreTable.append(label)

        # Sort ranking in decreasing order:
        self.score.sort(reverse=True)

        # Insert actual player's score:
        if self.rank < 10:
            self.score[self.rank:self.rank] = [self.playerScore]

            # Enable writing player's name:
            game.writeName = True

            # Show help:
            game.helpLabel.text = 'Write your name and press Enter'

        # Show player's name on the screen when typing:
        y = 390
        i = 1
        for line in self.score[:10]:
            for j in range(5):
                if j == 0:
                    text = '{}.'.format(i)
                else:
                    text = '%s' % line[j - 1]
                output = pyglet.text.Label(text=text, font_size=11,
                                x=columns[j], y=y, anchor_x='right',
                                anchor_y='center', batch=game.batch,
                                group=settings.layer_scoreTable)
                self.scoreTable.append(output)
            y -= 18
            i += 1

        # Remember player's name:
        if self.rank < 10:
            self.nameLabel = self.scoreTable[6 + 5*self.rank + 4]

    def saveScore(self, my_path):
        """
        Save new ranking into file.
        """

        # Remove whitespace from the beginning and end of a string:
        name = self.nameLabel.text.strip()

        # If player did not provide his name -> anonymous:
        if len(name) == 0:
            name = u'anonymous'

        # Save new rank table to file:
        self.score[self.rank] = self.score[self.rank][:-1] + (name,)
        with io.open(my_path + '/.highest_score.txt', 'w', encoding='utf8') as f:
            i = 1
            for line in self.score[:10]:
                text = '%10s. %7s%5s%7s%16s\n' % (i, line[0], line[1], line[2], line[3])
                f.write(text)
                i += 1

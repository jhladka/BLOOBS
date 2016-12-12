import settings
import pyglet

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
        10 best scores revise table.
        """
        with open('.highest_score.txt', 'r') as f:
            self.score = []
            for line in f:
                line = line.split()
                self.score.append((int(line[1]), int(line[2]), int(line[3]), line[4]))
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
            game.writeName = True
            game.helpLabel.text = 'Write your name and press Enter'
        y = 390
        i = 1
        for line in self.score[:10]:
            for j in range(5):
                if j == 0:
                    text = '{}.'.format(i)
                else:
                    text = '{}'.format(line[j - 1])
                output = pyglet.text.Label(text=text, font_size=11,
                                x=columns[j], y=y, anchor_x='right',
                                anchor_y='center', batch=game.batch,
                                group=settings.layer_scoreTable)
                self.scoreTable.append(output)
            y -= 18
            i += 1
        if self.rank < 10:
            self.nameLabel = self.scoreTable[6 + 5*self.rank + 4]

    def saveScore(self):
        """
        Save new ranking into file.
        """
        name = str(self.nameLabel.text)
        if name == '':
            name = 'anonymous'
        self.score[self.rank] = self.score[self.rank][:-1] + (name,)
        with open('.highest_score.txt', 'w') as f:
            i = 1
            for line in self.score[:10]:
                f.write('{0:>2}. {1:>7}{2:>5}{3:>7}{4:>16}\n'.format(i, *line))
                i += 1


import pyglet
from pyglet.window import mouse
import pyglet
import itertools
import chess
from game import Game

class MenuGUI(pyglet.window.Window):

    backgroundImg = pyglet.resource.image('MenuGUI/Background.png')
    exitBImg = pyglet.resource.image('MenuGUI/ExitB.png')
    exitNImg = pyglet.resource.image('MenuGUI/ExitN.png')
    pvspBImg = pyglet.resource.image('MenuGUI/PvsPB.png')
    pvspNImg = pyglet.resource.image('MenuGUI/PvsPN.png')
    pvscBImg = pyglet.resource.image('MenuGUI/PvsCB.png')
    pvscNImg = pyglet.resource.image('MenuGUI/PvsCN.png')
    mouseAxis=(-1,-1)

    def __init__(self):
        super(MenuGUI, self).__init__(900, 600,
                                       resizable=False,
                                       caption='Chess',
                                       config=pyglet.gl.Config(double_buffer=True),
                                       vsync=False)
        self.exitB = pyglet.sprite.Sprite(self.exitBImg)
        self.exitN = pyglet.sprite.Sprite(self.exitNImg)
        self.pvspB = pyglet.sprite.Sprite(self.pvspBImg)
        self.pvspN = pyglet.sprite.Sprite(self.pvspNImg)
        self.pvscB = pyglet.sprite.Sprite(self.pvscBImg)
        self.pvscN = pyglet.sprite.Sprite(self.pvscNImg)
        self.background = pyglet.sprite.Sprite(self.backgroundImg)

    def draw(self,sprite,x,y):
        sprite.x = x
        sprite.y = y
        sprite.draw()

    def on_draw(self):
        x=self.mouseAxis[0]
        y=self.mouseAxis[1]
        self.clear()
        self.background.draw()

        if (x <= 595 and x >= 305 and y <= 265 and y >= 211):
            self.draw(self.pvspB, 305, 211)
        else:
            self.draw(self.pvspN, 305, 211)

        if (x <= 598 and x >= 303 and y <= 110 and y >= 55):
            self.draw(self.exitB, 303, 55)
        else:
            self.draw(self.exitN, 303, 55)

        if (x<=634 and x>=368 and y<=189 and y>=128):
            self.draw(self.pvscB,266,128)
        else:
            self.draw(self.pvscN, 266, 128)

    def on_mouse_motion(self,x, y, dx, dy):
        self.mouseAxis = (x,y)



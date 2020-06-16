import chessGUI
import menuGUI
import boardCreatorGUI
import pyglet
from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button, OneTimeButton, Checkbox, GroupButton
from pyglet_gui.containers import VerticalContainer
from pyglet_gui.theme import Theme
from theme import getTheme


def main():
    batch = pyglet.graphics.Batch()
    mygame = boardCreatorGUI.BoardCreatorGUI(batch)

    chessGUI.pyglet.app.run()


if __name__ == '__main__':
    main()

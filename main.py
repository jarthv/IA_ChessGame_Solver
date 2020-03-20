import guiChess
from LoadFile import LoadFile


def main():
    loader = LoadFile()
    loader.mainloop()
    mygame = guiChess.Chess(loader.get_path())
    guiChess.pyglet.clock.schedule_interval(mygame.update, 1 / 60.)
    guiChess.pyglet.app.run()


if __name__ == '__main__':
    main()

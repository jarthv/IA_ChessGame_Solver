import guiChess


def main():
    mygame = guiChess.Chess()
    guiChess.pyglet.clock.schedule_interval(mygame.update, 1 / 60.)
    guiChess.pyglet.app.run()


if __name__ == '__main__':
    main()

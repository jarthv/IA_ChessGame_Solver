import chessGUI
import menuGUI
import boardCreatorGUI


def main():
    mygame = boardCreatorGUI.BoardCreatorGUI()
    chessGUI.pyglet.app.run()



if __name__ == '__main__':
    main()

#coding:utf8
from PyQt4.QtGui import QApplication

def init():
    from ljn.repository.Repository import init as repo_init
    repo_init()


def main():
    init()

    app = QApplication([])
    from ljn.ui.MainWindow import MainWindow
    mw = MainWindow()
    mw.show()
    app.exec_()

if __name__ == '__main__':
    main()

#coding:utf8
from PyQt4.QtGui import QApplication
import logging

def init():
    logging.basicConfig()

    from Backup import update_data
    update_data()

    from ljn.Repository import init as repo_init
    repo_init()


def main():
    init()

    from Backup import backup_data, get_data_file_md5
    md5 = get_data_file_md5()

    app = QApplication([])
    from ljn.ui.MainWindow import MainWindow, MainWindowDirector
    mwd = MainWindowDirector()
    mw = MainWindow()
    mw.show()
    app.exec_()

    if get_data_file_md5() != md5:
        backup_data()

if __name__ == '__main__':
    main()

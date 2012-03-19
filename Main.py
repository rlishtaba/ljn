#coding:utf8
from os.path import exists, join
from PyQt4.QtGui import QApplication, QIcon
import logging
import g

MB = 1024 * 1024

def init_log():
    from logging.handlers import RotatingFileHandler
    dir = join(g.ROOT, 'log')
    if not exists(dir):
        import os
        os.makedirs(dir)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(join(dir, 'ljn.log'), maxBytes=10 * MB, backupCount=10)
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(process)d - %(name)s %(levelname)-5s - %(message)s"))
    logger.addHandler(handler)
    logger.info('')
    logger.info('System start')


def init():
    init_log()

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
    mw.setWindowIcon(QIcon(join(g.ROOT, 'ljn.png')))
    mw.show()
    app.exec_()

    if get_data_file_md5() != md5:
        backup_data()

if __name__ == '__main__':
    main()

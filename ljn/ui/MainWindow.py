#coding:utf8
from PyQt4.QtGui import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(u'LJ Notes')

        self._create_menu()

    def _create_menu(self):
        self._create_article_menu()

    def _create_article_menu(self):
        m = self.menuBar().addMenu(u'&Articles')
        m.addAction(u'New ...').triggered.connect(self._on_new_article)
        m.addAction(u'Delete').triggered.connect(self._on_delete_article)

    def _on_new_article(self):
        print 'new article'

    def _on_delete_article(self):
        print 'delete article'

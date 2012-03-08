#coding:utf8
from PyQt4.QtGui import QMainWindow, QStackedLayout, QWidget, QHBoxLayout
from ljn.ui.component.ArticleBrowser import ArticleBrowser
from ljn.ui.component.CategoryList import CategoryList

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(u'LJ Notes')

        self.setCentralWidget(self._create_central_widget())
        self.resize(800, 600)

    def _create_central_widget(self):
        w = QWidget(self)
        layout = QHBoxLayout(w)
        layout.addLayout(self._create_lists(w))
        layout.addWidget(self._create_article_browser(w), 1)
        return w

    def _create_article_browser(self, parent):
        self.article_browser = ab = ArticleBrowser(parent)
        ab.setReadOnly(True)
        return ab

    def _create_lists(self, parent):
        self.category_list = cl = CategoryList(parent)
        layout = QStackedLayout()
        layout.addWidget(self.category_list)
        return layout

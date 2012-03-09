#coding:utf8
from PyQt4.QtGui import QMainWindow, QStackedLayout, QWidget, QHBoxLayout, QAction
from ljn.Model import Category
from ljn.Repository import get_session

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
        from ljn.ui.component.ArticleBrowser import ArticleBrowser
        self.article_browser = ab = ArticleBrowser(parent)
        ab.setReadOnly(True)
        return ab

    def _create_lists(self, parent):
        self.list_layout = layout = QStackedLayout()
        layout.addWidget(self._create_article_list(parent))
        layout.addWidget(self._create_article_list(parent))
        return layout

    def _create_category_list(self, parent):
        from ljn.ui.component.CategoryList import CategoryList
        self.category_list = cl = CategoryList(parent)
        cl.itemDoubleClicked.connect(self._open_category)
        action = QAction(cl)
        action.setShortcut("Return")
        action.triggered.connect(self._open_category)
        cl.addAction(action)
        return cl

    def _create_article_list(self, parent):
        from ljn.ui.component.ArticleList import ArticleList
        self.article_list = al = ArticleList(parent)
        al.itemDoubleClicked.connect(self._open_article)
        return al

    def _open_category(self):
        items = self.category_list.selectedItems()
        if not items:
            return

        item = items[0]
        from ljn.ui.component.CategoryList import CategoryItem
        if not isinstance(item, CategoryItem):
            return

        self.article_list.update_articles(item.category.id)
        self.list_layout.setCurrentWidget(self.article_list)

    def _open_article(self, item):
        from ljn.ui.component.ArticleList import ArticleItem
        if not isinstance(item, ArticleItem):
            self.list_layout.setCurrentWidget(self.category_list)
            return

        self.article_browser.set_article(item.article)

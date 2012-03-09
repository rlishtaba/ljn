#coding:utf8
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMainWindow, QStackedLayout, QWidget, QAction, QDockWidget

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(u'LJ Notes')

        self._create_dock_pane()

        self.setCentralWidget(self._create_article_browser(self))
        self.resize(800, 600)

    def _create_dock_pane(self):
        self.dock_pane = d = QDockWidget(self)
        d.setFeatures(QDockWidget.NoDockWidgetFeatures)
        d.setAllowedAreas(Qt.LeftDockWidgetArea)
        d.setWidget(self._create_lists())
        self.addDockWidget(Qt.LeftDockWidgetArea, d)

    def _create_article_browser(self, parent):
        from ljn.ui.component.ArticleBrowser import ArticleBrowser
        self.article_browser = ab = ArticleBrowser(parent)
        ab.setReadOnly(True)
        return ab

    def _create_lists(self):
        w = QWidget(self)
        self.list_layout = layout = QStackedLayout(w)
        layout.addWidget(self._create_category_list(w))
        layout.addWidget(self._create_article_list(w))
        self._show_category_list()
        return w

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

        action = QAction(al)
        action.setShortcut("Return")
        action.triggered.connect(self._open_article)
        al.addAction(action)

        action = QAction(al)
        action.setShortcut("Backspace")
        action.triggered.connect(self._show_category_list)
        al.addAction(action)

        return al

    def _get_selected_category_id(self):
        items = self.category_list.selectedItems()
        if not items:
            return None

        item = items[0]
        from ljn.ui.component.CategoryList import CategoryItem
        if not isinstance(item, CategoryItem):
            return None

        return item.category.id

    def _open_category(self):
        id = self._get_selected_category_id()
        if id is None:
            return

        self.article_list.update_articles(id)
        self._show_article_list()

    def _open_article(self):
        items = self.article_list.selectedItems()
        if not items:
            return

        item = items[0]
        from ljn.ui.component.ArticleList import ArticleItem
        if not isinstance(item, ArticleItem):
            self._show_category_list()
            return

        self.article_browser.set_article(item.article)

    def _show_category_list(self):
        self.dock_pane.setWindowTitle("Category List")
        self.list_layout.setCurrentWidget(self.category_list)

    def _show_article_list(self):
        from ljn.Model import Category
        from ljn.Repository import get_session
        id = self._get_selected_category_id()
        if id is not None:
            msg = ' (%s)' % Category.find_by_id(get_session(), id).name
        else:
            msg = ''
        self.dock_pane.setWindowTitle("Article List" + msg)
        self.list_layout.setCurrentWidget(self.article_list)

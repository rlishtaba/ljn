#coding:utf8
from functools import partial
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMainWindow, QStackedLayout, QWidget, QAction, QDockWidget
from ljn.Event import EventPublisher
from ljn.ui.UiUtil import create_widget_action

class MainWindow(QMainWindow):
    onWindowCreate = EventPublisher(QMainWindow)
    onWindowInit = EventPublisher(QMainWindow)

    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowTitle(u'LJ Notes')

        self._create_dock_panes()
        self.setCentralWidget(self._create_article_browser(self))

        self.word_list.onWordSelected.connect(self.article_browser.navigate_word)

        self.resize(800, 600)

        MainWindow.onWindowCreate.emit(self)
        MainWindow.onWindowInit.emit(self)
        self._create_actions()


    def _create_dock_panes(self):
        self._create_list_dock_pane()
        self._create_word_dock_pane()

    def _create_list_dock_pane(self):
        self.list_dock_pane = d = QDockWidget(self)
        d.setFeatures(QDockWidget.NoDockWidgetFeatures)
        d.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, d)

    def _create_actions(self):
        action = create_widget_action(self, "ESC", self.article_browser.setFocus)
        self.article_list.addAction(action)
        self.category_list.addAction(action)

        action = QAction(self)
        action.setShortcut("CTRL+A")
        action.setShortcutContext(Qt.ApplicationShortcut)
        action.triggered.connect(self._toggle_dock_pane_view)
        self.addAction(action)

        action = QAction(self)
        action.setShortcut("CTRL+W")
        action.setShortcutContext(Qt.ApplicationShortcut)
        action.triggered.connect(lambda : self.word_dock_pane.toggleViewAction().trigger())
        self.addAction(action)

    def _create_word_dock_pane(self):
        self.word_dock_pane = d = QDockWidget(self)
        d.setFeatures(QDockWidget.NoDockWidgetFeatures)
        d.setAllowedAreas(Qt.RightDockWidgetArea)
        d.setWidget(self._create_word_list())
        self.addDockWidget(Qt.RightDockWidgetArea, d)

    def _create_article_browser(self, parent):
        from ljn.ui.component.ArticleBrowser import ArticleBrowser
        self.article_browser = ab = ArticleBrowser(parent)
        ab.setReadOnly(True)
        ab.addAction(create_widget_action(ab, "ESC", self._set_focus_to_list))
        ab.onArticleLoaded.connect(self._update_word_list)
        return ab

    def _create_word_list(self):
        from ljn.ui.component.WordList import WordList
        self.word_list = WordList(self)
        return self.word_list

    def _set_focus_to_list(self):
        if self.article_list.isVisible():
            self.article_list.setFocus()
        else:
            self.category_list.setFocus()

    def _toggle_dock_pane_view(self):
        self.list_dock_pane.toggleViewAction().trigger()

        if self.list_dock_pane.isVisible():
            self._set_focus_to_list()

    def _update_word_list(self, article_id):
        self.word_list.update_words(article_id)
        self.word_dock_pane.setWindowTitle('Words (%d)' % len(self.word_list.new_words))


class ListDirector(object):
    def __init__(self):
        MainWindow.onWindowCreate.connect(self.window_create)
        MainWindow.onWindowInit.connect(self.window_init)

    def window_create(self, window):
        w = QWidget(window)
        window.list_layout = layout = QStackedLayout(w)
        layout.addWidget(self._create_category_list(window, w))
        layout.addWidget(self._create_article_list(window, w))
        window.list_dock_pane.setWidget(w)

    def _create_category_list(self, window, parent):
        from ljn.ui.component.CategoryList import CategoryList
        window.category_list = cl = CategoryList(parent)
        cl.itemDoubleClicked.connect(partial(self._open_category, window))
        cl.addAction(create_widget_action(cl, "Return", partial(self._open_category)))
        return cl

    def _create_article_list(self, window, parent):
        from ljn.ui.component.ArticleList import ArticleList
        window.article_list = al = ArticleList(parent)
        al.itemDoubleClicked.connect(partial(self._open_article, window))
        al.addAction(create_widget_action(al, "Return", partial(self._open_article, window)))
        al.addAction(create_widget_action(al, "Backspace", partial(self._show_category_list, window)))
        return al

    def _open_category(self, window):
        id = self._get_selected_category_id(window)
        if id is None:
            return

        window.article_list.update_articles(id)
        self._show_article_list(window)

    def _get_selected_category_id(self, window):
        items = window.category_list.selectedItems()
        if not items:
            return None

        item = items[0]
        from ljn.ui.component.CategoryList import CategoryItem
        if not isinstance(item, CategoryItem):
            return None

        return item.category.id

    def _show_article_list(self, window):
        from ljn.Model import Category
        from ljn.Repository import get_session
        id = self._get_selected_category_id(window)
        if id is not None:
            msg = ' (%s)' % Category.find_by_id(get_session(), id).name
        else:
            msg = ''
        window.list_dock_pane.setWindowTitle("Article List" + msg)
        window.list_layout.setCurrentWidget(window.article_list)

    def _open_article(self, window):
        items = window.article_list.selectedItems()
        if not items:
            return

        item = items[0]
        from ljn.ui.component.ArticleList import ArticleItem
        if not isinstance(item, ArticleItem):
            self._show_category_list(window)
            return

        from ljn.Model import Article
        from ljn.Repository import get_session

        window.article_browser.setFocus()
        window.article_browser.set_article(Article.find_by_id(get_session(), item.article.id))

    def _show_category_list(self, window):
        window.list_dock_pane.setWindowTitle("Category List")
        window.list_layout.setCurrentWidget(window.category_list)


    def window_init(self, window):
        pass

class MainWindowDirector(object):
    def __init__(self):
        self._list_director = ListDirector()

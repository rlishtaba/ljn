#coding:utf8
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QListWidget, QListWidgetItem, QInputDialog, QMessageBox
from ljn.Model import Article, Category
from ljn.Repository import get_session
from ljn.ui.UiUtil import create_widget_action
from ljn.ui.component import ArticleEditor

class ArticleItem(QListWidgetItem):
    def __init__(self, article):
        QListWidgetItem.__init__(self, article.title)

        self.article = article


class ArticleList(QListWidget):

    onArticleCreated = pyqtSignal(int)

    def __init__(self, parent):
        QListWidget.__init__(self, parent)

        self.category_id = None
        self.update_articles()
        self.addAction(create_widget_action(self, "F2", self._rename_article))
        self.addAction(create_widget_action(self, "Del", self._del_article))
        self.addAction(create_widget_action(self, "CTRL+N", self._new_article))

    def update_articles(self, category_id=None):
        self.clear()
        self.addItem('..')

        if category_id is None:
            category_id = self.category_id

        if category_id is None:
            return

        self.category_id = category_id
        category = Category.find_by_id(get_session(), category_id)

        if category is not None:
            for a in category.articles:
                self.addItem(ArticleItem(a))


    def _new_article(self):
        article = ArticleEditor.create_new_article(self)
        if article is None:
            return

        article.category_id = self.category_id
        s = get_session()
        s.add(article)
        s.commit()
        self.update_articles()

        self.onArticleCreated.emit(article.id)


    def _rename_article(self):
        items = self.selectedItems()
        if not items:
            return

        article = items[0].article
        text, result = QInputDialog.getText(self, 'Rename article', 'New article title:', text=article.title)
        if not result:
            return

        text = str(text)
        if not text or text == article.title:
            return

        s = get_session()
        a = Article.find_by_id(s, article.id)
        a.title = text
        s.commit()
        self.update_articles()


    def _del_article(self):
        items = self.selectedItems()
        if not items:
            return

        article = items[0].article
        msg = 'Delete "%s"?' % article.title
        btn = QMessageBox.question(self, 'Delete article', msg, QMessageBox.Yes | QMessageBox.No)
        if btn == QMessageBox.No:
            return

        s = get_session()
        s.delete(Article.find_by_id(s, article.id))
        s.commit()
        self.update_articles()

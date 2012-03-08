#coding:utf8
from PyQt4.QtGui import QListWidget, QListWidgetItem, QAction, QInputDialog, QMessageBox
from ljn.Model import Article, Category
from ljn.Repository import get_session

class ArticleItem(QListWidgetItem):
    def __init__(self, article):
        QListWidgetItem.__init__(self, article.title)

        self.article = article


class ArticleList(QListWidget):
    def __init__(self, parent):
        QListWidget.__init__(self, parent)

        self.update_articles()
        self.addAction(self._create_rename_action())
        self.addAction(self._create_delete_action())

    def _create_rename_action(self):
        a = QAction("Rename", self)
        a.setShortcut("F2")
        a.triggered.connect(self._rename_article)
        return a

    def _create_delete_action(self):
        a = QAction("Delete", self)
        a.setShortcut("Del")
        a.triggered.connect(self._del_article)
        return a

    def update_articles(self, category=None):
        self.category = category
        self.clear()
        self.addItem('..')
        if category is None:
            return

        for a in category.articles:
            self.addItem(ArticleItem(a))

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
        self.update_articles(Category.find_by_id(get_session(), self.category.id))


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
        self.update_articles(Category.find_by_id(get_session(), self.category.id))

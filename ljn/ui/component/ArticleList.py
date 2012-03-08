#coding:utf8
from PyQt4.QtGui import QListWidget, QListWidgetItem

class ArticleItem(QListWidgetItem):
    def __init__(self, article):
        QListWidgetItem.__init__(self, article.title)

        self.article = article


class ArticleList(QListWidget):
    def __init__(self, parent):
        QListWidget.__init__(self, parent)

        self.update_articles()

    def update_articles(self, category=None):
        self.clear()
        self.addItem('..')
        if category is None:
            return

        for a in category.articles:
            self.addItem(ArticleItem(a))

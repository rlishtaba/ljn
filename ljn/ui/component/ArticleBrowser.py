#coding:utf8
from PyQt4.QtGui import QTextEdit

class ArticleBrowser(QTextEdit):
    def __init__(self, parent):
        QTextEdit.__init__(self, parent)

    def set_article(self, article):
        self.setText(article.content)

#coding:utf8
from PyQt4.QtGui import QTextEdit

STYLE_SHEET = r'''
QTextEdit {
    font-family: Cambria,"Hoefler Text",Georgia,"Times New Roman",serif;
    font-size: 22px;
    font-weight: 400;
    color: #3D3936;
    background-color: #F4EED9;
}
'''

class ArticleBrowser(QTextEdit):
    def __init__(self, parent):
        QTextEdit.__init__(self, parent)

        self.setStyleSheet(STYLE_SHEET)

    def set_article(self, article):
        self.setText(article.content)

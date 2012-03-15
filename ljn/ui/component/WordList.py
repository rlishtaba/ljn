#coding:utf-8
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QListWidget, QListWidgetItem
from ljn.Model import ArticleNewWord
from ljn.Repository import get_session
from ljn.ui.UiUtil import create_widget_action

class WordItem(QListWidgetItem):
    def __init__(self, new_word):
        QListWidgetItem.__init__(self, new_word.word.word)

        self.word_content = new_word.word_content


class WordList(QListWidget):

    onWordSelected = pyqtSignal(str)

    def __init__(self, parent):
        QListWidget.__init__(self, parent)

        self.article_id = None
        self.update_words()

        self.itemDoubleClicked.connect(self._select_item)
        self.addAction(create_widget_action(self, "Return", self._select_item))

    def update_words(self, article_id=None):
        self.clear()

        if article_id is None:
            article_id = self.article_id

        if article_id is None:
            return

        self.article_id = article_id
        s = get_session()
        self.new_words = ArticleNewWord.all_article_new_word(s, article_id)
        for nw in self.new_words:
            self.addItem(WordItem(nw))
        self.sortItems()

    def _select_item(self):
        items = self.selectedItems()
        if items:
            self.onWordSelected.emit(items[0].word_content)

#coding:utf8
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QTextEdit, QColor, QSyntaxHighlighter, QTextCharFormat
from string import ascii_letters

STYLE_SHEET = r'''
QTextEdit {
    font-family: Cambria,"Hoefler Text",Georgia,"Times New Roman",serif;
    font-size: 22px;
    font-weight: 400;
    color: #3D3936;
    background-color: #F4EED9;
}
'''

HIGHLIGHT_COLOR = QColor.fromRgb(251, 240, 132)
WORDS = set(ascii_letters)

def is_word(c):
    return c in WORDS

def whole_word(text, start, word_length):
    if start != 0 and is_word(text[start-1]):
        return False

    if len(text) > start + word_length and is_word(text[start+word_length]):
        return False
    return True


class ArticleHighlight(QSyntaxHighlighter):
    def highlightBlock(self, content):
        content = str(content)

        f = QTextCharFormat()
        f.setBackground(HIGHLIGHT_COLOR)

        for new_word in self.parent().new_words:
            word = new_word.word_content
            word_len = len(word)
            start = -1
            while True:
                start = content.find(word, start + 1)
                if start < 0:
                    break

                if whole_word(content, start, word_len):
                    self.setFormat(start, word_len, f)


class ArticleBrowser(QTextEdit):
    def __init__(self, parent):
        QTextEdit.__init__(self, parent)

        self.setStyleSheet(STYLE_SHEET)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu)

        self.new_words = []
        self.highlight = ArticleHighlight(self)

    def set_article(self, article):
        content = article.content
        self.setText(content)
        self.new_words = list(article.new_words)
        self.highlight.rehighlight()

    def _on_context_menu(self, point=None):
        print '_on_context_menu:', point

    def mouseReleaseEvent(self, QMouseEvent):
        QTextEdit.mouseReleaseEvent(self, QMouseEvent)

        selection = unicode(self.textCursor().selectedText()).strip()
        if not selection:
            return

        self._on_selection_changed(selection)

    def _on_selection_changed(self, selection):
        pass

#coding:utf8
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QTextEdit, QColor, QSyntaxHighlighter, QTextCharFormat, QTextCursor, QMessageBox
from string import ascii_letters
from ljn.Model import ArticleNewWord, Article
from ljn.Repository import get_session
from ljn.ui.UiUtil import create_widget_action

STYLE_SHEET = r'''
QTextEdit {
    font-family: Cambria,"Hoefler Text",Georgia,"Times New Roman",serif;
    font-size: 22px;
    font-weight: 400;
    color: #3D3936;
    background-color: #F4EED9;
    padding: 20px;
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

def normalize(word):
    while word and not word[0].isalpha():
        word = word[1:]

    while word and not word[-1].isalpha():
        word = word[:-1]

    return word


class ArticleHighlight(QSyntaxHighlighter):
    def __init__(self, parent):
        QSyntaxHighlighter.__init__(self, parent)
        self.to_word = []

    def rehighlight(self):
        self.to_word = []
        QSyntaxHighlighter.rehighlight(self)

    def highlightBlock(self, content):
        block_pos = self.currentBlock().position()
        content = unicode(content)

        to_word = self.to_word

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
                    to_word.append((block_pos + start, word_len, content[start:start+word_len]))

        to_word.sort()

    def get_word_of_position(self, pos):
        for start, word_len, word in self.to_word:
            if start <= pos < start + word_len:
                return word

        return None

    def get_position_of_word(self, word):
        for start, word_len, w in self.to_word:
            if word == w:
                return start, word_len

        return -1, -1


class ArticleBrowser(QTextEdit):

    onArticleLoaded = pyqtSignal(int)

    def __init__(self, parent):
        QTextEdit.__init__(self, parent)

        self.setStyleSheet(STYLE_SHEET)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu)

        self.addAction(create_widget_action(self, 'Alt+Return', self._show_article_property))

        self.article_id = None
        self.new_words = []
        self.highlight = ArticleHighlight(self)

    def set_article(self, article):
        self.article_title = article.title
        self.article_id = article.id
        content = article.content
        self.setText(content)
        self.new_words = list(article.new_words)
        self.highlight.rehighlight()
        self.onArticleLoaded.emit(self.article_id)

    def _refresh(self):
        article = Article.find_by_id(get_session(), self.article_id)
        self.new_words = list(article.new_words)
        self.highlight.rehighlight()
        self.onArticleLoaded.emit(self.article_id)

    def _on_context_menu(self, point=None):
        selection = normalize(unicode(self.textCursor().selectedText()))
        word = self.highlight.get_word_of_position(self.cursorForPosition(point).position())
        if word is None:
            if not self.textCursor().hasSelection():
                return

            # highlight selected word
            from NewWordEditor import create_new_word
            nw = create_new_word(self, selection)
            if nw is None:
                return

            nw.article_id = self.article_id
            s = get_session()
            s.add(nw)
            s.commit()

            cursor = self.textCursor()
            cursor.clearSelection()
            self.setTextCursor(cursor)

        else:
            s = get_session()
            s.delete(ArticleNewWord.find_by_article_word(s, self.article_id, word))
            s.commit()

        self._refresh()

    def _show_article_property(self):
        from ljn.util import word_count

        content = unicode(self.toPlainText())
        text = '''
Words:    %d
Letters:  %d
        '''.strip() % (word_count(content), len(content))
        QMessageBox.information(self, self.article_title, text)

    def navigate_word(self, word):
        start, len = self.highlight.get_position_of_word(word)
        if start < 0:
            return

        tc = self.textCursor()
        tc.setPosition(start)
        tc.setPosition(start + len, QTextCursor.KeepAnchor)
        self.setTextCursor(tc)
        self.setFocus()

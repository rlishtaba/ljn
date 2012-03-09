#coding:utf8
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog, QFormLayout, QDialogButtonBox, QLineEdit
from ljn.Model import ArticleNewWord, Word
from ljn.Repository import get_session

class NewWordEditor(QDialog):
    def __init__(self, word_content, title, parent):
        QDialog.__init__(self, parent)
        self.setWindowTitle(title)

        self.word_content = word_content
        layout = QFormLayout(self)
        layout.addRow('&Word', self._create_word())
        layout.addRow('&Content', self._create_content())
        layout.addRow(self._create_buttons())

    def _create_buttons(self):
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal ,self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        return buttons

    def _create_word(self):
        self.word_edit = QLineEdit(self.word_content.lower(), self)
        return self.word_edit

    def _create_content(self):
        self.content_edit = QLineEdit(self.word_content, self)
        return self.content_edit

    def get_new_word(self):
        s = get_session()
        w = unicode(self.word_edit.text()).strip()
        word = Word.find(s, w)
        if word is not None:
            word = word.id
        else:
            word = Word(w)
        return ArticleNewWord(None, word, unicode(self.content_edit.text()).strip())

def create_new_word(parent, word_content):
    """ @rtype: ArticleNewWord """
    dlg = NewWordEditor(word_content, 'Create new word', parent)
    if dlg.exec_() == QDialog.Accepted:
        return dlg.get_new_word()
    return None

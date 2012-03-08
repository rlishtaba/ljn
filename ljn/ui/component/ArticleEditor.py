#coding:utf8
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog, QFormLayout, QLineEdit, QTextEdit, QDialogButtonBox
from ljn.Model import Article

class ArticleEditor(QDialog):
    def __init__(self, article, title, parent):
        """ @type article: Article """
        QDialog.__init__(self, parent)
        self.setWindowTitle(title)

        self.article = article
        layout = QFormLayout(self)
        layout.addRow('Title', self._create_title())
        layout.addRow('Author', self._create_author())
        layout.addRow('URL', self._create_url())
        layout.addRow('Content', self._create_content())
        layout.addRow(self._create_buttons())

    def _create_buttons(self):
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal ,self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        return buttons

    def _create_title(self):
        self.title_edit = QLineEdit(self.article.title, self)
        return self.title_edit

    def _create_author(self):
        self.author_edit = QLineEdit(self.article.author, self)
        return self.author_edit

    def _create_url(self):
        self.url_edit = QLineEdit(self.article.url, self)
        return self.url_edit

    def _create_content(self):
        self.content_edit = QTextEdit(self.article.content, self)
        return self.content_edit

    def get_article(self):
        content = unicode(self.content_edit.toPlainText())
        title = unicode(self.title_edit.text())
        author = str(self.author_edit.text())
        url = str(self.url_edit.text())
        return Article(content, None, title, author, url)


def create_new_article(parent):
    article = Article(u'', None)
    dlg = ArticleEditor(article, 'Create new article', parent)
    if dlg.exec_() == QDialog.Accepted:
        return dlg.get_article()
    return None

def edit_article(article, parent):
    dlg = ArticleEditor(article, 'Edit article', parent)
    dlg.exec_()
    if dlg.exec_() == QDialog.Accepted:
        a = dlg.get_article()
        a.category_id = article.category.id
        return a
    return None

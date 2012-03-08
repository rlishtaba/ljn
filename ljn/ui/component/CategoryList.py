#coding:utf8
from PyQt4.QtGui import QListWidget, QListWidgetItem, QAction, QInputDialog
from ljn.Model import Category
from ljn.Repository import get_session

class CategoryItem(QListWidgetItem):
    def __init__(self, category):
        QListWidgetItem.__init__(self, category.name)

        self.category = category


class CategoryList(QListWidget):
    def __init__(self, parent):
        QListWidget.__init__(self, parent)

        self.update_categories()
        self.addAction(self._create_rename_action())

    def _create_rename_action(self):
        a = QAction("Rename", self)
        a.setShortcut("F2")
        a.triggered.connect(self._rename_category)
        return a

    def update_categories(self):
        self.clear()
        for c in Category.all(get_session()):
            self.addItem(CategoryItem(c))

    def _rename_category(self, *args):
        items = self.selectedItems()
        if not items:
            return

        category = items[0].category
        text, result = QInputDialog.getText(self, 'Rename', 'New category name:', text=category.name)
        if not result:
            return

        text = str(text)
        if not text or text == category.name:
            return

        s = get_session()
        c = Category.find_by_id(s, category.id)
        c.name = text
        s.commit()
        self.update_categories()

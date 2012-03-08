#coding:utf8
from PyQt4.QtGui import QListWidget, QListWidgetItem, QAction, QInputDialog, QMessageBox
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
        self.addAction(self._create_delete_action())

    def _create_rename_action(self):
        a = QAction("Rename", self)
        a.setShortcut("F2")
        a.triggered.connect(self._rename_category)
        return a

    def _create_delete_action(self):
        a = QAction("Delete", self)
        a.setShortcut("Del")
        a.triggered.connect(self._del_category)
        return a

    def update_categories(self):
        self.clear()
        for c in Category.all(get_session()):
            self.addItem(CategoryItem(c))

    def _rename_category(self):
        items = self.selectedItems()
        if not items:
            return

        category = items[0].category
        text, result = QInputDialog.getText(self, 'Rename category', 'New category name:', text=category.name)
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

    def _del_category(self):
        items = self.selectedItems()
        if not items:
            return

        category = items[0].category
        msg = 'Delete "%s"?' % category.name
        btn = QMessageBox.question(self, 'Delete category', msg, QMessageBox.Yes | QMessageBox.No)
        if btn == QMessageBox.No:
            return

        s = get_session()
        s.delete(Category.find_by_id(s, category.id))
        s.commit()
        self.update_categories()

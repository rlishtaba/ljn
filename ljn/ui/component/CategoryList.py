#coding:utf8
from PyQt4.QtGui import QListWidget, QListWidgetItem
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

    def update_categories(self):
        self.clear()
        for c in Category.all(get_session()):
            self.addItem(CategoryItem(c))

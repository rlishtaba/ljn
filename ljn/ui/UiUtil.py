#coding:utf-8
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAction

def create_widget_action(parent, shortcut, func):
    action = QAction(parent)
    action.setShortcut(shortcut)
    action.setShortcutContext(Qt.WidgetShortcut)
    action.triggered.connect(func)
    return action

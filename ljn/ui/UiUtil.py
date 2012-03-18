#coding:utf-8
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAction

def create_action(parent, shortcut, context, func):
    action = QAction(parent)
    action.setShortcut(shortcut)
    action.setShortcutContext(context)
    action.triggered.connect(func)
    return action

def create_widget_action(parent, shortcut, func):
    return create_action(parent, shortcut, Qt.WidgetShortcut, func)

def create_app_action(parent, shortcut, func):
    return create_action(parent, shortcut, Qt.ApplicationShortcut, func)

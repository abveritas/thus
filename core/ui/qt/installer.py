from core.ui.qt.wizard import Wizard
from PySide import QtGui


class Installer(object):
    def __init__(self, loader):
        self.loader = loader

    def run(self):
        app = QtGui.QApplication([])
        wizard = Wizard(self.loader)
        return app.exec_()

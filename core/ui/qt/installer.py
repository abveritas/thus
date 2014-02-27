from core.ui.qt.wizard import Wizard
from PyQt5.QtWidgets import QApplication


class Installer(object):
    def __init__(self, loader):
        self.loader = loader

    def run(self):
        app = QApplication([])
        wizard = Wizard(self.loader)
        return app.exec_()

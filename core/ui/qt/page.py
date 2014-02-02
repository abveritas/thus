from PySide import QtGui


class AbstractPage(QtGui.QWidget):
    def load(self, values, wizard):
        pass

    def get_values(self):
        return {}



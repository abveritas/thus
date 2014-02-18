from PyQt5 import QtWidgets


class AbstractPage(QtWidgets.QWidget):
    def load(self, values, wizard):
        pass

    def get_values(self):
        return {}



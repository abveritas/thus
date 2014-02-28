from core.ui.qt.page import AbstractPage
import os.path
from PyQt5 import uic
from PyQt5.QtWidgets import QCheckBox, QSpacerItem, QSizePolicy


class Page(AbstractPage):
    def __init__(self, parent=None):
        super(Page, self).__init__(parent)
        self.dir = os.path.dirname(__file__)
        self.init()
        self.setupUi()

    def init(self):
        """
        private constructor.
        Change the checklist if you want by extending from this class, and overriding
        the self.checklist attribute
        """
        self.checklist = (
            ('has at least 6GB of storage', self.check_storage),
            ('is connected to the power source', self.check_power_source),
            ('is connected to the internet', self.check_internet_connection),
        )

    def setupUi(self):
        uic.loadUi('%s/ui/checklist.ui' % self.dir, self)
        for (check, sentinel) in self.checklist:
            checkbox = QCheckBox(check)
            checkbox.setEnabled(False)
            checkbox.setChecked(sentinel())
            self.layout().addWidget(checkbox)
        spacerItem = QSpacerItem(20, 466, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout().addItem(spacerItem)



    def check_storage(self):
        return True

    def check_power_source(self):
        return False

    def check_internet_connection(self):
        return True
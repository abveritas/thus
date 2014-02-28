import sys
from importlib import import_module
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox


class Wizard(QtWidgets.QMainWindow):
    def __init__(self, loader):
        super(Wizard, self).__init__()
        self.loader = loader
        self.page = None
        self.pagename = None
        self.settings = {}
        sys.path.append(self.loader.config.get('distro', 'module'))
        self.initUI()

    def getPage(self, page):
        page = import_module(page)
        # page = page.Page(self.pageWidget)
        page = page.Page()

        self.prevStepButton.setEnabled(False)
        self.nextStepButton.setEnabled(False)
        try:
            if page.prev_page:
                self.prevStepButton.setEnabled(True)
            if page.next_page:
                self.nextStepButton.setEnabled(True)
        except:
            pass

        return page

    def prevpage(self):
        if self.page.prev_page:
            self.loadPage(self.page.prev_page)

    def nextpage(self):
        try:
            self.settings[self.pagename] = self.page.get_values()
            self.loadPage(self.page.next_page)
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def initUI(self):
        centralWidget = QtWidgets.QWidget(self)
        self.statusBar().showMessage(
            'Thus installer v. %s' % self.loader.version())

        vLayout = QtWidgets.QVBoxLayout(centralWidget)

        distrolabel = QtWidgets.QLabel(self.loader.config.get('distro', 'name'))

        self.pageWidget = QtWidgets.QWidget()
        self.pageWidget.setLayout(QtWidgets.QVBoxLayout())

        stepswidget = QtWidgets.QLabel('Steps')

        self.exitButton = QtWidgets.QPushButton("Exit")
        self.exitButton.clicked.connect(self.quit)

        self.prevStepButton = QtWidgets.QPushButton("Prev")
        self.prevStepButton.clicked.connect(
            self.prevpage
        )
        self.nextStepButton = QtWidgets.QPushButton("Next")
        self.nextStepButton.clicked.connect(
            self.nextpage
        )
        bottomWidget = QtWidgets.QWidget(self)
        bottomLine = QtWidgets.QHBoxLayout(bottomWidget)
        bottomLine.addWidget(stepswidget)
        bottomLine.addStretch(1)
        bottomLine.addWidget(self.exitButton)
        bottomLine.addWidget(self.prevStepButton)
        bottomLine.addWidget(self.nextStepButton)

        vLayout.addWidget(distrolabel)
        vLayout.addStretch(1)
        vLayout.addWidget(self.pageWidget)
        vLayout.addStretch(1)
        vLayout.addWidget(bottomWidget)

        self.setCentralWidget(centralWidget)
        self.loadPage(self.loader.config.get('distro', 'initial'))
        self.setGeometry(0, 0, 640, 480)
        self.show()

    def loadPage(self, page):
        self.pagename = page
        if self.page:
            self.page.setParent(None)
        self.page = self.getPage(page)
        self.pageWidget.layout().addWidget(self.page)
        self.page.load(
            self.settings.get(self.pagename, {}),
            self
        )

    def quit(self):
        self.close()
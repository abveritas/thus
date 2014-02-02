import sys
from importlib import import_module
from PySide import QtGui


class Wizard(QtGui.QMainWindow):
    def __init__(self, loader):
        super(Wizard, self).__init__()
        self.loader = loader
        self.page = None
        self.pagename = None
        self.settings = {}
        sys.path.append(self.loader.config.get('distro', 'module'))
        self.initUI()

    def getPage(self, page):
        page = import_module('pages.%s' % page)
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
        self.settings[self.pagename] = self.page.get_values()
        self.loadPage(self.page.next_page)

    def initUI(self):
        centralWidget = QtGui.QWidget(self)
        self.statusBar().showMessage(
            'Thus installer v. %s' % self.loader.version())

        vLayout = QtGui.QVBoxLayout(centralWidget)

        distrolabel = QtGui.QLabel(self.loader.config.get('distro', 'name'))

        self.pageWidget = QtGui.QWidget()
        self.pageWidget.setLayout(QtGui.QVBoxLayout())

        stepswidget = QtGui.QLabel('Steps')

        self.prevStepButton = QtGui.QPushButton("Prev")
        self.prevStepButton.clicked.connect(
            self.prevpage
        )
        self.nextStepButton = QtGui.QPushButton("Next")
        self.nextStepButton.clicked.connect(
            self.nextpage
        )
        bottomWidget = QtGui.QWidget(self)
        bottomLine = QtGui.QHBoxLayout(bottomWidget)
        bottomLine.addWidget(stepswidget)
        bottomLine.addStretch(1)
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

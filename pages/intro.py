from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from core.ui.qt.page import AbstractPage
from os.path import dirname
from subprocess import getoutput
import gzip
import codecs
from PyQt5.QtCore import QTextCodec, QByteArray
from PyQt5.QtGui import QFontDatabase


class Page(AbstractPage):
    def data(self, path):
        return '%s/../data/%s' % (dirname(__file__), path)

    def __init__(self, parent=None):
        super(Page, self).__init__(parent=parent)
        # a collection of models (language names)
        self.languages = QtGui.QStandardItemModel()
        with gzip.open(self.data('languagelist.data.gz')) as f:
            for line in f:
                l = line.decode('utf-8').strip('\n').split(':')
                # if l[0] is empty string then we've reached the end of file
                # if l[0] == '0' then this denotes C => no localisation
                if l[0] and l[0] != '0':
                    display = l[-1]
                    # those 4 languages unfortunetely don't display nicely
                    # so we'll stick with their english name.
                    if l[1] in ('km', 'dz', 'ml', 'pa'):
                        display = l[2]
                    # an item will hold a language code and displayed name
                    # language code is needed so that we could serialize it.
                    item = QtGui.QStandardItem(display)
                    item.setData(l[1])
                    self.languages.appendRow(item)

        self.fonts = QFontDatabase()
        #id = self.fonts.addApplicationFont("data/fonts/FUTURAM.ttf")
        #fontName = self.fonts.applicationFontFamilies(id)[0]
        #style = self.fonts.styles(fontName)[0]
        #self._font = self.fonts.font(fontName, style, self.font().pointSize())

        self.setupUi()


    def setupUi(self):
        layout = QtWidgets.QVBoxLayout()
        language_choice_layout = QtWidgets.QHBoxLayout()
        language_search_layout = QtWidgets.QVBoxLayout()
        language_filter = QtWidgets.QLineEdit()
        language_view = QtWidgets.QListView()

        self.proxy = QtCore.QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.languages)
        self.proxy.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        language_view.setModel(self.proxy)
        self.language_view = language_view

        language_search_layout.addWidget(language_filter)
        language_search_layout.addWidget(language_view)

        languages_image = QtWidgets.QLabel()
        languages_image.setPixmap(QtGui.QPixmap('%s/../data/languages.png' % dirname(__file__)))

        language_choice_layout.addLayout(language_search_layout)
        language_choice_layout.addWidget(languages_image)
        layout.addLayout(language_choice_layout)

        self.setLayout(layout)

        language_filter.textChanged.connect(self.proxy.setFilterFixedString)

    @property
    def next_page(self):
        return 'pages.second'

    @property
    def prev_page(self):
        return None

    def get_values(self):
        selected_language = self.language_view.selectedIndexes()[0]

        return {
            'language': selected_language.data(QtCore.Qt.UserRole + 1),
            'row': selected_language.row()
        }

    def load(self, values, wizard):
        if 'row' in values:
            index = self.proxy.index(values['row'], 0)
            self.language_view.setCurrentIndex(index)
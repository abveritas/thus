import xml.etree.ElementTree as etree
from PyQt5 import uic
from PyQt5 import QtCore
from core.ui.qt.page import AbstractPage
import os.path
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class Page(AbstractPage):
    def __init__(self, parent=None):
        super(Page, self).__init__(parent)
        self.dir = os.path.dirname(__file__)
        self.territories = QStandardItemModel()
        self.load_locales()
        self.setupUi()

    def setupUi(self):
        uic.loadUi('%s/ui/territory.ui' % self.dir, self)

    def load_locales(self):
        data_dir = '%s/../data' % self.dir
        xml_path = os.path.join(data_dir, "locales.xml")

        self.locales = {}
        self.locales_by_location = {}

        tree = etree.parse(xml_path)
        root = tree.getroot()
        for child in root.iter("language"):
            for item in child:
                if item.tag == 'language_name':
                    language_name = item.text
                elif item.tag == 'locale_name':
                    locale_name = item.text
            self.locales[locale_name] = language_name

        xml_path = os.path.join(data_dir, "iso3366-1.xml")

        countries = {}

        tree = etree.parse(xml_path)
        root = tree.getroot()
        for child in root:
            code = child.attrib['value']
            name = child.text
            countries[code] = name

        for locale_name in self.locales:
            language_name = self.locales[locale_name]
            location = locale_name[:2]
            for country_code in countries:
                if country_code in language_name:
                    self.locales[locale_name] = self.locales[locale_name] + ", " + countries[country_code]
                    if location not in self.locales_by_location:
                        self.locales_by_location[location] = []
                    self.locales_by_location[location].append((locale_name, self.locales[locale_name]))
            self.locales_by_location[location].sort()

    def load(self, data, wizard):
        location = wizard.settings['pages.intro']['language']

        for language in self.locales_by_location[location]:
            territory = QStandardItem(language[1])
            territory.setData(language[0])
            self.territories.appendRow(territory)
        self.lvTerritories.setModel(self.territories)

    def get_values(self):
        try:
            localization = self.lvTerritories.selectedIndexes()[0]
            return {
                'localization': localization.data(QtCore.Qt.UserRole + 1),
                'row': localization.row()
            }
        except IndexError:
            raise Exception("Please select a territory")


    @property
    def prev_page(self):
        return 'pages.intro'

    @property
    def next_page(self):
        return 'pages.checklist'
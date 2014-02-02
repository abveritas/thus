from importlib import import_module
from configparser import SafeConfigParser
from . import __version__


class Loader(object):
    def __init__(self, args):
        self.args = args
        config = SafeConfigParser()
        config.read(args.config)
        self.config = config
        self.ui = args.interface

    def version(self):
        return __version__

    def run(self):
        installer = import_module('core.ui.%s.installer' % self.ui).Installer(self)
        installer.run()

import argparse
import coloredlogs
import configparser
import json
import logging
import os
import pprint



class Route:
    def __init__(self, args, cfg):
        self.args = args
        self.cfg = cfg
        self.log = logging.getLogger('Route')
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.listdir = os.listdir(self.path)
        self.log.debug(f'script path: "{self.path}"')
        self.log.debug(f'list dir: "{pprint.pformat(self.listdir)}"')

        # Props initialization goes here

        self.log.debug('initialization complete')


    def execute(self):
        self.log = logging.getLogger('Execution')

        # Logic goes here



class App:

    #   #########################   #
    #   App Configuration Section   #
    #   #########################   #


    # Set a name for your App.
    NAME = 'App'


    # This is the App description. Things it does and problems it solves.
    DESCRIPTION = 'Welcome to App!'


    # Default configuration file path relative to __file__'s
    DEFAULT_CFG_FILE = 'cfg.py'


    # List of dictionaries representing arguments by their name or flags
    #   ('name' key) and his options ('options' key) as used in argparse
    # Allowed options are: 'action', 'nargs', 'const', 'default', 'type',
    #   'choices', 'required', 'help', 'metavar', 'dest' and 'version'.
    ARGS = [
        {
            'name': ['-c', '--cfg'],
            'options': {'default': DEFAULT_CFG_FILE, 'help': 'use specific cfg file', 'metavar': 'FILE', }
        },
        {
            'name': ['-v', '--verbose'],
            'options': {'action': 'store_true', 'help': 'show more verbose output', }
        },
        # Add custom arguments here.
        # {
        #     'name': [],
        #     'options': {}
        # },
    ]

    def __init__(self):
        self.loadArguments()
        self.loadConfiguration(self.args['cfg'])
        self.loadLogger()

    def loadArguments(self):
        parser = argparse.ArgumentParser(description=self.DESCRIPTION)
        for arg in self.ARGS:
            parser.add_argument(*arg['name'], **arg['options'])
        self.args = vars(parser.parse_args())

    def loadConfiguration(self, cfg_file_path=DEFAULT_CFG_FILE):
        if not os.path.exists(cfg_file_path) or not os.path.isfile(cfg_file_path):
            raise ValueError('Config not found at ' + cfg_file_path)
        _, extension = os.path.splitext(cfg_file_path)
        if extension == '.py':
            import cfg
            self.cfg =  cfg.cfg
        elif extension == '.ini':
            parser = configparser.ConfigParser()
            parser.read(cfg_file_path)
            self.cfg = { section: dict(parser.items(section)) for section in parser.sections() }
            for section in self.cfg.keys():
                for key in self.cfg[section]:
                    if self.cfg[section][key].lower() in ('false', 'true'):
                        self.cfg[section][key] = self.cfg[section][key] == 'true'
                    elif len(self.cfg[section][key].splitlines()) > 1:
                        self.cfg[section][key] = [item.strip() for item in self.cfg[section][key].splitlines() if len(item.strip())]
        elif extension == '.json':
            with open(cfg_file_path, 'r') as cfg_file:
                self.cfg = json.load(cfg_file)
        else:
            raise NotImplementedError(f'{extension} configuration file is not supported')

    def loadLogger(self):
        config = {
            'format': '[%(asctime)s] %(levelname)s (%(name)s): %(message)s',
            'level': (logging.INFO, logging.DEBUG)[self.args['verbose']],
        }
        coloredlogs.install(level=config['level'])
        logging.basicConfig(**config)

    def run(self):
        log = logging.getLogger('Run')
        route = {'args': self.args, 'cfg': self.cfg}
        log.debug(f'Running {self.NAME} with the following route:\n{pprint.pformat(route)}')
        Route(**route).execute()



if __name__ == '__main__':
    App().run()

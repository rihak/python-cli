import os
import argparse
import logging



class Route:
    def __init__(self, args, cfg):
        self.args = args
        self.cfg = cfg
        self.log = logging.getLogger('Route')
        self.path = os.path.dirname(os.path.abspath(__file__))


    def execute(self):
        self.log = logging.getLogger('Execution')
        self.log.info(f'Starting {App.NAME}...')
        # Logic goes here



class App:

    #   #########################   #
    #   App Configuration Section   #
    #   #########################   #


    # Set a name for your App.
    NAME = 'App'


    # This is the App description. Things it does and problems it solves.
    DESCRIPTION = 'Welcome to App!'

    # List of dictionaries representing arguments by their name or flags
    #   ('name' key) and his options ('options' key) as used in argparse
    # Allowed options are: 'action', 'nargs', 'const', 'default', 'type',
    #   'choices', 'required', 'help', 'metavar', 'dest' and 'version'.
    ARGS = [
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
        self.loadConfiguration()
        self.loadLogger()

    def loadArguments(self):
        parser = argparse.ArgumentParser(description=self.DESCRIPTION)
        for arg in self.ARGS:
            parser.add_argument(*arg['name'], **arg['options'])
        self.args = vars(parser.parse_args())

    def loadConfiguration(self, cfg_file_path='cfg.py'):
        if not os.path.exists(cfg_file_path) or not os.path.isfile(cfg_file_path):
            raise ValueError('Config not found at ' + cfg_file_path)
        import cfg
        self.cfg =  cfg.cfg

    def loadLogger(self):
        ll = (logging.INFO, logging.DEBUG)[self.args['verbose']]
        logging.basicConfig(level=ll)

    def run(self):
        if self.args['verbose']:
            import pprint
            print(f'\nRunning {self.NAME} with the following route:\n')
            pprint.pprint({'args': self.args, 'cfg': self.cfg})
        Route(self.args, self.cfg).execute()



if __name__ == '__main__':
    App().run()

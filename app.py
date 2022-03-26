import argparse
import logging
import os
import pprint


name = None
description = None
arguments = None
args = None
configuration = 'configuration.py'
cfg = None
log = None
path = None
listdir = None


def load():
    global name, desc, arguments, args, configuration, cfg, log, path, listdir

    parser = argparse.ArgumentParser(description=description)
    for arg in arguments:
        parser.add_argument(*arg['name'], **arg['options'])
    args = vars(parser.parse_args())

    if not os.path.exists(configuration) or not os.path.isfile(configuration):
        raise ValueError('Config not found at ' + configuration)
    import configuration
    cfg = configuration.cfg

    config = {
        'format': '[%(asctime)s] %(levelname)s (%(name)s): %(message)s',
        'level': logging.DEBUG if 'verbose' in args and args['verbose'] else logging.INFO,
    }
    logging.basicConfig(**config)
    log = logging.getLogger(name)

    path = os.path.dirname(os.path.abspath(__file__))
    listdir = os.listdir(path)

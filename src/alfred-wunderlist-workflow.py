#!/usr/bin/python
# encoding: utf-8

import logging
from logging.config import fileConfig
import sys

fileConfig('logging_config.ini')

from wunderlist.handlers.route import route
from wunderlist.util import workflow

log = logging.getLogger('wunderlist')

def main(wf):
    route(wf.args)
    log.info('Workflow response complete')

if __name__ == '__main__':
    wf = workflow()
    sys.exit(wf.run(main))

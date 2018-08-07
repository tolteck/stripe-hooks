#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from flask import Flask

from .helpers import load_configuration

# Create the app and configure
app = Flask(__name__)
app.config['DEBUG'] = False

parser = argparse.ArgumentParser()
parser.add_argument(dest='config_file', action='store',
                    help='path to config file')
args = parser.parse_args()

app.config.update(load_configuration(args.config_file))

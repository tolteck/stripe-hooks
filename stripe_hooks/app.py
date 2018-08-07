#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask

from .helpers import load_configuration

# The instance path has to be absolute so lets get the absolute path to our
# root directory.
my_directory = os.path.dirname(__file__)
root_directory = os.path.abspath(os.path.join(my_directory, ".."))

# Create the app and configure
app = Flask(__name__,
            instance_path=root_directory,
            instance_relative_config=True)

app.config.from_pyfile("settings.py")

path = os.path.join(my_directory, "../configuration.json")

app.config["email"] = load_configuration(path)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stripe

from .app import app
from .helpers import jsonify_with_status
from .hook import hook

app.register_blueprint(hook)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify_with_status(404, {"error": "resource not found"})

# stripe configuration
if app.config['stripe'].get('api_base', 'default') != 'default':
    stripe.api_base = app.config['stripe']['api_base']

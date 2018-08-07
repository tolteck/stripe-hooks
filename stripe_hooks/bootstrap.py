#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stripe

from .app import app
from .helpers import jsonify_with_status
from .hook import hook

app.register_blueprint(hook, url_prefix='/webhook')


@app.errorhandler(404)
def page_not_found(error):
    return jsonify_with_status(404, {"error": "resource not found"})

# Configurat stripe
stripe.api_key = app.config.get('STRIPE_KEY')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, request
import stripe

from .app import app
from .helpers import jsonify_with_status, CleanParseException
from .parser import parse_hook

hook = Blueprint("hook", __name__)


@hook.route("/webhook", methods=["POST"])
def receieve_hook():
    """
    Path:       /webhook
    Method:     POST
    """
    # Abort if we're not sent JSON
    if not request.json:
        return jsonify_with_status(406, {'error': 'Requires application/json'})

    # If the event doesn't have a id, it's not an event
    # https://stripe.com/docs/api#events
    if not request.json.get("id"):
        return jsonify_with_status(406, {'error': 'Does not have an id'})

    try:
        event = stripe.Webhook.construct_event(
            request.get_data(),
            request.headers.get('Stripe-Signature', None),
            app.config['stripe']['endpoint_secret'])
    except ValueError:
        return '', 400
    except stripe.error.SignatureVerificationError:
        return '', 401

    try:
        parse_hook(event)
    except stripe.error.InvalidRequestError as e:
        # If the hook failed to parse, send back why to stripe
        # This will be visible in your dashboard
        return jsonify_with_status(406, {'error': str(e)})
    except CleanParseException as e:
        # If the hook failed to parse, but we don't want it
        # to try again, send back why and a 200 so Stripe stops trying.
        return jsonify_with_status(200, {'error': str(e)})

    return jsonify_with_status(200, {'success': True})

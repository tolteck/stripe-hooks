#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
from flask import jsonify


def jsonify_with_status(status, *args, **kwargs):
    """Takes a status code and an object to be jsonified and returns a response
    object that can be returned from an API endpoint.
    """
    response = jsonify(*args, **kwargs)
    response.status_code = status
    return response


def humanize_date(epoch):
    "Converts an epoch timestamp to a human readable time"
    return time.strftime("%a, %d %b %Y %H:%M:%S",
                         time.gmtime(epoch))


def humanize_money(amount):
    "Make all those cents turn to dollaz"
    return float(amount) / 100


def format_stripe_object(stripe_object):
    """Returns an array of key-value pairs that can be easily iterated
    in templates.
    """

    # Copy the stripe object
    data = stripe_object.to_dict()

    return data


def load_configuration(path):
    """Loads the JSON configuration from a path and returns it as a
    dictionary, validating any required attributes.
    """
    data = json.load(open(path))

    if data["email"].get("business") is None:
        raise Exception(
            "Configuration failure: a business attribute is required")
    if data["email"]["business"].get("email_address") is None:
        raise Exception(
            "Configuration failure: a business email address is required")
    if data["email"]["business"].get("notification_address") is None:
        raise Exception(
            "Configuration failure: a notification address is required")
    if data["email"].get("templates_path") is None:
        raise Exception(
            "Configuration failure: email templates_path is required")
    if data["stripe"].get("endpoint_secret") is None:
        raise Exception(
            "Configuration failure: stripe endpoint secret is required")
    if data["smtp"].get("url") is None:
        raise Exception(
            "Configuration failure: smtp server url is required")

    return data


class CleanParseException(Exception):

    """An Exception used when a failure parsing the content of a webhook
    is caused, but we should respond to Stripe with a 200
    """

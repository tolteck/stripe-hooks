#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import datetime
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from .app import app
from .helpers import humanize_date, humanize_money

# Global variables in the Jinga templates.
globals = {'business': app.config['email'][
    'business'], 'humanize_date': humanize_date, 'humanize_money': humanize_money}

path = app.config['email']['templates_path']
notify_templates = Environment(
    loader=FileSystemLoader(path + '/notifications'),
    undefined=StrictUndefined)
notify_templates.globals = globals
receipt_templates = Environment(
    loader=FileSystemLoader(path + '/receipts'), undefined=StrictUndefined)
receipt_templates.globals = globals


def send_email(from_address, subject, txt_rendered,
               recipient, html):
    msg_root = MIMEMultipart('related')
    msg_root['Subject'] = subject
    msg_root['From'] = from_address
    msg_root['To'] = recipient

    msg_alternative = MIMEMultipart('alternative')
    msg_root.attach(msg_alternative)

    msg_alternative.attach(MIMEText(txt_rendered, 'plain'))
    msg_alternative.attach(MIMEText(html, 'html'))

    s = smtplib.SMTP('localhost', 25)
    s.send_message(msg_root)
    s.quit()


def send_receipt(key, recipient, data=None):
    "Sends a receipt type of notification to a user"
    # If we don't have an ID, which we shouldn't, default it.
    if data is None:
        data = {"id": "no_event"}

    txt_template = receipt_templates.get_template(
        '%s.%s' % (key.replace(".", "/"), 'txt'))
    html_template = receipt_templates.get_template(
        '%s.%s' % (key.replace(".", "/"), 'html'))

    # Configuration for the business
    business = app.config['email']['business']

    # Get the configuration for the type of event
    event_conf = app.config['email']['receipts'].get(key)

    if event_conf.get("subject") is None:
        subject_title = "%s (%s)" % (key.replace(".", " ").title(), data["id"])
    else:
        subject_title = event_conf["subject"]

    from_address = business['email_address']
    subject = "[%s] %s" % (business['name'], subject_title)

    # Add some namespaced helpers to the data
    meta = {}
    meta['subject'] = subject
    meta['current_timestamp'] = datetime.datetime.now()

    txt_rendered = txt_template.render(data=data, meta=meta)
    html_rendered = html_template.render(data=data, meta=meta)

    if app.config.get("TESTING") is True:
        # Don't send while unit/integration testing
        return

    # Send the actual email
    send_email(
        from_address,
        subject,
        txt_rendered,
        recipient,
        html_rendered)


def send_notification(key, data=None):
    "Sends a notification to an administrator"

    txt_template = notify_templates.get_template(
        '%s.%s' % (key.replace(".", "/"), 'txt'))
    html_template = notify_templates.get_template(
        '%s.%s' % (key.replace(".", "/"), 'html'))

    # Configuration for the business
    business = app.config['email']['business']

    # Get the configuration for the type of event
    event_conf = app.config['email']['notifications'].get(key)

    # Default the subject if there isn't one specified
    if event_conf.get("subject") is None:
        subject_title = "%s (%s)" % (
            key.replace(".", " ").title(), data.get("id", int(time.time())))
    else:
        subject_title = event_conf["subject"]

    from_address = business['email_address']
    subject = "[Stripe Notification] %s" % (subject_title)

    # Add some namespaced helpers to the data
    meta = {}
    meta['subject'] = subject
    meta['current_timestamp'] = datetime.datetime.now()

    txt_rendered = txt_template.render(data=data, meta=meta)
    html_rendered = html_template.render(data=data, meta=meta)

    if app.config.get("TESTING") is True:
        # Don't send while unit/integration testing
        return

    # Send the actual email
    send_email(
        from_address,
        subject,
        txt_rendered,
        business['notification_address'],
        html_rendered)

import boto
from jinja2 import Environment, FileSystemLoader

from .app import app

# This is the mail instance that is used to send all email
conn = boto.connect_ses(
    aws_access_key_id=app.config['AWS_ACCESS_KEY'],
    aws_secret_access_key=app.config['AWS_SECRET_KEY'])

# Global variables in the Jinga templates.
globals = {'business': app.config['email']['business']}

notify_templates = Environment(loader=FileSystemLoader('notifications'))
notify_templates.globals = globals

receipt_templates = Environment(loader=FileSystemLoader('receipts'))
receipt_templates.globals = globals


def send_receipt(key, recipient, data=None):
    "Sends a receipt type of notification to a user"
    txt_template = receipt_templates.get_template('%s.%s' % (key, 'txt'))
    html_template = receipt_templates.get_template(
        'email/%s.%s' % (key, 'html'))

    txt_rendered = txt_template.render(data=data)
    html_rendered = html_template.render(data=data)

    if app.config.get("TESTING") is True:
        # Don't send while unit/integration testing
        return

    # Configuration for the business
    business = app.config['email']['business']

    # Get the configuration for the type of event
    event_conf = app.config['email']['receipts'].get(key)

    if event_conf.get("subject") is None:
        subject_title = key.replace(".", " ").title()

    from_address = business['email_address']
    subject = "[%s] %s" % (business['name'], subject_title)

    # Send the actual email
    conn.send_email(
        from_address,
        subject,
        txt_rendered,
        [recipient],
        html_body=html_rendered)


def send_notification(key, data=None):
    "Sends a notification to an administrator"
    txt_template = receipt_templates.get_template('%s.%s' % (key, 'txt'))
    html_template = receipt_templates.get_template(
        'email/%s.%s' % (key, 'html'))

    txt_rendered = txt_template.render(data=data)
    html_rendered = html_template.render(data=data)

    if app.config.get("TESTING") is True:
        # Don't send while unit/integration testing
        return

    # Configuration for the business
    business = app.config['email']['business']

    # Get the configuration for the type of event
    event_conf = app.config['email']['notifications'].get(key)

    # Default the subject if there isn't one specified
    if event_conf.get("subject") is None:
        subject_title = key.replace(".", " ").title()
    else:
        subject_title = event_conf["subject"]

    from_address = business['email_address']
    subject = "[Stripe Notification] %s" % (subject_title)

    # Send the actual email
    conn.send_email(
        from_address,
        subject,
        txt_rendered,
        [business['notification_address']],
        html_body=html_rendered)
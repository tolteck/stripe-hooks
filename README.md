## stripe-hooks

This is a Python web application to receive [webhooks](https://stripe.com/docs/webhooks)
from Stripe and send emails accordingly.

This is a fork of [Jack Pearkes](https://github.com/pearkes/stripe-hooks/) original work:
[stripe-hooks](https://github.com/pearkes/stripe-hooks).

There are two types of emails:

- [Notifications](https://github.com/pearkes/stripe-hooks-emails/tree/master/notifications), sent to administrators
- [Receipts](https://github.com/pearkes/stripe-hooks-emails/tree/master/receipts), sent to customers

Use cases:

- Sending notifications about important Stripe events, such as failed
charges or new customers, to administrators
- Sending receipts to user after they have been charged

It supports **all** Stripe [events](https://stripe.com/docs/api#event_types).

The email content included by default is versatile English. Any
of it can be modified to fit your business or use case. It's easy to
deploy and you shouldn't need to touch Python to configure it.

### Installation

```sh
    $ python3 setup.py install
```

### Configuration

All of the configuration is done in JSON.

Create a `.json` file following [`configuration_template.json`](configuration_template.json) and drop it in the command line:

```sh
    $ stripe-hooks configuration.json 
```

More details below:

#### Emails type

All receipts and notifications are **off by default** with a blank `configuration.json`.

To activate a notification or receipt, simply create a new key, named by the
event type (the list can be found [here](https://stripe.com/docs/api#event_types))
and formatted like this:

```json
{
  ...
  "email": {
    "charge.failed": {
      "active": true,
      "subject": "Oh nos! A Charge Has Failed!"
    }
  }
  ...
}
```

`subject` is optional. By default, the email subject will be the type,
periods replacing spaces and titlecased, prefixed with your
business name (if it exists) like so: `charge.failed -> [Acme Inc.] Charge Failed`.

Everything falls back to safe, generic defaults, like not showing a business name
if it doesn't exist.

Emails type configuration could look something like this:

```json
{
  ...
  "email": {
    "business": {
      "name": "Acme, Inc.",
      "signoff": "The Acme Team",
      "email": "Acme Support Team <support@example.com>"
    },
    "notifications": {
      "balance.available": {
        "active": true,
        "subject": "Dat chedda is available..."
      },
      "charge.succeeded": {
        "active": true
      },
      "charge.failed": {
        "active": true
      },
      "charge.refunded": {
        "active": true
      }
    },
    "receipts": {
      "invoice.created": {
        "active": true,
        "subject": "New Invoice"
      }
    }
  }
  ...
}
```

#### Emails Content

You need to provide a path to your emails templates:

```json
{
  ...
  "email": {
    "templates_path": "stripe-hooks-emails",
    ...
  }
  ...
}
```


You can fork [that repository](https://github.com/pearkes/stripe-hooks-emails) and you will have a good start.

#### stripe

You need to configure a stripe webhook in stripe GUI [stripe webhooks](https://dashboard.stripe.com/account/webhooks).

The service default port is `5000` and route url is `/webhook`.

When you have your endpoint secret just drop it in the configuration file:

```json
{
  ...
  "stripe": {
    "endpoint_secret": "whsec_..."
  },
  ...
}
```

The endpoint secret will be use to authenticate stripe `POST` requests following [stripe documentation](https://stripe.com/docs/webhooks/signatures).

#### Email Provider

SMTP is use as the default interface with your email provider.

Add this in your configuration file:

```json
{
  ...
  "smtp": {
    "url": "localhost:25"
  },
  ...
}
```

Mailgun is a good provider. Stripe team use it in there own documentation.

[Jack Pearkes](https://github.com/pearkes/stripe-hooks/) original work uses [Amazon SES](http://aws.amazon.com/ses/).

Revert commit `refactor(mail): use a smtp server instead of aws ses` if you want to use Amazon SES.


### Test

WIP

### Contributing

Just drop a PR following [git karma](http://karma-runner.github.io/2.0/dev/git-commit-msg.html) style.

When unit tests will be up-to-date, they will need to pass.

Project isn't compliant with [Flake8](http://flake8.pycqa.org/en/latest/) lint for now, so it's not mandatory, but it could be cool.

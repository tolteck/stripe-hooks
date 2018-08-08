#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .bootstrap import app


def start():
    app.run(host="0.0.0.0", port='5000')


if __name__ == "__main__":
    start()

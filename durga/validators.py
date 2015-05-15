# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import uuid

from durga import exceptions

email_regex = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"  # noqa
url_regex = r"^\w+://(\S+:\S+@){0,1}([^/:]+\.\S{2,10}|(\d{1,3}\.){3}\d{1,3})(:\d+)?(\/.*)?$"

email_pattern = re.compile(email_regex)
url_pattern = re.compile(url_regex)


def email(value):
    """Check if ``value`` is a valid email address."""
    if not email_pattern.match(value):
        raise exceptions.ValidationError("{0} is not a valid email address.".format(value))
    return value


def url(value):
    """Check if ``value`` is a valid URL."""
    if not url_pattern.match(value):
        raise exceptions.ValidationError("{0} is not a valid URL.".format(value))
    return value


def uuid4(value):
    """Check if ``value`` is a valid UUID version 4."""
    if uuid.UUID(value, version=4).hex != value:
        raise exceptions.ValidationError("{0} is not a valid UUID version 4.".format(value))
    return value

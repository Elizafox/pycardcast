# Copyright © 2015 Elizabeth Myers.
# All rights reserved.
# This file is part of the pycardcast project. See LICENSE in the root
# directory for licensing information.

from datetime import datetime


def isoformat(date):
    """Small, unpedantic ISO format parser (as used by Cardcast)."""

    assert date.endswith("+00:00"), "This cannot handle non-UTC offsets yet!"
    return datetime.strptime(date[:-6], "%Y-%m-%dT%H:%M:%S")

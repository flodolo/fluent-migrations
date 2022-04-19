# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
from fluent.migrate.helpers import transforms_from


def migrate(ctx):
    """Bug 1684950 - Change the remaining Firefox Account panel strings to sentence case. - part {index}"""
    ctx.add_transforms(
        "browser/browser/accounts.ftl",
        "browser/browser/accounts.ftl",
        transforms_from(
            """
account-send-to-all-devices = { COPY(from_path, "sendToAllDevices.menuitem") }
account-manage-devices = { COPY(from_path, "manageDevices.menuitem") }
""",
            from_path="browser/chrome/browser/accounts.properties",
        ),
    )

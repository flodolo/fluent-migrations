# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from

def migrate(ctx):
    """Bug 1625480 - Migrate remaining notifications strings from browser.dtd to Fluent, part {index}."""

    ctx.add_transforms(
        "browser/browser/appMenuNotifications.ftl",
        "browser/browser/appMenuNotifications.ftl",
    transforms_from(
"""
appmenu-new-tab-controlled =
    .label = { COPY(from_path, "newTabControlled.header.message", trim:"True") }
    .buttonlabel = { COPY(from_path, "newTabControlled.keepButton.label", trim:"True") }
    .buttonaccesskey = { COPY(from_path, "newTabControlled.keepButton.accesskey", trim:"True") }
    .secondarybuttonlabel = { COPY(from_path, "newTabControlled.disableButton.label", trim:"True") }
    .secondarybuttonaccesskey = { COPY(from_path, "newTabControlled.disableButton.accesskey", trim:"True") }
appmenu-homepage-controlled =
    .label = { COPY(from_path, "homepageControlled.header.message", trim:"True") }
    .buttonlabel = { COPY(from_path, "homepageControlled.keepButton.label", trim:"True") }
    .buttonaccesskey = { COPY(from_path, "homepageControlled.keepButton.accesskey", trim:"True") }
    .secondarybuttonlabel = { COPY(from_path, "homepageControlled.disableButton.label", trim:"True") }
    .secondarybuttonaccesskey = { COPY(from_path, "homepageControlled.disableButton.accesskey", trim:"True") }
appmenu-tab-hide-controlled =
    .label = { COPY(from_path, "tabHideControlled.header.message", trim:"True") }
    .buttonlabel = { COPY(from_path, "tabHideControlled.keepButton.label", trim:"True") }
    .buttonaccesskey = { COPY(from_path, "tabHideControlled.keepButton.accesskey", trim:"True") }
    .secondarybuttonlabel = { COPY(from_path, "tabHideControlled.disableButton.label", trim:"True") }
    .secondarybuttonaccesskey = { COPY(from_path, "tabHideControlled.disableButton.accesskey", trim:"True") }
""", from_path="browser/chrome/browser/browser.dtd"))

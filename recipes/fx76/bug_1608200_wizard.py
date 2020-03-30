# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import MESSAGE_REFERENCE, TERM_REFERENCE

def migrate(ctx):
    """Bug 1608200 - Migrate wizard to Fluent, part {index}."""

    ctx.add_transforms(
        "toolkit/toolkit/global/wizard.ftl",
        "toolkit/toolkit/global/wizard.ftl",
    transforms_from(
"""
wizard-macos-button-back =
    .label = { COPY(from_path, "button-back-mac.label", trim:"True") }
    .accesskey = { COPY(from_path, "button-back-mac.accesskey", trim:"True") }
wizard-linux-button-back =
    .label = { COPY(from_path, "button-back-unix.label", trim:"True") }
    .accesskey = { COPY(from_path, "button-back-unix.accesskey", trim:"True") }
wizard-win-button-back =
    .label = { COPY(from_path, "button-back-win.label", trim:"True") }
    .accesskey = { COPY(from_path, "button-back-win.accesskey", trim:"True") }
wizard-macos-button-next =
    .label = { COPY(from_path, "button-next-mac.label", trim:"True") }
    .accesskey = { COPY(from_path, "button-next-mac.accesskey", trim:"True") }
wizard-linux-button-next =
    .label = { COPY(from_path, "button-next-unix.label", trim:"True") }
    .accesskey = { COPY(from_path, "button-next-unix.accesskey", trim:"True") }
wizard-win-button-next =
    .label = { COPY(from_path, "button-next-win.label", trim:"True") }
    .accesskey = { COPY(from_path, "button-next-win.accesskey", trim:"True") }
wizard-macos-button-finish =
    .label = { COPY(from_path, "button-finish-mac.label", trim:"True") }
wizard-linux-button-finish =
    .label = { COPY(from_path, "button-finish-unix.label", trim:"True") }
wizard-win-button-finish =
    .label = { COPY(from_path, "button-finish-win.label", trim:"True") }
wizard-macos-button-cancel =
    .label = { COPY(from_path, "button-cancel-mac.label", trim:"True") }
wizard-linux-button-cancel =
    .label = { COPY(from_path, "button-cancel-unix.label", trim:"True") }
wizard-win-button-cancel =
    .label = { COPY(from_path, "button-cancel-win.label", trim:"True") }
""", from_path="toolkit/chrome/global/wizard.dtd"))

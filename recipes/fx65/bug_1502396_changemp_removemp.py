# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import TERM_REFERENCE
from fluent.migrate import COPY
from fluent.migrate import REPLACE


def migrate(ctx):
    """Bug 1502396 - Convert change and remove master password dialogs in about:preferences to use Fluent"""

    ctx.add_transforms(
        "toolkit/toolkit/preferences/preferences.ftl",
        "toolkit/toolkit/preferences/preferences.ftl",
        transforms_from(
            """
set-password =
    .title = { COPY(from_path, "setPassword.title") }
set-password-old-password = { COPY(from_path, "setPassword.oldPassword.label") }
set-password-new-password = { COPY(from_path, "setPassword.newPassword.label") }
set-password-reenter-password = { COPY(from_path, "setPassword.reenterPassword.label") }
set-password-meter = { COPY(from_path, "setPassword.meter.label") }
set-password-meter-loading = { COPY(from_path, "setPassword.meter.loading") }
master-password-warning = { COPY(from_path, "masterPasswordWarning.label") }
""", from_path="toolkit/chrome/mozapps/preferences/changemp.dtd") + [
        FTL.Message(
            id=FTL.Identifier("master-password-description"),
            value=REPLACE(
                "toolkit/chrome/mozapps/preferences/changemp.dtd",
                "masterPasswordDescription.label",
                {
                    "&brandShortName;": TERM_REFERENCE("-brand-short-name")
                },
                trim=True
            )
        ),
    ])

    ctx.add_transforms(
        "toolkit/toolkit/preferences/preferences.ftl",
        "toolkit/toolkit/preferences/preferences.ftl",
        transforms_from(
            """
remove-password =
    .title = { COPY(from_path, "removePassword.title") }
remove-info =
    .value = { COPY(from_path, "removeInfo.label") }
remove-warning1 = { COPY(from_path, "removeWarning1.label") }
remove-warning2 = { COPY(from_path, "removeWarning2.label") }
remove-password-old-password =
    .value = { COPY(from_path, "setPassword.oldPassword.label") }
""", from_path="toolkit/chrome/mozapps/preferences/removemp.dtd"))

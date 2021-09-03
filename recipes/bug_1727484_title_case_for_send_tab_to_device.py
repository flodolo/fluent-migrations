# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from, VARIABLE_REFERENCE
from fluent.migrate import COPY, PLURALS, REPLACE, REPLACE_IN_TEXT


def migrate(ctx):
    """Bug 1727484 - Convert the 'Send Tab to Device' string in the tab context menu to title case, part {index}"""

    ctx.add_transforms(
        "browser/browser/tabContextMenu.ftl",
        "browser/browser/tabContextMenu.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("tab-context-send-tabs-to-device"),
                attributes=[
                    FTL.Attribute(
                        id=FTL.Identifier("label"),
                        value=PLURALS(
                            "browser/chrome/browser/browser.properties",
                            "sendTabsToDevice.label",
                            VARIABLE_REFERENCE("tabCount"),
                            lambda text: REPLACE_IN_TEXT(
                                text, {"#1": VARIABLE_REFERENCE("tabCount")}
                            ),
                        ),
                    ),
                    FTL.Attribute(
                        id=FTL.Identifier("accesskey"),
                        value=COPY(
                            "browser/chrome/browser/browser.properties",
                            "sendTabsToDevice.accesskey",
                        ),
                    ),
                ],
            )
        ],
    )

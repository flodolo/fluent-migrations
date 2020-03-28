# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate import CONCAT, REPLACE
from fluent.migrate.helpers import COPY, TERM_REFERENCE

def migrate(ctx):
    """Bug 1608188 - Migrate blocklist.dtd to Fluent, part {index}."""
    ctx.add_transforms(
        "toolkit/toolkit/extensions/blocklist.ftl",
        "toolkit/toolkit/extensions/blocklist.ftl",
    transforms_from(
"""
blocklist-window =
    .title = { COPY(from_path, "blocklist.title", trim:"True") }
    .style = { COPY(from_path, "blocklist.style", trim:"True") }

blocklist-soft-and-hard = { COPY(from_path, "blocklist.softandhard", trim:"True") }
blocklist-hard-blocked = { COPY(from_path, "blocklist.hardblocked", trim:"True") }
blocklist-soft-blocked = { COPY(from_path, "blocklist.softblocked", trim:"True") }
blocklist-more-information =
    .value = { COPY(from_path, "blocklist.moreinfo", trim:"True") }
blocklist-blocked =
    .label = { COPY(from_path, "blocklist.blocked.label", trim:"True") }
blocklist-checkbox =
    .label = { COPY(from_path, "blocklist.checkbox.label", trim:"True") }
""",from_path="toolkit/chrome/mozapps/extensions/blocklist.dtd"))

    ctx.add_transforms(
        "toolkit/toolkit/extensions/blocklist.ftl",
        "toolkit/toolkit/extensions/blocklist.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("blocklist-accept"),
                attributes=[
                    FTL.Attribute(
                        id=FTL.Identifier("label"),
                        value=REPLACE(
                            "toolkit/chrome/mozapps/extensions/blocklist.dtd",
                            "blocklist.accept.label",
                            {
                                "&brandShortName;": TERM_REFERENCE("brand-short-name")
                            },
                            trim=True,
                        )
                    ),
                    FTL.Attribute(
                        id=FTL.Identifier("accesskey"),
                        value=COPY(
                            "toolkit/chrome/mozapps/extensions/blocklist.dtd",
                            "blocklist.accept.accesskey",
                            trim=True,
                        )
                    ),
                ]
            ),
            FTL.Message(
                id = FTL.Identifier("blocklist-label-summary"),
                value = REPLACE(
                    "toolkit/chrome/mozapps/extensions/blocklist.dtd",
                    "blocklist.summary",
                    {
                        "&brandShortName;": TERM_REFERENCE("brand-short-name")
                    },
                    trim=True,
                )
            ),

        ]
    )

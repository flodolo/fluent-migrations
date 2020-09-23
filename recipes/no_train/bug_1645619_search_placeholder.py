# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate import REPLACE
from fluent.migrate.helpers import VARIABLE_REFERENCE


def migrate(ctx):
    """Bug 1645619 - Migrate address bar placeholder to Fluent, part {index}."""

    ctx.add_transforms(
        "browser/browser/browser.ftl",
        "browser/browser/browser.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("urlbar-placeholder-with-name"),
                attributes=[
                    FTL.Attribute(
                        id=FTL.Identifier("placeholder"),
                        value=REPLACE(
                            "browser/chrome/browser/browser.properties",
                            "urlbar.placeholder",
                            {
                                "%1$S": VARIABLE_REFERENCE("name"),
                            },
                            normalize_printf=True
                        )
                    ),
                ]
            )
        ]
    )

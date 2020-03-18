# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate import REPLACE
from fluent.migrate.helpers import TERM_REFERENCE

def migrate(ctx):
    """Bug 1608165 - Migrate profileSelection to Fluent, part {index}."""

    ctx.add_transforms(
        "toolkit/toolkit/global/profileSelection.ftl",
        "toolkit/toolkit/global/profileSelection.ftl",
    transforms_from(
"""
profile-selection-button-cancel =
    .label = { COPY(from_path, "exit.label", trim:"True") }
profile-selection-new-button =
    .label = { COPY(from_path, "newButton.label", trim:"True") }
    .accesskey = { COPY(from_path, "newButton.accesskey", trim:"True") }
profile-selection-rename-button =
    .label = { COPY(from_path, "renameButton.label", trim:"True") }
    .accesskey = { COPY(from_path, "renameButton.accesskey", trim:"True") }
profile-selection-delete-button =
    .label = { COPY(from_path, "deleteButton.label", trim:"True") }
    .accesskey = { COPY(from_path, "deleteButton.accesskey", trim:"True") }
profile-manager-work-offline =
    .label = { COPY(from_path, "offlineState.label", trim:"True") }
    .accesskey = { COPY(from_path, "offlineState.accesskey", trim:"True") }
profile-manager-use-selected =
    .label = { COPY(from_path, "useSelected.label", trim:"True") }
    .accesskey = { COPY(from_path, "useSelected.accesskey", trim:"True") }
""", from_path="toolkit/chrome/mozapps/profile/profileSelection.dtd"))
    ctx.add_transforms(
    "toolkit/toolkit/global/profileSelection.ftl",
    "toolkit/toolkit/global/profileSelection.ftl",
    [
    FTL.Message(
        id=FTL.Identifier("profile-selection-window"),
        attributes=[
            FTL.Attribute(
                id=FTL.Identifier("title"),
                value=REPLACE(
                    "toolkit/chrome/mozapps/profile/profileSelection.dtd",
                    "windowtitle.label",
                    {
                        "&brandShortName;": TERM_REFERENCE("brand-short-name")
                    },
                    trim=True
                )
            )
        ]
    ),
    FTL.Message(
        id=FTL.Identifier("profile-selection-button-accept"),
        attributes=[
            FTL.Attribute(
                id=FTL.Identifier("label"),
                value=REPLACE(
                    "toolkit/chrome/mozapps/profile/profileSelection.dtd",
                    "start.label",
                    {
                        "&brandShortName;": TERM_REFERENCE("brand-short-name")
                    },
                    trim=True
                )
            )
        ]
    ),
    FTL.Message(
        id=FTL.Identifier("profile-manager-description"),
        value=REPLACE(
            "toolkit/chrome/mozapps/profile/profileSelection.dtd",
            "pmDescription.label",
            {
                "&brandShortName;": TERM_REFERENCE("brand-short-name")
            },
            trim=True
        )
    ),
    ]
    )

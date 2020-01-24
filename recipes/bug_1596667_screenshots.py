# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
from __future__ import unicode_literals
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate import COPY, CONCAT, REPLACE
from fluent.migrate.helpers import MESSAGE_REFERENCE, TERM_REFERENCE


def migrate(ctx):
    """Bug 1596667 - Migrate Screenshots add-on to Fluent, part {index}"""

    target_ftl = "locales/{}/screenshots.ftl".format(ctx.locale)
    reference_ftl = "locales/en-US/screenshots.ftl"
    webextension_properties = "locales/{}/webextension.properties".format(
        ctx.locale)
    ctx.add_transforms(
        target_ftl,
        reference_ftl,
        transforms_from(
            """
screenshots-context-menu = { COPY(from_path, "contextMenuLabel", trim: "True") }
screenshots-my-shots-button = { COPY(from_path, "myShotsLink", trim: "True") }
screenshots-instructions = { COPY(from_path, "screenshotInstructions", trim: "True") }
screenshots-cancel-button = { COPY(from_path, "cancelScreenshot", trim: "True") }
screenshots-save-visible-button = { COPY(from_path, "saveScreenshotVisibleArea", trim: "True") }
screenshots-save-page-button = { COPY(from_path, "saveScreenshotFullPage", trim: "True") }
screenshots-download-button = { COPY(from_path, "downloadScreenshot", trim: "True") }
screenshots-download-button-tooltip = { COPY(from_path, "downloadScreenshotTitle", trim: "True") }
screenshots-copy-button = { COPY(from_path, "copyScreenshot", trim: "True") }
screenshots-copy-button-tooltip = { COPY(from_path, "copyScreenshotTitle", trim: "True") }
screenshots-notification-link-copied-title = { COPY(from_path, "notificationLinkCopiedTitle", trim: "True") }
screenshots-notification-image-copied-title = { COPY(from_path, "notificationImageCopiedTitle", trim: "True") }
screenshots-request-error-title = { COPY(from_path, "requestErrorTitle", trim: "True") }
screenshots-request-error-details = { COPY(from_path, "requestErrorDetails", trim: "True") }
screenshots-connection-error-title = { COPY(from_path, "connectionErrorTitle", trim: "True") }
screenshots-unshootable-page-error-title = { COPY(from_path, "unshootablePageErrorTitle", trim: "True") }
screenshots-unshootable-page-error-details = { COPY(from_path, "unshootablePageErrorDetails", trim: "True") }
screenshots-empty-selection-error-title = { COPY(from_path, "emptySelectionErrorTitle", trim: "True") }
screenshots-private-window-error-details = { COPY(from_path, "privateWindowErrorDetails", trim: "True") }
screenshots-generic-error-details = { COPY(from_path, "genericErrorDetails", trim: "True") }

screenshots-meta-key = {
  PLATFORM() ->
    [macos] ⌘
   *[other] Ctrl
}
""", from_path=webextension_properties))

    ctx.add_transforms(
        target_ftl,
        reference_ftl,
        [
            FTL.Message(
                id=FTL.Identifier(
                    "screenshots-notification-link-copied-details"),
                value=REPLACE(
                    webextension_properties,
                    "notificationLinkCopiedDetails",
                    {
                        "{meta_key}": MESSAGE_REFERENCE("screenshots-meta-key")
                    },
                    trim=True
                )
            ),
            FTL.Message(
                id=FTL.Identifier(
                    "screenshots-notification-image-copied-details"),
                value=REPLACE(
                    webextension_properties,
                    "notificationImageCopiedDetails",
                    {
                        "{meta_key}": MESSAGE_REFERENCE("screenshots-meta-key")
                    },
                    trim=True
                )
            ),
            FTL.Message(
                id=FTL.Identifier("screenshots-login-error-details"),
                value=REPLACE(
                    webextension_properties,
                    "loginErrorDetails",
                    {
                        "Firefox Screenshots": TERM_REFERENCE("screenshots-brand-name")
                    },
                    trim=True
                )
            ),
            FTL.Message(
                id=FTL.Identifier("screenshots-self-screenshot-error-title"),
                value=REPLACE(
                    webextension_properties,
                    "selfScreenshotErrorTitle",
                    {
                        "Firefox Screenshots": TERM_REFERENCE("screenshots-brand-name")
                    },
                    trim=True
                )
            ),
            FTL.Message(
                id=FTL.Identifier("screenshots-private-window-error-title"),
                value=REPLACE(
                    webextension_properties,
                    "privateWindowErrorTitle",
                    {
                        "Screenshots": TERM_REFERENCE("screenshots-brand-name")
                    },
                    trim=True
                )
            ),
            FTL.Message(
                id=FTL.Identifier("screenshots-generic-error-title"),
                value=REPLACE(
                    webextension_properties,
                    "genericErrorTitle",
                    {
                        "Firefox Screenshots": TERM_REFERENCE("screenshots-brand-name")
                    },
                    trim=True
                )
            ),
            FTL.Message(
                id=FTL.Identifier("screenshots-connection-error-details"),
                value=REPLACE(
                    webextension_properties,
                    "connectionErrorDetails",
                    {
                        "Firefox Screenshots": TERM_REFERENCE("screenshots-brand-name")
                    },
                    trim=True
                )
            ),
        ]
    )

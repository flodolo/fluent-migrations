# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate import CONCAT
from fluent.migrate.helpers import COPY, transforms_from

def migrate(ctx):
    """Bug 1608199 - Port devtools/client/styleeditor.dtd to Fluent, part {index}."""

    ctx.add_transforms(
        "devtools/client/styleeditor.ftl",
        "devtools/client/styleeditor.ftl",
    transforms_from(
"""
styleeditor-new-button =
    .tooltiptext = { COPY(from_path, "newButton.tooltip", trim:"True") }
    .accesskey = { COPY(from_path, "newButton.accesskey", trim:"True") }
styleeditor-import-button =
    .tooltiptext = { COPY(from_path, "importButton.tooltip", trim:"True") }
    .accesskey = { COPY(from_path, "importButton.accesskey", trim:"True") }
styleeditor-visibility-toggle =
    .tooltiptext = { COPY(from_path, "visibilityToggle.tooltip")}
    .accesskey = { COPY(from_path, "saveButton.accesskey", trim:"True") }
styleeditor-save-button = { COPY(from_path, "saveButton.label", trim:"True") }
    .tooltiptext = { COPY(from_path, "saveButton.tooltip", trim:"True") }
    .accesskey = { COPY(from_path, "saveButton.accesskey", trim:"True") }
styleeditor-options-button =
    .tooltiptext = { COPY(from_path, "optionsButton.tooltip", trim:"True") }
styleeditor-media-rules = { COPY(from_path, "mediaRules.label", trim:"True") }
styleeditor-editor-textbox =
    .data-placeholder = { COPY(from_path, "editorTextbox.placeholder", trim:"True") }
styleeditor-no-stylesheet = { COPY(from_path, "noStyleSheet.label", trim:"True") }
styleeditor-open-link-new-tab =
    .label = { COPY(from_path, "openLinkNewTab.label", trim:"True") }
styleeditor-copy-url =
    .label = { COPY(from_path, "copyUrl.label", trim:"True") }
""", from_path="devtools/client/styleeditor.dtd"))

    ctx.add_transforms(
        "devtools/client/styleeditor.ftl",
        "devtools/client/styleeditor.ftl",
        [
            FTL.Message(
                        id=FTL.Identifier("styleeditor-no-stylesheet-tip"),
                        value=CONCAT(
                                    COPY(
                                        "devtools/client/styleeditor.dtd",
                                         "noStyleSheet-tip-start.label",
                                         ),
                                    FTL.TextElement('<a data-l10n-name="append-new-stylesheet">'),
                                    COPY(
                                        "devtools/client/styleeditor.dtd",
                                        "noStyleSheet-tip-action.label",
                                        ),
                                    FTL.TextElement("</a>"),
                                    COPY("devtools/client/styleeditor.dtd",
                                         "noStyleSheet-tip-end.label",
                                         ),
                                    ),
            )
        ]
    )

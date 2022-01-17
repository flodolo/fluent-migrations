# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from

def migrate(ctx):
    """Bug 1624713 - Convert editBookmarkOverlay to Fluent, part {index}."""

    ctx.add_transforms(
        "browser/browser/editBookmarkOverlay.ftl",
        "browser/browser/editBookmarkOverlay.ftl",
    transforms_from(
"""
bookmark-overlay-name =
    .value = { COPY(from_path, "editBookmarkOverlay.name.label", trim:"True") }
    .accesskey = { COPY(from_path, "editBookmarkOverlay.name.accesskey", trim:"True") }
bookmark-overlay-location =
    .value = { COPY(from_path, "editBookmarkOverlay.location.label", trim:"True") }
    .accesskey = { COPY(from_path, "editBookmarkOverlay.location.accesskey", trim:"True") }
bookmark-overlay-folder =
    .value = { COPY(from_path, "editBookmarkOverlay.folder.label", trim:"True") }
bookmark-overlay-choose =
    .label = { COPY(from_path, "editBookmarkOverlay.choose.label", trim:"True") }
bookmark-overlay-folders-expander =
  .tooltiptext = { COPY(from_path, "editBookmarkOverlay.foldersExpanderDown.tooltip", trim:"True") }
  .tooltiptextdown = { bookmark-overlay-folders-expander.tooltiptext }
  .tooltiptextup = { COPY(from_path, "editBookmarkOverlay.expanderUp.tooltip", trim:"True") }
bookmark-overlay-new-folder-button =
    .label = { COPY(from_path, "editBookmarkOverlay.newFolderButton.label", trim:"True") }
    .accesskey = { COPY(from_path, "editBookmarkOverlay.newFolderButton.accesskey", trim:"True") }
bookmark-overlay-tags =
    .value = { COPY(from_path, "editBookmarkOverlay.tags.label", trim:"True") }
    .accesskey ={ COPY(from_path, "editBookmarkOverlay.tags.accesskey", trim:"True") }
bookmark-overlay-tags-empty-description =
    .placeholder = { COPY(from_path, "editBookmarkOverlay.tagsEmptyDesc.label", trim:"True") }
bookmark-overlay-tags-expander =
  .tooltiptext = { COPY(from_path, "editBookmarkOverlay.tagsExpanderDown.tooltip", trim:"True") }
  .tooltiptextdown = { bookmark-overlay-tags-expander.tooltiptext }
  .tooltiptextup = { COPY(from_path, "editBookmarkOverlay.expanderUp.tooltip", trim:"True") }
bookmark-overlay-keyword =
    .value = { COPY(from_path, "editBookmarkOverlay.keyword.label", trim:"True") }
    .accesskey = { COPY(from_path, "editBookmarkOverlay.keyword.accesskey", trim:"True") }
""", from_path="browser/chrome/browser/places/editBookmarkOverlay.dtd"))

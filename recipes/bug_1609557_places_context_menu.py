# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from, TERM_REFERENCE, MESSAGE_REFERENCE
from fluent.migrate import COPY_PATTERN, REPLACE, COPY


def migrate(ctx):
    """Bug 1609557 - Migrate placesContextMenu.inc.xhtml to Fluent, part {index}."""

    ctx.add_transforms(
        'browser/browser/places.ftl',
        'browser/browser/places.ftl',
        transforms_from(
"""
places-open =
    .label = { COPY(from_path, "cmd.open.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.open.accesskey", trim:"True") }
places-open-tab =
    .label = { COPY(from_path, "cmd.open_tab.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.open_tab.accesskey", trim:"True") }
places-open-all-in-tabs =
    .label = { COPY(from_path, "cmd.open_all_in_tabs.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.open_all_in_tabs.accesskey", trim:"True") }
places-open-window =
    .label = { COPY(from_path, "cmd.open_window.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.open_window.accesskey", trim:"True") }
places-open-private-window =
    .label = { COPY(from_path, "cmd.open_private_window.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.open_private_window.accesskey", trim:"True") }
places-new-bookmark =
    .label = { COPY(from_path, "cmd.new_bookmark.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.new_bookmark.accesskey", trim:"True") }
places-new-folder-contextmenu =
    .label = { COPY(from_path, "cmd.new_folder.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.context_new_folder.accesskey", trim:"True") }
places-new-folder =
    .label = { COPY(from_path, "cmd.new_folder.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.new_folder.accesskey", trim:"True") }
places-new-separator =
    .label = { COPY(from_path, "cmd.new_separator.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.new_separator.accesskey", trim:"True") }
places-view =
    .label = { COPY(from_path, "view.label" , trim:"True") }
    .accesskey = { COPY(from_path, "view.accesskey", trim:"True") }
places-by-date =
    .label = { COPY(from_path, "byDate.label" , trim:"True") }
    .accesskey = { COPY(from_path, "byDate.accesskey" , trim:"True") }
places-by-site =
    .label = { COPY(from_path, "bySite.label" , trim:"True") }
    .accesskey = { COPY(from_path, "bySite.accesskey" , trim:"True") }
places-by-most-visited =
    .label = { COPY(from_path, "byMostVisited.label" , trim:"True") }
    .accesskey = { COPY(from_path, "byMostVisited.accesskey" , trim:"True") }
places-by-last-visited =
    .label = { COPY(from_path, "byLastVisited.label" , trim:"True") }
    .accesskey = { COPY(from_path, "byLastVisited.accesskey" , trim:"True") }
places-by-day-and-site =
    .label = { COPY(from_path, "byDayAndSite.label" , trim:"True") }
    .accesskey = { COPY(from_path, "byDayAndSite.accesskey" , trim:"True") }
places-history-search =
    .placeholder = { COPY(from_path, "historySearch.placeholder" , trim:"True") }
places-bookmarks-search =
    .placeholder = { COPY(from_path, "bookmarksSearch.placeholder" , trim:"True") }
places-delete-domain-data =
    .label = { COPY(from_path, "cmd.deleteDomainData.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.deleteDomainData.accesskey", trim:"True") }
places-sortby-name =
    .label = { COPY(from_path, "cmd.sortby_name.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.context_sortby_name.accesskey", trim:"True") }
places-properties =
    .label = { COPY(from_path, "cmd.properties.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.properties.accesskey", trim:"True") }
""", from_path="browser/chrome/browser/places/places.dtd")
    )

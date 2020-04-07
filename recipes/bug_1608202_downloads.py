# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate import COPY, CONCAT, REPLACE

def migrate(ctx):
    """Bug 1608202 - Migrate downloads to Fluent, part {index}."""

    ctx.add_transforms(
        "browser/browser/downloads.ftl",
        "browser/browser/downloads.ftl",
    transforms_from(
"""
downloads-window =
    .title = { COPY(from_path, "downloads.title", trim:"True") }
downloads-panel =
    .aria-label = { COPY(from_path, "downloads.title", trim:"True") }
downloads-panel-list =
    .style = width: { COPY(from_path, "downloads.width", trim:"True") }
downloads-cmd-pause =
    .label = { COPY(from_path, "cmd.pause.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.pause.accesskey", trim:"True") }
downloads-cmd-resume =
    .label = { COPY(from_path, "cmd.resume.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.resume.accesskey", trim:"True") }
downloads-cmd-cancel =
    .tooltiptext = { COPY(from_path, "cmd.cancel.label", trim:"True") }
downloads-cmd-cancel-panel =
    .aria-label = { COPY(from_path, "cmd.cancel.label", trim:"True") }
downloads-cmd-show =
    .label = { COPY(from_path, "cmd.show.label", trim:"True") }
    .tooltiptext = { downloads-cmd-show.label }
    .accesskey = { COPY(from_path, "cmd.show.accesskey", trim:"True") }
downloads-cmd-show-mac =
    .label = { COPY(from_path, "cmd.showMac.label", trim:"True") }
    .tooltiptext = { downloads-cmd-show-mac.label }
    .accesskey = { COPY(from_path, "cmd.showMac.accesskey", trim:"True") }
downloads-cmd-show-panel =
    .aria-label = { PLATFORM() ->
        [macos] { COPY(from_path, "cmd.showMac.label", trim:"True") }
       *[other] { COPY(from_path, "cmd.show.label", trim:"True") }
    }
downloads-cmd-show-description =
    .value = { PLATFORM() ->
        [macos] { COPY(from_path, "cmd.showMac.label", trim:"True") }
       *[other] { COPY(from_path, "cmd.show.label", trim:"True") }
    }
downloads-cmd-show-downloads =
    .label = { COPY(from_path, "cmd.showDownloads.label", trim:"True") }
downloads-cmd-retry =
    .tooltiptext = { COPY(from_path, "cmd.retry.label", trim:"True") }
downloads-cmd-retry-panel =
    .aria-label = { COPY(from_path, "cmd.retry.label", trim:"True") }
downloads-cmd-go-to-download-page =
    .label = { COPY(from_path, "cmd.goToDownloadPage.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.goToDownloadPage.accesskey", trim:"True") }
downloads-cmd-copy-download-link =
    .label = { COPY(from_path, "cmd.copyDownloadLink.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.copyDownloadLink.accesskey", trim:"True") }
downloads-cmd-remove-from-history =
    .label = { COPY(from_path, "cmd.removeFromHistory.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.removeFromHistory.accesskey", trim:"True") }
downloads-cmd-clear-list =
    .label = { COPY(from_path, "cmd.clearList2.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.clearList2.accesskey", trim:"True") }
downloads-cmd-clear-downloads =
    .label = { COPY(from_path, "cmd.clearDownloads.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.clearDownloads.accesskey", trim:"True") }
downloads-cmd-unblock =
    .label = { COPY(from_path, "cmd.unblock2.label", trim:"True") }
    .accesskey = { COPY(from_path, "cmd.unblock2.accesskey", trim:"True") }
downloads-cmd-remove-file =
    .tooltiptext = { COPY(from_path, "cmd.removeFile.label", trim:"True") }
downloads-cmd-remove-file-panel =
    .aria-label = { COPY(from_path, "cmd.removeFile.label", trim:"True") }
downloads-cmd-choose-unblock =
    .tooltiptext = { COPY(from_path, "cmd.chooseUnblock.label", trim:"True") }
downloads-cmd-choose-unblock-panel =
    .aria-label = { COPY(from_path, "cmd.chooseUnblock.label", trim:"True") }
downloads-cmd-choose-open =
    .tooltiptext = { COPY(from_path, "cmd.chooseOpen.label", trim:"True") }
downloads-cmd-choose-open-panel =
    .aria-label = { COPY(from_path, "cmd.chooseOpen.label", trim:"True") }
downloads-show-more-information =
    .value = { COPY(from_path, "showMoreInformation.label", trim:"True") }
downloads-open-file =
    .value = { COPY(from_path, "openFile.label", trim:"True") }
downloads-retry-download =
    .value = { COPY(from_path, "retryDownload.label", trim:"True") }
downloads-cancel-download =
    .value = { COPY(from_path, "cancelDownload.label", trim:"True") }
downloads-history =
    .label = { COPY(from_path, "downloadsHistory.label", trim:"True") }
    .accesskey = { COPY(from_path, "downloadsHistory.accesskey", trim:"True") }
downloads-details =
    .title = { COPY(from_path, "downloadDetails.label", trim:"True") }
downloads-clear-downloads-button =
    .label = { COPY(from_path, "clearDownloadsButton.label", trim:"True") }
    .tooltiptext = { COPY(from_path, "clearDownloadsButton.tooltip", trim:"True") }
downloads-list-empty =
    .value = { COPY(from_path, "downloadsListEmpty.label", trim:"True") }
downloads-panel-empty =
    .value = { COPY(from_path, "downloadsPanelEmpty.label", trim:"True") }
""", from_path="browser/chrome/browser/downloads/downloads.dtd"))

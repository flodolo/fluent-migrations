# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import COPY

def migrate(ctx):
    """Bug 1591003 - Migrate urlbar notification tooltips to Fluent, part {index}"""

    ctx.add_transforms(
        "browser/browser/browser.ftl",
        "browser/browser/browser.ftl",
        transforms_from(
            """

urlbar-geolocation-blocked =
    .tooltiptext = { COPY(path1, "urlbar.geolocationBlocked.tooltip", trim: "True") }
urlbar-web-notifications-blocked =
    .tooltiptext = { COPY(path1, "urlbar.webNotificationsBlocked.tooltip", trim: "True") }
urlbar-camera-blocked =
    .tooltiptext = { COPY(path1, "urlbar.cameraBlocked.tooltip", trim: "True") }
urlbar-microphone-blocked =
    .tooltiptext = { COPY(path1, "urlbar.microphoneBlocked.tooltip", trim: "True") }
urlbar-screen-blocked =
    .tooltiptext = { COPY(path1, "urlbar.screenBlocked.tooltip", trim: "True") }
urlbar-persistent-storage-blocked =
    .tooltiptext = { COPY(path1, "urlbar.persistentStorageBlocked.tooltip", trim: "True") }
urlbar-popup-blocked =
    .tooltiptext = { COPY(path1, "urlbar.popupBlocked.tooltip", trim: "True") }
urlbar-autoplay-media-blocked =
    .tooltiptext = { COPY(path1, "urlbar.autoplayMediaBlocked.tooltip", trim: "True") }
urlbar-canvas-blocked =
    .tooltiptext = { COPY(path1, "urlbar.canvasBlocked.tooltip", trim: "True") }
urlbar-midi-blocked =
    .tooltiptext = { COPY(path1, "urlbar.midiBlocked.tooltip", trim: "True") }
urlbar-install-blocked =
    .tooltiptext = { COPY(path1, "urlbar.installBlocked.tooltip", trim: "True") }
""", path1="browser/chrome/browser/browser.dtd"))

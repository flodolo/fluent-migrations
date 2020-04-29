# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate import REPLACE, CONCAT, COPY
from fluent.migrate.helpers import TERM_REFERENCE

def migrate(ctx):
    """Bug 1609559 - Migrate protectionsPanel.inc.xhtml to Fluent, part {index}."""

    ctx.add_transforms(
        "browser/browser/protectionsPanel.ftl",
        "browser/browser/protectionsPanel.ftl",
    transforms_from(
"""
protections-panel-etp-more-info =
    .aria-label = { COPY(from_path, "protections.etpMoreInfo.label", trim:"True") }
protections-panel-etp-on-header = { COPY(from_path, "protections.etpON.header", trim:"True") }
protections-panel-etp-off-header = { COPY(from_path, "protections.etpOFF.header", trim:"True") }
protections-panel-site-not-working = { COPY(from_path, "protections.siteNotWorking.label", trim:"True") }
protections-panel-site-not-working-view =
    .title = { COPY(from_path, "protections.siteNotWorkingView.title", trim:"True") }
protections-panel-not-blocking-why-label = { COPY(from_path, "protections.notBlocking.why.label", trim:"True") }
protections-panel-not-blocking-why-etp-on-tooltip = { COPY(from_path, "protections.notBlocking.why.etpOn.tooltip", trim:"True") }
protections-panel-not-blocking-why-etp-off-tooltip = { COPY(from_path, "protections.notBlocking.why.etpOff2.tooltip", trim:"True") }
protections-panel-content-blocking-tracking-protection = { COPY(from_path, "contentBlocking.trackingProtection4.label", trim:"True") }
protections-panel-content-blocking-socialblock = { COPY(from_path, "contentBlocking.socialblock.label", trim:"True") }
protections-panel-content-blocking-cryptominers-label = { COPY(from_path, "contentBlocking.cryptominers.label", trim:"True") }
protections-panel-content-blocking-fingerprinters-label = { COPY(from_path, "contentBlocking.fingerprinters.label", trim:"True") }
protections-panel-blocking-label = { COPY(from_path, "protections.blocking2.label", trim:"True") }
protections-panel-not-blocking-label = { COPY(from_path, "protections.notBlocking2.label", trim:"True") }
protections-panel-not-found-label = { COPY(from_path, "protections.notFound.label", trim:"True") }
protections-panel-settings-label = { COPY(from_path, "protections.settings.label", trim:"True") }
protections-panel-showreport-label = { COPY(from_path, "protections.showreport.label", trim:"True") }
protections-panel-site-not-working-view-header = { COPY(from_path, "protections.siteNotWorkingView.header", trim:"True") }
protections-panel-site-not-working-view-issue-list-login-fields = { COPY(from_path, "protections.siteNotWorkingView.issueList.logInFields", trim:"True") }
protections-panel-site-not-working-view-issue-list-forms = { COPY(from_path, "protections.siteNotWorkingView.issueList.forms", trim:"True") }
protections-panel-site-not-working-view-issue-list-payments = { COPY(from_path, "protections.siteNotWorkingView.issueList.payments", trim:"True") }
protections-panel-site-not-working-view-issue-list-comments = { COPY(from_path, "protections.siteNotWorkingView.issueList.comments", trim:"True") }
protections-panel-site-not-working-view-issue-list-videos = { COPY(from_path, "protections.siteNotWorkingView.issueList.videos", trim:"True") }
protections-panel-site-not-working-view-send-report = { COPY(from_path, "protections.siteNotWorkingView.sendReport.label", trim:"True") }
protections-panel-cross-site-tracking-cookies = { COPY(from_path, "protections.crossSiteTrackingCookies.description", trim:"True") }
protections-panel-cryptominers = { COPY(from_path, "protections.cryptominers.description", trim:"True") }
protections-panel-fingerprinters = { COPY(from_path, "protections.fingerprinters.description", trim:"True") }
protections-panel-tracking-content = { COPY(from_path, "protections.trackingContent2.description", trim:"True") }
protections-panel-social-media-trackers = { COPY(from_path, "protections.socialMediaTrackers.description", trim:"True") }
protections-panel-content-blocking-manage-settings =
    .label = { COPY(from_path, "contentBlocking.manageSettings2.label", trim:"True") }
    .accesskey = { COPY(from_path, "contentBlocking.manageSettings2.accesskey", trim:"True") }
protections-panel-content-blocking-breakage-report-view =
    .title = { COPY(from_path, "contentBlocking.breakageReportView.title", trim:"True") }
protections-panel-content-blocking-breakage-report-view-collection-url = { COPY(from_path, "contentBlocking.breakageReportView.collection.url.label", trim:"True") }
protections-panel-content-blocking-breakage-report-view-collection-url-label =
    .aria-label = { COPY(from_path, "contentBlocking.breakageReportView.collection.url.label", trim:"True") }
protections-panel-content-blocking-breakage-report-view-collection-comments = { COPY(from_path, "contentBlocking.breakageReportView2.collection.comments.label", trim:"True") }
protections-panel-content-blocking-breakage-report-view-collection-comments-label =
    .aria-label = { COPY(from_path, "contentBlocking.breakageReportView2.collection.comments.label", trim:"True") }
protections-panel-content-blocking-breakage-report-view-cancel =
    .label = { COPY(from_path, "contentBlocking.breakageReportView.cancel.label", trim:"True") }
protections-panel-content-blocking-breakage-report-view-send-report =
    .label = { COPY(from_path, "contentBlocking.breakageReportView.sendReport.label", trim:"True") }
""", from_path="browser/chrome/browser/browser.dtd"))
    ctx.add_transforms(
    "browser/browser/protectionsPanel.ftl",
    "browser/browser/protectionsPanel.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("protections-panel-no-trackers-found"),
                value=REPLACE(
                    "browser/chrome/browser/browser.dtd",
                    "protections.noTrackersFound.description",
                    {
                        "&brandShortName;": TERM_REFERENCE("brand-short-name")
                    },
                    trim=True
                )
            ),
            FTL.Message(
                id=FTL.Identifier("protections-panel-content-blocking-breakage-report-view-description"),
                value=CONCAT(
                    REPLACE(
                        "browser/chrome/browser/browser.dtd",
                        "contentBlocking.breakageReportView3.description",
                        {
                            "&brandShortName;": TERM_REFERENCE("brand-short-name")
                        },
                        trim=True
                    ),
                    FTL.TextElement(' <label data-l10n-name="learn-more">'),
                    COPY(
                        "browser/chrome/browser/browser.dtd",
                        "contentBlocking.breakageReportView2.learnMore",
                        trim=True
                    ),
                    FTL.TextElement('</label>')
                )
            ),
        ]
    )

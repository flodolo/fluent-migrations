# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from, TERM_REFERENCE
from fluent.migrate import COPY, REPLACE


def migrate(ctx):
    """Bug 1622269 - Migrate cert error titles from netError.dtd to aboutCertError.ftl, part {index}"""
    ctx.add_transforms(
        "browser/browser/aboutCertError.ftl",
        "browser/browser/aboutCertError.ftl",
            transforms_from(
"""
generic-title = { COPY(from_path, "generic.title", trim:"True") }
captivePortal-title = { COPY(from_path, "captivePortal.title", trim:"True") }
dnsNotFound-title = { COPY(from_path, "dnsNotFound.title1", trim:"True") }
fileNotFound-title = { COPY(from_path, "fileNotFound.title", trim:"True") }
fileAccessDenied-title = { COPY(from_path, "fileAccessDenied.title", trim:"True") }
malformedURI-title = { COPY(from_path, "malformedURI.title1", trim:"True") }
unknownProtocolFound-title = { COPY(from_path, "unknownProtocolFound.title", trim:"True") }
connectionFailure-title = { COPY(from_path, "connectionFailure.title", trim:"True") }
netTimeout-title = { COPY(from_path, "netTimeout.title", trim:"True") }
redirectLoop-title = { COPY(from_path, "redirectLoop.title", trim:"True") }
unknownSocketType-title = { COPY(from_path, "unknownSocketType.title", trim:"True") }
netReset-title = { COPY(from_path, "netReset.title", trim:"True") }
notCached-title = { COPY(from_path, "notCached.title", trim:"True") }
netOffline-title = { COPY(from_path, "netOffline.title", trim:"True") }
netInterrupt-title = { COPY(from_path, "netInterrupt.title", trim:"True") }
deniedPortAccess-title = { COPY(from_path, "deniedPortAccess.title", trim:"True") }
proxyResolveFailure-title = { COPY(from_path, "proxyResolveFailure.title", trim:"True") }
proxyConnectFailure-title = { COPY(from_path, "proxyConnectFailure.title", trim:"True") }
contentEncodingError-title = { COPY(from_path, "contentEncodingError.title", trim:"True") }
unsafeContentType-title = { COPY(from_path, "unsafeContentType.title", trim:"True") }
nssFailure2-title = { COPY(from_path, "nssFailure2.title", trim:"True") }
nssBadCert-title = { COPY(from_path, "certerror.longpagetitle2", trim:"True") }
nssBadCert-sts-title = { COPY(from_path, "certerror.sts.longpagetitle", trim:"True") }
cspBlocked-title = { COPY(from_path, "cspBlocked.title", trim:"True") }
xfoBlocked-title = { COPY(from_path, "xfoBlocked.title", trim:"True") }
remoteXUL-title = { COPY(from_path, "remoteXUL.title", trim:"True") }
corruptedContentError-title = { COPY(from_path, "corruptedContentErrorv2.title", trim:"True") }
sslv3Used-title = { COPY(from_path, "sslv3Used.title", trim:"True") }
inadequateSecurityError-title = { COPY(from_path, "inadequateSecurityError.title", trim:"True") }
blockedByPolicy-title = { COPY(from_path, "blockedByPolicy.title", trim:"True") }
clockSkewError-title = { COPY(from_path, "clockSkewError.title", trim:"True") }
networkProtocolError-title = { COPY(from_path, "networkProtocolError.title", trim:"True") }
""", from_path="browser/chrome/overrides/netError.dtd"))
    ctx.add_transforms(
        "browser/browser/aboutCertError.ftl",
        "browser/browser/aboutCertError.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("certerror-mitm-title"),
                value=REPLACE(
                    "browser/chrome/overrides/netError.dtd",
                    "certerror.mitm.title",
                    {
                        "&brandShortName;": TERM_REFERENCE("brand-short-name"),
                    },
                    trim=True
                ),
            ),
        ]
    )

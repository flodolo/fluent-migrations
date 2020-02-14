# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from

def migrate(ctx):
    """Bug 1608215 - Migrate pippki to Fluent, part {index}."""

    ctx.add_transforms(
        "security/manager/security/pippki/pippki.ftl",
        "security/manager/security/pippki/pippki.ftl",
    transforms_from(
"""
password-quality-meter = { COPY(from_path, "setPassword.meter.label", trim:"True") }
change-password-window =
    .title = { COPY(from_path, "setPassword.title", trim:"True") }
change-password-token = { COPY(from_path, "setPassword.tokenName.label", trim:"True") }: { $tokenName }
change-password-old = { COPY(from_path, "setPassword.oldPassword.label", trim:"True") }
change-password-new = { COPY(from_path, "setPassword.newPassword.label", trim:"True") }
change-password-reenter = { COPY(from_path, "setPassword.reenterPassword.label", trim:"True") }
reset-password-window =
    .title = { COPY(from_path, "resetPassword.title", trim:"True") }
    .style = width: 40em
reset-password-button-label =
  .label = { COPY(from_path, "resetPasswordButtonLabel", trim:"True") }
reset-password-text = { COPY(from_path, "resetPassword.text", trim:"True") }
download-cert-window =
    .title = { COPY(from_path, "downloadCert.title", trim:"True") }
    .style = width: 46em
download-cert-message = { COPY(from_path, "downloadCert.message1", trim:"True") }
download-cert-trust-ssl =
    .label = { COPY(from_path, "downloadCert.trustSSL", trim:"True") }
download-cert-trust-email =
    .label = { COPY(from_path, "downloadCert.trustEmail", trim:"True") }
download-cert-message-desc = { COPY(from_path, "downloadCert.message3", trim:"True") }
download-cert-view-cert =
    .label = { COPY(from_path, "downloadCert.viewCert.label", trim:"True") }
download-cert-view-text = { COPY(from_path, "downloadCert.viewCert.text", trim:"True") }
client-auth-window =
    .title = { COPY(from_path, "clientAuthAsk.title", trim:"True") }
client-auth-site-description = { COPY(from_path, "clientAuthAsk.message1", trim:"True") }
client-auth-choose-cert = { COPY(from_path, "clientAuthAsk.message2", trim:"True") }
client-auth-cert-details = { COPY(from_path, "clientAuthAsk.message3", trim:"True") }
set-password-window =
    .title = { COPY(from_path, "pkcs12.setpassword.title", trim:"True") }
set-password-message = { COPY(from_path, "pkcs12.setpassword.message", trim:"True") }
set-password-backup-pw =
    .value = { COPY(from_path, "pkcs12.setpassword.label1", trim:"True") }
set-password-repeat-backup-pw =
    .value = { COPY(from_path, "pkcs12.setpassword.label2", trim:"True") }
set-password-reminder = { COPY(from_path, "pkcs12.setpassword.reminder", trim:"True") }
protected-auth-window =
    .title = { COPY(from_path, "protectedAuth.title", trim:"True") }
protected-auth-msg = { COPY(from_path, "protectedAuth.msg", trim:"True") }
protected-auth-token = { COPY(from_path, "protectedAuth.tokenName.label", trim:"True") }
""", from_path="security/manager/chrome/pippki/pippki.dtd"))

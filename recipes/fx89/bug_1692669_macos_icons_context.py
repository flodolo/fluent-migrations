# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
from fluent.migrate.helpers import transforms_from
from fluent.migrate import COPY_PATTERN


def migrate(ctx):
    """Bug 1692669: Replace icon group navigation on macOS page context menu, part {index}."""
    ctx.add_transforms(
        "browser/browser/browserContext.ftl",
        "browser/browser/browserContext.ftl",
        transforms_from(
            """
main-context-menu-back-mac =
    .label = { COPY_PATTERN(from_path, "main-context-menu-back-2.aria-label") }
    .accesskey = { COPY_PATTERN(from_path, "main-context-menu-back-2.accesskey") }

main-context-menu-forward-mac =
    .label = { COPY_PATTERN(from_path, "main-context-menu-forward-2.aria-label") }
    .accesskey = { COPY_PATTERN(from_path, "main-context-menu-forward-2.accesskey") }

main-context-menu-reload-mac =
    .label = { COPY_PATTERN(from_path, "main-context-menu-reload.aria-label") }
    .accesskey = { COPY_PATTERN(from_path, "main-context-menu-reload.accesskey") }

main-context-menu-stop-mac =
    .label = { COPY_PATTERN(from_path, "main-context-menu-stop.aria-label") }
    .accesskey = { COPY_PATTERN(from_path, "main-context-menu-stop.accesskey") }

""",
            from_path="browser/browser/browserContext.ftl",
        ),
    )

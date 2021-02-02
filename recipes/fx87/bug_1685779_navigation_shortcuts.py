# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
from fluent.migrate.helpers import transforms_from


def migrate(ctx):
    """Bug 1685779 - Add keyboard shortcut to Back/Forward button tooltip, part {index}."""
    ctx.add_transforms(
        "browser/browser/browserContext.ftl",
        "browser/browser/browserContext.ftl",
        transforms_from(
            """
main-context-menu-back-2 =
    .tooltiptext = { COPY_PATTERN(from_path, "main-context-menu-back.tooltiptext") } ({ $shortcut })
    .aria-label = { COPY_PATTERN(from_path, "main-context-menu-back.aria-label") }
    .accesskey = { COPY_PATTERN(from_path, "main-context-menu-back.accesskey") }
navbar-tooltip-back-2 =
    .value = { main-context-menu-back-2.tooltiptext }
toolbar-button-back-2 =
    .label = { main-context-menu-back-2.aria-label }

main-context-menu-forward-2 =
    .tooltiptext = { COPY_PATTERN(from_path, "main-context-menu-forward.tooltiptext") } ({ $shortcut })
    .aria-label = { COPY_PATTERN(from_path, "main-context-menu-forward.aria-label") }
    .accesskey = { COPY_PATTERN(from_path, "main-context-menu-forward.accesskey") }
navbar-tooltip-forward-2 =
    .value = { main-context-menu-forward-2.tooltiptext }
toolbar-button-forward-2 =
    .label = { main-context-menu-forward-2.aria-label }    
""",
            from_path="browser/browser/browserContext.ftl",
        ),
    )

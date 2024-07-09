# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from fluent.migrate.helpers import transforms_from


def migrate(ctx):
    """Bug 1904714 - rename Nightly Experiments to Firefox Labs, part {index}."""

    source = "browser/browser/preferences/preferences.ftl"
    target = "browser/browser/preferences/preferences.ftl"

    ctx.add_transforms(
        target,
        target,
        transforms_from(
            """
# This is necessary to let the migration run
pane-sync-title3 = {COPY_PATTERN(from_path, "pane-sync-title3")}
settings-pane-labs-title = { -firefoxlabs-brand-name }
settings-category-labs =
    .tooltiptext = { -firefoxlabs-brand-name }
""",
            from_path=source,
        ),
    )

    source = "toolkit/toolkit/branding/brandings.ftl"
    target = "toolkit/toolkit/branding/brandings.ftl"

    ctx.add_transforms(
        target,
        target,
        transforms_from(
            """
-firefoxlabs-brand-name = Firefox Labs
""",
            from_path=source,
        ),
    )

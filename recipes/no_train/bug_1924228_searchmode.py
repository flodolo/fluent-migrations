# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from fluent.migrate.helpers import transforms_from


def migrate(ctx):
    """Bug 1924228 - Localize Searchmode Switcher Button, part {index}."""

    source = "browser/browser/browser.ftl"
    target = source

    ctx.add_transforms(
        target,
        target,
        transforms_from(
            """
urlbar-searchmode-bookmarks =
    .label = {COPY_PATTERN(from_path, "urlbar-search-mode-bookmarks")}
urlbar-searchmode-tabs =
    .label = {COPY_PATTERN(from_path, "urlbar-search-mode-tabs")}
urlbar-searchmode-history =
    .label = {COPY_PATTERN(from_path, "urlbar-search-mode-history")}
urlbar-searchmode-actions =
    .label = {COPY_PATTERN(from_path, "urlbar-search-mode-actions")}
""",
            from_path=source,
        ),
    )

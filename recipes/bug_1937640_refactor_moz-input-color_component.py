# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from fluent.migrate.helpers import transforms_from


def migrate(ctx):
    """Bug 1937640 - Refactor moz-input-color component, part {index}."""

    source = "toolkit/toolkit/about/aboutReader.ftl"
    target = source

    ctx.add_transforms(
        target,
        target,
        transforms_from(
            """
about-reader-custom-colors-foreground2 =
    .label = {COPY_PATTERN(from_path, "about-reader-custom-colors-foreground")}
    .title = {COPY_PATTERN(from_path, "about-reader-custom-colors-foreground.title")}
about-reader-custom-colors-background2 =
    .label = {COPY_PATTERN(from_path, "about-reader-custom-colors-background")}
    .title = {COPY_PATTERN(from_path, "about-reader-custom-colors-background.title")}

about-reader-custom-colors-unvisited-links2 =
    .label = {COPY_PATTERN(from_path, "about-reader-custom-colors-unvisited-links")}
    .title = {COPY_PATTERN(from_path, "about-reader-custom-colors-unvisited-links.title")}
about-reader-custom-colors-visited-links2 =
    .label = {COPY_PATTERN(from_path, "about-reader-custom-colors-visited-links")}
    .title = {COPY_PATTERN(from_path, "about-reader-custom-colors-visited-links.title")}
about-reader-custom-colors-selection-highlight2 =
    .label = {COPY_PATTERN(from_path, "about-reader-custom-colors-selection-highlight")}
    .title = {COPY_PATTERN(from_path, "about-reader-custom-colors-selection-highlight.title")}
""",
            from_path=source,
        ),
    )

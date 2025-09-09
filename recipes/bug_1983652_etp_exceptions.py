# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from fluent.migrate.helpers import transforms_from


def migrate(ctx):
    """Bug 1983652 - Desktop UI updates for ETP Strict Exceptions Options, part {index}"""

    source = "browser/browser/preferences/preferences.ftl"
    target = source

    ctx.add_transforms(
        target,
        target,
        transforms_from(
            """
content-blocking-baseline-exceptions-3 =
    .label = { COPY_PATTERN(from_path, "content-blocking-baseline-label") }
    .description = { COPY_PATTERN(from_path, "content-blocking-baseline-exceptions-2.label") }

content-blocking-convenience-exceptions-3 =
    .label = { COPY_PATTERN(from_path, "content-blocking-convenience-label") }
    .description = { COPY_PATTERN(from_path, "content-blocking-convenience-exceptions-2.label") }
""",
            from_path=source,
        ),
    )

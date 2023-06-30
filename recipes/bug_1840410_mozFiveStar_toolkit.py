# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from fluent.migrate.helpers import transforms_from
from fluent.migrate import COPY_PATTERN


def migrate(ctx):
    """Bug 1840410 - Move mozFiveStar.ftl to toolkit, part {index}."""
    ctx.add_transforms(
        "toolkit/toolkit/global/mozFiveStar.ftl",
        "toolkit/toolkit/global/mozFiveStar.ftl",
        transforms_from(
            """
moz-five-star-rating =
  .title = {COPY_PATTERN(from_path, "moz-five-star-rating.title")}
    """,
            from_path="browser/browser/components/mozFiveStar.ftl",
        ),
    )

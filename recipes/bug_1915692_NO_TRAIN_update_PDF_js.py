# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from


def migrate(ctx):
    """Bug 1915692 - Update PDF.js to new version, part {index}"""

    translations_ftl = "toolkit/toolkit/pdfviewer/viewer.ftl"

    ctx.add_transforms(
        translations_ftl,
        translations_ftl,
        transforms_from(
            """
pdfjs-editor-resizer-top-left =
    .aria-label = {COPY_PATTERN(from_path, "pdfjs-editor-resizer-label-top-left")}
pdfjs-editor-resizer-top-middle =
    .aria-label = {COPY_PATTERN(from_path, "pdfjs-editor-resizer-label-top-middle")}
pdfjs-editor-resizer-top-right =
    .aria-label = {COPY_PATTERN(from_path, "pdfjs-editor-resizer-label-top-right")}
pdfjs-editor-resizer-middle-right =
    .aria-label = {COPY_PATTERN(from_path, "pdfjs-editor-resizer-label-middle-right")}
pdfjs-editor-resizer-bottom-right =
    .aria-label = {COPY_PATTERN(from_path, "pdfjs-editor-resizer-label-bottom-right")}
pdfjs-editor-resizer-bottom-middle =
    .aria-label = {COPY_PATTERN(from_path, "pdfjs-editor-resizer-label-bottom-middle")}
pdfjs-editor-resizer-bottom-left =
    .aria-label = {COPY_PATTERN(from_path, "pdfjs-editor-resizer-label-bottom-left")}
pdfjs-editor-resizer-middle-left =
    .aria-label = {COPY_PATTERN(from_path, "pdfjs-editor-resizer-label-middle-left")}
""",
            from_path=translations_ftl,
        ),
    )

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from fluent.migrate.helpers import transforms_from


def migrate(ctx):
    """1943635 - Set tooltips on color options in the tab group panel, part {index}."""

    source = "browser/browser/tabbrowser.ftl"
    target = source

    ctx.add_transforms(
        target,
        target,
        transforms_from(
            """
newtab-toast-thumbs-up-or-down2 =
    .message = {COPY_PATTERN(from_path, "newtab-toast-thumbs-up-or-down")}

tab-group-editor-color-selector2-blue = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-blue")}
  .title = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-blue")}
tab-group-editor-color-selector2-purple = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-purple")}
  .title = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-purple")}
tab-group-editor-color-selector2-cyan = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-cyan")}
  .title = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-cyan")}
tab-group-editor-color-selector2-orange = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-orange")}
  .title = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-orange")}
tab-group-editor-color-selector2-yellow = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-yellow")}
  .title = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-yellow")}
tab-group-editor-color-selector2-pink = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-pink")}
  .title = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-pink")}
tab-group-editor-color-selector2-green = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-green")}
  .title = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-green")}
tab-group-editor-color-selector2-gray = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-gray")}
  .title = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-gray")}
tab-group-editor-color-selector2-red = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-red")}
  .title = {COPY_PATTERN(from_path, "tab-group-editor-color-selector-red")}
""",
            from_path=source,
        ),
    )

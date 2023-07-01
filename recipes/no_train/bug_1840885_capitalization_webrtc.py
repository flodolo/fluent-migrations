# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.transforms import TransformPattern


class CAPITALIZE_FIRST_WORD(TransformPattern):
    # Capitalize the first character
    def visit_TextElement(self, node):
        node.value = node.value.capitalize()

        return node


def migrate(ctx):
    """Bug 1840885 - Normalize capitalization in about:webrtc, part {index}."""

    aboutwebrtc_ftl = "toolkit/toolkit/about/aboutWebrtc.ftl"

    ctx.add_transforms(
        aboutwebrtc_ftl,
        aboutwebrtc_ftl,
        transforms_from(
            """
about-webrtc-aec-logging-toggled-on-state-msg = { COPY_PATTERN(from_path, "about-webrtc-aec-logging-on-state-msg") }
    """,
            from_path=aboutwebrtc_ftl,
        ),
    )

    ctx.add_transforms(
        aboutwebrtc_ftl,
        aboutwebrtc_ftl,
        [
            FTL.Message(
                id=FTL.Identifier("about-webrtc-aec-logging-toggled-off-state-msg"),
                value=CAPITALIZE_FIRST_WORD(
                    aboutwebrtc_ftl, "about-webrtc-aec-logging-off-state-msg"
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("about-webrtc-log-section-show-msg"),
                value=CAPITALIZE_FIRST_WORD(
                    aboutwebrtc_ftl, "about-webrtc-log-show-msg"
                ),
                attributes=[
                    FTL.Attribute(
                        id=FTL.Identifier("title"),
                        value=CAPITALIZE_FIRST_WORD(
                            aboutwebrtc_ftl, "about-webrtc-log-show-msg.title"
                        ),
                    )
                ],
            ),
            FTL.Message(
                id=FTL.Identifier("about-webrtc-log-section-hide-msg"),
                value=CAPITALIZE_FIRST_WORD(
                    aboutwebrtc_ftl, "about-webrtc-log-hide-msg"
                ),
                attributes=[
                    FTL.Attribute(
                        id=FTL.Identifier("title"),
                        value=CAPITALIZE_FIRST_WORD(
                            aboutwebrtc_ftl, "about-webrtc-log-hide-msg.title"
                        ),
                    )
                ],
            ),
            FTL.Message(
                id=FTL.Identifier("about-webrtc-raw-cand-section-show-msg"),
                value=CAPITALIZE_FIRST_WORD(
                    aboutwebrtc_ftl, "about-webrtc-raw-cand-show-msg"
                ),
                attributes=[
                    FTL.Attribute(
                        id=FTL.Identifier("title"),
                        value=CAPITALIZE_FIRST_WORD(
                            aboutwebrtc_ftl, "about-webrtc-raw-cand-show-msg.title"
                        ),
                    )
                ],
            ),
            FTL.Message(
                id=FTL.Identifier("about-webrtc-raw-cand-section-hide-msg"),
                value=CAPITALIZE_FIRST_WORD(
                    aboutwebrtc_ftl, "about-webrtc-raw-cand-hide-msg"
                ),
                attributes=[
                    FTL.Attribute(
                        id=FTL.Identifier("title"),
                        value=CAPITALIZE_FIRST_WORD(
                            aboutwebrtc_ftl, "about-webrtc-raw-cand-hide-msg.title"
                        ),
                    )
                ],
            ),
            FTL.Message(
                id=FTL.Identifier("about-webrtc-fold-default-show-msg"),
                value=CAPITALIZE_FIRST_WORD(
                    aboutwebrtc_ftl, "about-webrtc-fold-show-msg"
                ),
                attributes=[
                    FTL.Attribute(
                        id=FTL.Identifier("title"),
                        value=CAPITALIZE_FIRST_WORD(
                            aboutwebrtc_ftl, "about-webrtc-fold-show-msg.title"
                        ),
                    )
                ],
            ),
            FTL.Message(
                id=FTL.Identifier("about-webrtc-fold-default-hide-msg"),
                value=CAPITALIZE_FIRST_WORD(
                    aboutwebrtc_ftl, "about-webrtc-fold-hide-msg"
                ),
                attributes=[
                    FTL.Attribute(
                        id=FTL.Identifier("title"),
                        value=CAPITALIZE_FIRST_WORD(
                            aboutwebrtc_ftl, "about-webrtc-fold-hide-msg.title"
                        ),
                    )
                ],
            ),
            FTL.Message(
                id=FTL.Identifier("about-webrtc-save-page-complete-msg"),
                value=CAPITALIZE_FIRST_WORD(
                    aboutwebrtc_ftl, "about-webrtc-save-page-msg"
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("about-webrtc-debug-mode-toggled-off-state-msg"),
                value=CAPITALIZE_FIRST_WORD(
                    aboutwebrtc_ftl, "about-webrtc-debug-mode-off-state-msg"
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("about-webrtc-debug-mode-toggled-on-state-msg"),
                value=CAPITALIZE_FIRST_WORD(
                    aboutwebrtc_ftl, "about-webrtc-debug-mode-on-state-msg"
                ),
            ),
        ],
    )

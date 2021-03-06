# coding=utf8

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import MESSAGE_REFERENCE, EXTERNAL_ARGUMENT
from fluent.migrate.transforms import REPLACE
from fluent.migrate import COPY


def migrate(ctx):
    """Bug 1415733 - Migrate the "Search" section of Preferences to the new Localization API, part {index}"""

    ctx.add_transforms(
        'browser/browser/preferences/preferences.ftl',
        'browser/browser/preferences/preferences.ftl',
        [
            FTL.Message(
                id=FTL.Identifier('search-bar-header'),
                value=COPY(
                    'browser/chrome/browser/preferences/search.dtd',
                    'searchBar.label'
                )
            ),
            FTL.Message(
                id=FTL.Identifier('search-bar-hidden'),
                attributes=[
                    FTL.Attribute(
                        FTL.Identifier('label'),
                        COPY(
                            'browser/chrome/browser/preferences/search.dtd',
                            'searchBar.hidden.label'
                        )
                    )
                ]
            ),
            FTL.Message(
                id=FTL.Identifier('search-bar-shown'),
                attributes=[
                    FTL.Attribute(
                        FTL.Identifier('label'),
                        COPY(
                            'browser/chrome/browser/preferences/search.dtd',
                            'searchBar.shown.label'
                        )
                    )
                ]
            ),
            FTL.Message(
                id=FTL.Identifier('search-engine-default-header'),
                value=COPY(
                    'browser/chrome/browser/preferences/search.dtd',
                    'defaultSearchEngine.label'
                )
            ),
            FTL.Message(
                id=FTL.Identifier('search-engine-default-desc'),
                value=COPY(
                    'browser/chrome/browser/preferences/search.dtd',
                    'chooseYourDefaultSearchEngine2.label'
                )
            ),
            FTL.Message(
                id=FTL.Identifier('search-suggestions-option'),
                attributes=[
                    FTL.Attribute(
                        FTL.Identifier('label'),
                        COPY(
                            'browser/chrome/browser/preferences/search.dtd',
                            'provideSearchSuggestions.label'
                        )
                    ),
                    FTL.Attribute(
                        FTL.Identifier('accesskey'),
                        COPY(
                            'browser/chrome/browser/preferences/search.dtd',
                            'provideSearchSuggestions.accesskey'
                        )
                    )
                ]
            ),
            FTL.Message(
                id=FTL.Identifier('search-show-suggestions-url-bar-option'),
                attributes=[
                    FTL.Attribute(
                        FTL.Identifier('label'),
                        COPY(
                            'browser/chrome/browser/preferences/search.dtd',
                            'showURLBarSuggestions2.label'
                        )
                    ),
                    FTL.Attribute(
                        FTL.Identifier('accesskey'),
                        COPY(
                            'browser/chrome/browser/preferences/search.dtd',
                            'showURLBarSuggestions2.accesskey'
                        )
                    )
                ]
            ),
            FTL.Message(
                id=FTL.Identifier('search-show-suggestions-above-history-option'),
                attributes=[
                    FTL.Attribute(
                        FTL.Identifier('label'),
                        COPY(
                            'browser/chrome/browser/preferences/search.dtd',
                            'showSearchSuggestionsAboveHistory.label'
                        )
                    ),
                ]
            ),
            FTL.Message(
                id=FTL.Identifier('search-suggestions-cant-show'),
                value=REPLACE(
                    'browser/chrome/browser/preferences/search.dtd',
                    'urlBarSuggestionsPermanentPB.label',
                    {
                        '&brandShortName;': MESSAGE_REFERENCE(
                            '-brand-short-name'
                        )
                    }
                ),
            ),
            FTL.Message(
                id=FTL.Identifier('search-one-click-header'),
                value=COPY(
                    'browser/chrome/browser/preferences/search.dtd',
                    'oneClickSearchEngines.label'
                )
            ),
            FTL.Message(
                id=FTL.Identifier('search-one-click-desc'),
                value=COPY(
                    'browser/chrome/browser/preferences/search.dtd',
                    'chooseWhichOneToDisplay2.label'
                )
            ),
            FTL.Message(
                id=FTL.Identifier('search-choose-engine-column'),
                attributes=[
                    FTL.Attribute(
                        FTL.Identifier('label'),
                        COPY(
                            'browser/chrome/browser/preferences/search.dtd',
                            'engineNameColumn.label'
                        )
                    ),
                ]
            ),
            FTL.Message(
                id=FTL.Identifier('search-choose-keyword-column'),
                attributes=[
                    FTL.Attribute(
                        FTL.Identifier('label'),
                        COPY(
                            'browser/chrome/browser/preferences/search.dtd',
                            'engineKeywordColumn.label'
                        )
                    ),
                ]
            ),
            FTL.Message(
                id=FTL.Identifier('search-restore-default'),
                attributes=[
                    FTL.Attribute(
                        FTL.Identifier('label'),
                        COPY(
                            'browser/chrome/browser/preferences/search.dtd',
                            'restoreDefaultSearchEngines.label'
                        )
                    ),
                    FTL.Attribute(
                        FTL.Identifier('accesskey'),
                        COPY(
                            'browser/chrome/browser/preferences/search.dtd',
                            'restoreDefaultSearchEngines.accesskey'
                        )
                    )
                ]
            ),
            FTL.Message(
                id=FTL.Identifier('search-remove-engine'),
                attributes=[
                    FTL.Attribute(
                        FTL.Identifier('label'),
                        COPY(
                            'browser/chrome/browser/preferences/search.dtd',
                            'removeEngine.label'
                        )
                    ),
                    FTL.Attribute(
                        FTL.Identifier('accesskey'),
                        COPY(
                            'browser/chrome/browser/preferences/search.dtd',
                            'removeEngine.accesskey'
                        )
                    )
                ]
            ),
            FTL.Message(
                id=FTL.Identifier('search-find-more-link'),
                value=COPY(
                    'browser/chrome/browser/preferences/search.dtd',
                    'findMoreSearchEngines.label'
                )
            ),
            FTL.Message(
                id=FTL.Identifier('search-keyword-warning-title'),
                value=COPY(
                    'browser/chrome/browser/engineManager.properties',
                    'duplicateTitle'
                )
            ),
            FTL.Message(
                id=FTL.Identifier('search-keyword-warning-engine'),
                value=REPLACE(
                    'browser/chrome/browser/engineManager.properties',
                    'duplicateEngineMsg',
                    {
                        '%S': EXTERNAL_ARGUMENT(
                            'name'
                        )
                    }
                ),
            ),
            FTL.Message(
                id=FTL.Identifier('search-keyword-warning-bookmark'),
                value=COPY(
                    'browser/chrome/browser/engineManager.properties',
                    'duplicateBookmarkMsg'
                )
            ),
        ]
    )

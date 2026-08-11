"""UI strings per build flavour.

The two language variants used to be forked copies of the whole template plus a
forked Dockerfile. The entire difference is the handful of strings below.
"""

STRINGS: dict[str, dict[str, str]] = {
    "en": {
        "lang": "en",
        "title": "Simple Calendar",
        "logo_prefix": "Simple",
        "logo_suffix": "Calendar",
        "search_placeholder": "Find..",
        "search_label": "Search events",
        "location": "Location",
        "description": "Description",
        "all_day": "All day",
        "empty": "No upcoming events.",
    },
    "ctt": {
        "lang": "cs",
        "title": "Tech Scenar",
        "logo_prefix": "Tech",
        "logo_suffix": "Scénář",
        "search_placeholder": "Hledat..",
        "search_label": "Hledat události",
        "location": "Lokace",
        "description": "Popis",
        "all_day": "Celý den",
        "empty": "Žádné nadcházející události.",
    },
}

DEFAULT_LANG = "en"


def get_strings(lang: str) -> dict[str, str]:
    return STRINGS.get(lang, STRINGS[DEFAULT_LANG])

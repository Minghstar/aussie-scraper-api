def detect_platform(url: str, html: str) -> str:
    if "sidearm" in url or "sidearm-roster-player" in html:
        return "sidearm"
    elif "gostanford.com" in url or ("roster-card-item" in html and "roster-player-card-profile-field" in html):
        return "stanford"
    elif "<ul" in html and "li" in html:
        return "list"
    elif "athletics" in url:
        return "custom"
    else:
        return "unknown"



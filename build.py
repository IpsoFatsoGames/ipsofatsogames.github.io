"""Builds the site's pages from games.json (the catalogue the games read too) and site.json (the page text).

    python build.py

Writes index.html and <game>/index.html for every game in games.json, and puts the shared header and footer into
privacy.html between its site:header / site:footer markers (its text is written by hand). A game with "live": true
gets its store button, banner and screenshots; the others show as coming soon. Standard library only.
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PLAY = "https://play.google.com/store/apps/details?id={package}&utm_source=website&utm_medium={medium}"


def main():
    catalogue = json.loads((ROOT / "games.json").read_text(encoding="utf-8"))
    site = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
    studio, pages = site["studio"], site["pages"]
    games = catalogue["games"]
    for game in games:
        game["page"] = pages.get(game["id"], {})
        game["icon_path"] = (game.get("icon") or f"{game['id']}/icon.png").split("?")[0]
        game["banner_path"] = (game.get("banner") or f"{game['id']}/feature.png").split("?")[0]

    live = [g for g in games if g.get("live")]
    soon = [g for g in games if not g.get("live")]
    write(ROOT / "index.html", home(studio, live, soon))
    for game in games:
        write(ROOT / game["id"] / "index.html", game_page(studio, game))
    inject(ROOT / "privacy.html", studio, "")
    print(f"Built index.html and {len(games)} game pages ({len(live)} live); privacy.html header and footer.")


# ---------------------------------------------------------------- Pages

def home(studio: dict, live: list[dict], soon: list[dict]) -> str:
    out = [hero(studio, live + soon)]
    if live:
        out.append('<section class="section" id="games"><h2 class="section-title">Out now</h2>')
        out.extend(featured(g) for g in live)
        out.append("</section>")
    if soon:
        out.append('<section class="section"><h2 class="section-title">Coming soon</h2><ul class="grid">')
        out.extend(card(g) for g in soon)
        out.append("</ul></section>")
    description = f"{studio['name']}: {studio['headline']} {studio['intro']}"
    return document(studio, studio["name"], description, "", "\n".join(out),
                    image=(live[0]["banner_path"] if live else None))


def hero(studio: dict, games: list[dict]) -> str:
    """The headline (its "highlight" words in the brand gradient) beside a tilted wall of the games' icons."""
    headline = escape(studio["headline"])
    highlight = escape(studio.get("highlight", ""))
    if highlight and highlight in headline:
        headline = headline.replace(highlight, f'<span class="grad">{highlight}</span>', 1)
    icons = "".join(f'<img src="{escape(g["icon_path"])}" alt="" width="120" height="120">' for g in games[:9])
    return (f'<section class="hero"><div class="hero-text"><h1>{headline}</h1>'
            f'<p class="lead">{escape(studio["intro"])}</p>'
            f'<p><a class="button ghost" href="#games">See our games</a></p></div>'
            f'<div class="hero-art" aria-hidden="true">{icons}</div></section>')


def featured(game: dict) -> str:
    gid, page = game["id"], game["page"]
    shots = "".join(f'<img src="{gid}/{escape(s)}" alt="{escape(game["name"])} screenshot {i + 1}" loading="lazy" '
                    f'width="270" height="480">' for i, s in enumerate(page.get("screenshots", [])[:5]))
    text = escape((page.get("description") or [game.get("tagline", "")])[-1])
    return (f'<article class="feature">'
            f'<a href="{gid}/"><img class="banner" src="{escape(game["banner_path"])}" alt="" width="1024" height="500"></a>'
            f'<div class="feature-body"><div class="title-row"><img class="icon" src="{escape(game["icon_path"])}" alt="" '
            f'width="96" height="96"><div><h3><a href="{gid}/">{escape(game["name"])}</a></h3>'
            f'<p class="tagline">{escape(game.get("tagline", ""))}</p></div></div>'
            f'<p>{text}</p><p class="actions">{store_button(game, "home", "")}'
            f'<a class="button ghost" href="{gid}/">More about {escape(game["name"])}</a></p></div>'
            + (f'<div class="shots">{shots}</div>' if shots else "") + "</article>")


def card(game: dict) -> str:
    gid = game["id"]
    text = escape((game["page"].get("description") or [game.get("tagline", "")])[0])
    return (f'<li class="card"><a href="{gid}/"><img class="icon" src="{escape(game["icon_path"])}" alt="" width="72" '
            f'height="72"><span class="chip">Coming soon</span><h3>{escape(game["name"])}</h3>'
            f'<p>{text}</p></a></li>')


def game_page(studio: dict, game: dict) -> str:
    page = game["page"]
    paragraphs = "".join(f"<p>{escape(p)}</p>" for p in page.get("description") or [game.get("tagline", "")])
    features = page.get("features", [])
    feature_list = ("<h2>Features</h2><ul class=\"ticks\">" + "".join(f"<li>{escape(f)}</li>" for f in features)
                    + "</ul>") if features else ""
    shots = page.get("screenshots", []) if game.get("live") else []
    gallery = ('<h2>Screenshots</h2><div class="shots large">' + "".join(
        f'<img src="{escape(s)}" alt="{escape(game["name"])} screenshot {i + 1}" loading="lazy" width="270" height="480">'
        for i, s in enumerate(shots)) + "</div>") if shots else ""
    action = store_button(game, "game_page", "../") if game.get("live") else '<span class="chip big">Coming soon to Google Play</span>'
    banner = (f'<img class="banner" src="../{escape(game["banner_path"])}" alt="" width="1024" height="500">'
              if (ROOT / game["banner_path"]).exists() else "")
    # The tagline under the title only when the description doesn't already open with it.
    tagline = game.get("tagline", "")
    first = (page.get("description") or [""])[0]
    if tagline and first.startswith(tagline.rstrip(".")):
        tagline = ""
    body = (f'<article class="game">{banner}<div class="title-row big"><img class="icon" src="../{escape(game["icon_path"])}" '
            f'alt="{escape(game["name"])} icon" width="128" height="128"><div><h1>{escape(game["name"])}</h1>'
            f'<p class="tagline">{escape(tagline)}</p><p class="actions">{action}</p></div></div>'
            f'{paragraphs}{feature_list}{gallery}</article>')
    description = " ".join(page.get("description") or [game.get("tagline", "")])
    return document(studio, f"{game['name']} · {studio['name']}", description, "../", body,
                    image=(game["banner_path"] if game.get("live") else None))


def store_button(game: dict, medium: str, up: str) -> str:
    """Google's own "Get it on Google Play" badge (img/google-play-badge.png, unaltered, as their badge rules ask)."""
    url = PLAY.format(package=game["android"], medium=medium)
    return (f'<a class="store-badge" href="{escape(url)}"><img src="{up}img/google-play-badge.png" '
            f'alt="Get it on Google Play" width="646" height="250"></a>')


# ---------------------------------------------------------------- Frame

def header(studio: dict, up: str) -> str:
    return (f'<header class="top"><div class="wrap"><a class="brand" href="{up or "./"}">Ipso<span>Fatso</span>Games</a>'
            f'<nav><a href="{up or "./"}#games">Games</a><a href="{up}privacy.html">Privacy</a>'
            f'<a href="mailto:{studio["email"]}">Contact</a></nav></div></header>')


def footer(studio: dict, up: str) -> str:
    return (f'<footer class="bottom"><div class="wrap"><p>© {escape(studio["name"])} · Berlin</p>'
            f'<p><a href="{up}privacy.html">Privacy policy</a> · '
            f'<a href="mailto:{studio["email"]}">{studio["email"]}</a></p>'
            f'<p class="legal">Google Play and the Google Play logo are trademarks of Google LLC.</p></div></footer>')


def document(studio: dict, title: str, description: str, up: str, body: str, image: str | None) -> str:
    meta = [f'<meta name="description" content="{escape(description)}">',
            f'<meta property="og:title" content="{escape(title)}">',
            f'<meta property="og:description" content="{escape(description)}">']
    if image:
        meta.append(f'<meta property="og:image" content="{studio["url"]}{escape(image)}">')
    return "\n".join([
        "<!doctype html>", '<html lang="en">', "<head>", '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">', f"<title>{escape(title)}</title>",
        *meta, f'<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">',
        f'<link rel="stylesheet" href="{up}style.css">', "</head>", "<body>",
        "<!-- Built by build.py from games.json and site.json: edit those, not this file. -->",
        header(studio, up), f'<main class="wrap">{body}</main>', footer(studio, up), "</body>", "</html>", ""])


def inject(path: Path, studio: dict, up: str):
    """Puts the shared header and footer into a hand-written page between its marker comments."""
    text = path.read_text(encoding="utf-8")
    for name, part in (("header", header(studio, up)), ("footer", footer(studio, up))):
        start, end = f"<!-- site:{name} -->", f"<!-- /site:{name} -->"
        a, b = text.index(start) + len(start), text.index(end)
        text = text[:a] + "\n" + part + "\n" + text[b:]
    path.write_text(text, encoding="utf-8", newline="\n")


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

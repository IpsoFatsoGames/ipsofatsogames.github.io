# IpsoFatsoGames website

Static site: studio page, one page per game, the shared privacy policy and `app-ads.txt`.

## Hosting

Served by GitHub Pages as the org site of `IpsoFatsoGames` (repo
`IpsoFatsoGames/ipsofatsogames.github.io`, branch `main`, folder `/`):

- Site: https://ipsofatsogames.github.io/
- Privacy policy: https://ipsofatsogames.github.io/privacy.html
- Hexa Tower: https://ipsofatsogames.github.io/hexatower/
- app-ads.txt: https://ipsofatsogames.github.io/app-ads.txt

Pushing to `main` redeploys. Keep links relative (no leading `/`) so the site also works if it
is ever served from a subpath.

## app-ads.txt

Ad networks read `app-ads.txt` from the root of the domain given as the Play Store listing's
"Website", so set that to `https://ipsofatsogames.github.io/`. `github.io` is on the Public
Suffix List, so this org site counts as its own domain. A custom domain can be added later
(Settings > Pages > Custom domain); GitHub then redirects the `github.io` URLs to it.

## Before launch

- An Impressum page (a German site generally needs one; the privacy policy already has the
  controller's name and postal address for GDPR Art. 13).
- `app-ads.txt`: refresh from the Unity dashboard (Monetization > Settings > Organization >
  App-ads.txt) and the ironSource reseller list when the dashboard reports missing sellers.

## games.json (cross-promotion)

Every game reads `games.json` to promote the studio's other games: house ads, the More Games list
and store links (the crosspromo package in `_studio/kit`; see `_studio/README.md`). Each entry has an
`id`, `name`, a short `tagline`, the Play package (`android`), the App Store app id (`ios`, empty
until then), an `icon` (square) and a `banner` (the 1024x500 feature graphic as `<game>/feature.png`),
both relative to this file, a `weight`, and `live`. Only `live` games are shown, so set it to
`true` once the store page is public. The top-level numbers tune the house ads for all games. Games
cache images by URL, so give a changed image a new name (or add `?v=2`). After editing, re-bundle
the copy each game ships with: `ipso add <game> crosspromo --apply`.

## Pages (build.py)

`index.html` and every `<game>/index.html` are generated: edit `games.json` (name, tagline, store
package, icon, banner, `live`) and `site.json` (the studio text, and per game its description,
features and screenshots), then run `python build.py` (standard library only) and commit the result.
A `live` game gets Google's "Get it on Google Play" badge (`img/google-play-badge.png`, downloaded unaltered
from Google's badge page; their rules want it unmodified and the trademark line the footer carries; links tagged
`utm_source=website`), a featured
card on the home page with its first screenshots, and its gallery; the others show as coming soon.
`privacy.html` is written by hand; `build.py` only puts the shared header and footer between its
`site:header` / `site:footer` markers. Styles are in `style.css`.

Screenshots go in `<game>/screens/` as 540x960 WebP (the store's 1080x1920 PNGs halved, quality 82,
about 25 KB each), listed in `site.json`.

## Adding a game

Make `<game>/` with `icon.png` (512x512) and `feature.png` (the 1024x500 feature graphic), add the
game to `games.json` and `site.json`, and run `python build.py`. When it goes live, set `"live": true`,
add its screenshots, and build again.

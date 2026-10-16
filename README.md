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

## Adding a game

Copy `hexatower/` to `<game>/`, swap the icon and text, and add it to `index.html`. Copy its feature
graphic to `<game>/feature.png` and add it to `games.json`.

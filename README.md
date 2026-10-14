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

- `privacy.html`: replace `[postal address]` (GDPR Art. 13 needs the controller's identity and
  contact; a German site generally also needs an Impressum).
- `app-ads.txt`: refresh from the Unity dashboard (Monetization > Settings > Organization >
  App-ads.txt) and the ironSource reseller list when the dashboard reports missing sellers.

## Adding a game

Copy `hexatower/` to `<game>/`, swap the icon and text, and add it to `index.html`.

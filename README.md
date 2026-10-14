# IpsoFatsoGames website

Static site: studio page, one page per game, the shared privacy policy and `app-ads.txt`.

## Hosting

Served by GitHub Pages from this repo (`BraveSirAndrew/IpsoFatsoGames`, branch `main`, folder `/`):

- Site: https://bravesirandrew.github.io/IpsoFatsoGames/
- Privacy policy: https://bravesirandrew.github.io/IpsoFatsoGames/privacy.html
- Hexa Tower: https://bravesirandrew.github.io/IpsoFatsoGames/hexatower/

Pushing to `main` redeploys. The site lives under a subpath, so keep every link relative
(no leading `/`).

## app-ads.txt

Ad networks only read `app-ads.txt` from the root of the domain given as the Play Store
listing's "Website" (`https://<domain>/app-ads.txt`). At the current subpath it is not valid.
To make it count, either:

- add a custom domain (Settings > Pages > Custom domain) and use it as the store website, or
- host the site as a user/org site, e.g. a repo named `<name>.github.io`.

## Before launch

- `privacy.html`: replace `[postal address]` (GDPR Art. 13 needs the controller's identity and
  contact; a German site generally also needs an Impressum).
- `app-ads.txt`: add the LevelPlay lines.

## Adding a game

Copy `hexatower/` to `<game>/`, swap the icon and text, and add it to `index.html`.

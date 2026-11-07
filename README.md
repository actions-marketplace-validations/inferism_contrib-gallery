# contrib-gallery

Gallery of GitHub contribution graph styles with copy-paste snippets.

Pick a style, copy two snippets, and a GitHub Action keeps the chart on your profile up to date every day. The gallery page shows every style on made-up sample data, in a dark terminal and space look.

**Gallery:** https://inferism.github.io/contrib-gallery/

## Use a style

Works in any repo, for example your profile repo (the one named after your username).

1. Copy the workflow from the gallery card to `.github/workflows/contrib-chart.yml`. It looks like this:

   ```yaml
   name: Contribution chart
   on:
     schedule:
       - cron: "0 18 * * *"
     workflow_dispatch:

   permissions:
     contents: write

   jobs:
     chart:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: inferism/contrib-gallery@main
           with:
             style: spiral-galaxy
         - name: Commit and push
           run: |
             git config user.name "${{ github.repository_owner }}"
             git config user.email "${{ github.repository_owner_id }}+${{ github.repository_owner }}@users.noreply.github.com"
             git add -A
             git commit -m "chore: update contribution chart" || exit 0
             git push
   ```

2. Add the image to your README:

   ```html
   <p align="center">
     <img src="./contrib-charts/spiral-galaxy.svg" alt="My contribution chart" width="100%" />
   </p>
   ```

3. In your repo, open **Settings, Actions, General, Workflow permissions** and choose **Read and write permissions**. Then open the **Actions** tab, pick the workflow, and click **Run workflow** once.

Action inputs: `style` (required), `theme` (default: `mono`), `accent` (custom color like `#ff66aa`, overrides `theme`), `username` (default: the repository owner), `token` (default: the workflow token), `output-dir` (default: `contrib-charts`).

## Themes

Every style comes in six color themes: `mono` (default), `ice`, `ember`, `matrix`, `sakura` and `violet`. Pick one with the theme swatches on the gallery page, and the snippet updates to include it:

```yaml
- uses: inferism/contrib-gallery@main
  with:
    style: spiral-galaxy
    theme: ice
```

Want your own color? Use `accent: "#ff66aa"` instead of `theme`.

## Make it fit your profile

The default look is a dark terminal panel with a border and corner brackets. If your README looks different, change it with these inputs:

| Input | Values | What it does |
|---|---|---|
| `mode` | `dark` (default), `light` | `light` draws dark ink, for light READMEs |
| `frame` | `terminal` (default), `none` | `none` drops the border, corner brackets and dots, and matches GitHub's own page color so the chart blends in |
| `header` | `show` (default), `hide` | `hide` removes the title lines at the top |

```yaml
- uses: inferism/contrib-gallery@main
  with:
    style: skyline
    mode: light
    frame: none
    header: hide
```

The gallery previews show the default look. These options are applied when your workflow generates the chart.

## Styles ready to use

| Style | Name to use | What it shows |
|---|---|---|
| Spiral galaxy | `spiral-galaxy` | One star per day on a spiral arm, brighter when busier |
| Htop monitor | `htop-monitor` | Monthly bars with percentages, like a system monitor |
| Constellation | `constellation` | Active days as stars, joined into constellations |
| Ridgeline | `ridgeline` | One jagged line per month, stacked on black |
| Vinyl record | `vinyl-record` | One ring of grooves per month, every active day a blip |
| Piano roll | `piano-roll` | Weekdays as piano keys, active days as notes |
| Tree | `tree-growth` | A branch for every active week, a leaf for every active day |
| Ocean waves | `ocean-waves` | One wave per month, stacked in the sea |
| Space invaders | `space-invaders` | Active days as invaders, busier days bigger |
| RPG status | `rpg-status` | A character sheet: level, XP and stat bars |
| 3D skyline | `skyline` | A 3D city in space, one building per day |
| Terrain mesh | `terrain-mesh` | A wireframe landscape where height is how busy you were |

The gallery also previews many more styles (games, 3D, music and others). They are preview only for now, and generators for them are coming.

## Things to know

- **Last 12 months only.** The charts use the same window as GitHub's own graph.
- **Private contributions.** The default workflow token can only see public activity. To include private contributions, pass a personal access token with the `token` input, stored as a repository secret.
- **Commits as you.** The workflow commits with your GitHub no-reply address, so the daily update shows as you. Each daily run adds a commit.
- **No outside services.** Everything is generated inside your own workflow run.

## Run it yourself

Needs Python 3. Real data also needs the [GitHub CLI](https://cli.github.com) signed in.

```bash
python generator/generate.py --list
python generator/generate.py --style spiral-galaxy --sample --out charts                   # made-up data
python generator/generate.py --style spiral-galaxy --theme ice --username YOU --out charts  # your data
```

## Add a style

1. Create `generator/styles/your_style.py` with a `render(days)` function. `days` is a list of `{"date": "YYYY-MM-DD", "count": n}`. Return a dict with `w`, `h`, `body`, `defs`, `title`, `cmd` and `aria`. The existing styles are good examples.
2. Register it in `generator/styles/__init__.py`.
3. Run `python generator/build_samples.py` to rebuild `samples/<theme>/<style>.svg` for every theme, then add the style's id and image height to `READY` in `gallery.js`.

## License

MIT

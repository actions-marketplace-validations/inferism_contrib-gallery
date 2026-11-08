# contrib-gallery

Gallery of GitHub contribution graph styles with copy-paste snippets.

Pick a style, copy two snippets, and a GitHub Action keeps the chart on your profile up to date every day.

**Gallery:** https://inferism.github.io/contrib-gallery/

## Fits your profile, whatever it looks like

> **Not everyone has a dark GitHub, and not every README looks the same.** So a chart comes plain by default, and you choose everything else.

**By default a chart is just the chart:** no frame, no title, no extras, and it follows GitHub's light or dark setting. Change the look with these inputs:

| Input | Values | What it does |
|---|---|---|
| `mode` | `auto` (default), `dark`, `light` | `auto` follows the viewer's light or dark setting. `light` draws dark ink for light READMEs, `dark` draws light ink for dark ones. |
| `frame` | `none` (default), `simple`, `brackets`, `terminal` | The frame around the chart. `simple` is a thin border, `brackets` is corner brackets only, `terminal` is a border with corner brackets and a dotted background. |
| `header` | `none` (default), `title`, `terminal` | The text above the chart. `title` is one line with the style's name, `terminal` adds a command line under it. |
| `details` | `hide` (default), `show` | `show` adds the decorations (stars, a planet, a score) and a stats line under the chart. |
| `background` | a color like `"#0a0a0a"` | The page color behind the chart, for READMEs with a custom background. |
| `theme` | `mono` (default), `ice`, `ember`, `matrix`, `sakura`, `violet` | The accent color. |
| `accent` | a color like `"#ff66aa"` | Your own accent color. Overrides `theme`. |

The plain default:

```yaml
- uses: inferism/contrib-gallery@main
  with:
    style: skyline
```

The full terminal look, like the profile this gallery came from:

```yaml
- uses: inferism/contrib-gallery@main
  with:
    style: skyline
    frame: terminal
    header: terminal
    details: show
    mode: dark
```

The gallery previews show the plain default on a dark page. These options are applied when your workflow generates the chart.

`mode: auto` follows the viewer's browser or system setting. If someone's GitHub theme differs from their system setting, the chart can mismatch, so choose `dark` or `light` yourself if you want a fixed look.

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

Other inputs: `username` (default: the repository owner), `token` (default: the workflow token), `output-dir` (default: `contrib-charts`).

## Styles ready to use

<!-- styles:start -->
| Style | Name to use | What it shows |
|---|---|---|
| Spiral galaxy | `spiral-galaxy` | Your year winds out from the center along a spiral arm. Brighter stars are busier days. |
| Constellation | `constellation` | Active days are stars. Close days connect into constellations. |
| Htop monitor | `htop-monitor` | Months as system-monitor bars with percentages. Shows how busy each month was. |
| Ridgeline mountains | `ridgeline` | One jagged line per month stacked on black, like the Unknown Pleasures album cover. Peaks are busy days. |
| Vinyl record | `vinyl-record` | A record with one ring of grooves per month. Every active day is a blip along its ring. |
| Piano roll | `piano-roll` | Weekdays are piano keys, weeks run left to right, and every active day is a note. Longer notes are busier days. |
| Tree | `tree-growth` | A tree grows a branch for every active week. Longer branches are busier weeks, and each leaf is an active day. |
| Ocean waves | `ocean-waves` | One wave per month, stacked in the sea. Taller swells are busier days. |
| Space invaders | `space-invaders` | Every active day is an invader. Busier days are bigger, brighter invaders. |
| RPG status | `rpg-status` | A character sheet built from your year: level, XP and stat bars like HP and mana. |
| 3D skyline | `skyline` | A 3D city floating in space. One building per day, taller and brighter when you were busier. |
| Terrain mesh | `terrain-mesh` | A wireframe landscape. Weeks run left to right, weekdays go into the distance, and height is how busy you were. |
| Dig site | `dig-site` | A cross-section of the ground. Every active week digs a shaft, deeper when busier, with a gem at the bottom. |
| Obby course | `obby-course` | An obstacle course of floating platforms, one for each active week. Higher platforms are busier weeks. |
| Block stack | `block-stack` | A falling-block puzzle. One column per month, stacked as high as the month was busy. |
| Farm plots | `farm-plots` | A farm where every day is a plot. Busy days grow from a seed to a ripe crop. |
| Test runner | `test-runner` | Test-runner output: a row per month, a dot for every active day and a dash for every quiet one. |
| Commit log | `commit-log` | Your ten busiest days, sorted like terminal output with a bar for each. |
| Aurora | `aurora` | Northern lights: curtains of light that swell in the weeks you were busy. |
| Black hole | `black-hole` | Your days orbit a black hole on an accretion disk, the newest days closest to the edge. |
| Activity rings | `activity-rings` | Three rings: this week, this month against your best, and your streak against your longest. |
| Year sparkline | `year-sparkline` | The whole year as one smooth line, with your busiest week and today marked. |
| Orbit rings | `orbit-rings` | One ring per month. The dots on a ring are that month's days. |
| Terminal heatmap | `terminal-heatmap` | The usual grid, but drawn with text characters like command output. |
| Radial bars | `radial-bars` | Every day is a spoke around a circle, longer for busier days. It starts at the top and runs clockwise. |
| Tower | `tower` | A tower with one floor per month. Wider floors and more lit windows mean busier months. |
| Streak timeline | `streak-timeline` | Every streak as a block along one year. Long streaks get a label. |
| Moon phases | `moon-phases` | Each day is a moon: new when quiet, full when busy. Shows the last 26 weeks. |
| Git graph | `git-graph` | A main line with a node for every active week and branches that fork and merge back, like git log --graph. |
| Hex dump | `hex-dump` | Each day is one byte. Busy days are bigger hex values, like opening a binary file. |
| Topographic map | `topographic-map` | Contour lines rise around the weeks you were busiest, like a hiking map. |
| Barcode | `barcode` | Your year as a product barcode. Thick bars are active days. |
| DNA helix | `dna-helix` | Two twisting strands with a rung for every active day. |
| Pulse line | `pulse-line` | A heartbeat monitor with a spike for every active day. The bright pulse keeps scanning along. |
| Equalizer | `equalizer` | One bar per week that bounces like an audio equalizer, taller for busier weeks. |
| Snake | `snake` | A snake eats its way across the year, one active day at a time, and starts over at the end. |
| Pac-man | `pac-man` | A chomping circle eats the days one row at a time, left to right and back again. |
| Falling blocks | `falling-blocks` | Blocks stack into one column per week, and a few more keep dropping in. |
| Radar sweep | `radar-sweep` | A scan line sweeps around and lights up the days it passes. Weeks go around, weekdays go outward. |
| Meteor shower | `meteor-shower` | Every active day is a streak across the sky, longer and brighter when busier. |
| Matrix rain | `matrix-rain` | Falling code with a column for every week. Busier weeks rain brighter. |
| Solar system | `solar-system` | One planet for each month orbiting a sun. Bigger planets are busier months. |
<!-- styles:end -->

The game styles are inspired by digging, obstacle-course, falling-block and farming games. They use only simple shapes drawn for this project, and they are not affiliated with any game.

Three more styles are previews only, because they need data the contribution graph does not have: a punch card (the hour of each commit), a word cloud (commit messages) and repo bubbles (repository names, which could expose private repos). Each preview says so.

## Things to know

- **Last 12 months only.** The charts use the same window as GitHub's own graph.
- **Private contributions.** The default workflow token can only see public activity. To include private contributions, pass a personal access token with the `token` input, stored as a repository secret.
- **Commits as you.** The workflow commits with your GitHub no-reply address, so the daily update shows as you. Each daily run adds a commit.
- **No outside services.** Everything is generated inside your own workflow run.

## Run it yourself

Needs Python 3. Real data also needs the [GitHub CLI](https://cli.github.com) signed in.

```bash
python generator/generate.py --list
python generator/generate.py --style spiral-galaxy --sample --out charts                    # made-up data
python generator/generate.py --style spiral-galaxy --theme ice --username YOU --out charts   # your data
python generator/generate.py --style skyline --sample --frame terminal --header terminal --details show
```

## Add a style

1. Create `generator/styles/your_style.py` with a `render(days)` function. `days` is a list of `{"date": "YYYY-MM-DD", "count": n}`. Return a dict with `w`, `h`, `body`, `defs`, `title`, `cmd` and `aria`. Optional keys: `deco` (decorations behind the chart), `caption` (the stats line), `foot` (where the chart ends), `top` (where it starts) and `css` (animation rules), so the chart can be shown plain. The existing styles are good examples. A style's name is the file name with dashes, so `your_style.py` is `your-style`.
2. Add a line for it to `generator/styles/catalog.py`: its name, a title, a category and a one-line description.
3. Run `python generator/build_samples.py`. It rebuilds the samples in every theme, the list the gallery loads, and the styles table in this README, so the gallery and the README update by themselves.

## License

MIT

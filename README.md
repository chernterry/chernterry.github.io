# Personal website

Static site (HTML/CSS/vanilla JS) for [terrychern.com](https://terrychern.com), hosted on GitHub Pages.
No build step — what's in this repo is what gets served.

See [PLAN.md](PLAN.md) for the full content plan and go-live checklist.

## Local development

```bash
pixi install          # one time
pixi run dev          # http://localhost:8000
```

## Tasks

| Command | What it does |
|---|---|
| `pixi run dev` | Serve the site locally on port 8000 |
| `pixi run check` | List any `[[PLACEHOLDER]]` markers still unfilled |
| `pixi run optimize-images` | Resize/compress `assets/img/_raw/` into `assets/img/` |

## Layout

```
index.html              the entire site — one page, anchored sections
404.html                custom not-found page
assets/css/style.css    all styling; design tokens at the top of the file
assets/js/main.js       theme toggle, mobile nav, footer year
assets/img/             committed, web-optimized images
assets/img/_raw/        full-size originals (gitignored)
scripts/                pixi task scripts
```

## Adding photos

1. Drop originals into `assets/img/_raw/`
2. `pixi run optimize-images`
3. Point the `<img>` tags at the generated files in `assets/img/`

The optimizer strips EXIF, which matters: phone photos embed GPS coordinates.

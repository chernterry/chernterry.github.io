# Personal website — build & launch plan

**Goal:** a single-page site that works as a second resume, a credibility signal
for consulting leads, and an obvious way to contact you.

**Stack:** hand-written HTML + CSS + a little vanilla JS. No framework, no build
step. pixi manages the Python tooling (local server, image optimization,
placeholder checks). GitHub Pages serves the repo directly.

**Why no static site generator:** Hugo/Jekyll/Astro earn their complexity when
you have many pages or a blog. For one page, a generator adds a build step, a
dependency to keep current, and a layer between you and the output — for no
benefit. If you later add a blog, revisit this; migrating a single HTML page is
an afternoon.

---

## Status

- [x] Scaffold: `index.html`, `404.html`, stylesheet, JS, pixi tasks, `.gitignore`
- [x] Design system: light/dark themes, responsive layout, accessible nav
- [ ] **Content — your job, the real work** (see Phase 1)
- [ ] Photos and portrait
- [ ] Git repo + first commit
- [ ] GitHub Pages deploy
- [ ] Custom domain + HTTPS
- [ ] Second domain redirect

---

## Phase 1 — Content

This is the part that determines whether the site works. The scaffold is scenery.

Run `pixi run check` at any point to list every `[[PLACEHOLDER]]` still unfilled.

### Priority order

1. **Hero pitch** (`index.html`, `.lede`) — the two sentences that decide whether
   anyone scrolls. Say what you do, for whom, and what changes because of it.
   Avoid "passionate," "innovative," "cutting-edge."
2. **Contact + Google Scholar link** — the whole point of the site is being
   reachable and verifiable. Get these right before anything else is polished.
3. **Consulting section** — the two service tracks are drafted; edit them down to
   the work you actually want. Being narrower makes you more hireable, not less.
   A prospect who reads a list of everything concludes you specialize in nothing.
4. **Research entries** — one per significant project. Keep the **So what** line;
   for a non-specialist (a founder, a recruiter, an investor) it's the only line
   that survives. Link papers and code where they exist.
5. **Education** — institutions, years, dissertation title, advisor.
6. **Projects** — the commercial-potential section. Be concrete about what stage
   each is at. "Exploring" is a perfectly respectable label and reads as honest.
7. **Beyond work** — write this in your own voice. It's the section people
   remember, and the one that makes a cold email feel possible.
8. **Skills** — prune hard. A shorter list reads as more senior.

### Writing notes

- Second person, active voice. "I build X" beats "X was built."
- Numbers beat adjectives: "validated across 40 participants" > "extensively validated."
- Every claim a stranger might doubt should link to evidence — paper, repo, demo.
- Read the whole page out loud once. Anything you'd never say aloud, cut.

### Also needed

- **Portrait** — `assets/img/portrait.jpg`, roughly 4:5, well lit, plain background.
- **CV PDF** — drop into `assets/`, update the two links, set `[[CV_FILENAME.pdf]]`.
- **Fun photos** — 3+ into `assets/img/_raw/`, then `pixi run optimize-images`.
- **OG card** — `assets/img/og-card.jpg` at 1200x630. This is the preview image
  when someone shares your site in Slack or LinkedIn. Worth doing.

---

## Phase 2 — Git

Nothing has been committed. These commands are yours to run — the scaffold was
built without committing, as you asked.

```bash
cd ~/sideprojects/personal_website

git init
git add -A
git status                     # confirm: no .pixi/, no website_prompt.txt
git commit -m "Initial commit: static personal site scaffold with pixi tooling"
```

Verify the identity picked up your personal account, not Columbia:

```bash
git log -1 --format='%an <%ae>'      # expect the personal GitHub noreply address
```

That comes from the `includeIf "gitdir:~/sideprojects/"` rule in `~/.gitconfig`.
If it shows the Columbia address, stop and fix the config before pushing.

This repo is public, so commits use the GitHub-provided noreply address
rather than a real inbox. Set it once per machine with:

```bash
git config user.email '170845059+chernterry@users.noreply.github.com'
```

---

## Phase 3 — GitHub Pages

### Repository name matters

| Repo name | Served at | Verdict |
|---|---|---|
| `chernterry.github.io` | domain root | **Use this** |
| anything else | `/repo-name/` subpath | needs path prefixes; avoid |

Create it on the **chernterry** account (not tlc2156), public — Pages requires
public repos on the free tier.

```bash
git remote add origin git@github.com:chernterry/chernterry.github.io.git
git branch -M main
git push -u origin main
```

SSH URL, not HTTPS — that's what routes you through the personal key.

Then: **repo → Settings → Pages → Source: Deploy from a branch → `main` / `/ (root)` → Save.**

Live at `https://chernterry.github.io` within a couple of minutes. Confirm it
works there before touching DNS — it isolates "site is broken" from "DNS is
broken," which are much harder to debug together.

---

## Phase 4 — Custom domain

**Constraint: GitHub Pages allows exactly one custom domain per site.** You own
two. Pick the primary; the other becomes a redirect (Phase 5).

Choosing: pick the one you'd say out loud on a call. `.com` over alternatives,
shorter over longer, no hyphens.

### Porkbun DNS for the primary

Delete Porkbun's default parking records first, then add:

| Type | Host | Answer |
|---|---|---|
| A | *(blank)* | `185.199.108.153` |
| A | *(blank)* | `185.199.109.153` |
| A | *(blank)* | `185.199.110.153` |
| A | *(blank)* | `185.199.111.153` |
| AAAA | *(blank)* | `2606:50c0:8000::153` |
| AAAA | *(blank)* | `2606:50c0:8001::153` |
| AAAA | *(blank)* | `2606:50c0:8002::153` |
| AAAA | *(blank)* | `2606:50c0:8003::153` |
| CNAME | `www` | `chernterry.github.io` |

Confirm those IPs against GitHub's current Pages documentation before trusting
them — they change rarely, but they do change, and a stale IP means a dead site.
Porkbun also supports `ALIAS` at the root pointing to `chernterry.github.io`,
which tracks IP changes automatically. Either approach works; ALIAS ages better.

### Then on GitHub

**Settings → Pages → Custom domain** → enter the apex domain → Save.

This writes a `CNAME` file into your repo root. Commit it; don't delete it. (I
deliberately did *not* create that file in the scaffold — a `CNAME` containing a
placeholder would break Pages, and the GitHub UI generates the correct one.)

Wait for the DNS check to pass, then tick **Enforce HTTPS**. Certificate
provisioning takes anywhere from a few minutes to an hour.

DNS propagation is typically minutes but can take up to 48 hours. Check with:

```bash
dig +short YOURDOMAIN.COM
dig +short www.YOURDOMAIN.COM
```

---

## Phase 5 — Second domain

Use Porkbun's built-in **URL Forwarding** on the second domain, permanent (301),
pointing at the primary.

Do **not** point both domains at Pages. Only the one in the `CNAME` file gets a
certificate; the other will fail HTTPS and show visitors a security warning.

---

## Phase 6 — After launch

- [ ] Submit to [Google Search Console](https://search.google.com/search-console)
      and the sitemap at `/sitemap.xml`
- [ ] Fill in `[[YOURDOMAIN.COM]]` in `robots.txt`, `sitemap.xml`, and the
      `<head>` meta tags of `index.html`
- [ ] Test on a real phone, not just a narrowed browser window
- [ ] Run [PageSpeed Insights](https://pagespeed.web.dev/) — a static site with
      optimized images should score near 100
- [ ] Check the social preview by pasting the URL into Slack or LinkedIn
- [ ] Add the URL to LinkedIn, Google Scholar, GitHub profile, email signature

### Analytics (optional)

If you want to know whether the consulting pitch is landing, use something
privacy-respecting and cookieless — Plausible or GoatCounter. Both are a single
script tag and neither requires a cookie banner. Google Analytics on a personal
site is more legal surface than the data is worth.

### Deploying updates

```bash
pixi run check                 # no placeholders left
pixi run dev                   # eyeball it locally
git add -A && git commit -m "..." && git push
```

Pages redeploys in under a minute. Hard-refresh (Ctrl+Shift+R) if you don't see
the change — CSS caching is the usual culprit.

---

## Ideas for later

- **Blog / writing** — the strongest inbound-consulting channel there is. Would
  justify moving to a generator.
- **Case studies** — one page per consulting engagement, with outcomes.
- **Talks & press** — a section if you accumulate them.
- **Contact form** — Formspree or similar if a `mailto:` link proves too
  high-friction. Start with `mailto:` and see.

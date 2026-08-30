# 🖋️ Editorial Review & Work Items — From Claude (Editor-in-Chief)

**To**: Antigravity (Infrastructure Lead)
**From**: Claude — Content, Style & Editorial Lead
**Date**: 30 August 2026
**Status**: Live-site audit complete across all 7 sub-sites. Several customer-facing issues need fixing before further design polish is worth doing.

---

## 0. Standing Rulings (so we stop re-litigating these)

- **Colors are settled.** The live `:root` tokens already in each child theme's `style.css` match `docs/GWP_MASTER_WORK_REGISTRY.md`. The `*_master.docx` files in `~/GWP Website Docs/` have a different, never-implemented palette for glamour/family/fashion/cosplay — treat those docx color sections as superseded. **No site gets recolored.** `HANDOVER_CLAUDE_DESIGN_DIRECTIVES.md`'s color table also has transcription errors vs. what's live — worth a quick correction pass but not urgent.
- **`gary-wedding-pro` is the style baseline**, per Gary directly. It's the mature, hand-built parent theme (4,672-line `style.css`, 10-80-10 layout rule, Never-Crop rule, hero slider, medallion icons, Z-pattern editorial blocks, investment sidebar, FAQ accordion). The other 6 child themes correctly inherit it (parent-style + child-style both enqueued, confirmed in each `functions.php`) — so the work on those 6 is refinement and genre-specific component styling on top of what's inherited, not a rebuild.

---

## 1. Critical Content Bugs (fix before anything else — these are customer-facing embarrassments)

1. **Unrendered AI citation artifacts on the live family homepage**: the headline copy contains literal `[cite: 31]`, `[cite: 50]` markers. This reads as broken to any visitor. Needs an immediate copy pass on family.garywallage.uk.
2. **Wrong hero copy duplicated across unrelated sites**: boudoir, glamour, and **cosplay** all show the identical "Capture Your Own Story... unhurried artistry, thoughtful direction, complete discretion" block. That copy was written for boudoir's intimacy/discretion framing — it makes no sense on a cosplay character-photography site.
3. **Separately, fashion and portrait/staging both show an unrelated "Preserving Legacies... visual historian... darkroom" block**, and it also appears as the **footer tagline on boudoir, glamour, and family** ("Wiltshire Historian"). This looks like Gary's personal-hobby bio text leaking into commercial site copy/footers site-wide. Needs a real per-site footer tagline + hero copy pass — I'll own the copy, but need to know which script/template is pulling this default text in (`phase_c_site_builder.py`? a shared footer widget?) so the fix sticks instead of reverting on next content sync.
4. **Cosplay has a literal WordPress default post live**: "Welcome to Gary Wallage Photography Network Sites. This is your first post." — the sample content was never deleted.
5. **Raw CR2 filenames showing as visitor-facing captions** on cosplay (e.g. `2024-11-11-18-13-11.cr2`) — `ingest_all_stories.py`/`parse_and_ingest_stories.py` isn't generating real captions for at least this site, or hasn't been run there yet.
6. **"Sample Page" still in the nav** on boudoir, glamour, and portrait.
7. **Fashion's main navigation is broken** — homepage renders only `[HOME (Safety Link)]`, no other menu items. Looks like a `configure_site_menus.py` failure specific to fashion.
8. **Portrait/staging nav has wedding items bled in** ("Book your Wedding Day", duplicate "About Gary"/"About Me" entries) — cross-site menu contamination, likely a shared-menu misconfiguration in the multisite setup.
9. **Contact email inconsistency**: booking CTAs point to `gary@wallage.org.uk` (personal portal domain) on boudoir/portrait, while portrait's footer shows `gary@garywallage.uk`. Needs one canonical business contact address across every site — my instinct is `garywallage.uk`, not the personal `wallage.org.uk` domain, but confirm with Gary before changing anything customer-facing.

## 2. Service Catalog Coverage Gap

Only wedding is fully populated (13 priced packages + 15+ add-ons). Every other site is showing a fraction of its master-doc service list live:

| Site | Live services shown | Master doc total |
|---|---|---|
| Boudoir | 7 | 9 |
| Glamour | 5 | 9 |
| Family | 5 | 9 |
| Fashion | 4 | 10 |
| Cosplay | 4 | 8 |
| Portrait | 4 | 11 |

The good news: where services **are** live, real GBP pricing is showing (not `£POA`), so the pricing-mismatch risk I flagged earlier from the docx review is a non-issue on the actual sites. This is purely a completeness gap in `publish_package_landing_pages.py` / `ingest_bookly_services.php` — worth checking why those 6 sites stopped short of their full catalogs. Bookly plugin data itself has **zero `bookly_service` posts** on boudoir, so the booking engine and the marketing pages may be out of sync regardless of what's visually showing.

## 3. Infra/Automation Backlog (from repo + Swarm audit)

**Done, with evidence:**
- Core Swarm stack (wordpress + nginx on `zone_dmz`/`zone_internal`), central `databases_mariadb`/`databases_redis` migration, nginx hardening (xmlrpc block, fastcgi_pass isolation), WP-CLI tooling (`bin/gw-wp`, `bin/run-cron.sh`), Bookly plugin stack installed network-wide.
- **Host→Swarm migration is further along than `docs/HOST_APACHE_MARIADB_MIGRATION_PLAN.md` admits**: `mariadb.service` is already inactive, `catherine-portfolio` stack is live in Swarm, and Caddy vhosts for catherinewallage/wallage/quattrotech already exist. **Please update that doc to reflect reality** — as written it reads like Work Items 1–3 haven't started, and someone could waste time re-doing finished work.

**Partial:**
- Migration Work Item 4 (host cleanup): `apache2.service` is still active — not yet stopped/disabled.
- Bookly/WooCommerce catalog: plugins live, zero actual service/product posts found on boudoir.

**Not started:**
- WP-D1 security hardening: no Melapress 2FA installed anywhere. A custom `gw-security` plugin exists but is **inactive** — was this abandoned or deliberately parked? Worth a direct answer rather than us both assuming.
- Zoho Books / Google Shopping / Meta catalog integration (Integration Guide sections 3, 5, 6).
- Story ingestion completeness unverified beyond the cosplay gap noted above.
- DocuSeal is running in Swarm but not wired to the contract template.

**Undocumented and worth clarifying:**
- `/opt/docker-stacks/gary-legacy/` and `/opt/docker-stacks/gwp-hub/` both exist with their own compose/html/nginx and appear nowhere in the registry or migration plan. Finished, half-built, or superseded — which?

## 4. Process Issue: `html/` Is Entirely Gitignored

`.gitignore` line 1 excludes `/html/` wholesale — every theme, plugin, and content change across all 7 sites (including the CSS work I'm about to do) has **no version history and no rollback path**. Recommend carving out an allowlist for theme/plugin code (`html/wp-content/themes/`, `html/wp-content/mu-plugins/` etc.) while keeping uploads/cache/core excluded, so editorial and infra work on the actual sites is trackable the same way this backlog is. Flagging rather than just doing it myself since it touches your build/deploy assumptions — let me know if there's a reason it's excluded (e.g. size, secrets in wp-config) before I change it.

## 5. Tracking

Every item above is now filed as an individual GitHub issue (#8-#34) using the existing `[Design/Claude]` / `[DevOps/Antigravity]` convention, so this doc isn't the source of truth going forward — the issue tracker is. Highest priority: **#8, a full QA pass on wedding.garywallage.uk** (Gary wants it 100% perfect and fully functional before further polish elsewhere), followed by #9 (family homepage citation artifacts — visibly broken right now).

## 6. What I'm Doing Next

Starting the Work Item 1 CSS pass (typography, spacing, micro-interactions) on the 6 non-wedding child themes, using `gary-wedding-pro` as the structural reference and each site's existing color tokens — per Gary's direct instruction. Will hold off touching copy/content (items in Section 1) until we've confirmed where that text is actually generated, so fixes don't get overwritten by the next automation run.

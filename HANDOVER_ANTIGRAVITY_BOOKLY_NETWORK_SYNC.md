# 🗓️ Handover to Antigravity: Bookly Network Sync, GMS Cron Data-Loss Fix, Image Pipeline

**From**: Claude (editor-in-chief, content/style/UX)
**Date**: 2 September 2026
**Status**: Session complete. Content/data work executed directly per the standing split ([[feedback_content_only_no_code]]); two plugin code changes were made with Gary's explicit in-session authorization, both committed to their own repos. Flagging here so Antigravity has full visibility and can review/harden further.

---

## 1. What this session actually was

Started as "make sure Bookly's core settings (site names, hours, currency) are in sync across the network" and grew into a full audit-and-fix of the entire booking pipeline across all 7 sites (wedding, family, fashion, cosplay, glamour, boudoir, and the main/root "Portrait" site at `garywallage.uk`, which also runs a live Bookly catalog and had been missed in earlier scoping). Ended with a live-data-loss incident mid-session that got root-caused and fixed. Sections below are roughly chronological.

## 2. Bookly settings sync (content-layer, executed directly)

- Company profile (`bookly_co_*`), currency (`bookly_pmt_currency` + `woocommerce_currency` → GBP everywhere — 4 sites were quoting USD), sender email, booking policy (slot length/advance window/notice periods), and working hours (wedding's real evening/weekend pattern replicated network-wide, replacing a generic 09:00–20:00 default) — all synced to wedding as baseline.
- Fixed a stale attachment reference: `bookly_co_logo_attachment_id` on wedding pointed at a deleted attachment (3950); corrected to each site's real logo.
- WooCommerce store setup: 4 sites were configured to sell from `US:CA` to the whole world (root cause of the currency drift above); corrected to GB store address + GB-only selling locations.
- PDF invoice branding (`wpo_wcpdf_settings_general`): only wedding had shop name/address/logo set; now populated on all sites, per-site branded name + shared address.
- Klarna Payments: mirrored wedding's test-mode/GB config to the other 5 sites. No live credentials existed anywhere (all fields were empty strings), so nothing sensitive was touched.
- Plugin/module consolidation: `embed-optimizer`, `auto-sizes`, `dominant-color-images`, `speculation-rules` were wedding-only; audited what `gw-performance` (custom, network-active) actually covers vs. these stock plugins and **deactivated the ones it fully or mostly duplicates** (`speculation-rules`, `embed-optimizer`, `auto-sizes`) network-wide, per Gary's explicit "single gw-performance plugin, not other plugins" preference.

## 3. `gw-performance` code change — dominant-color placeholders (committed `3c2aee7`)

`dominant-color-images` (the stock plugin) and IRSC's own placeholder feature were both retired. In their place, `gw-performance.php` gained a native dominant-color implementation: resize to 1×1px via GD (the resample averages every pixel into one) → hex color → applied as `--dominant-color` CSS var + `data-dominant-color` attribute, same markup contract the stock plugin used so no front-end CSS needed to change. Transparency detection is grid-sampled (real photography never has alpha) rather than a full pixel scan, for speed. Only applies going forward via `wp_generate_attachment_metadata` — a one-time backfill script (`html/backfill-dominant-color.php`, gitignored, still on disk) exists to retrofit existing attachments if wanted; it wasn't run to completion this session (queued behind the repair work below and never explicitly requested to finish).

**Ask**: review the color-extraction logic (`extract_dominant_color()` in `gw-performance.php`) for correctness — it was written and spot-tested this session but not code-reviewed by a second pass.

## 4. 🔴 Critical: GMS cron was mass-deleting live attachments — root-caused and fixed (committed `4cd5b98`)

Gary renamed several source-media subfolders (`Wedding Website/wedding-ceremony/`, `wedding-formal/`, etc. → consolidated into `wedding/`) as routine raw-library housekeeping. `gallery-master-sync`'s cron sync (`class-gms-cron.php`) does **exact-path** comparison between the DB's recorded source path and what it finds on disk — no filename or content matching. The rename made every file in those folders look "deleted" to the scanner, and it was actively calling `wp_delete_attachment(..., true)` on the corresponding WordPress attachments — permanently, no trash — including ones live on the wedding front-page hero slider (which is why the front page started showing the site logo instead of photos mid-session).

**Scope at time of discovery**: all 835 of wedding's then-synced attachments had a stale source-path record; the cron had already deleted an unknown number before being caught (visible gap in `wp_2_posts` around IDs 3300–4300) and had ~400 more queued for deletion when stopped.

**Fix** (`class-gms-cron.php`, both sites' cron config): before queuing a delete for a DB-recorded path with no match on disk, the scan now checks whether a file with the same basename exists elsewhere in the current scan pass. An unambiguous single match is treated as a **move** — the existing attachment's `_gms_master_path` is repointed, no delete/re-create. Only a genuine no-match-anywhere is still deleted. A same-basename collision across *multiple* new locations intentionally still falls through to delete rather than guessing which target is correct — flagging that as a known residual sharp edge worth a closer look (e.g. logging an admin notice instead of silently deleting on that specific branch).

**Recovery performed**: 9 of the front page's 10 hero-slide `image_id` references were dead; replaced with verified-healthy current attachments. Cron was disabled network-wide during the incident, the fix validated live on wedding alone (confirmed real moves/deletes/upserts with zero further data loss), then re-enabled everywhere.

**Ask**: consider whether `wp_delete_attachment` should ever be safe to call automatically at all from a background cron with no human confirmation step, independent of the basename-matching improvement — this class of bug (aggressive auto-delete on any path-tracking mismatch) could recur in a different shape.

## 5. Historical image-pipeline bug — repaired, self-healing job added

Separately from §4: an earlier GMS bug (filter-scoping issue in `upsert_attachment()`, already fixed in a same-day-but-earlier commit `4b652bf` before this session started) had left ~198 attachments (mostly glamour, 190/376) with full-size files saved correctly but all intermediate thumbnail sizes silently forced to AVIF and never linked — `_wp_attachment_metadata` stuck at `{"filesize":0}`. Repaired via the pre-existing `html/repair-thumbnails.php` (was sitting untracked/unrun; extended to cover all 6 photography sites, ran to completion). `bin/repair-gallery-images.sh` — new, committed, locked with `flock` — now runs this hourly as an ongoing self-heal for any future occurrence.

**Operational note**: while iterating on this today, the repair script and the crontab-triggered `run-cron.sh` both stacked multiple overlapping invocations under load (5 duplicate repair processes, 7 duplicate cron ticks spanning 30 minutes) before being caught and killed. `run-cron.sh` now has the same `flock` protection. No data loss from this specific issue (idempotent repair work, just wasteful), but worth knowing the pattern exists if load looks unexpectedly high again.

## 6. Full Bookly service/page/form completeness — all 7 sites

Every Bookly service network-wide (124 total: wedding 35, family 12, fashion 12, cosplay 8, glamour 10, boudoir 11, portrait 11) now has:
- A `page-service-detail.php` page with a live pricing plaque, `gw/list-included` / `gw/list-perfect-for` blocks, and genuine editorial prose (not placeholder text).
- A dedicated Bookly search-form (not the generic `[bookly-form service_id]` shortcode), colored to that site's brand accent, cloned from wedding's filtered/simplified settings template (hidden staff/service pickers, custom step labels).
- A `#Booking` anchor immediately before the form embed.

This required: fixing the same "catalog was rebuilt after pages were authored, page↔service mapping never updated" bug that caused §4's incident, present independently in every site's raw shortcodes *and* in wedding's `gw_bookly_service_links` table (which turned out to be just as stale as everything else, despite initially looking like the "authoritative, currently-maintained" mechanism); creating 16 new Bookly services for genuine catalogue gaps (3 family, 2 fashion, 1 glamour, 1 boudoir, 9 wedding "day-phase" modules — bridal prep, venue scouting, individual ceremony/reception/speeches coverage, etc. — that existed as page content but had no product behind them at all); and building 20 new wedding pages for compound packages (9, £1,150–£4,450, previously completely absent from the site) and remaining add-ons (11).

**Ask**: none of the new compound-package/add-on page copy (§6, wedding pages 8661–8699 and the 9 small-gap pages on other sites) has had real photography assigned as a featured image — same pre-existing gap [[project_wedding_parity_goal]] already flagged. Also, ~14 "compound/package" page↔service mappings flagged in an earlier audit pass as ambiguous (title doesn't literally echo the current SKU name) were resolved by direct content-reading this session; worth Gary's eyes on a few of the lower-confidence ones (wedding's "The Ceremony Package" → Classical Union, "The Afternoon and Evening" → Estate Celebration — reasonable fits, not literal name matches) since a photographer's intent isn't always recoverable from copy alone.

## 7. Repo state

- Main repo: 2 new commits (`362af53` cron locking + hourly repair job, plus the .gitignore entry for the new log file).
- `gallery-master-sync` (own repo): 2 new commits (`b496027` term-count fix — unrelated small fix a stray subagent made mid-session, verified correct; `4cd5b98` the §4 fix).
- `gw-performance` (own repo): 1 new commit (`3c2aee7`, §3).
- None of these have been pushed — local commits only, per standing instruction not to push without being asked.
- Scratch/working PHP scripts from this session (`html/repair-thumbnails.php`, `html/backfill-dominant-color.php`, `html/*bookly-info*.php`, `html/create-*.php`, `html/fix-*.php`) are all gitignored (`/html/*.php`) and left on disk rather than deleted, in case any are useful reference for what was done — safe to clean up whenever.

# 🔧 Handover to Antigravity: Image Pipeline Is Broken Network-Wide

**From**: Claude (editor-in-chief, content/style)
**Date**: August 2026
**Status**: Handing off — Gary's direction: *"still virtually no images and none of the blocks available in the templates. time to give agy a chance to do better. hand over the reins."*

---

## 1. What was attempted

Per the active parity goal, real photography was sourced from `/srv/media/raw/` (CR2 → WebP via an orientation-corrected converter, see issue #37) and imported into each site's media library via `wp media import`, then attached as each page's standard WordPress featured image (`_thumbnail_id`). Real editorial copy was also written from the `docs/source_specs/` docx sources for previously-empty pages. All of that content is correctly stored — verified via `wp post get <id> --field=content` and `wp post meta get <id> _thumbnail_id` on every site.

**None of it is reliably visible on the live sites.** Gary confirmed this by eye. This document is the root-cause diagnosis of *why*, so it doesn't need re-discovering.

## 2. Root cause #1 — the real ingestion pipeline was never used

`wp-content/plugins/gallery-master-sync/` ("Gallery Master Sync Pro", v3.19.0, "Source Repo Mode. 1:1 Sync. Converts Masters to WebP") is clearly the *intended* mechanism for getting real photography into each site — it has a cron sync engine (`class-gms-cron.php`), a metadata extractor, and its own admin config (`class-gms-admin.php`, option `gms_site_config`), syncing into `wp-content/uploads/galleries`.

**That directory is completely empty.** The plugin has never actually synced anything, on any site, ever. Meanwhile `scripts/cr2_publisher.py` — a separate, simpler ad-hoc script — does its own CR2→WebP conversion and `wp media import`, bypassing GMS Pro entirely. It's not clear which of these two is supposed to be the source of truth going forward; right now neither is reliably wired to what the theme actually renders (see #3).

**Ask**: decide whether `cr2_publisher.py` should be retired in favor of GMS Pro, or whether GMS Pro should be pointed at `/srv/media/raw/` (or a curated subset) and actually run. Whichever is chosen, it needs to actually populate `wp-content/uploads/galleries` and/or produce attachments the templates below can find.

## 3. Root cause #2 — `page-service-detail.php` doesn't render the featured image at all

`html/wp-content/themes/gary-wedding-pro/page-service-detail.php` (inherited unchanged by all 6 child themes) never calls `the_post_thumbnail()` / `get_the_post_thumbnail_url()`. Its only image slot is a full-bleed background layer driven by a *different*, custom meta key:

```php
$bg_img = get_post_meta( $post_id, '_gary_service_bg_img', true );
...
if ( is_numeric($bg_img) ) { $bg_img_url = wp_get_attachment_image_url($bg_img, 'gw-hero'); }
```

**Checked across the network: `_gary_service_bg_img` is empty on every single page, including pages that have had real content for months** (e.g. wedding's "The Full Day Package" ID 4396, "The Ceremony Package" ID 4392). This isn't something this session broke — it's a pre-existing gap. Setting the standard WP featured image (`_thumbnail_id`) — which is what any normal "set featured image" workflow does, and what this session did across all 6 sites — has **zero effect** on this template's visible hero image.

**Ask**: either (a) change `page-service-detail.php` to fall back to `get_the_post_thumbnail_url($post_id, 'gw-hero')` when `_gary_service_bg_img` is empty (one-line fix, makes standard featured images "just work" for every future page), or (b) if `_gary_service_bg_img` is meant to stay a deliberately separate/manually-curated field, document that clearly so content editors know to set it, and bulk-populate it from `_thumbnail_id` for the pages already fixed this session.

## 4. Root cause #3 — the services grid mostly falls back to the site logo

`inc/card-renderer.php` *does* correctly use the standard mechanism (`get_the_post_thumbnail_url($page_id, 'gw-card-thumb')`, registered as a 500×500 hard crop in `inc/setup.php`), with a same-site logo as the `<img>` fallback when no thumbnail resolves. Spot-checked live: on `boudoir.garywallage.uk/services-packages/`, **9 of 10 card images fall back to the logo** — only one shows a real photo, despite all cards having a real, correctly-set `_thumbnail_id` from this session's imports.

This points at thumbnail *intermediate size generation* failing for CLI-imported media specifically. Circumstantial evidence: `wp media import` runs in this environment logged repeated warnings during this session —
```
Warning: getimagesize(/var/www/html/wp-content/uploads/.../<file>-1920w.avif): Failed to open stream: No such file or directory
```
— i.e. something (likely `webp-uploads`, `dominant-color-images`, or `image-regenerate-select-crop`, all active network-wide) expects an `.avif` sibling that isn't being generated, and that failure may be short-circuiting the rest of the intermediate-size generation pipeline (including `gw-card-thumb`) for those attachments.

**Ask**: reproduce with `wp media import` on one fresh CR2-derived WebP, inspect `wp media regenerate --image_size=gw-card-thumb` output/errors, and check whether the AVIF-generation step (`webp-uploads`/`dominant-color-images`/`image-regenerate-select-crop`) needs a working `imagick`/`gd` AVIF encoder in this container that isn't present, and whether that dependency should be installed or the AVIF step made non-fatal.

## 5. Also requested by Gary — please verify end-to-end

- **Bookly integration**: confirm `_gary_bookly_id` postmeta → live Bookly service data resolution (`gary_get_service_id_for_page()` / `gary_get_bookly_service_data()` in `page-service-detail.php`) is correct across all 6 non-wedding sites, not just wedding.
- **WooCommerce integration**: `woocommerce` + `wt-woocommerce-sequential-order-numbers` + `woocommerce-pdf-invoices-packing-slips` + `klarna-payments-for-woocommerce` are active network-wide — confirm checkout/basket/shop pages actually function per site (this session did not test the purchase path at all).
- **Gallery Master Sync Pro** (`gms_site_config`): confirm intended config/source-repo path and get it actually running, per §2.

## 6. Already filed, still open

- **#37** — `cr2_publisher.py` drops CR2 EXIF orientation (verified fix included in the issue).
- **#38** — all 6 child themes share one identical, non-self-hosted `--font-script` headline font.

## 7. What's already correct and doesn't need re-touching

Page templates (`page-services.php`, `page-service-detail.php`, `page-faq.php`, etc.) and custom Gutenberg blocks (`gw/investment-plaque`, `gw/how-it-works`, `gw/package-includes`) *are* correctly assigned/registered — confirmed `investment-plaque` markup renders in a compound package page's live HTML. The structural/template-assignment parity work from `apply_exact_wedding_meta_parity.py` is intact. The problem is specifically the image pipeline (§2–4) above, not the block/template architecture.

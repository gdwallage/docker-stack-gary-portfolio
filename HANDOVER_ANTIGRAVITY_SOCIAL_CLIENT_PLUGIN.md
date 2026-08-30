# 🔌 Handover to Antigravity: New Plugin — Unified Facebook + Instagram Social Client

**From**: Claude (editor-in-chief, content/style/UX)
**Date**: 30 August 2026
**Status**: Design spec for a 100% new plugin feature. Gary confirmed: FB Pages + linked IG Business accounts already exist per site, and a Meta Developer App/Business Manager already exists. This is a build spec, not exploratory research — implementation is Antigravity's, per the standing content-vs-code split ([[feedback_content_only_no_code]]).

---

## Scope ruling: admin-side only, not public-facing

This entire plugin is a **wp-admin management console** for Gary to run FB/IG from inside WordPress — it is not a front-end feature. No public templates, shortcodes, widgets, embedded feeds, or visitor-facing UI of any kind are in scope. Nothing here touches what a site visitor sees; it's purely an internal tool sitting behind `manage_options`. Every screen described below (§4) lives in wp-admin only.

---

## 0. Read this section first — platform reality check

Gary's ask is to treat Facebook + Instagram as one virtual client inside wp-admin: link one FB Page + one IG Business account per site, then manage profile, URLs, follower/following counts, **an audit of followers/following to surface idle or dead accounts**, and full CRUD over posts and Stories — tagging, comments, location, all of it.

Most of that is buildable on the official Meta Graph API / Instagram Graph API. Three parts of the ask are **not possible through any officially sanctioned API**, by deliberate design on Meta's side (anti-scraping and privacy law compliance), not a gap we can code around:

| Ask | Reality |
|---|---|
| **Follower/following audit (idle/dead account detection)** | There is no API endpoint, and never has been, that lists the individual accounts following a Page/IG Business account, or the individual accounts it follows. Only aggregate counts (`followers_count`, `follows_count`) are exposed. This blocks the feature as literally specified. |
| **Edit or delete a published Instagram post/Reel/carousel** | The Instagram Graph API has no update or delete endpoint for media once published. Facebook Page posts *can* be deleted/edited via API; Instagram content cannot. |
| **Read back or manage Facebook Page Stories** | Meta never shipped a Stories API for Pages (unlike Instagram, where Stories can be *published* but not read back after ~24h, updated, or deleted via API either). |

**Ruling**: we build against the real API surface and design an honest fallback for the follower-audit feature (§5) instead of promising something that requires scraping, which would also risk the Meta App's API access being revoked entirely (breaking every other feature in this plugin, across all 7 sites, if Meta detects ToS-violating access). Everything else in the ask (profile display, URLs, post/comment/tagging/location CRUD within the limits above) is genuinely buildable — scoped precisely below.

---

## 1. Confirmed inputs (from Gary, 2026-08-30)

- All 7 sites (`wedding`, `boudoir`, `glamour`, `family`, `fashion`, `cosplay`, `staging`) already have a live Facebook Page and a linked Instagram Business/Creator account.
- A Meta Developer App + Business Manager account already exists for the garywallage.uk business.
- **Not yet confirmed — Antigravity to verify as step zero**: which specific FB Page ID / IG Business Account ID belongs to which of the 7 sites, what permissions/App Review tier the existing Meta App currently holds, and whether it's in Development Mode (works only for admin/tester accounts) or Live Mode (works for the real Pages, requires App Review approval for restricted permissions like `instagram_content_publish`, `pages_manage_posts`, `instagram_manage_comments`, `instagram_manage_insights`, `pages_read_engagement`). If it's still in Development Mode, App Review is a real prerequisite (can take days-to-weeks, needs a screencast + business verification) and should be scheduled before UI work starts, not discovered at the end.

---

## 2. Plugin architecture

New network-activated plugin, suggested slug `gw-social-client` (network plugin, not per-site, so one codebase serves all 7 sites but each site gets its own connection + data — same pattern as the existing `gw-bookly-addons`/`gw-security` custom plugins already in `html/wp-content/plugins/`).

**Per-site association** (one FB Page + one IG Business account per site, per Gary's spec):
- Store as site options on each subsite: `gw_social_fb_page_id`, `gw_social_ig_user_id`, plus encrypted long-lived access tokens (`gw_social_fb_token`, shared token also covers the linked IG account under the Instagram Graph API model — store once, scoped per FB Page).
- Connection UI: new top-level wp-admin menu **"Social"** on each site (visible to `manage_options` capability only), with a **Connect** screen per platform doing the OAuth handshake (Facebook Login for Business → page picker → confirm linked IG account → exchange short-lived for long-lived Page token → store encrypted).
- Token refresh: long-lived Page tokens last ~60 days and don't auto-refresh via a refresh-token flow like OAuth2 normally does — they need to be re-exchanged before expiry. Add a `wp_cron` job (daily) that re-exchanges tokens nearing expiry and emails/admin-notices Gary if a reconnect is needed (this happens automatically if an admin who is a Page admin visits an authenticated screen, but shouldn't be assumed — build the explicit refresh job).

**Data model** (custom tables via `$wpdb`, one set shared across the network since post/comment data should be queryable cross-site for a unified inbox — see §4):
- `wp_gw_social_accounts` — site_id, platform (fb/ig), external_id, display_name, profile_url, followers_count, following_count, last_synced_at.
- `wp_gw_social_posts` — internal id, site_id, platform, external_post_id (nullable until published), status (draft/scheduled/published/failed), caption, media refs, location_id, tagged_users (JSON), scheduled_at, published_at, permalink, raw_api_response (JSON, for debugging).
- `wp_gw_social_comments` — external_comment_id, post ref, platform, author, text, hidden (bool), replied (bool), synced_at — populated by a polling cron (Meta does support webhooks for comments via `page` subscription — prefer webhook over polling if the existing App's webhook config allows it, falls back to a 15-min cron poll otherwise).
- `wp_gw_social_audience_snapshots` — see §5, populated from manual export ingestion, not live API.

---

## 3. Feature-by-feature capability matrix

| Feature | Facebook Page | Instagram Business | Build as |
|---|---|---|---|
| Connect/link account (OAuth) | ✅ | ✅ (via linked FB Page) | Phase 1 |
| Display profile (name, bio, pic, URL) | ✅ read; bio/pic edit possible via API with `pages_manage_metadata` | ✅ read only — **no write**, bio/pic must be edited in Instagram app | Phase 1 |
| Follower/following **counts** | ✅ aggregate only | ✅ aggregate only | Phase 1 |
| Follower/following **lists** + idle/dead audit | ❌ no API | ❌ no API | Phase 3, manual-export based — see §5 |
| Create post (photo/video/carousel/text+link) | ✅ | ✅ (2-step container→publish) | Phase 2 |
| Read/list posts | ✅ | ✅ | Phase 2 |
| Edit published post | ✅ (text posts; limited on photo/video) | ❌ not supported | Phase 2, FB only |
| Delete published post | ✅ | ❌ not supported | Phase 2, FB only |
| Location tagging on publish | ✅ (Place ID) | ✅ (Place ID, photo/video only, not carousel/stories) | Phase 2 |
| User tagging on publish | ✅ (limited) | ✅ (taggable business/creator/public accounts) | Phase 2 |
| Comments: read/reply/hide/delete | ✅ | ✅ | Phase 2 |
| Publish Stories | ❌ no API at all | ✅ photo/video only, no stickers/links via API | Phase 3 |
| Read back Stories after publish | ❌ | ⚠️ only while still active (<24h), minimal fields | Phase 3, best-effort |
| Edit/delete Stories | ❌ | ❌ | Not buildable — omit |
| Post/media insights (reach, impressions, engagement) | ✅ | ✅ | Phase 3 |

---

## 4. UI/UX design (Claude's scope — Antigravity implements against this)

**Unified "Social" admin screen per site**, three tabs:

1. **Overview** — connected FB Page + IG account cards side by side (avatar, name, bio, follower/following counts, "last synced" timestamp, Reconnect button if token is stale). This is the "treat FB+IG as one tool" surface Gary asked for — same screen, same visual treatment for both platforms, not two separate disconnected settings pages.
2. **Composer + Feed** — a unified chronological feed of posts from both platforms (query across `wp_gw_social_posts`), each card tagged with a small FB/IG badge. A "New Post" button opens a composer: media upload, caption, per-platform toggle (post to FB only / IG only / both), location search-and-tag (autocomplete against the Places search endpoint), user-tag picker, and a schedule-vs-publish-now choice. Edit/Delete actions only appear on FB-sourced cards per the capability matrix above (grey out with a tooltip on IG cards: "Instagram doesn't allow editing or deleting posts after publishing — do this in the Instagram app").
3. **Comments Inbox** — unified list of comments across both platforms needing attention (unreplied), with inline reply/hide/delete, same cross-platform badge treatment as the feed.

**Audience Health** (Phase 3, see §5) gets its own tab once the export-ingestion pipeline exists — not before, so we don't ship an empty promise.

Visual treatment: match each site's existing admin aesthetic minimally (this is a wp-admin tool, not front-of-site — function over genre-branding is fine here, no need for per-site color theming inside wp-admin).

---

## 5. Follower/following audit — the realistic version

Since there is no live API for this, the honest design is a **periodic manual-export ingestion tool**, not a live dashboard:

1. Gary (or whoever is a Page/IG admin) periodically downloads the official self-service data export — Instagram's own **"Download Your Information"** export (Settings → Your Activity → Download Your Information → Followers and Following, JSON or HTML) and/or Meta Business Suite's audience CSV export where available. This is the account owner exporting their own data through Meta's own sanctioned tool — not scraping, not a ToS issue.
2. Add an **upload screen** in the "Audience Health" tab: drop in the exported file, plugin parses it into `wp_gw_social_audience_snapshots` (account handle, first-seen snapshot date, last-seen snapshot date).
3. Diff consecutive snapshots to flag: accounts present in an old snapshot but gone now (unfollowed/removed), and — as a proxy for "idle/dead" since activity data isn't in the export — cross-reference against Instagram's separately-exportable **"Accounts you don't follow back"** / inactive suggestions where the export includes them, and flag accounts with placeholder/default avatar or zero posts if that's present in the export fields (varies by export format/version, needs validation against an actual sample export before committing to exact fields).
4. This is inherently a manual, periodic (e.g. monthly) workflow, not real-time — set that expectation with Gary up front rather than after building it.

If this manual cadence isn't acceptable, the only other legitimate route is a paid Meta Marketing Partner tool (e.g. Meta Business Suite itself already shows some audience insights, or a paid platform like Sprout Social/Hootsuite that has special elevated access) — flagging as an alternative, not recommending we build a from-scratch scraper.

---

## 6. Security notes

- Access tokens are bearer credentials for the real business Pages — store encrypted at rest (not plain `wp_options`), scope the "Social" admin menu to `manage_options` only, and never log raw tokens even in the debug `raw_api_response` column (redact before insert).
- This plugin needs its own dedicated Meta App permission review — do not reuse an ad-hoc personal access token; use the proper Page-scoped long-lived token flow described in §2.
- Multisite network-activation means one compromised site admin account with `manage_options` could see/post to another site's connected Page/IG — confirm this is acceptable (all 7 sites are Gary's own business) or add an extra capability gate if not.

---

## 7. Suggested phasing

1. **Phase 0** (prerequisite): verify Meta App is in Live Mode with the permissions listed in §1; confirm exact FB Page ID / IG User ID per site; if still Development Mode, start App Review now — this has the longest lead time of anything in this spec.
2. **Phase 1**: OAuth connect flow + Overview tab (read-only profile + counts).
3. **Phase 2**: Composer + Feed tab (create/read posts, location/user tagging, FB edit/delete, Comments Inbox).
4. **Phase 3**: Stories publishing (photo/video only), post/media insights, Audience Health manual-export tool (§5).

---

## 8. What I need back from Antigravity

- Confirmation of Phase 0 findings (App Mode, exact Page/IG IDs per site).
- A sample of what an actual Instagram "Download Your Information" followers/following export looks like today (format has changed across Meta's product versions) before §5's parser is built against assumed fields.
- Flag if network-wide token/data storage (§2, shared tables) conflicts with any existing multisite security boundary Antigravity has already set up — if sites need to stay hard-isolated from each other's social data, the data model in §2 needs per-site table prefixes instead of shared tables.

I own the UI/UX and content-workflow design above; the OAuth backend, Graph API integration, and cron/webhook plumbing are Antigravity's to build, per the standing split.

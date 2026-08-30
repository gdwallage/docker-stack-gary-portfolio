# 🎨 GWP Multi-Site Portfolio: Design, Aesthetics & Editorial Handover for Claude

**Role**: Aesthetic, Visual & Editorial Design Editor  
**Infrastructure Lead**: Antigravity (Docker Swarm, MariaDB 11.4 LTS, Redis Object Cache, Caddy v2, PHP 8.3-FPM)  
**Date**: August 2026  
**Status**: All 7 sub-sites are **LIVE** (`HTTP/2 200 OK`, TTFB ~250–350ms).

---

## 🏛️ 1. Architecture & Child Theme Hierarchy

All sub-sites run within a unified WordPress Multisite network on Docker Swarm.
- **Parent Theme**: `gary-wedding-pro` (`/opt/docker-stacks/gary-portfolio/html/wp-content/themes/gary-wedding-pro/`)
  - Contains core layout templates (`front-page.php`, `header.php`, `footer.php`, `page-experience.php`, `page-services.php`, `page-service-detail.php`, `page-faq.php`, `page-about.php`).
  - Contains modular architecture in `inc/` (customizer, card renderer, service blocks, shortcodes, and enqueue).
- **Child Themes**: Each genre has its own child theme that inherits parent templates and overrides styling, tokens, and typography via `style.css`:
  1. `gary-boudoir-pro` (`boudoir.garywallage.uk`)
  2. `gary-glamour-pro` (`glamour.garywallage.uk`)
  3. `gary-family-pro` (`family.garywallage.uk`)
  4. `gary-fashion-pro` (`fashion.garywallage.uk`)
  5. `gary-cosplay-pro` (`cosplay.garywallage.uk`)
  6. `gary-portrait-pro` (`staging.garywallage.uk`)
  7. `gary-wedding-pro` (`wedding.garywallage.uk`)

---

## 🎨 2. Design Tokens & Genre Brand Palettes

| Sub-Site | Domain | Primary Token | Accent Token | Background Dark | Aesthetic Mandate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Wedding** | `wedding.garywallage.uk` | `#B08D55` *(Estate Gold)* | `#C5A059` *(Light Gold)* | `#0e0d0c` | Timeless documentary, architectural romance, serif elegance (`Cinzel` / `Inter`) |
| **Boudoir** | `boudoir.garywallage.uk` | `#B08585` *(Dusty Rose)* | `#C5A5A5` *(Soft Silk)* | `#1A1415` | Intimate, empowering, soft window light, 18+ privacy shield |
| **Glamour** | `glamour.garywallage.uk` | `#4A2C40` *(Deep Plum)* | `#E0D4C3` *(Champagne)* | `#11110E` | High-fashion studio strobes, neon gels, magazine confidence |
| **Family** | `family.garywallage.uk` | `#7B8C7A` *(Sage Green)* | `#D27D56` *(Terracotta)* | `#0F1711` | Warm outdoor parkland, candid unposed joy, generational warmth |
| **Fashion** | `fashion.garywallage.uk` | `#4F5B66` *(Slate Graphite)*| `#C0C5CE` *(Cool Silver)*| `#121110` | Structural lookbooks, textile drape, sharp commercial clarity |
| **Cosplay** | `cosplay.garywallage.uk` | `#4B0082` *(Indigo Purple)* | `#00E5FF` *(Cyber Cyan)* | `#150B1A` | Cinema character fidelity, practical haze, FX composite |
| **Portraits** | `staging.garywallage.uk` | `#1A365D` *(Executive Navy)*| `#4A90E2` *(Vibrant Sky)* | `#0F172A` | Authoritative executive presence, personal brand, casting bios |

---

## 📷 3. Master Image Pipeline & RAW Assets

- **Master RAW Storage**: `/srv/media/raw/` (Contains **13,875 Canon .cr2 RAW files** organized by year and shoot).
- **Automated RAW Converter**: `/opt/docker-stacks/gary-portfolio/scripts/cr2_publisher.py`
  - Automatically develops Canon CR2 files into responsive WebP/AVIF (1920w hero, 1024w story, 600w thumb) with camera color profiles and `© Gary Wallage Photography` EXIF metadata.
  - Usage Example:
    ```bash
    /opt/docker-stacks/gary-portfolio/scripts/cr2_publisher.py \
      "/srv/media/raw/2025/10 - Aria Wild" \
      --site https://glamour.garywallage.uk
    ```
- **Logos & Icons**: Master PNG assets are located in `/home/wallagegd/GWP Images/` and assigned via WordPress media attachments.

---

## 📋 4. Active Work Items for Claude (Aesthetic & Editorial Refinements)

### Work Item 1: Typography & CSS Micro-Interactions
- Refine letter-spacing, line-heights, and heading hierarchy in each child theme's `style.css`.
- Ensure strict adherence to the **10-80-10 Rule** (10% outer breathing room, 80% content width) and **Never-Crop Rule** (preserving unclipped photo ratios).

### Work Item 2: Hero Slider & Gallery Story Visuals
- Populate high-impact WebP hero slides from `/srv/media/raw/` into each sub-site's theme customizer (`hero_slide_1_img`, `hero_slide_2_img`, etc.).
- Curate and style the Story / Portfolio post layouts (`single.php` and story cards).

### Work Item 3: Service Detail Plaque Polish
- Review individual package pages (`/the-boudoir-experience`, `/the-lookbook-collection`, etc.) to ensure block styling, pill tags, and CTA buttons blend seamlessly with the genre palette.

---

## 🛠️ 5. Technical Context & Commands

- **Container Access**: `CID=$(docker ps --filter "name=gary-portfolio_wordpress" --filter "status=running" --format "{{.ID}}" | head -n 1)`
- **WP-CLI Path**: `docker exec "$CID" wp --path=/var/www/html --url=<site_url> ...`
- **Redis Cache**: DB Index 2 (`WP_REDIS_PREFIX: 'gwp_'`). Flush with `wp redis flush`.

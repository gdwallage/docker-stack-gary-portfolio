# 📚 Gary Wallage Photography — Master Architecture & Work Registry

**Document Version**: 2.0  
**Updated**: 30 August 2026  
**Infrastructure Stack**: Docker Swarm, Caddy v2, MariaDB 11.4 LTS, Redis 7, PHP 8.3-FPM  

---

## 🏛️ Stack Architecture & Directory Inventory

### 1. `/opt/docker-stacks/gary-portfolio/` (Multisite Network Engine)
* **Purpose**: Houses the main 7-subsite WordPress Multisite network (`wedding.`, `boudoir.`, `glamour.`, `family.`, `fashion.`, `cosplay.`, `staging.`).
* **Database**: `gary_portfolio` inside `databases_mariadb`.
* **Caching**: Redis DB Index 2 (`WP_REDIS_PREFIX: 'gwp_'`).
* **Child Themes**: Dedicated child themes in `html/wp-content/themes/` inheriting from `gary-wedding-pro`.

### 2. `/opt/docker-stacks/gwp-hub/` (Master Root Gateway Portal)
* **Purpose**: Serves the ultra-fast, luxury root landing portal at `https://garywallage.uk/` and `https://www.garywallage.uk/`.
* **Architecture**: Lightweight Alpine Nginx micro-service serving static HTML5/CSS3 with speculative prefetching rules to warm connections to sub-sites.
* **Git Repository**: [`gdwallage/gwp-hub`](https://github.com/gdwallage/gwp-hub).

### 3. `/opt/docker-stacks/gary-legacy/` (Legacy Single-Site WordPress Archive)
* **Purpose**: Standalone single-site archive preserving Gary's legacy articles, historical tags, and 286 database tables from the original Apache site.
* **Domain**: `https://legacy.garywallage.uk/`.
* **Database**: `garywallage` inside `databases_mariadb`.
* **Caching**: Redis DB Index 3 (`WP_REDIS_PREFIX: 'gw_leg_'`).
* **Git Repository**: [`gdwallage/docker-stack-gary-legacy`](https://github.com/gdwallage/docker-stack-gary-legacy).

### 4. `/opt/docker-stacks/catherine-portfolio/` (Catherine Wallage Photography Store)
* **Purpose**: Dedicated standalone WooCommerce store for Catherine Wallage Photography.
* **Domain**: `https://catherinewallage.uk/`.
* **Database**: `catherinedb` inside `databases_mariadb`.
* **Caching**: Redis DB Index 1 (`WP_REDIS_PREFIX: 'cw_'`).
* **Git Repository**: [`gdwallage/docker-stack-catherine-portfolio`](https://github.com/gdwallage/docker-stack-catherine-portfolio).

### 5. `/opt/docker-stacks/quattrotech/` (Quattrotech Legacy Site)
* **Purpose**: Static corporate website for Quattrotech.
* **Domain**: `https://quattrotech.co.uk/`.
* **Architecture**: Alpine Nginx container.
* **Git Repository**: [`gdwallage/docker-stack-quattrotech`](https://github.com/gdwallage/docker-stack-quattrotech).

### 6. `/opt/docker-stacks/core-infra/` (Edge Reverse Proxy & Networking)
* **Purpose**: Central Caddy v2 reverse proxy handling automatic HTTPS certificates, TLS termination, and routing to Swarm services over `zone_dmz`.
* **Git Repository**: [`gdwallage/docker-stack-core-infra`](https://github.com/gdwallage/docker-stack-core-infra).

### 7. `/opt/docker-stacks/databases/` (Central Persistence Tier)
* **Purpose**: Central MariaDB 11.4 LTS and Redis 7 services on `zone_internal`.
* **Git Repository**: [`gdwallage/docker-stack-databases`](https://github.com/gdwallage/docker-stack-databases).

---

## 🚀 Session Handover & Work Summary (3 September 2026)

### 1. Typography & Header Harmonization
- **Network-Wide Typography Standard**: Unified all child themes to use the Wedding standard typography (`Lato` for body/headings, `Blacksword` for titles & scripts).
- **Blacksword Top-Swash Clipping Fix**: Restored `.site-title-blacksword` font-size to `2.1rem` with `line-height: 1.25`, `padding-top: 4px;` and `overflow: visible;` in parent theme `style.css` (v3003.57).
- **Genre-Specific Header Harmonization**: Clean white `#FFFFFF` header background with matching primary genre accent color across site title, tagline, menu toggle, hamburger icon, and bottom border (Cosplay: `#4B0082`, Glamour: `#4A2C40`).
- **Tagline Constraint**: Bottom-aligned 1-line taglines with `max-width: calc(50vw - 90px)` clearance away from the center logo.

### 2. Scrollytelling Carousel Alignment & Sizing
- **Top-Lock Under Header**: Replaced `bottom: 0 !important` with `top: 0 !important; bottom: auto !important` on `.scroll-bg-image` so photos stick directly below the header/hero slider without top deadspace.
- **100% Top-to-Bottom Fill**: Set `.scroll-bg-image` to `height: 100% !important; object-fit: cover !important; max-width: none !important;` allowing horizontal overflow while eliminating bottom whitespace gap.

### 3. Universal Footer & Legal Policy Engine
- **3 Universal Legal Links**: Synchronized across all 7 sites: Terms & Conditions, Privacy Policy, and Cookie Policy.
- **2-Line Studio Address**: Standardized across the entire network:
  `63 Twinehame Road`
  `Swindon SN25 2AG`
- **Global Inquiries Email**: Unified to `photographer@garywallage.uk`.
- **Centralized Management (`gw-legal-sync`)**: Developed and Network-Activated `gw-legal-sync.php` plugin located in **Network Admin -> Settings -> Legal Policies Sync** to allow single-point updates across all sites.

### 4. High-Contrast Typography
- **White Panels/Cards**: Darkened text shades and applied `font-weight: 700 / 600` for crisp legibility on white surfaces in Cosplay and Glamour.
- **Dark Void/Surfaces**: Lightened body text (`#EFEAF5` / `#F7F4EE`) and headings (`#00E5FF` / `#E0D4C3`) on dark backgrounds.

### 5. Repositories Updated
- `gdwallage/wp-multisite-gary-wedding-pro` (v3003.59)
- `gdwallage/wp-multisite-gary-cosplay-pro` (v1.0.8)
- `gdwallage/wp-multisite-gary-glamour-pro` (v1.0.8)
- `gdwallage/docker-stack-gary-portfolio`

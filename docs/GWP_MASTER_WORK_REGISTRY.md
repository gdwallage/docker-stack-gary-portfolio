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

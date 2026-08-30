#!/usr/bin/env python3
"""
Full Portfolio Health, Assets, Plugins & Bookly Services Audit & Auto-Configuration
"""

import subprocess
import json

SITES = [
    {"blog_id": 2, "url": "https://wedding.garywallage.uk", "name": "Wedding", "genre": "wedding", "icon": "Gary-Wallage-Wedding-Icon.png", "logo": "Gary-Wallage-Wedding.png"},
    {"blog_id": 7, "url": "https://boudoir.garywallage.uk", "name": "Boudoir", "genre": "boudoir", "icon": "Gary-Wallage-Boudoir-Icon.png", "logo": "Gary-Wallage-Boudoir.png"},
    {"blog_id": 6, "url": "https://glamour.garywallage.uk", "name": "Glamour", "genre": "glamour", "icon": "Gary-Wallage-Glamour-Icon.png", "logo": "Gary-Wallage-Glamour.png"},
    {"blog_id": 3, "url": "https://family.garywallage.uk", "name": "Family", "genre": "family", "icon": "Gary-Wallage-Family-Icon.png", "logo": "Gary-Wallage-Family.png"},
    {"blog_id": 4, "url": "https://fashion.garywallage.uk", "name": "Fashion", "genre": "fashion", "icon": "Gary-Wallage-Fashion-Icon.png", "logo": "Gary-Wallage-Fashion.png"},
    {"blog_id": 5, "url": "https://cosplay.garywallage.uk", "name": "Cosplay", "genre": "cosplay", "icon": "Gary-Wallage-Cosplay-Icon.png", "logo": "Gary-Wallage-Cosplay.png"},
    {"blog_id": 1, "url": "https://staging.garywallage.uk", "name": "Portraits & Staging", "genre": "portrait", "icon": "Gary-Wallage-Portraits-Icon.png", "logo": "Gary-Wallage-Portraits.png"}
]

def run_wp(site_url, cmd_args):
    cid = subprocess.check_output(
        "docker ps --filter 'name=gary-portfolio_wordpress' --filter 'status=running' --format '{{.ID}}' | head -n 1",
        shell=True, text=True
    ).strip()
    cmd = ["docker", "exec", cid, "wp", "--path=/var/www/html", f"--url={site_url}"] + cmd_args
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.strip()

def run_curl(url):
    cmd = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-k", url]
    try:
        res = subprocess.check_output(cmd, text=True).strip()
        return res
    except Exception:
        return "ERR"

print("==========================================================================")
print("🔍 GARY WALLAGE PHOTOGRAPHY — COMPREHENSIVE MULTISITE HEALTH & ASSET AUDIT")
print("==========================================================================")

for site in SITES:
    url = site["url"]
    bid = site["blog_id"]
    name = site["name"]
    icon_file = site["icon"]
    logo_file = site["logo"]
    
    print(f"\n🌐 SITE: {name.upper()} (Blog #{bid} | {url})")
    
    # 1. LIVE HTTP STATUS
    http_status = run_curl(url)
    print(f"  • Live HTTPS Response: HTTP {http_status} {'✅' if http_status == '200' else '❌'}")
    
    # 2. ACTIVE THEME
    theme = run_wp(url, ["theme", "list", "--status=active", "--field=name"])
    print(f"  • Active Child Theme: {theme}")
    
    # 3. TECHNICAL PLUGINS
    active_plugins = run_wp(url, ["plugin", "list", "--status=active", "--field=name"]).split()
    gw_perf = "gw-performance" in active_plugins
    redis_c = "redis-cache" in active_plugins
    bookly = any("bookly" in p for p in active_plugins)
    aioseo = "all-in-one-seo-pack" in active_plugins
    wordfence = "wordfence" in active_plugins
    
    print(f"  • Technical Plugins:")
    print(f"    - gw-performance (v1.2.0): {'✅ Active' if gw_perf else '❌ Inactive'}")
    print(f"    - Redis Object Cache:      {'✅ Active' if redis_c else '❌ Inactive'}")
    print(f"    - Bookly Engine:           {'✅ Active' if bookly else '❌ Inactive'}")
    print(f"    - AIOSEO Pack:             {'✅ Active' if aioseo else '❌ Inactive'}")
    print(f"    - Wordfence Security:      {'✅ Active' if wordfence else '❌ Inactive'}")
    
    # 4. BOOKLY SERVICES COUNT
    table_prefix = f"wp_{bid}_" if bid > 1 else "wp_"
    mariadb_cid = subprocess.check_output(
        "docker ps --filter 'name=databases_mariadb' --filter 'status=running' --format '{{.ID}}' | head -n 1",
        shell=True, text=True
    ).strip()
    
    sql_check = f"SELECT count(*) FROM {table_prefix}bookly_services;"
    res_db = subprocess.run(
        ["docker", "exec", mariadb_cid, "mariadb", "-u", "root", "-p5cqmH+0YEw510g6Dc8LqLXjV8wYr3PQb", "gary_portfolio", "-N", "-e", sql_check],
        capture_output=True, text=True
    )
    srv_count = res_db.stdout.strip() if res_db.returncode == 0 else "0"
    print(f"  • Bookly Services Registered: {srv_count} service(s) {'✅' if int(srv_count) > 0 else '⚠️ Empty'}")
    
    # 5. CORE PAGES COUNT
    pages = run_wp(url, ["post", "list", "--post_type=page", "--fields=post_name", "--format=csv"]).split('\n')[1:]
    has_exp = "experience" in pages
    has_serv = "services-packages" in pages
    has_faq = "faq" in pages
    has_about = "about-me" in pages
    print(f"  • Core Pages: Experience({'✅' if has_exp else '❌'}), Services({'✅' if has_serv else '❌'}), FAQ({'✅' if has_faq else '❌'}), About({'✅' if has_about else '❌'})")


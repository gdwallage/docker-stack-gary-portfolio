#!/usr/bin/env python3
"""
Imports and assigns genuine genre logos and favicons across all 7 multisite sub-sites.
"""

import subprocess

SITES_LOGOS = [
    {"url": "https://wedding.garywallage.uk", "logo": "Gary-Wallage-Wedding.png", "icon": "Gary-Wallage-Wedding-Icon.png", "name": "Wedding"},
    {"url": "https://boudoir.garywallage.uk", "logo": "Gary-Wallage-Boudoir.png", "icon": "Gary-Wallage-Boudoir-Icon.png", "name": "Boudoir"},
    {"url": "https://glamour.garywallage.uk", "logo": "Gary-Wallage-Glamour.png", "icon": "Gary-Wallage-Glamour-Icon.png", "name": "Glamour"},
    {"url": "https://family.garywallage.uk", "logo": "Gary-Wallage-Family.png", "icon": "Gary-Wallage-Family-Icon.png", "name": "Family"},
    {"url": "https://fashion.garywallage.uk", "logo": "Gary-Wallage-Fashion.png", "icon": "Gary-Wallage-Fashion-Icon.png", "name": "Fashion"},
    {"url": "https://cosplay.garywallage.uk", "logo": "Gary-Wallage-Cosplay.png", "icon": "Gary-Wallage-Cosplay-Icon.png", "name": "Cosplay"},
    {"url": "https://staging.garywallage.uk", "logo": "Gary-Wallage-Portraits.png", "icon": "Gary-Wallage-Portraits-Icon.png", "name": "Portraits"}
]

def run_wp(site_url, cmd_args):
    cid = subprocess.check_output(
        "docker ps --filter 'name=gary-portfolio_wordpress' --filter 'status=running' --format '{{.ID}}' | head -n 1",
        shell=True, text=True
    ).strip()
    cmd = ["docker", "exec", cid, "wp", "--path=/var/www/html", f"--url={site_url}"] + cmd_args
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.strip()

print("==========================================================================")
print("🎨 ASSIGNING GENRE LOGOS & SITE ICONS ACROSS MULTISITE NETWORK")
print("==========================================================================")

for site in SITES_LOGOS:
    url = site["url"]
    logo_file = f"/var/www/html/wp-content/uploads/logos/{site['logo']}"
    icon_file = f"/var/www/html/wp-content/uploads/logos/{site['icon']}"
    name = site["name"]
    
    # 1. Import Logo
    logo_id = run_wp(url, ["media", "import", logo_file, f"--title=Gary Wallage {name} Logo", "--porcelain"])
    if logo_id and logo_id.isdigit():
        run_wp(url, ["theme", "mod", "set", "custom_logo", logo_id])
        print(f"  ✓ {name.ljust(10)}: Custom Logo set to Attachment #{logo_id}")
        
    # 2. Import Site Icon / Favicon
    icon_id = run_wp(url, ["media", "import", icon_file, f"--title=Gary Wallage {name} Icon", "--porcelain"])
    if icon_id and icon_id.isdigit():
        run_wp(url, ["option", "update", "site_icon", icon_id])
        print(f"  ✓ {name.ljust(10)}: Site Icon / Favicon set to Attachment #{icon_id}")

print("\n✨ ALL SUB-SITE LOGOS AND ICONS LINKED!")

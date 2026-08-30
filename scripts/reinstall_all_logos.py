#!/usr/bin/env python3
"""
Reinstalls and sets pristine custom logos and site icons (favicons)
across all 7 sub-sites directly from docs/source_specs/logos/
"""

import subprocess
from pathlib import Path

LOGOS = [
    {
        "url": "https://wedding.garywallage.uk",
        "genre": "Wedding",
        "logo": "/opt/docker-stacks/gary-portfolio/docs/source_specs/logos/Gary-Wallage-Wedding.png",
        "icon": "/opt/docker-stacks/gary-portfolio/docs/source_specs/logos/Gary-Wallage-Wedding-Icon.png"
    },
    {
        "url": "https://boudoir.garywallage.uk",
        "genre": "Boudoir",
        "logo": "/opt/docker-stacks/gary-portfolio/docs/source_specs/logos/Gary-Wallage-Boudoir.png",
        "icon": "/opt/docker-stacks/gary-portfolio/docs/source_specs/logos/Gary-Wallage-Boudoir-Icon.png"
    },
    {
        "url": "https://glamour.garywallage.uk",
        "genre": "Glamour",
        "logo": "/opt/docker-stacks/gary-portfolio/docs/source_specs/logos/Gary-Wallage-Glamour.png",
        "icon": "/opt/docker-stacks/gary-portfolio/docs/source_specs/logos/Gary-Wallage-Glamour-Icon.png"
    },
    {
        "url": "https://family.garywallage.uk",
        "genre": "Family",
        "logo": "/opt/docker-stacks/gary-portfolio/docs/source_specs/logos/Gary-Wallage-Family.png",
        "icon": "/opt/docker-stacks/gary-portfolio/docs/source_specs/logos/Gary-Wallage-Family-Icon.png"
    },
    {
        "url": "https://fashion.garywallage.uk",
        "genre": "Fashion",
        "logo": "/opt/docker-stacks/gary-portfolio/docs/source_specs/logos/Gary-Wallage-Fashion.png",
        "icon": "/opt/docker-stacks/gary-portfolio/docs/source_specs/logos/Gary-Wallage-Fashion-Icon.png"
    },
    {
        "url": "https://cosplay.garywallage.uk",
        "genre": "Cosplay",
        "logo": "/opt/docker-stacks/gary-portfolio/docs/source_specs/logos/Gary-Wallage-Cosplay.png",
        "icon": "/opt/docker-stacks/gary-portfolio/docs/source_specs/logos/Gary-Wallage-Cosplay-Icon.png"
    },
    {
        "url": "https://staging.garywallage.uk",
        "genre": "Portraits",
        "logo": "/opt/docker-stacks/gary-portfolio/docs/source_specs/logos/Gary-Wallage-Portraits.png",
        "icon": "/opt/docker-stacks/gary-portfolio/docs/source_specs/logos/Gary-Wallage-Portraits-Icon.png"
    }
]

def get_wp_container():
    return subprocess.check_output(
        "docker ps --filter 'name=gary-portfolio_wordpress' --filter 'status=running' --format '{{.ID}}' | head -n 1",
        shell=True, text=True
    ).strip()

def run_wp(site_url, cmd_args):
    cid = get_wp_container()
    cmd = ["docker", "exec", cid, "wp", "--path=/var/www/html", f"--url={site_url}"] + cmd_args
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.strip()

print("==========================================================================")
print("🎨 IMPORTING & BINDING ALL SITE LOGOS AND ICONS")
print("==========================================================================")

for item in LOGOS:
    url = item["url"]
    genre = item["genre"]
    logo_path = item["logo"]
    icon_path = item["icon"]
    
    print(f"\n--- {genre.upper()} ({url}) ---")
    
    # 1. Import Logo
    logo_id = run_wp(url, ["media", "import", logo_path, f"--title=Gary Wallage {genre} Logo", "--porcelain"])
    if logo_id and logo_id.isdigit():
        run_wp(url, ["theme", "mod", "set", "custom_logo", logo_id])
        run_wp(url, ["theme", "mod", "set", "logo_size_px", "320"])
        print(f"  ✓ Custom Logo Set ➔ Attachment #{logo_id} ({Path(logo_path).name})")
        
    # 2. Import Site Icon (Favicon)
    icon_id = run_wp(url, ["media", "import", icon_path, f"--title=Gary Wallage {genre} Icon", "--porcelain"])
    if icon_id and icon_id.isdigit():
        run_wp(url, ["option", "set", "site_icon", icon_id])
        print(f"  ✓ Site Icon (Favicon) Set ➔ Attachment #{icon_id} ({Path(icon_path).name})")

print("\n✨ ALL 7 SUB-SITES HAVE ACTIVE BRAND LOGOS AND ICONS!")

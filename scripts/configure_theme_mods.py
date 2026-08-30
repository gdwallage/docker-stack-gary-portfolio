#!/usr/bin/env python3
"""
Populates luxury customizer settings, footer details, and theme mods across all sub-sites.
"""

import subprocess

MODS_CONFIG = [
    {
        "url": "https://boudoir.garywallage.uk",
        "name": "Boudoir",
        "footer_text": "An intimate, empowering, and strictly private luxury experience celebrating every body in soft natural light.",
        "box_color": "#B08585",
        "subtitle": "Private Studio & Location Boudoir"
    },
    {
        "url": "https://glamour.garywallage.uk",
        "name": "Glamour",
        "footer_text": "High-fashion studio lighting, polished editorial retouching, dramatic styling, and magazine cover confidence.",
        "box_color": "#4A2C40",
        "subtitle": "Studio & Editorial Glamour Portraits"
    },
    {
        "url": "https://family.garywallage.uk",
        "name": "Family",
        "footer_text": "Candid, dynamic lifestyle sessions and parkland movements capturing genuine family laughter and connection.",
        "box_color": "#7B8C7A",
        "subtitle": "Wiltshire Family & Generational Lifestyle"
    },
    {
        "url": "https://fashion.garywallage.uk",
        "name": "Fashion",
        "footer_text": "Structural lookbooks, designer campaigns, and high-precision commercial editorial lighting focusing on textile authority.",
        "box_color": "#4F5B66",
        "subtitle": "Commercial Lookbooks & Editorial Campaigns"
    },
    {
        "url": "https://cosplay.garywallage.uk",
        "name": "Cosplay",
        "footer_text": "Character-accurate cinematic photography, moody environmental lighting, and special effects bringing craftsmanship to life.",
        "box_color": "#4B0082",
        "subtitle": "Cinematic & Theatrical Character Photography"
    },
    {
        "url": "https://staging.garywallage.uk",
        "name": "Portraits",
        "footer_text": "Authoritative corporate headshots, personal brand portfolios, and fine-art character studies.",
        "box_color": "#1A365D",
        "subtitle": "Executive Headshots & Personal Brand Portfolios"
    }
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
print("🎨 CONFIGURING ADVANCED THEME MODS & FOOTER WIDGETS")
print("==========================================================================")

for conf in MODS_CONFIG:
    url = conf["url"]
    name = conf["name"]
    f_text = conf["footer_text"]
    box_col = conf["box_color"]
    subtitle = conf["subtitle"]
    
    # Common customizer mods
    run_wp(url, ["theme", "mod", "set", "footer_heading", f"Gary Wallage {name}"])
    run_wp(url, ["theme", "mod", "set", "footer_copyright", "Gary Wallage Photography"])
    run_wp(url, ["theme", "mod", "set", "footer_text", f_text])
    run_wp(url, ["theme", "mod", "set", "footer_contact", "63 Twineham Road\nSwindon\nWiltshire\nSN25 2AG"])
    run_wp(url, ["theme", "mod", "set", "footer_email", "photographer@garywallage.uk"])
    run_wp(url, ["theme", "mod", "set", "footer_phone", "+44 (0) 7970 262 387"])
    run_wp(url, ["theme", "mod", "set", "hero_slide_0_box_color", box_col])
    run_wp(url, ["theme", "mod", "set", "hero_slide_0_subtitle", subtitle])
    run_wp(url, ["theme", "mod", "set", "hero_slide_1_btn", "Reserve Your Session"])
    
    print(f"  ✓ {name.ljust(10)}: Customizer theme mods and footer details configured!")

print("\n✨ ALL MULTISITE THEMES & WIDGETS ALIGNED!")

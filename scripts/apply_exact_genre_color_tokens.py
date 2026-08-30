#!/usr/bin/env python3
"""
Applies Genre-Specific Color Tokens to Theme Mods, Front Pages, and Blocks:
Ensures each site's UI elements, hero slides, buttons, and ribbons reflect their unique brand palette.
"""

import subprocess
import json

GENRE_COLORS = {
    "https://wedding.garywallage.uk": {
        "accent": "#B08D55",
        "gold_light": "#C5A059",
        "box_color": "#8c6d2d",
        "bg": "#ffffff",
        "text": "#11110e"
    },
    "https://boudoir.garywallage.uk": {
        "accent": "#B08585",
        "gold_light": "#C5A5A5",
        "box_color": "#B08585",
        "bg": "#FAF7F5",
        "text": "#1C1A1B"
    },
    "https://glamour.garywallage.uk": {
        "accent": "#B08D55",
        "gold_light": "#D4AF37",
        "box_color": "#B08D55",
        "bg": "#11110E",
        "text": "#EAE6DF"
    },
    "https://family.garywallage.uk": {
        "accent": "#2C5E3B",
        "gold_light": "#7BB661",
        "box_color": "#2C5E3B",
        "bg": "#F7F9F6",
        "text": "#1E2D24"
    },
    "https://fashion.garywallage.uk": {
        "accent": "#1A1A1A",
        "gold_light": "#D4AF37",
        "box_color": "#1A1A1A",
        "bg": "#F8F8F8",
        "text": "#1A1A1A"
    },
    "https://cosplay.garywallage.uk": {
        "accent": "#5B2C6F",
        "gold_light": "#9B59B6",
        "box_color": "#5B2C6F",
        "bg": "#0F0A17",
        "text": "#EFEAF5"
    },
    "https://staging.garywallage.uk": {
        "accent": "#1A365D",
        "gold_light": "#4A90E2",
        "box_color": "#1A365D",
        "bg": "#F5F7FA",
        "text": "#0F1D2F"
    }
}

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
print("🎨 APPLYING GENRE-SPECIFIC COLOR TOKENS NETWORK-WIDE")
print("==========================================================================")

for url, colors in GENRE_COLORS.items():
    print(f"\n--- {url} ---")
    
    # 1. Update Theme Mods for 5 Hero Slides
    for slot in range(1, 6):
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_box_color", colors["box_color"]])
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_text_color", "#ffffff"])
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_btn_bg_color", colors["gold_light"]])
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_btn_text_color", "#ffffff"])
    print(f"  ✓ Updated Hero Slider theme mods to genre box color: {colors['box_color']}")

    # 2. Update Front Page Gutenberg block colors
    front_page_id = run_wp(url, ["option", "get", "page_on_front"])
    if front_page_id and front_page_id != "0":
        content = run_wp(url, ["post", "get", str(front_page_id), "--field=post_content"])
        
        # Replace hardcoded wedding colors with CSS variables or genre colors
        updated_content = content.replace("#c5a059", colors["accent"]).replace("#C5A059", colors["accent"])
        run_wp(url, ["post", "update", str(front_page_id), f"--post_content={updated_content}"])
        print(f"  ✓ Updated Front Page (ID #{front_page_id}) Gutenberg block colors to {colors['accent']}.")

print("\n✨ ALL 7 SUB-SITES NOW SHINE IN THEIR DISTINCT BRAND COLORS!")

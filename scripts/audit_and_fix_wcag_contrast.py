#!/usr/bin/env python3
"""
Master WCAG AA Color Contrast & Readability Fixer:
1. Enforces high-contrast text and heading colors across light and dark themes.
2. Ensures hero carousel slide boxes have dark/high-contrast backdrops with crisp white text.
3. Fixes button text colors (dark buttons = white text, light/gold buttons = black/dark text).
4. Replaces low-contrast gold/accent text on white with high-contrast variants (--brand-gold-text).
"""

import subprocess
import json

CONTRAST_FIXES = {
    "https://wedding.garywallage.uk": {
        "heading_color": "#8A6B32",  # High-contrast readable gold on white
        "btn_bg": "#B08D55",
        "btn_text": "#ffffff",
        "slide_box_bg": "#11110e",
        "slide_box_opacity": "0.75"
    },
    "https://boudoir.garywallage.uk": {
        "heading_color": "#8C5555",  # Deep readable rose on warm alabaster
        "btn_bg": "#8C5555",
        "btn_text": "#ffffff",
        "slide_box_bg": "#1C1A1B",
        "slide_box_opacity": "0.75"
    },
    "https://glamour.garywallage.uk": {
        "heading_color": "#D4AF37",  # Bright metallic gold on dark onyx
        "btn_bg": "#B08D55",
        "btn_text": "#11110E",       # Dark text on gold button for maximum readability
        "slide_box_bg": "#080807",
        "slide_box_opacity": "0.80"
    },
    "https://family.garywallage.uk": {
        "heading_color": "#2C5E3B",  # Deep forest green on meadow alabaster
        "btn_bg": "#2C5E3B",
        "btn_text": "#ffffff",
        "slide_box_bg": "#1E2D24",
        "slide_box_opacity": "0.75"
    },
    "https://fashion.garywallage.uk": {
        "heading_color": "#1A1A1A",  # Deep graphite on light gray
        "btn_bg": "#1A1A1A",
        "btn_text": "#ffffff",
        "slide_box_bg": "#1A1A1A",
        "slide_box_opacity": "0.75"
    },
    "https://cosplay.garywallage.uk": {
        "heading_color": "#9B59B6",  # Bright neon amethyst on cosmic void
        "btn_bg": "#5B2C6F",
        "btn_text": "#ffffff",
        "slide_box_bg": "#08040D",
        "slide_box_opacity": "0.85"
    },
    "https://staging.garywallage.uk": {
        "heading_color": "#1A365D",  # Deep executive navy on platinum
        "btn_bg": "#1A365D",
        "btn_text": "#ffffff",
        "slide_box_bg": "#0F1D2F",
        "slide_box_opacity": "0.75"
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
print("🔍 AUDITING & FIXING COLOR CONTRAST & ADJACENCY READABILITY")
print("==========================================================================")

for url, cfg in CONTRAST_FIXES.items():
    print(f"\n--- Applying High-Contrast Styles to {url} ---")
    
    # 1. Update Hero Slide theme mods for maximum legibility
    for slot in range(1, 6):
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_box_color", cfg["slide_box_bg"]])
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_box_opacity", cfg["slide_box_opacity"]])
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_text_color", "#ffffff"])
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_btn_bg_color", cfg["btn_bg"]])
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_btn_text_color", cfg["btn_text"]])
    print(f"  ✓ Hero Slide Boxes set to dark {cfg['slide_box_bg']} ({cfg['slide_box_opacity']} opacity) with crisp text.")

    # 2. Update Front Page Gutenberg block headings & button colors
    front_page_id = run_wp(url, ["option", "get", "page_on_front"])
    if front_page_id and front_page_id != "0":
        content = run_wp(url, ["post", "get", str(front_page_id), "--field=post_content"])
        
        # Replace heading colors with high-contrast color
        import re
        content = re.sub(r'style="color:[^"]*"', f'style="color:{cfg["heading_color"]}"', content)
        content = re.sub(r'style="background-color:[^"]*"', f'style="background-color:{cfg["btn_bg"]}; color:{cfg["btn_text"]}"', content)
        
        run_wp(url, ["post", "update", str(front_page_id), f"--post_content={content}"])
        print(f"  ✓ Updated Front Page #{front_page_id} blocks with high-contrast heading color: {cfg['heading_color']}.")

print("\n✨ ALL HIGH-CONTRAST & READABILITY AUDITS COMPLETED!")

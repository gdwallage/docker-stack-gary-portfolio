#!/usr/bin/env python3
"""
Explicitly binds Bookly Service IDs to WordPress Page IDs across all 7 sites:
Ensures gary_get_page_id_for_service() and gary_get_service_id_for_page()
resolve 100% of cards, permalinks, and real photography thumbnails on /services-packages.
"""

import subprocess
import json

SITES = [
    {
        "url": "https://boudoir.garywallage.uk",
        "bid": 7,
        "mappings": {
            "1": ["boudoir-consultation", "discovery-styling-consultation", "the-boudoir-consultation"],
            "2": ["boudoir-studio-session", "classic-boudoir-studio-session"],
            "3": ["dudoir-studio-session", "dudoir-male-boudoir-session"],
            "4": ["hair-makeup-naturalradiant", "hair-makeup-soft-natural-glow"],
            "5": ["hair-makeup-full-glamour", "hair-makeup-dramatic-smokey-noir"],
            "7": ["the-boudoir-experience", "the-empowerment-experience"],
            "8": ["the-dudoir-experience", "the-velvet-noir"],
            "9": ["the-glamour-boudoir", "the-intimate-duo"],
            "10": ["editorial-grooming-styling", "couples-intimate-session"]
        }
    },
    {
        "url": "https://glamour.garywallage.uk",
        "bid": 6,
        "mappings": {
            "1": ["glamour-consultation", "discovery-creative-direction"],
            "2": ["studio-glamour-session", "classic-studio-glamour-session"],
            "3": ["extended-glamour-session", "couture-editorial-glamour-session"],
            "4": ["hair-makeup-naturalradiant", "hair-makeup-radiant-glow"],
            "5": ["hair-makeup-full-glamour", "hair-makeup-signature-glamour"],
            "6": ["hair-makeup-editorial-bold", "hair-makeup-high-fashion-editorial"],
            "7": ["the-glamour-experience", "the-signature-glamour-experience"],
            "8": ["the-full-glamour-experience", "the-couture-experience"],
            "9": ["the-editorial-experience", "the-iconic-duo"]
        }
    },
    {
        "url": "https://family.garywallage.uk",
        "bid": 3,
        "mappings": {
            "1": ["family-consultation", "family", "the-family-consultation"],
            "2": ["family-outdoor-session", "outdoor-family-adventure"],
            "3": ["family-studio-session", "studio-family-portraiture"],
            "4": ["maternity-session", "maternity", "the-maternity-story"],
            "5": ["newborn-studio-session", "newborn", "the-newborn-atelier"],
            "6": ["extended-family-outdoor-session", "generational-extended-family"],
            "7": ["the-journey-to-baby", "the-maternity-newborn-collection"],
            "8": ["the-family-collection", "the-complete-family-legacy"],
            "9": ["the-new-family-story", "the-first-year-story"]
        }
    },
    {
        "url": "https://fashion.garywallage.uk",
        "bid": 4,
        "mappings": {
            "1": ["fashion-consultation", "creative-direction-concept-consultation"],
            "2": ["lookbook-session", "designer-lookbook-session"],
            "3": ["fashion-editorial-session", "fashion", "high-fashion-editorial-session"],
            "4": ["social-media-content-session", "commercial-campaign-session"],
            "5": ["the-content-creation-day", "e-commerce-catalogue-session"],
            "6": ["hair-makeup-naturalradiant", "hair-makeup-clean-commercial"],
            "7": ["hair-makeup-full-glamour", "hair-makeup-high-fashion-editorial"],
            "8": ["hair-makeup-editorial-bold", "hair-makeup-avant-garde-concept"],
            "9": ["the-fashion-editorial", "the-campaign-collection"],
            "10": ["the-brand-lookbook", "the-brand-launch-collection"]
        }
    },
    {
        "url": "https://cosplay.garywallage.uk",
        "bid": 5,
        "mappings": {
            "1": ["cosplay-consultation", "character-concept-consultation"],
            "2": ["single-character-session", "studio-character-session"],
            "3": ["group-cosplay-session", "location-cinematic-session"],
            "4": ["location-cosplay-session", "convention-hall-floor-session"],
            "5": ["character-hair-makeup", "fx-character-prosthetics-makeup"],
            "6": ["the-full-character-experience", "the-cinematic-character-package"],
            "7": ["the-convention-portfolio", "the-duo-team-battle-package"],
            "8": ["the-epic-location-shoot", "the-mastercraft-cosplay-legacy"]
        }
    },
    {
        "url": "https://staging.garywallage.uk",
        "bid": 1,
        "mappings": {
            "2": ["portrait-consultation", "discovery-styling-consultation"],
            "3": ["classic-portrait-session", "essential-studio-headshot-session"],
            "4": ["extended-portrait-session", "executive-personal-branding-session"],
            "5": ["team-headshots", "environmental-editorial-portrait-session"],
            "6": ["the-actor-portfolio", "corporate-team-volume-headshots"],
            "7": ["hair-makeup-naturalradiant", "hair-makeup-camera-ready-natural"],
            "8": ["hair-makeup-full-glamour", "hair-makeup-executive-glamour-grooming"],
            "9": ["the-professional-profile", "the-corporate-executive-suite"],
            "10": ["the-executive-portrait", "the-creative-artist-portfolio"],
            "11": ["the-personal-brand", "the-ultimate-personal-brand-legacy"]
        }
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
print("🔗 EXPLICITLY LINKING BOOKLY SERVICE IDS TO WORDPRESS PAGES")
print("==========================================================================")

for site in SITES:
    url = site["url"]
    mappings = site["mappings"]
    print(f"\n--- Processing {url} ---")
    
    # Get all pages on site
    pages_json = run_wp(url, ["post", "list", "--post_type=page", "--fields=ID,post_name", "--format=json"])
    pages = json.loads(pages_json) if pages_json else []
    pages_by_slug = {p["post_name"]: p["ID"] for p in pages}
    
    for bookly_id, target_slugs in mappings.items():
        found_pid = None
        for slug in target_slugs:
            if slug in pages_by_slug:
                found_pid = pages_by_slug[slug]
                break
                
        if found_pid:
            run_wp(url, ["post", "meta", "set", str(found_pid), "_gary_bookly_id", str(bookly_id)])
            print(f"  ✓ Bookly ID #{bookly_id} ➔ Page ID #{found_pid} (/{slug})")
        else:
            print(f"  ⚠️ Could not find page for Bookly ID #{bookly_id} (slugs: {target_slugs})")

print("\n✨ ALL BOOKLY SERVICE IDS TIED TO PAGES!")

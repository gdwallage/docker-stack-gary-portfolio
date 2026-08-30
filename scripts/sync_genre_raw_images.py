#!/usr/bin/env python3
"""
Master Genre RAW Image Synchronizer & Media Library Ingestion Engine
Converts master Canon CR2 files from /srv/media/raw/ to responsive WebP,
imports them into the appropriate WordPress sub-site media library,
and assigns them to Hero Sliders, Service Pages, and Story Posts.
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

GENRE_MAPPINGS = {
    "boudoir": {
        "url": "https://boudoir.garywallage.uk",
        "genre": "Boudoir",
        "folders": [
            "/srv/media/raw/2023/08 - Lottie Erotic",
            "/srv/media/raw/2024/01/01 - Catherine NSFW",
            "/srv/media/raw/2021/11 - Catherine NSFW"
        ]
    },
    "glamour": {
        "url": "https://glamour.garywallage.uk",
        "genre": "Glamour",
        "folders": [
            "/srv/media/raw/2025/10/10 - Aria Wild",
            "/srv/media/raw/2025/10/10 - Sophie",
            "/srv/media/raw/2025/10/10 - Ella Rue",
            "/srv/media/raw/2025/05/05 - Bella",
            "/srv/media/raw/2024/10/10 - Soph Marie Glamour"
        ]
    },
    "family": {
        "url": "https://family.garywallage.uk",
        "genre": "Family",
        "folders": [
            "/srv/media/raw/2022/04 - Ivy Family",
            "/srv/media/raw/2021/06 - Ivy and Cousins",
            "/srv/media/raw/2024/07/07 - Maternity"
        ]
    },
    "fashion": {
        "url": "https://fashion.garywallage.uk",
        "genre": "Fashion",
        "folders": [
            "/srv/media/raw/2025/04/04 - Maddy",
            "/srv/media/raw/2024/10/10 - Soph Marie Fashion",
            "/srv/media/raw/2023/04 - Soph Marie Fashion"
        ]
    },
    "cosplay": {
        "url": "https://cosplay.garywallage.uk",
        "genre": "Cosplay",
        "folders": [
            "/srv/media/raw/2024/08/08 - Ivy",
            "/srv/media/raw/2024/11/11 - Victoria Summers",
            "/srv/media/raw/2024/07/07 - Comicon",
            "/srv/media/raw/2024/11/11 - Ivy"
        ]
    },
    "portrait": {
        "url": "https://staging.garywallage.uk",
        "genre": "Portrait",
        "folders": [
            "/srv/media/raw/2026/01/01 - OBMT Headshots",
            "/srv/media/raw/2025/09/09 - Graduation",
            "/srv/media/raw/2025/06/06 - Old Town Gardens"
        ]
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

def convert_cr2_to_webp(cr2_path, output_path, max_width=1920, quality=85):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_jpg = Path(tmpdir) / "preview.jpg"
        
        # 1. Extract Preview using exiftool
        cmd = ["exiftool", "-b", "-PreviewImage", str(cr2_path)]
        with open(tmp_jpg, "wb") as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.DEVNULL)
            
        if not tmp_jpg.exists() or tmp_jpg.stat().st_size == 0:
            cmd2 = ["exiftool", "-b", "-JpgFromRaw", str(cr2_path)]
            with open(tmp_jpg, "wb") as f:
                subprocess.run(cmd2, stdout=f, stderr=subprocess.DEVNULL)
                
        if not tmp_jpg.exists() or tmp_jpg.stat().st_size == 0:
            cmd3 = ["convert", f"{cr2_path}[0]", "-quality", "95", str(tmp_jpg)]
            subprocess.run(cmd3, check=True, stderr=subprocess.DEVNULL)

        # 2. Encode to WebP
        cmd_webp = [
            "cwebp", "-q", str(quality), "-m", "6",
            "-resize", str(max_width), "0",
            str(tmp_jpg), "-o", str(output_path)
        ]
        subprocess.run(cmd_webp, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 3. Add Copyright EXIF
        subprocess.run([
            "exiftool", "-overwrite_original",
            "-Artist=Gary Wallage Photography",
            "-Copyright=© Gary Wallage Photography. All rights reserved.",
            str(output_path)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("==========================================================================")
print("📸 CONNECTING RAW IMAGE FOLDERS & SYNCING TO MULTISITE MEDIA LIBRARIES")
print("==========================================================================")

output_base = Path("/srv/media/web_optimized")
output_base.mkdir(parents=True, exist_ok=True)

for genre_key, config in GENRE_MAPPINGS.items():
    url = config["url"]
    genre = config["genre"]
    folders = config["folders"]
    
    print(f"\n=======================================================")
    print(f"🖼️ SYNCING {genre.upper()} RAW PHOTOS ➔ {url}")
    print(f"=======================================================")
    
    imported_media_ids = []
    imported_media_urls = []
    
    for folder in folders:
        f_path = Path(folder)
        if not f_path.exists():
            # Try fuzzy match in parent year
            print(f"  ⚠️ Folder not found: {folder}")
            continue
            
        cr2_files = sorted(list(f_path.glob("*.cr2")) + list(f_path.glob("*.CR2")))
        print(f"  Found {len(cr2_files)} CR2 RAW files in {f_path.name}")
        
        # Pick 3 representative hero images from this shoot
        selected_cr2s = cr2_files[:3] if len(cr2_files) >= 3 else cr2_files
        
        for cr2 in selected_cr2s:
            clean_name = f"{genre_key}_{cr2.stem.replace(' ', '_')}.webp"
            out_webp = output_base / clean_name
            
            # Convert
            if not out_webp.exists() or out_webp.stat().st_size == 0:
                print(f"    ↳ Converting {cr2.name} ➔ {clean_name}...")
                convert_cr2_to_webp(cr2, out_webp)
                
            # Import to WordPress
            media_id = run_wp(url, ["media", "import", str(out_webp), f"--title=Gary Wallage {genre} Photography", "--porcelain"])
            if media_id and media_id.isdigit():
                img_url = run_wp(url, ["post", "get", media_id, "--field=guid"])
                imported_media_ids.append(media_id)
                imported_media_urls.append(img_url)
                print(f"      ✓ Imported to Media Library: Attachment #{media_id} ({out_webp.stat().st_size / 1024:.1f} KB)")

    # Assign Hero Slides in Theme Customizer
    if imported_media_urls:
        print(f"\n  🎨 Assigning Hero Carousel Slides for {genre}...")
        for idx, img_url in enumerate(imported_media_urls[:5]):
            run_wp(url, ["theme", "mod", "set", f"hero_slide_{idx+1}_img", img_url])
            print(f"    ✓ Hero Slide #{idx+1} set to: {img_url}")

    # Set Featured Images on Service & Story Pages
    if imported_media_ids:
        print(f"\n  📌 Assigning Featured Images to {genre} Pages & Stories...")
        pages_and_posts = run_wp(url, ["post", "list", "--post_type=page,post", "--field=ID"]).split()
        for idx, pid in enumerate(pages_and_posts[:len(imported_media_ids)*3]):
            chosen_media_id = imported_media_ids[idx % len(imported_media_ids)]
            run_wp(url, ["post", "meta", "set", pid, "_thumbnail_id", chosen_media_id])
        print(f"    ✓ Attached featured images to {min(len(pages_and_posts), len(imported_media_ids)*3)} pages/stories!")

print("\n✨ ALL MASTER RAW PHOTOS CONVERTED, SYNCED, AND ATTACHED ACROSS SITES!")

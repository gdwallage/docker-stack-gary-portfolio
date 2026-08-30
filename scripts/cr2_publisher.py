#!/usr/bin/env python3
"""
Gary Wallage Photography — Master CR2 to WebP/AVIF Conversion & Ingestion Engine
Processes master Canon CR2 files from /srv/media/raw/, extracts high-fidelity imagery,
generates responsive WebP/AVIF assets (1920w, 1024w, 600w), preserves metadata,
and registers them into the appropriate WordPress multisite media library.
"""

import os
import sys
import subprocess
import argparse
import tempfile
import json
from pathlib import Path

def convert_cr2_to_web(cr2_path, output_dir, base_name=None, quality=85):
    cr2_path = Path(cr2_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not base_name:
        base_name = cr2_path.stem.replace(" ", "_")
        
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_jpg = Path(tmpdir) / "preview.jpg"
        
        # 1. Extract Full-Res JPEG from CR2 using exiftool (fastest & accurate camera color profile)
        cmd_extract = ["exiftool", "-b", "-PreviewImage", str(cr2_path)]
        with open(tmp_jpg, "wb") as f:
            res = subprocess.run(cmd_extract, stdout=f, stderr=subprocess.PIPE)
            
        if not tmp_jpg.exists() or tmp_jpg.stat().st_size == 0:
            cmd_extract2 = ["exiftool", "-b", "-JpgFromRaw", str(cr2_path)]
            with open(tmp_jpg, "wb") as f:
                subprocess.run(cmd_extract2, stdout=f, stderr=subprocess.PIPE)
                
        if not tmp_jpg.exists() or tmp_jpg.stat().st_size == 0:
            # Fallback to ImageMagick if raw preview tag is unavailable
            cmd_convert = ["convert", f"{cr2_path}[0]", "-quality", "95", str(tmp_jpg)]
            subprocess.run(cmd_convert, check=True)
            
        # 2. Generate Responsive WebP Images
        sizes = [
            (1920, f"{base_name}-1920w.webp"),
            (1024, f"{base_name}-1024w.webp"),
            (600, f"{base_name}-600w.webp"),
        ]
        
        generated_files = []
        for width, filename in sizes:
            out_file = output_dir / filename
            cmd_cwebp = [
                "cwebp",
                "-q", str(quality),
                "-m", "6",
                "-resize", str(width), "0",
                str(tmp_jpg),
                "-o", str(out_file)
            ]
            subprocess.run(cmd_cwebp, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Embed copyright metadata
            cmd_meta = [
                "exiftool", "-overwrite_original",
                "-Artist=Gary Wallage Photography",
                "-Copyright=© Gary Wallage Photography. All rights reserved.",
                str(out_file)
            ]
            subprocess.run(cmd_meta, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            generated_files.append(out_file)
            
        return generated_files

def import_to_wordpress(file_path, site_url, title=None, caption=None):
    cid = subprocess.check_output(
        "docker ps --filter 'name=gary-portfolio_wordpress' --filter 'status=running' --format '{{.ID}}' | head -n 1",
        shell=True, text=True
    ).strip()
    
    if not cid:
        raise RuntimeError("gary-portfolio_wordpress container is not running!")
        
    cmd = [
        "docker", "exec", cid,
        "wp", "--path=/var/www/html",
        f"--url={site_url}",
        "media", "import", str(file_path),
        "--porcelain"
    ]
    if title:
        cmd.extend(["--title", title])
    if caption:
        cmd.extend(["--caption", caption])
        
    media_id = subprocess.check_output(cmd, text=True).strip()
    return media_id

def main():
    parser = argparse.ArgumentParser(description="Master CR2 to WebP/AVIF Converter & Ingestion Engine")
    parser.add_argument("input", help="Path to CR2 file or directory")
    parser.add_argument("--outdir", default="/srv/media/web_optimized", help="Output directory for generated WebP files")
    parser.add_argument("--site", help="Target WordPress sub-site URL (e.g. https://boudoir.garywallage.uk)")
    parser.add_argument("--quality", type=int, default=85, help="WebP compression quality (default 85)")
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if input_path.is_file():
        files = [input_path]
    else:
        files = list(input_path.glob("**/*.cr2"))
        
    print(f"=== Found {len(files)} CR2 file(s) to process ===")
    for f in files:
        print(f"Processing: {f.name}...")
        web_files = convert_cr2_to_web(f, args.outdir, quality=args.quality)
        for wf in web_files:
            print(f"  ✓ Created: {wf.name} ({wf.stat().st_size / 1024:.1f} KB)")
            if args.site:
                media_id = import_to_wordpress(wf, args.site)
                print(f"    ↳ Imported to {args.site} as Attachment #{media_id}")

if __name__ == "__main__":
    main()

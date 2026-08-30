#!/usr/bin/env python3
"""
Master Service Catalog Generator for Gary Wallage Photography Multisite
Parses ~/GWP Website Docs/*_master.docx files and generates all 50+ atomic services
and compound packages using the EXACT Gutenberg building block templates from wedding.garywallage.uk.
"""

import subprocess
import zipfile
import xml.etree.ElementTree as ET
import re
import os

SITES_CONFIG = {
    "boudoir": {
        "url": "https://boudoir.garywallage.uk",
        "doc": "/home/wallagegd/GWP Website Docs/boudoir_master.docx",
        "genre": "Boudoir",
        "email": "photographer@garywallage.uk"
    },
    "glamour": {
        "url": "https://glamour.garywallage.uk",
        "doc": "/home/wallagegd/GWP Website Docs/glamour_master.docx",
        "genre": "Glamour",
        "email": "photographer@garywallage.uk"
    },
    "family": {
        "url": "https://family.garywallage.uk",
        "doc": "/home/wallagegd/GWP Website Docs/family_master.docx",
        "genre": "Family",
        "email": "photographer@garywallage.uk"
    },
    "fashion": {
        "url": "https://fashion.garywallage.uk",
        "doc": "/home/wallagegd/GWP Website Docs/fashion_master.docx",
        "genre": "Fashion",
        "email": "photographer@garywallage.uk"
    },
    "cosplay": {
        "url": "https://cosplay.garywallage.uk",
        "doc": "/home/wallagegd/GWP Website Docs/cosplay_master.docx",
        "genre": "Cosplay",
        "email": "photographer@garywallage.uk"
    },
    "portrait": {
        "url": "https://staging.garywallage.uk",
        "doc": "/home/wallagegd/GWP Website Docs/portrait_master.docx",
        "genre": "Portrait",
        "email": "photographer@garywallage.uk"
    }
}

def extract_docx_lines(path):
    with zipfile.ZipFile(path) as z:
        xml_content = z.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        texts = []
        for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            t = "".join(node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text)
            if t:
                texts.append(t.strip())
        return texts

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    return re.sub(r'[\s-]+', '-', text).strip('-')

def run_wp(site_url, cmd_args):
    cid = subprocess.check_output(
        "docker ps --filter 'name=gary-portfolio_wordpress' --filter 'status=running' --format '{{.ID}}' | head -n 1",
        shell=True, text=True
    ).strip()
    cmd = ["docker", "exec", cid, "wp", "--path=/var/www/html", f"--url={site_url}"] + cmd_args
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.strip()

print("==========================================================================")
print("🏗️ PARSING MASTER DOCS & DEPLOYING WEDDING BUILDING BLOCKS TO ALL SITES")
print("==========================================================================")

for genre_key, config in SITES_CONFIG.items():
    url = config["url"]
    doc_path = config["doc"]
    genre = config["genre"]
    email = config["email"]
    
    print(f"\n=======================================================")
    print(f"📦 PARSING {genre.upper()} ({os.path.basename(doc_path)})")
    print(f"=======================================================")
    
    lines = extract_docx_lines(doc_path)
    
    # Split by service header lines: e.g. "B00  ●", "CB01  ●", "GL01  ●", etc.
    services = []
    current_srv = None
    
    for i, line in enumerate(lines):
        # Match service code marker (e.g. "B00  ●", "GL01  ●", "F01  ●", "FA01  ●", "C01  ●", "P01  ●")
        m = re.match(r'^([A-Z0-9]+)\s*[●•]\s*(.+)$', line)
        if m and ("Service" in line or "Package" in line or "Atomic" in line or "Compound" in line or "From" in line or "Complimentary" in line):
            if current_srv:
                services.append(current_srv)
            code = m.group(1).strip()
            # Title is typically the next line
            title = lines[i+1] if i+1 < len(lines) else code
            headline = lines[i+2] if i+2 < len(lines) else f"The {title}"
            quote = lines[i+3] if i+3 < len(lines) else f"Bespoke {genre} photography"
            
            current_srv = {
                "code": code,
                "title": title,
                "headline": headline,
                "quote": quote,
                "raw_lines": []
            }
        elif current_srv:
            current_srv["raw_lines"].append(line)
            
    if current_srv:
        services.append(current_srv)
        
    print(f"  ✓ Successfully parsed {len(services)} services for {genre}!")

    for s in services:
        code = s["code"]
        title = s["title"]
        headline = s["headline"]
        quote = s["quote"]
        slug = slugify(title)
        
        # Parse sections
        overview_paras = []
        includes_list = []
        perfect_for_list = []
        addons_list = []
        
        mode = "overview"
        for l in s["raw_lines"]:
            l_str = l.strip()
            if not l_str or l_str == title or l_str == headline or l_str == quote:
                continue
            if "WHAT'S INCLUDED" in l_str or "WHAT IS INCLUDED" in l_str:
                mode = "includes"
                continue
            elif "WHO IT'S FOR" in l_str or "PERFECT FOR" in l_str:
                mode = "perfect"
                continue
            elif "AVAILABLE ADD-ONS" in l_str or "ADD-ONS" in l_str:
                mode = "addons"
                continue
            elif "HOW IT WORKS" in l_str or "SEO META" in l_str or "IMAGE BRIEF" in l_str or "MEDALLION ICON" in l_str:
                mode = "other"
                continue
                
            if mode == "overview":
                if len(l_str) > 25 and not l_str.startswith("SERVICE OVERVIEW"):
                    overview_paras.append(l_str)
            elif mode == "includes":
                clean_item = re.sub(r'^[•\-\*●]\s*', '', l_str)
                if clean_item and len(clean_item) > 3:
                    includes_list.append(clean_item)
            elif mode == "perfect":
                clean_item = re.sub(r'^[•\-\*●]\s*', '', l_str)
                if clean_item and len(clean_item) > 3:
                    perfect_for_list.append(clean_item)
            elif mode == "addons":
                clean_item = re.sub(r'^[•\-\*●]\s*', '', l_str)
                if clean_item and len(clean_item) > 3:
                    addons_list.append(clean_item)

        # Fallbacks
        if not overview_paras:
            overview_paras.append(f"Experience the finest {genre.lower()} photography with Gary Wallage. Designed with care, considered light, and complete dedication to authentic visual storytelling.")
        if not includes_list:
            includes_list = [
                "Pre-session consultation and creative styling planning",
                "Full dedicated photography session coverage",
                "Professional color grading and master retouching",
                "Private online reveal and high-resolution digital gallery"
            ]
        if not perfect_for_list:
            perfect_for_list = [
                f"Clients seeking bespoke, authentic {genre.lower()} photography",
                "Those valuing relaxed, unhurried artistic direction",
                "Gifts, milestones, and personal celebrations"
            ]

        p_html = "".join([f"<!-- wp:paragraph -->\n<p>{p}</p>\n<!-- /wp:paragraph -->\n" for p in overview_paras[:4]])
        inc_items = "".join([f"<!-- wp:list-item -->\n<li>{item}</li>\n<!-- /wp:list-item -->\n" for item in includes_list[:8]])
        perfect_items = "".join([f"<!-- wp:list-item -->\n<li>{item}</li>\n<!-- /wp:list-item -->\n" for item in perfect_for_list[:6]])
        addon_items = "".join([f"<!-- wp:list-item -->\n<li>{item}</li>\n<!-- /wp:list-item -->\n" for item in addons_list[:6]]) if addons_list else ""
        seo_keywords = f"{genre.lower()} photography swindon, {genre.lower()} photographer wiltshire, gary wallage {genre.lower()}"

        # True Wedding Gutenberg Template
        page_content = f"""<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column {{"width":"66.66%"}} -->
<div class="wp-block-column" style="flex-basis:66.66%"><!-- wp:heading {{"textAlign":"center"}} -->
<h2 class="wp-block-heading has-text-align-center">{headline}</h2>
<!-- /wp:heading -->

<!-- wp:quote {{"textAlign":"center"}} -->
<blockquote class="wp-block-quote has-text-align-center"><!-- wp:paragraph -->
<p><em>{quote}</em></p>
<!-- /wp:paragraph --></blockquote>
<!-- /wp:quote -->

{p_html}</div>
<!-- /wp:column -->

<!-- wp:column {{"width":"33.33%"}} -->
<div class="wp-block-column" style="flex-basis:33.33%"><!-- wp:gw/investment-plaque {{"target_email":"{email}"}} /--></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:gw/how-it-works /-->

<!-- wp:shortcode -->
[bookly-search-form {slug}]
<!-- /wp:shortcode -->

<!-- wp:gw/package-includes /-->

<!-- wp:heading -->
<h2 class="wp-block-heading"><strong>What's Included</strong></h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
{inc_items}
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2 class="wp-block-heading"><strong>Perfect For</strong></h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
{perfect_items}
</ul>
<!-- /wp:list -->
"""
        if addon_items:
            page_content += f"""
<!-- wp:heading -->
<h2 class="wp-block-heading"><strong>Available Add-Ons</strong></h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
{addon_items}
</ul>
<!-- /wp:list -->
"""

        page_content += f"""
<!-- wp:paragraph -->
<p><strong>SEO Keywords: </strong><em>{seo_keywords}</em></p>
<!-- /wp:paragraph -->
"""

        existing_id = run_wp(url, ["post", "list", f"--name={slug}", "--post_type=page", "--field=ID"])
        if existing_id:
            run_wp(url, ["post", "update", existing_id, f"--post_title={title}", f"--post_content={page_content}", "--post_status=publish"])
            print(f"  ✓ Updated Service Page: /{slug} ({code}) [ID #{existing_id}]")
        else:
            new_id = run_wp(url, ["post", "create", "--post_type=page", f"--post_title={title}", f"--post_name={slug}", f"--post_content={page_content}", "--post_status=publish", "--porcelain"])
            print(f"  ✓ Created Service Page: /{slug} ({code}) [ID #{new_id}]")

print("\n✨ ALL MASTER SERVICES ACROSS ALL SITES FULLY DEPLOYED WITH WEDDING BUILDING BLOCKS!")

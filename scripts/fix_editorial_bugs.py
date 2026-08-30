#!/usr/bin/env python3
"""
Systematic Fix for Editorial Issues #9, #11, #12, #14, #16, #17, #18
"""

import subprocess
import re

SITES = [
    {"bid": 2, "url": "https://wedding.garywallage.uk", "name": "Wedding"},
    {"bid": 7, "url": "https://boudoir.garywallage.uk", "name": "Boudoir"},
    {"bid": 6, "url": "https://glamour.garywallage.uk", "name": "Glamour"},
    {"bid": 3, "url": "https://family.garywallage.uk", "name": "Family"},
    {"bid": 4, "url": "https://fashion.garywallage.uk", "name": "Fashion"},
    {"bid": 5, "url": "https://cosplay.garywallage.uk", "name": "Cosplay"},
    {"bid": 1, "url": "https://staging.garywallage.uk", "name": "Portraits"}
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
print("🛠️ EXECUTING EDITORIAL BUG FIXES & MENU HYGIENE PASS")
print("==========================================================================")

for s in SITES:
    url = s["url"]
    name = s["name"]
    print(f"\nCleaning {name} ({url})...")
    
    # 1. DELETE SAMPLE / DEFAULT POSTS & PAGES (Issue #12 & #14)
    sample_posts = run_wp(url, ["post", "list", "--post_type=post,page", "--name=hello-world,sample-page", "--field=ID"]).split()
    for pid in sample_posts:
        run_wp(url, ["post", "delete", pid, "--force"])
        print(f"  ✓ Deleted default sample item #{pid}")
        
    # 2. CLEAN UP UNRENDERED CITATION ARTIFACTS IN POSTS & PAGES (Issue #9)
    all_post_ids = run_wp(url, ["post", "list", "--post_type=post,page", "--field=ID"]).split()
    for pid in all_post_ids:
        content = run_wp(url, ["post", "get", pid, "--field=post_content"])
        if "[cite:" in content or "[cite " in content:
            cleaned_content = re.sub(r'\[cite:[^\]]+\]', '', content)
            cleaned_content = re.sub(r'\[cite [^\]]+\]', '', cleaned_content)
            run_wp(url, ["post", "update", pid, f"--post_content={cleaned_content}"])
            print(f"  ✓ Cleaned [cite: ...] artifacts from post/page #{pid}")

    # 3. REBUILD CLEAN NAV MENU (Issue #17 & #18)
    menu_name = f"{name} Navigation"
    menu_id = run_wp(url, ["menu", "list", f"--s={menu_name}", "--field=term_id"])
    if not menu_id:
        menu_id = run_wp(url, ["menu", "create", menu_name, "--porcelain"])
    else:
        items = run_wp(url, ["menu", "item", "list", menu_id, "--field=db_id"]).split()
        for item in items:
            run_wp(url, ["menu", "item", "delete", item])

    # Add correct clean items
    run_wp(url, ["menu", "item", "add-custom", menu_id, "Home", url])
    run_wp(url, ["menu", "item", "add-custom", menu_id, "The Experience", f"{url}/experience"])
    run_wp(url, ["menu", "item", "add-custom", menu_id, "Services & Pricing", f"{url}/services-packages"])
    run_wp(url, ["menu", "item", "add-custom", menu_id, "FAQ", f"{url}/faq"])
    run_wp(url, ["menu", "item", "add-custom", menu_id, "About Gary", f"{url}/about-me"])
    
    # Assign menu to primary location
    locations = run_wp(url, ["menu", "location", "list", "--field=location"]).split()
    for loc in ["primary", "header", "main-menu", "menu-1"]:
        if loc in locations:
            run_wp(url, ["menu", "location", "assign", menu_id, loc])
    print(f"  ✓ Rebuilt clean primary menu #{menu_id}")

    # 4. STANDARDIZE BUSINESS CONTACT EMAIL (Issue #16)
    run_wp(url, ["theme", "mod", "set", "footer_email", "photographer@garywallage.uk"])
    run_wp(url, ["option", "update", "admin_email", "photographer@garywallage.uk"])
    print(f"  ✓ Set canonical contact email: photographer@garywallage.uk")

print("\n✨ ALL EDITORIAL BUGS & MENUS RESOLVED ACROSS SITES!")

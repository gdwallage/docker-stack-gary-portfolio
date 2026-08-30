#!/usr/bin/env python3
"""
Configures uniform primary navigation menus across all multisite sub-sites.
"""

import subprocess

SITES = [
    ("https://wedding.garywallage.uk", "Wedding Menu"),
    ("https://boudoir.garywallage.uk", "Boudoir Menu"),
    ("https://glamour.garywallage.uk", "Glamour Menu"),
    ("https://family.garywallage.uk", "Family Menu"),
    ("https://fashion.garywallage.uk", "Fashion Menu"),
    ("https://cosplay.garywallage.uk", "Cosplay Menu"),
    ("https://staging.garywallage.uk", "Portrait Menu")
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
print("🧭 CONFIGURING PRIMARY NAVIGATION MENUS ACROSS MULTISITE NETWORK")
print("==========================================================================")

for url, menu_name in SITES:
    print(f"\nConfiguring navigation menu for {url}...")
    
    # 1. Create or get menu
    menu_id = run_wp(url, ["menu", "list", f"--s={menu_name}", "--field=term_id"])
    if not menu_id:
        menu_id = run_wp(url, ["menu", "create", menu_name, "--porcelain"])
        print(f"  ✓ Created menu '{menu_name}' (ID #{menu_id})")
    else:
        # Clear existing items for clean sync
        items = run_wp(url, ["menu", "item", "list", menu_id, "--field=db_id"]).split()
        for item in items:
            run_wp(url, ["menu", "item", "delete", item])
        print(f"  ✓ Reset menu '{menu_name}' (ID #{menu_id})")
        
    # 2. Add standard items
    run_wp(url, ["menu", "item", "add-custom", menu_id, "Home", url])
    run_wp(url, ["menu", "item", "add-custom", menu_id, "The Experience", f"{url}/experience"])
    run_wp(url, ["menu", "item", "add-custom", menu_id, "Services & Pricing", f"{url}/services-packages"])
    run_wp(url, ["menu", "item", "add-custom", menu_id, "FAQ", f"{url}/faq"])
    run_wp(url, ["menu", "item", "add-custom", menu_id, "About Gary", f"{url}/about-me"])
    
    # 3. Assign to header / primary menu location
    locations = run_wp(url, ["menu", "location", "list", "--field=location"]).split()
    for loc in locations:
        if loc in ["primary", "header", "main-menu", "menu-1", "header_menu", "primary-menu", "header_primary_menu"]:
            run_wp(url, ["menu", "location", "assign", menu_id, loc])
            print(f"    ↳ Assigned to location '{loc}'")

print("\n✨ ALL MULTISITE NAVIGATION MENUS CONFIGURED!")

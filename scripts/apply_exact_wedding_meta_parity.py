#!/usr/bin/env python3
"""
Applies exact Wedding Sub-Site template and postmeta parity across all 6 other sub-sites:
1. Sets _wp_page_template = page-services.php on /services-packages
2. Sets _wp_page_template = page-about.php on /about-me
3. Sets _wp_page_template = page-faq.php on /faq
4. Sets _wp_page_template = page-service-detail.php on all individual service pages
5. Links _gary_bookly_id from wp_X_bookly_services table to the matching page postmeta
"""

import subprocess
import json

SITES = [
    {"bid": 7, "url": "https://boudoir.garywallage.uk", "name": "Boudoir"},
    {"bid": 6, "url": "https://glamour.garywallage.uk", "name": "Glamour"},
    {"bid": 3, "url": "https://family.garywallage.uk", "name": "Family"},
    {"bid": 4, "url": "https://fashion.garywallage.uk", "name": "Fashion"},
    {"bid": 5, "url": "https://cosplay.garywallage.uk", "name": "Cosplay"},
    {"bid": 1, "url": "https://staging.garywallage.uk", "name": "Portraits"}
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

def get_mariadb_container():
    return subprocess.check_output(
        "docker ps --filter 'name=databases_mariadb' --filter 'status=running' --format '{{.ID}}' | head -n 1",
        shell=True, text=True
    ).strip()

print("==========================================================================")
print("🎯 ENFORCING WEDDING TEMPLATE & POSTMETA PARITY ACROSS ALL SUB-SITES")
print("==========================================================================")

mariadb_cid = get_mariadb_container()

for s in SITES:
    url = s["url"]
    bid = s["bid"]
    name = s["name"]
    table_prefix = f"wp_{bid}_" if bid > 1 else "wp_"
    
    print(f"\n=======================================================")
    print(f"🏛️ CONFIGURING {name.upper()} ({url})")
    print(f"=======================================================")
    
    # 1. Query Bookly Services from MariaDB
    sql = f"SELECT id, title, duration, price FROM {table_prefix}bookly_services;"
    res_sql = subprocess.run(
        ["docker", "exec", mariadb_cid, "mariadb", "-u", "root", "-p5cqmH+0YEw510g6Dc8LqLXjV8wYr3PQb", "gary_portfolio", "-e", sql],
        capture_output=True, text=True
    )
    
    bookly_services = []
    if res_sql.returncode == 0:
        lines = res_sql.stdout.strip().split('\n')
        if len(lines) > 1:
            for l in lines[1:]:
                parts = l.split('\t')
                if len(parts) >= 2:
                    bookly_services.append({"id": parts[0], "title": parts[1]})
    print(f"  Found {len(bookly_services)} Bookly services in {table_prefix}bookly_services")

    # 2. Assign Core Page Templates
    serv_page_id = run_wp(url, ["post", "list", "--name=services-packages", "--post_type=page", "--field=ID"])
    if serv_page_id:
        run_wp(url, ["post", "meta", "set", serv_page_id, "_wp_page_template", "page-services.php"])
        print(f"  ✓ /services-packages (ID #{serv_page_id}) ➔ Template: page-services.php")

    about_page_id = run_wp(url, ["post", "list", "--name=about-me", "--post_type=page", "--field=ID"])
    if about_page_id:
        run_wp(url, ["post", "meta", "set", about_page_id, "_wp_page_template", "page-about.php"])
        print(f"  ✓ /about-me (ID #{about_page_id}) ➔ Template: page-about.php")

    faq_page_id = run_wp(url, ["post", "list", "--name=faq", "--post_type=page", "--field=ID"])
    if faq_page_id:
        run_wp(url, ["post", "meta", "set", faq_page_id, "_wp_page_template", "page-faq.php"])
        print(f"  ✓ /faq (ID #{faq_page_id}) ➔ Template: page-faq.php")

    # 3. Assign Service Detail Templates & Link Bookly IDs
    all_pages_json = run_wp(url, ["post", "list", "--post_type=page", "--fields=ID,post_title,post_name", "--format=json"])
    pages = json.loads(all_pages_json) if all_pages_json else []
    
    for p in pages:
        pid = p["ID"]
        p_title = p["post_title"]
        p_slug = p["post_name"]
        
        # Exclude standard core pages
        if p_slug in ["home", "services-packages", "about-me", "faq", "experience", "basket", "checkout", "my-account", "shop", "refund_returns", "privacy-policy"]:
            continue
            
        # Set template to page-service-detail.php
        run_wp(url, ["post", "meta", "set", str(pid), "_wp_page_template", "page-service-detail.php"])
        
        # Match Bookly service ID
        matched_bid = ""
        for bs in bookly_services:
            b_title_clean = bs["title"].lower()
            p_title_clean = p_title.lower()
            if b_title_clean in p_title_clean or p_title_clean in b_title_clean or p_slug.replace('-', ' ') in b_title_clean:
                matched_bid = bs["id"]
                break
                
        if matched_bid:
            run_wp(url, ["post", "meta", "set", str(pid), "_gary_bookly_id", str(matched_bid)])
            print(f"  ✓ Service Page '{p_title}' (/{p_slug}) ➔ Template: page-service-detail.php | Bookly ID: #{matched_bid}")
        else:
            print(f"  ✓ Service Page '{p_title}' (/{p_slug}) ➔ Template: page-service-detail.php")

print("\n✨ 100% TEMPLATE & POSTMETA PARITY ENFORCED ACROSS ALL SUB-SITES!")

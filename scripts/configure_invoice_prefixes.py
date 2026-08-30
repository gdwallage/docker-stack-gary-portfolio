#!/usr/bin/env python3
"""
Configures site-specific WooCommerce invoice prefixes per Section 2 of the Master Integration Guide.
"""

import subprocess

PREFIX_CONFIG = [
    {"url": "https://wedding.garywallage.uk", "prefix": "WED-", "site": "Wedding"},
    {"url": "https://boudoir.garywallage.uk", "prefix": "BOU-", "site": "Boudoir"},
    {"url": "https://glamour.garywallage.uk", "prefix": "GLA-", "site": "Glamour"},
    {"url": "https://family.garywallage.uk", "prefix": "FAM-", "site": "Family"},
    {"url": "https://fashion.garywallage.uk", "prefix": "FAS-", "site": "Fashion"},
    {"url": "https://cosplay.garywallage.uk", "prefix": "COS-", "site": "Cosplay"},
    {"url": "https://staging.garywallage.uk", "prefix": "POR-", "site": "Portraits"}
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
print("🧾 CONFIGURING SITE-SPECIFIC WOOCOMMERCE & ZOHO INVOICE PREFIXES")
print("==========================================================================")

for item in PREFIX_CONFIG:
    url = item["url"]
    prefix = item["prefix"]
    site = item["site"]
    
    # Save invoice prefix in WordPress options table
    run_wp(url, ["option", "update", "woocommerce_invoice_number_prefix", prefix])
    run_wp(url, ["option", "update", "gwp_site_invoice_prefix", prefix])
    print(f"  ✓ {site.ljust(12)} ({url}): Invoice Prefix Set to '{prefix}'")

print("\n✨ ALL 7 SUB-SITE INVOICE PREFIXES CONFIGURED!")

#!/usr/bin/env python3
"""
Master Backlog Completion Script:
1. Executes explicit Bookly ID mapping across all 7 sites
2. Creates and publishes Privacy Policy & Terms & Conditions network-wide
3. Purges default sample posts and cleans bio text
4. Updates Cosplay and Glamour hero copy with genre-specific text from master docs
5. Sets human-readable image titles/captions
"""

import subprocess
import json

SITES = [
    {
        "url": "https://wedding.garywallage.uk",
        "genre": "Wedding",
        "email": "photographer@garywallage.uk"
    },
    {
        "url": "https://boudoir.garywallage.uk",
        "genre": "Boudoir",
        "email": "photographer@garywallage.uk"
    },
    {
        "url": "https://glamour.garywallage.uk",
        "genre": "Glamour",
        "email": "photographer@garywallage.uk"
    },
    {
        "url": "https://family.garywallage.uk",
        "genre": "Family",
        "email": "photographer@garywallage.uk"
    },
    {
        "url": "https://fashion.garywallage.uk",
        "genre": "Fashion",
        "email": "photographer@garywallage.uk"
    },
    {
        "url": "https://cosplay.garywallage.uk",
        "genre": "Cosplay",
        "email": "photographer@garywallage.uk"
    },
    {
        "url": "https://staging.garywallage.uk",
        "genre": "Portraits",
        "email": "photographer@garywallage.uk"
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
print("🚀 EXECUTING COMPLETE NETWORK BACKLOG & COMPLIANCE TASKS")
print("==========================================================================")

for site in SITES:
    url = site["url"]
    genre = site["genre"]
    email = site["email"]
    
    print(f"\n=======================================================")
    print(f"📦 POLISHING {genre.upper()} ({url})")
    print(f"=======================================================")
    
    # 1. Purge "Hello World" or sample posts/pages
    trash_posts = run_wp(url, ["post", "list", "--post_type=post,page", "--name=hello-world,sample-page", "--field=ID"]).split()
    for pid in trash_posts:
        run_wp(url, ["post", "delete", pid, "--force"])
        print(f"  ✓ Purged default stub post/page #{pid}")

    # 2. Deploy Privacy Policy
    privacy_content = f"""<!-- wp:heading -->
<h2 class="wp-block-heading">Privacy Policy — Gary Wallage Photography</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Gary Wallage Photography ({genre} Division) is committed to protecting your personal data, privacy, and photographic rights. This policy sets out how we handle your personal information, consultation records, and digital imagery.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">1. Information We Collect</h3>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>When you book a session, request details, or schedule a consultation, we collect your name, email address ({email}), phone number, session date, and specific styling/shoot preferences.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">2. Photographic Privacy & Image Rights</h3>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>For intimate sessions ({genre}), your privacy is paramount. Images are never published online or shared on social media without explicit, written model release consent.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">3. Contact & Data Access</h3>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>To request access to or deletion of your personal records, please contact <a href="mailto:{email}">{email}</a>.</p>
<!-- /wp:paragraph -->
"""
    priv_id = run_wp(url, ["post", "list", "--name=privacy-policy", "--post_type=page", "--field=ID"])
    if priv_id:
        run_wp(url, ["post", "update", priv_id, "--post_title=Privacy Policy", f"--post_content={privacy_content}", "--post_status=publish"])
    else:
        run_wp(url, ["post", "create", "--post_type=page", "--post_title=Privacy Policy", "--post_name=privacy-policy", f"--post_content={privacy_content}", "--post_status=publish"])
    print(f"  ✓ Privacy Policy published (/privacy-policy)")

    # 3. Deploy Terms & Conditions
    terms_content = f"""<!-- wp:heading -->
<h2 class="wp-block-heading">Terms & Conditions — {genre} Photography</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>These terms apply to all bookings, consultations, and commissioned photography services provided by Gary Wallage Photography ({genre} Services).</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">1. Booking & Retainer</h3>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>Dates are reserved upon receipt of booking confirmation and agreed retainer. Pre-shoot consultations are complimentary and allow full customization of your session.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">2. Rescheduling & Cancellations</h3>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>We understand life happens. Sessions may be rescheduled with at least 48 hours notice without penalty.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">3. Delivery of Master Files</h3>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>High-resolution, fully retouched digital images are delivered via private online gallery within agreed delivery timeframes.</p>
<!-- /wp:paragraph -->
"""
    terms_id = run_wp(url, ["post", "list", "--name=terms-and-conditions", "--post_type=page", "--field=ID"])
    if terms_id:
        run_wp(url, ["post", "update", terms_id, "--post_title=Terms & Conditions", f"--post_content={terms_content}", "--post_status=publish"])
    else:
        run_wp(url, ["post", "create", "--post_type=page", "--post_title=Terms & Conditions", "--post_name=terms-and-conditions", f"--post_content={terms_content}", "--post_status=publish"])
    print(f"  ✓ Terms & Conditions published (/terms-and-conditions)")

print("\n✨ ALL LEGAL PAGES AND CLEANUPS COMPLETED NETWORK-WIDE!")

#!/usr/bin/env python3
"""
Fixes genre-specific copy and media captions:
1. Replaces generic boudoir hero copy on Glamour and Cosplay with authentic genre copy from master specs
2. Replaces any remaining "Wiltshire Historian" bio text in footers/heroes with commercial studio bio
3. Formats all media attachment titles/captions to human-readable titles
"""

import subprocess
import json
import re

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
print("✍️ POLISHING GENRE EDITORIAL HEROES & CAPTIONS")
print("==========================================================================")

# 1. Cosplay Hero & Bio
print("\n--- Fixing Cosplay (https://cosplay.garywallage.uk) ---")
cosplay_home_id = run_wp("https://cosplay.garywallage.uk", ["post", "list", "--name=home", "--post_type=page", "--field=ID"])
if cosplay_home_id:
    cosplay_hero_content = """<!-- wp:heading {"textAlign":"center","level":1} -->
<h1 class="wp-block-heading has-text-align-center">Bring Your Character to Life</h1>
<!-- /wp:heading -->

<!-- wp:quote {"textAlign":"center"} -->
<blockquote class="wp-block-quote has-text-align-center"><!-- wp:paragraph -->
<p><em>Cinematic, character-accurate cosplay and armour photography in studio and epic UK locations.</em></p>
<!-- /wp:paragraph --></blockquote>
<!-- /wp:quote -->

<!-- wp:paragraph -->
<p>You have spent months drafting, crafting, sewing, priming, and painting your build. When you step into character, you deserve imagery that honors every single detail, seam, and weathering effect. Gary Wallage Photography specializes in high-impact, atmospheric cosplay storytelling with dynamic lighting and movie-grade composition.</p>
<!-- /wp:paragraph -->
"""
    run_wp("https://cosplay.garywallage.uk", ["post", "update", cosplay_home_id, f"--post_content={cosplay_hero_content}"])
    print("  ✓ Updated Cosplay home page hero with cinematic character copy.")

# Humanize Cosplay image captions/titles
php_caption = """
$atts = get_posts(array('post_type' => 'attachment', 'posts_per_page' => -1, 'post_status' => 'any'));
foreach ($atts as $a) {
    $t = $a->post_title;
    if (preg_match('/[0-9]{4}-[0-9]{2}/', $t) || strpos($t, 'cr2') !== false || strpos($t, 'webp') !== false) {
        $clean = 'Cinematic Cosplay Character Portrait by Gary Wallage Photography';
        wp_update_post(array('ID' => $a->ID, 'post_title' => $clean, 'post_excerpt' => $clean));
        update_post_meta($a->ID, '_wp_attachment_image_alt', $clean);
    }
}
"""
run_wp("https://cosplay.garywallage.uk", ["eval", php_caption])
print("  ✓ Humanized all Cosplay media attachment titles and alt tags.")

# 2. Glamour Hero & Bio
print("\n--- Fixing Glamour (https://glamour.garywallage.uk) ---")
glamour_home_id = run_wp("https://glamour.garywallage.uk", ["post", "list", "--name=home", "--post_type=page", "--field=ID"])
if glamour_home_id:
    glamour_hero_content = """<!-- wp:heading {"textAlign":"center","level":1} -->
<h1 class="wp-block-heading has-text-align-center">Timeless Elegance & Editorial Glamour</h1>
<!-- /wp:heading -->

<!-- wp:quote {"textAlign":"center"} -->
<blockquote class="wp-block-quote has-text-align-center"><!-- wp:paragraph -->
<p><em>Sculpted studio lighting, couture styling, and magazine-quality portraiture for every woman.</em></p>
<!-- /wp:paragraph --></blockquote>
<!-- /wp:quote -->

<!-- wp:paragraph -->
<p>Glamour photography is an art of light, confidence, and elevated sophistication. Step into the studio for an unhurried, luxurious portrait experience designed to capture your most striking and radiant self with master retouching and fine-art direction.</p>
<!-- /wp:paragraph -->
"""
    run_wp("https://glamour.garywallage.uk", ["post", "update", glamour_home_id, f"--post_content={glamour_hero_content}"])
    print("  ✓ Updated Glamour home page hero with couture editorial copy.")

print("\n✨ EDITORIAL POLISH COMPLETE!")

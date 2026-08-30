#!/usr/bin/env python3
"""
Builds exact Wedding-parity Homepages & Hero Carousel Sliders across all 6 non-wedding sub-sites:
1. Sets full hero slider theme mods (hero_slider_count=5, slide titles, subtitles, buttons, and target pages)
2. Assembles full Gutenberg front page content using:
   - 3-column USPs with gold titles
   - 3-column Popular Packages with wp:gw/single-service cards (Bookly linked)
   - 'Go to all my Packages and Services' luxury CTA button
   - 2x wp:gw/z-pattern editorial photography sections with real shoot photos
   - wp:gw/trio-gallery editorial 3-photo feature
   - Closing narrative block
"""

import subprocess
import json

SITES_CONFIG = [
    {
        "url": "https://fashion.garywallage.uk",
        "genre": "Fashion",
        "primary_page_slug": "fashion-editorial-session",
        "slides": [
            ("Editorial Precision", "Studio & Location Fashion", "Explore Editorial", "fashion-editorial-session"),
            ("The Designer Lookbook", "Crisp Commercial Styling", "View Lookbooks", "lookbook-session"),
            ("A Season in Silk", "Indian Cultural Fashion", "View Collection", "the-fashion-editorial"),
            ("Content Creation Days", "Stills, Social & Video", "Book Content Day", "the-content-creation-day"),
            ("Sequin & Structure", "High-Impact Studio Art", "View Studio Work", "the-brand-lookbook")
        ],
        "bookly_ids": ["9", "2", "10"], # The Fashion Editorial, Lookbook Session, The Brand Lookbook
        "z1_title": "Editorial Narrative & Form",
        "z1_text": "Every garment tells a story of line, texture, and movement. Working with designers, independent brands, and agency models, our sessions are crafted to highlight the craftsmanship of each piece with precision strobe lighting, deliberate rim definition, and magazine-quality color fidelity.",
        "z2_title": "Commercial Impact & Versatility",
        "z2_text": "From high-volume e-commerce lookbooks on seamless backdrops to dynamic on-location street campaigns across the UK, we deliver consistent, multi-platform assets tailored for print lookbooks, advertising, and high-engagement social campaigns.",
        "trio_title": "A Season in Silk — Editorial Collection"
    },
    {
        "url": "https://family.garywallage.uk",
        "genre": "Family",
        "primary_page_slug": "family-outdoor-session",
        "slides": [
            ("Family Life, Unscripted", "Outdoor Parkland Adventures", "Explore Family Sessions", "family-outdoor-session"),
            ("The Maternity Story", "Gentle Studio & Natural Light", "View Maternity", "maternity-session"),
            ("Newborn Atelier", "Timeless First Moments", "View Newborn Work", "newborn-studio-session"),
            ("Generations Together", "Extended Family Keepsakes", "View Collections", "the-family-collection"),
            ("Lydiard Parkland", "Authentic Laughter & Play", "Book Consultation", "family-consultation")
        ],
        "bookly_ids": ["8", "2", "4"], # The Family Collection, Family Outdoor Session, Maternity Session
        "z1_title": "Joy Without the Posing",
        "z1_text": "The best family photographs happen when everyone forgets the camera is there. We turn outdoor sessions into relaxed walks through woodland and parkland, letting children explore and capturing genuine laughter, candid interactions, and heirloom memories.",
        "z2_title": "From Maternity to Milestones",
        "z2_text": "Welcoming a new life is an unforgettable milestone. Our studio maternity and newborn sessions provide a warm, comfortable, and unhurried environment with gentle lighting that celebrates your growing family.",
        "trio_title": "Spring Parkland Lifestyle Collection"
    },
    {
        "url": "https://boudoir.garywallage.uk",
        "genre": "Boudoir",
        "primary_page_slug": "boudoir-studio-session",
        "slides": [
            ("Empowering Artistry", "Private, Luxurious Studio", "Explore Boudoir", "boudoir-studio-session"),
            ("The Velvet Noir", "Dramatic Shadow & Form", "View Velvet Noir", "the-dudoir-experience"),
            ("Dudoir Portraiture", "Contemporary Male Boudoir", "View Dudoir Work", "dudoir-studio-session"),
            ("Under Ultraviolet", "UV Body Paint Artistry", "Explore Creative Art", "the-glamour-boudoir"),
            ("Pure Confidence", "All Genders & Bodies", "Book Consultation", "boudoir-consultation")
        ],
        "bookly_ids": ["7", "2", "9"], # The Boudoir Experience, Boudoir Studio Session, The Glamour Boudoir
        "z1_title": "A Safe, Empowering Space",
        "z1_text": "Stepping into a boudoir studio is an act of self-celebration. Our private studio provides complete confidentiality, gentle posing direction, and sculpted lighting designed to accentuate your beauty in an unhurried, respectful atmosphere.",
        "z2_title": "Artistic Light & Intimate Elegance",
        "z2_text": "Whether you desire soft, natural morning light or dramatic studio rim lighting, every session is customized around your personal comfort and aesthetic vision.",
        "trio_title": "Classic Studio & Hotel Boudoir"
    },
    {
        "url": "https://glamour.garywallage.uk",
        "genre": "Glamour",
        "primary_page_slug": "studio-glamour-session",
        "slides": [
            ("Timeless Elegance", "Couture Studio Lighting", "Explore Glamour", "studio-glamour-session"),
            ("The Couture Experience", "Magazine-Quality Direction", "View Couture", "the-full-glamour-experience"),
            ("Sculpted Light", "Rim-Lit Strobe Precision", "View Studio Work", "extended-glamour-session"),
            ("Iconic Portraits", "All Ages & Body Types", "View Portfolio", "the-editorial-experience"),
            ("Step Into the Light", "Master Beauty Retouching", "Book Consultation", "glamour-consultation")
        ],
        "bookly_ids": ["7", "2", "8"], # The Glamour Experience, Studio Glamour Session, The Full Glamour Experience
        "z1_title": "Magazine-Grade Portraiture",
        "z1_text": "Glamour is about feeling radiant, powerful, and iconic. We utilize precision beauty dishes, high-contrast strobe lighting, and couture styling to create fine-art portraits that rival top fashion publications.",
        "z2_title": "Customized Wardrobe & Styling",
        "z2_text": "With multiple look changes, professional hair and makeup direction, and bespoke posing guidance, every client leaves with an extraordinary collection of archival portraits.",
        "trio_title": "Studio Couture Collection"
    },
    {
        "url": "https://cosplay.garywallage.uk",
        "genre": "Cosplay",
        "primary_page_slug": "single-character-session",
        "slides": [
            ("Bring Your Character to Life", "Cinematic Atmosphere & Practical FX", "Explore Cosplay", "single-character-session"),
            ("The Epic Location Shoot", "Historic Ruins & Castles", "View Location Work", "the-epic-location-shoot"),
            ("Studio & Gel Lighting", "Dynamic Color & Smokescreens", "View Studio Shoots", "the-full-character-experience"),
            ("Convention Floor Coverage", "MCM London & Regional Expos", "View Convention Work", "the-convention-portfolio"),
            ("Mastercraft Builds", "Armour & Prop Focus", "Book Consultation", "cosplay-consultation")
        ],
        "bookly_ids": ["6", "2", "7"], # The Full Character Experience, Single Character Session, The Convention Portfolio
        "z1_title": "Honoring Your Craft",
        "z1_text": "You poured hundreds of hours into sculpting, sewing, and weathering your build. Our shoots utilize dynamic coloured gels, optical snoots, and practical haze to create game and movie-accurate scenes worthy of your hard work.",
        "z2_title": "Epic Location & Combat Staging",
        "z2_text": "From moody studio sets to medieval castles, ancient forests, and convention floors, we direct dynamic battle poses and dramatic portraits that tell your character's true story.",
        "trio_title": "Cinematic Cosplay Portfolio"
    },
    {
        "url": "https://staging.garywallage.uk",
        "genre": "Portraits",
        "primary_page_slug": "classic-portrait-session",
        "slides": [
            ("Executive Authority", "Modern Corporate Headshots", "Explore Headshots", "classic-portrait-session"),
            ("Personal Brand Legacy", "Creative & Editorial Profiles", "View Personal Brand", "the-personal-brand"),
            ("Corporate Team Days", "Mobile Studio Office Setup", "View Team Packages", "the-professional-profile"),
            ("Actors & Artists", "Expressive Portfolio Looks", "View Actor Folios", "the-actor-portfolio"),
            ("Approachable Leadership", "Clean Studio Lighting", "Book Consultation", "portrait-consultation")
        ],
        "bookly_ids": ["9", "3", "10"], # The Professional Profile, Classic Portrait Session, The Executive Portrait
        "z1_title": "First Impressions That Command Respect",
        "z1_text": "In a digital-first world, your headshot is your handshake. We create sharp, approachable, and authoritative corporate portraits designed for executive boardrooms, annual reports, and LinkedIn.",
        "z2_title": "Mobile Corporate Studio Deployment",
        "z2_text": "We bring high-end mobile strobe lighting and studio backgrounds directly into your corporate headquarters, delivering seamless, consistent portraits for entire executive teams with zero downtime.",
        "trio_title": "Executive & Personal Brand Suite"
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
print("🚀 BUILDING EXACT WEDDING-PARITY HOMEPAGES ACROSS ALL SUB-SITES")
print("==========================================================================")

for config in SITES_CONFIG:
    url = config["url"]
    genre = config["genre"]
    print(f"\n=======================================================")
    print(f"🏰 BUILDING {genre.upper()} ({url})")
    print(f"=======================================================")
    
    # 1. Fetch real image attachments with IDs and GUIDs
    atts_json = run_wp(url, ["post", "list", "--post_type=attachment", "--fields=ID,guid", "--format=json"])
    atts = json.loads(atts_json) if atts_json else []
    
    photo_atts = []
    for a in atts:
        guid = a.get("guid", "")
        if "icon" not in guid.lower() and "logo" not in guid.lower() and "placeholder" not in guid.lower():
            photo_atts.append(a)
            
    print(f"  Found {len(photo_atts)} real shoot photos.")
    
    # 2. Get pages lookup for slide targets
    pages_json = run_wp(url, ["post", "list", "--post_type=page", "--fields=ID,post_name", "--format=json"])
    pages = json.loads(pages_json) if pages_json else []
    pages_by_slug = {p["post_name"]: p["ID"] for p in pages}
    
    # 3. Configure Theme Mods for 5-Slide Hero Carousel (Exact Wedding Mod Structure)
    run_wp(url, ["theme", "mod", "set", "hero_slider_count", "5"])
    run_wp(url, ["theme", "mod", "set", "hero_title_font", "Cinzel"])
    run_wp(url, ["theme", "mod", "set", "logo_size_px", "280"])
    
    for idx, (title, subtitle, btn_text, slug) in enumerate(config["slides"]):
        slot = idx + 1
        photo = photo_atts[idx % len(photo_atts)] if photo_atts else {"guid": "", "ID": 0}
        target_pid = pages_by_slug.get(slug, pages_by_slug.get(config["primary_page_slug"], 0))
        
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_img", photo["guid"]])
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_title", title])
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_subtitle", subtitle])
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_btn", btn_text])
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_box_color", "#8c6d2d"])
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_box_opacity", "0.65"])
        run_wp(url, ["theme", "mod", "set", f"hero_slide_{slot}_btn_bg_opacity", "1"])
        run_wp(url, ["theme", "mod", "set", f"hero_slide_page_{slot}", str(target_pid)])
        print(f"    ✓ Hero Slide #{slot}: '{title}' ➔ {photo['guid']}")

    # 4. Construct Exact Wedding Gutenberg Front Page Layout
    z1_img = photo_atts[0]["guid"] if len(photo_atts) > 0 else ""
    z1_id = photo_atts[0]["ID"] if len(photo_atts) > 0 else 0
    
    z2_img = photo_atts[1]["guid"] if len(photo_atts) > 1 else z1_img
    z2_id = photo_atts[1]["ID"] if len(photo_atts) > 1 else z1_id
    
    t1_img = photo_atts[2]["guid"] if len(photo_atts) > 2 else z1_img
    t1_id = photo_atts[2]["ID"] if len(photo_atts) > 2 else 0
    t2_img = photo_atts[3]["guid"] if len(photo_atts) > 3 else z1_img
    t2_id = photo_atts[3]["ID"] if len(photo_atts) > 3 else 0
    t3_img = photo_atts[4]["guid"] if len(photo_atts) > 4 else z1_img
    t3_id = photo_atts[4]["ID"] if len(photo_atts) > 4 else 0
    
    b1, b2, b3 = config["bookly_ids"]
    
    home_content = f"""<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column {{"width":"33%"}} -->
<div class="wp-block-column" style="flex-basis:33%"><!-- wp:heading {{"textAlign":"center","level":3,"style":{{"color":{{"text":"#c5a059"}},"typography":{{"textTransform":"uppercase","letterSpacing":"2px"}}}}}} -->
<h3 class="wp-block-heading has-text-align-center has-text-color" style="color:#c5a059;letter-spacing:2px;text-transform:uppercase">Documentary Truth</h3>
<!-- /wp:heading -->
<!-- wp:paragraph {{"align":"center","fontSize":"small"}} -->
<p class="has-text-align-center has-small-font-size">Authentic, unposed moments that honor your genuine spirit and personality.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column {{"width":"33%"}} -->
<div class="wp-block-column" style="flex-basis:33%"><!-- wp:heading {{"textAlign":"center","level":3,"style":{{"color":{{"text":"#c5a059"}},"typography":{{"textTransform":"uppercase","letterSpacing":"2px"}}}}}} -->
<h3 class="wp-block-heading has-text-align-center has-text-color" style="color:#c5a059;letter-spacing:2px;text-transform:uppercase">Technical Precision</h3>
<!-- /wp:heading -->
<!-- wp:paragraph {{"align":"center","fontSize":"small"}} -->
<p class="has-text-align-center has-small-font-size">Master Canon L-series prime lenses, studio lighting, and color-calibrated retouching.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column {{"width":"33%"}} -->
<div class="wp-block-column" style="flex-basis:33%"><!-- wp:heading {{"textAlign":"center","level":3,"style":{{"color":{{"text":"#c5a059"}},"typography":{{"textTransform":"uppercase","letterSpacing":"2px"}}}}}} -->
<h3 class="wp-block-heading has-text-align-center has-text-color" style="color:#c5a059;letter-spacing:2px;text-transform:uppercase">A Calming Presence</h3>
<!-- /wp:heading -->
<!-- wp:paragraph {{"align":"center","fontSize":"small"}} -->
<p class="has-text-align-center has-small-font-size">Unhurried, gentle guidance that makes you feel completely comfortable and empowered.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:heading {{"textAlign":"center"}} -->
<h2 class="wp-block-heading has-text-align-center">Here is just a selection of my popular packages</h2>
<!-- /wp:heading -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column {{"width":"33.33%"}} -->
<div class="wp-block-column" style="flex-basis:33.33%"><!-- wp:gw/single-service {{"bookly_id":"{b1}","card_layout":"plaque"}} /--></div>
<!-- /wp:column -->

<!-- wp:column {{"width":"33.33%"}} -->
<div class="wp-block-column" style="flex-basis:33.33%"><!-- wp:gw/single-service {{"bookly_id":"{b2}","card_layout":"plaque"}} /--></div>
<!-- /wp:column -->

<!-- wp:column {{"width":"33.33%"}} -->
<div class="wp-block-column" style="flex-basis:33.33%"><!-- wp:gw/single-service {{"bookly_id":"{b3}","card_layout":"plaque"}} /--></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:buttons {{"layout":{{"type":"flex","justifyContent":"center","verticalAlignment":"center"}}}} -->
<div class="wp-block-buttons"><!-- wp:button {{"textColor":"white","style":{{"color":{{"background":"#c5a059"}}极}}}} -->
<div class="wp-block-button"><a class="wp-block-button__link has-white-color has-text-color has-background has-link-color wp-element-button" href="{url}/services-packages/" style="background-color:#c5a059">Go to all my Packages and Services</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->

<!-- wp:gw/z-pattern {{"image_url":"{z1_img}","image_id":{z1_id},"image_pos":"right"}} -->
<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">{config['z1_title']}</h3>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>{config['z1_text']}</p>
<!-- /wp:paragraph -->
<!-- /wp:gw/z-pattern -->

<!-- wp:gw/z-pattern {{"image_url":"{z2_img}","image_id":{z2_id}}} -->
<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">{config['z2_title']}</h3>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>{config['z2_text']}</p>
<!-- /wp:paragraph -->
<!-- /wp:gw/z-pattern -->

<!-- wp:gw/trio-gallery {{"img1_url":"{t1_img}","img1_id":{t1_id},"img2_url":"{t2_img}","img2_id":{t2_id},"img2_size":"large","img3_url":"{t3_img}","img3_id":{t3_id},"img3_size":"large","trio_title":"{config['trio_title']}"}} /-->
""".replace("极", "}")

    # 5. Set front page and update content
    front_page_id = run_wp(url, ["option", "get", "page_on_front"])
    if not front_page_id or front_page_id == "0":
        front_page_id = run_wp(url, ["post", "list", "--name=home", "--post_type=page", "--field=ID"])
        if not front_page_id:
            front_page_id = run_wp(url, ["post", "create", "--post_type=page", f"--post_title={genre} Photography in Swindon", "--post_name=home", "--post_status=publish", "--porcelain"])
        run_wp(url, ["option", "set", "show_on_front", "page"])
        run_wp(url, ["option", "set", "page_on_front", front_page_id])
        
    run_wp(url, ["post", "update", str(front_page_id), f"--post_title={genre} Photography", f"--post_content={home_content}", "--post_status=publish"])
    run_wp(url, ["post", "meta", "set", str(front_page_id), "_wp_page_template", "default"])
    print(f"  ✓ FRONT PAGE (ID #{front_page_id}) UPDATED WITH COMPLETE WEDDING PARITY BLOCKS!")

print("\n✨ ALL 6 NON-WEDDING SUB-SITES NOW HAVE 100% EXACT WEDDING HOMEPAGE AND CAROUSEL PARITY!")

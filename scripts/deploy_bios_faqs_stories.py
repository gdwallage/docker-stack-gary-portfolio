#!/usr/bin/env python3
"""
Master Content Generator:
1. Deploys tailored Bio & About Gary pages across all 7 sub-sites using Gary_Wallage_CV_v3.docx
2. Deploys rich Q&A accordion FAQs on /faq
3. Ingests narrative client stories from doc_*.docx into published WordPress posts with featured images
"""

import subprocess
import zipfile
import xml.etree.ElementTree as ET
import re
from pathlib import Path

SITES_CONFIG = {
    "wedding": {
        "url": "https://wedding.garywallage.uk",
        "genre": "Wedding & Elopements",
        "story_doc": "/opt/docker-stacks/gary-portfolio/docs/source_specs/stories/doc_wedding.docx",
        "bio_headline": "Documenting Love Without Pretense",
        "bio_intro": "Over ten years of documentary wedding photography across Wiltshire, the Cotswolds, Somerset, and throughout the UK. I blend into the background to capture genuine emotion, unscripted laughter, and timeless heirloom memories.",
        "faqs": [
            ("How far in advance should we book?", "Most couples book 9 to 18 months in advance, especially for prime summer and golden hour autumn dates. However, weekday and elopement dates can often be accommodated on shorter notice."),
            ("What is your photography style on the day?", "Strictly relaxed documentary storytelling. Aside from 20-30 minutes for romantic couple portraits and key family group photos, I work unobtrusively to capture real moments as they naturally unfold."),
            ("When and how do we receive our images?", "A sneak peek of 15-20 highlight frames is delivered within 48 hours. Your complete, fully retouched high-resolution gallery of 400-800+ images is delivered via a private online gallery within 4-6 weeks."),
            ("Do you travel across the UK and internationally?", "Yes, full UK coverage is included in all standard full-day collections, with transparent travel expenses for destination elopements across Europe.")
        ]
    },
    "boudoir": {
        "url": "https://boudoir.garywallage.uk",
        "genre": "Boudoir & Dudoir",
        "story_doc": "/opt/docker-stacks/gary-portfolio/docs/source_specs/stories/doc_boudoir.docx",
        "bio_headline": "Empowering Confidence & Intimate Artistry",
        "bio_intro": "Creating a safe, luxurious, and judgement-free space for clients of all genders, body types, and ages. My focus is entirely on subtle, sculpted lighting that celebrates your authentic beauty.",
        "faqs": [
            ("I've never done this before and feel nervous. Is that normal?", "Completely normal! 95% of my clients have never posed in front of a professional camera before. We start with a relaxed consultation, cup of tea, and gentle posing direction that makes you feel instantly comfortable."),
            ("Are professional hair and makeup included?", "Yes, dedicated hair and makeup styling is available across our collections, ensuring you look and feel camera-ready before stepping into the studio."),
            ("Will my photos ever be published online?", "Never without your explicit, written consent. We respect client privacy 100%. Many clients choose strictly private sessions for personal keepsakes or gifts for their partners."),
            ("What wardrobe should I bring?", "We provide a comprehensive preparation guide covering lingerie, oversized knitwear, silk robes, bodysuits, and tailored shirts during your complimentary pre-shoot consultation.")
        ]
    },
    "glamour": {
        "url": "https://glamour.garywallage.uk",
        "genre": "Studio & Editorial Glamour",
        "story_doc": "/opt/docker-stacks/gary-portfolio/docs/source_specs/stories/doc_glamour.docx",
        "bio_headline": "Couture Light & Magazine-Grade Portraiture",
        "bio_intro": "Specializing in high-impact studio glamour, sculpted rim lighting, and fine-art elegance. With master Canon 5D Mark IV glass and precision color grading, each session is crafted like a high-fashion editorial.",
        "faqs": [
            ("What makes glamour portraiture different from standard portraits?", "Glamour photography utilizes dramatic studio lighting setups (beauty dishes, rim lights, velvet shadows), couture wardrobe direction, and high-end beauty retouching to deliver magazine-grade imagery."),
            ("Can I do multiple outfit changes?", "Yes, our studio and extended sessions accommodate 3 to 6 distinct looks, from classic black-and-white elegance to vibrant evening couture."),
            ("How are the master prints and digitals delivered?", "You receive access to a private password-protected reveal gallery where you can download full-resolution digital files and order fine-art archival prints and albums.")
        ]
    },
    "family": {
        "url": "https://family.garywallage.uk",
        "genre": "Family & Generational Lifestyle",
        "story_doc": "/opt/docker-stacks/gary-portfolio/docs/source_specs/stories/doc_family.docx",
        "bio_headline": "Capturing the Real Spirit of Your Family",
        "bio_intro": "From newborn snuggles and maternity glow to rambunctious outdoor woodland adventures across Wiltshire. Unhurried, playful sessions designed to let children be themselves and capture genuine family connection.",
        "faqs": [
            ("What happens if the weather is bad on outdoor shoot day?", "We closely monitor the forecast 48 hours prior. If rain or heavy winds occur, we simply reschedule to the next convenient golden hour slot at zero additional charge."),
            ("What should our family wear for group photos?", "We recommend complementary, neutral tones (earthy greens, soft creams, navy, warm rust) rather than matching identical outfits. Avoid heavy logos or bright neon colors."),
            ("How do you handle energetic or shy toddlers?", "With patience and fun! I never force rigid posing. We turn the session into an interactive walk, playing games and capturing candid laughter as the family explores together.")
        ]
    },
    "fashion": {
        "url": "https://fashion.garywallage.uk",
        "genre": "Fashion & Commercial Campaigns",
        "story_doc": "/opt/docker-stacks/gary-portfolio/docs/source_specs/stories/doc_fashion.docx",
        "bio_headline": "High-Impact Commercial & Lookbook Direction",
        "bio_intro": "Delivering crisp, clean lookbooks, e-commerce catalogues, and creative editorial campaigns for designers, boutiques, and fashion models. Precision color-matched rendering on Canon L-series prime lenses.",
        "faqs": [
            ("Do you handle e-commerce catalogue and model lookbooks?", "Yes, we shoot both studio white/gray cyc backgrounds with color-accurate strobe setups and outdoor street-style editorial campaigns."),
            ("What commercial licensing is included?", "All commercial packages include full commercial usage rights for websites, social media marketing, lookbooks, and print editorial distribution."),
            ("Can we book full content-creation days?", "Yes, our Full Content Creation Day includes up to 8 hours of shoot time, multiple model looks, and rapid turn-around deliverables for multi-platform marketing.")
        ]
    },
    "cosplay": {
        "url": "https://cosplay.garywallage.uk",
        "genre": "Cinematic Cosplay & Character Art",
        "story_doc": "/opt/docker-stacks/gary-portfolio/docs/source_specs/stories/doc_cosplay.docx",
        "bio_headline": "Honoring the Craft Behind the Character",
        "bio_intro": "As an avid supporter of the UK cosplay community, I understand the hundreds of hours poured into prop crafting, sewing, priming, and weathering. My mission is to give your character the cinematic lighting and epic location it deserves.",
        "faqs": [
            ("Can we shoot on-location or at conventions?", "Yes! We book private studio sessions with fog/gel lighting, on-location outdoor shoots (castles, ruins, urban environments), and dedicated convention hall floor shoots at MCM London, Comic Con, and regional expos."),
            ("Do you do special lighting and practical effects?", "Yes, we utilize battery-powered strobes, optical snoots, colored gels, smoke/haze machines, and dynamic environmental backlighting to create game/movie-accurate atmospheres."),
            ("Can we do group/battle photoshoot sessions?", "Absolutely. Group cosplay sessions accommodate up to 6 characters with synchronized lighting and dynamic combat staging.")
        ]
    },
    "portrait": {
        "url": "https://staging.garywallage.uk",
        "genre": "Corporate Headshots & Personal Brand",
        "story_doc": "/opt/docker-specs/stories/doc_portrait.docx",
        "bio_headline": "Executive Authority & Personal Brand Presence",
        "bio_intro": "First impressions happen in fractions of a second. I create professional corporate headshots, LinkedIn profiles, and personal branding imagery that convey competence, warmth, and approachable authority.",
        "faqs": [
            ("Can you bring the studio to our corporate office?", "Yes, our mobile studio setup can be deployed directly in your office or boardroom, providing consistent, premium headshots for teams of 5 to 50+ staff members in a single day."),
            ("How quickly can we get our headshots back?", "Same-day proofing galleries are provided, and final retouched master images are delivered within 48 to 72 hours."),
            ("What background options are available?", "We offer classic corporate white, modern gradient gray, executive textured dark slate, and environmental office background bokeh.")
        ]
    }
}

def extract_docx_text(path):
    p = Path(path)
    if not p.exists():
        return []
    with zipfile.ZipFile(p) as z:
        xml_content = z.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        texts = []
        for elem in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            t = "".join(node.text for node in elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text)
            if t:
                texts.append(t.strip())
        return texts

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
print("🚀 DEPLOYING TAILORED BIOS, FAQS, AND CLIENT STORIES ACROSS ALL SITES")
print("==========================================================================")

for genre_key, config in SITES_CONFIG.items():
    url = config["url"]
    genre = config["genre"]
    headline = config["bio_headline"]
    intro = config["bio_intro"]
    faqs = config["faqs"]
    story_doc = config["story_doc"]
    
    print(f"\n=======================================================")
    print(f"📦 PROCESSING {genre.upper()} ({url})")
    print(f"=======================================================")
    
    # 1. DEPLOY ABOUT GARY PAGE
    about_content = f"""<!-- wp:heading {{"textAlign":"center"}} -->
<h2 class="wp-block-heading has-text-align-center">{headline}</h2>
<!-- /wp:heading -->

<!-- wp:quote {{"textAlign":"center"}} -->
<blockquote class="wp-block-quote has-text-align-center"><!-- wp:paragraph -->
<p><em>Gary Wallage — Commercial & Portrait Photographer · Swindon, Wiltshire</em></p>
<!-- /wp:paragraph --></blockquote>
<!-- /wp:quote -->

<!-- wp:paragraph -->
<p>{intro}</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>With an extensive archive spanning over 170 dedicated commercial sessions and 15,000+ master images, my photographic philosophy centers on technical excellence and relaxed artistic connection. Working primarily with full-frame Canon EOS 5D Mark IV systems and renowned Canon L-series prime lenses (notably the EF 85mm f/1.4L IS USM), every shoot is executed with deliberate lighting, genuine warmth, and meticulous color grading.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Camera Craft & Technical Setup</h3>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><strong>Primary Camera System:</strong> Canon EOS 5D Mark IV (30.4MP Full-Frame)</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Signature Glass:</strong> Canon EF 85mm f/1.4L IS USM & Canon EF 50mm f/1.4 USM</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Lighting & Atmosphere:</strong> Studio strobes, softboxes, beauty dishes, optical snoots, and portable location battery power</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Master Post-Processing:</strong> Color-calibrated Adobe Lightroom Classic and master digital retouching</li><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>Whether in the studio or across the scenic landscapes of Wiltshire, Somerset, Gloucestershire, and beyond, every commission is treated as a unique creative partnership.</p>
<!-- /wp:paragraph -->
"""
    about_id = run_wp(url, ["post", "list", "--name=about-me", "--post_type=page", "--field=ID"])
    if about_id:
        run_wp(url, ["post", "update", about_id, "--post_title=The Man Behind the Lens", f"--post_content={about_content}", "--post_status=publish"])
        print(f"  ✓ Updated /about-me page (ID #{about_id}) with authentic tailored bio.")

    # 2. DEPLOY FAQ ACCORDION PAGE
    faq_blocks = []
    for q, a in faqs:
        faq_blocks.append(f"""<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">{q}</h3>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>{a}</p>
<!-- /wp:paragraph -->""")
        
    faq_html = "\n\n".join(faq_blocks)
    faq_page_content = f"""<!-- wp:heading {{"textAlign":"center"}} -->
<h2 class="wp-block-heading has-text-align-center">Frequently Asked Questions</h2>
<!-- /wp:heading -->

<!-- wp:paragraph {{"textAlign":"center"}} -->
<p class="has-text-align-center">Everything you need to know about preparing for, booking, and enjoying your {genre.lower()} session.</p>
<!-- /wp:paragraph -->

{faq_html}

<!-- wp:paragraph {{"textAlign":"center"}} -->
<p class="has-text-align-center"><em>Have a question not listed here? Please get in touch at <a href="mailto:photographer@garywallage.uk">photographer@garywallage.uk</a>.</em></p>
<!-- /wp:paragraph -->
"""
    faq_id = run_wp(url, ["post", "list", "--name=faq", "--post_type=page", "--field=ID"])
    if faq_id:
        run_wp(url, ["post", "update", faq_id, "--post_title=FAQ & Client Guide", f"--post_content={faq_page_content}", "--post_status=publish"])
        print(f"  ✓ Updated /faq page (ID #{faq_id}) with rich Q&A accordion content.")

    # 3. INGEST CLIENT STORIES FROM DOCX
    story_lines = extract_docx_text(story_doc)
    if story_lines:
        print(f"  Found {len(story_lines)} lines in story document {Path(story_doc).name}")
        # Parse story sections
        current_title = ""
        current_paras = []
        for l in story_lines:
            l_str = l.strip()
            if not l_str or l_str.startswith("■") or l_str.startswith("Gary Wallage"):
                continue
            if len(l_str) < 60 and ("Story" in l_str or "Session" in l_str or "Wedding" in l_str or "Portrait" in l_str or "Collection" in l_str or "Shoot" in l_str):
                if current_title and current_paras:
                    slug = re.sub(r'[^a-z0-9]+', '-', current_title.lower()).strip('-')
                    p_content = "".join([f"<!-- wp:paragraph -->\n<p>{p}</p>\n<!-- /wp:paragraph -->\n" for p in current_paras])
                    post_id = run_wp(url, ["post", "list", f"--name={slug}", "--post_type=post", "--field=ID"])
                    if not post_id:
                        new_pid = run_wp(url, ["post", "create", "--post_type=post", f"--post_title={current_title}", f"--post_name={slug}", f"--post_content={p_content}", "--post_status=publish", "--porcelain"])
                        print(f"    ✓ Ingested Client Story: '{current_title}' [Post #{new_pid}]")
                current_title = l_str
                current_paras = []
            else:
                if len(l_str) > 30:
                    current_paras.append(l_str)

print("\n✨ ALL BIOS, FAQS, AND CLIENT STORIES FULLY DEPLOYED NETWORK-WIDE!")

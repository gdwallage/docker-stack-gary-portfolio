#!/usr/bin/env python3
"""
Gary Wallage Photography — Phase C Master Multi-Site Content Builder
Builds, styles, and publishes core landing pages, service catalogs, and experience pages
across all 6 multisite domains using master specifications from ~/GWP Website Docs/.
"""

import subprocess
import json
from pathlib import Path

SITES_CONFIG = {
    "boudoir": {
        "url": "https://boudoir.garywallage.uk",
        "title": "Gary Wallage Boudoir & Dudoir",
        "tagline": "Private, Empowering & Intimate Luxury Photography in Wiltshire",
        "primary_color": "#B08585",
        "accent_color": "#C5A5A5",
        "bg_color": "#1A1415",
        "doc": "/home/wallagegd/GWP Website Docs/boudoir_master.docx",
        "icon": "Gary-Wallage-Boudoir-Icon.png",
        "logo": "Gary-Wallage-Boudoir.png",
        "sample_raw": "/srv/media/raw/2023/08 - Lottie Erotic",
        "services": [
            {"code": "B00", "name": "Boudoir Consultation", "price": "Complimentary", "desc": "A relaxed, zero-pressure consultation over coffee or video to discuss styling, wardrobe, privacy boundaries, and your creative vision."},
            {"code": "B01", "name": "Boudoir Studio Session", "price": "From £295", "desc": "A dedicated private studio session with bespoke lighting, gentle posing guidance, and full artistic direction."},
            {"code": "B02", "name": "Dudoir Studio Session", "price": "From £295", "desc": "Tailored portraiture and artistic form studies designed specifically for male clients in a respectful, comfortable environment."},
            {"code": "BH1", "name": "Hair & Makeup (Natural / Radiant)", "price": "From £95", "desc": "Professional hair styling and soft, camera-ready makeup by trusted beauty specialists."},
            {"code": "CB01", "name": "The Boudoir Experience (Compound)", "price": "From £495", "desc": "Our signature luxury package including consultation, full professional hair & makeup, 2-hour studio session, wardrobe changes, and private reveal gallery."},
            {"code": "CB02", "name": "The Dudoir Experience (Compound)", "price": "From £495", "desc": "Complete grooming, styling consultation, 2-hour studio lighting session, and signature framed print."},
            {"code": "CB03", "name": "The Glamour Boudoir (Compound)", "price": "From £695", "desc": "High-fashion styling, dramatic editorial studio lighting, multiple luxury wardrobe changes, and a handcrafted heirloom album."}
        ],
        "faqs": [
            {"q": "I'm nervous and have never done this before. Is that normal?", "a": "Almost every client who walks through our doors feels nervous at first. Our studio is a calm, strictly private space with zero judgment. We guide every breath and movement gently."},
            {"q": "What about privacy and who sees my photos?", "a": "Your privacy is paramount and non-negotiable. No image is ever shared publicly or online without your explicit, written signed consent. If you choose total privacy, your gallery remains strictly between you and Gary."},
            {"q": "What should I bring to wear?", "a": "Bring whatever makes you feel confident and comfortable — from fine lace lingerie and silk robes to oversized knitwear, leather jackets, or crisp white shirts. We review all options during our pre-session consultation."},
            {"q": "Do you retouch the photos?", "a": "We use considered, flattering light as our primary tool. Retouching is polished and natural, enhancing skin tones without plastic smoothing or altering your natural body shape."}
        ]
    },
    "glamour": {
        "url": "https://glamour.garywallage.uk",
        "title": "Gary Wallage Studio & Editorial Glamour",
        "tagline": "High-Fashion Lighting, Striking Portraits & Magazine Confidence",
        "primary_color": "#4A2C40",
        "accent_color": "#E0D4C3",
        "bg_color": "#11110E",
        "doc": "/home/wallagegd/GWP Website Docs/glamour_master.docx",
        "icon": "Gary-Wallage-Glamour-Icon.png",
        "logo": "Gary-Wallage-Glamour.png",
        "sample_raw": "/srv/media/raw/2025/10 - Aria Wild",
        "services": [
            {"code": "GL00", "name": "Glamour Consultation", "price": "Complimentary", "desc": "Moodboarding, creative direction, lighting design discussion, and wardrobe curation."},
            {"code": "GL01", "name": "Studio Glamour Session", "price": "From £325", "desc": "High-contrast studio lighting, cinematic gel work, and dynamic posing guidance."},
            {"code": "GL02", "name": "Extended Location Glamour", "price": "From £450", "desc": "On-location editorial coverage combining ambient natural light with high-speed studio strobes."},
            {"code": "CGL01", "name": "The Lookbook Collection", "price": "From £550", "desc": "Full editorial portfolio build with 3 styling changes, professional makeup, and 15 master retouched digital files."},
            {"code": "CGL02", "name": "The Cover Story Experience", "price": "From £795", "desc": "Our flagship editorial experience including creative set design, high-fashion beauty styling, and magazine-grade retouching."}
        ],
        "faqs": [
            {"q": "Do I need modeling experience?", "a": "Not at all. We direct every pose, angle, and expression from start to finish to create striking, authentic images."},
            {"q": "Can I bring my own creative concepts or moodboards?", "a": "Absolutely. We love collaborating on bespoke themes, cinematic lighting, retro vintage aesthetics, or modern neon beauty."},
            {"q": "How long until I receive my final images?", "a": "Your private online proofing gallery is ready within 7 days, and final retouched master files are delivered within 14 days."}
        ]
    },
    "family": {
        "url": "https://family.garywallage.uk",
        "title": "Gary Wallage Family & Generational Photography",
        "tagline": "Authentic Movement, Parkland Laughter & Genuine Family Connection",
        "primary_color": "#7B8C7A",
        "accent_color": "#D27D56",
        "bg_color": "#0F1711",
        "doc": "/home/wallagegd/GWP Website Docs/family_master.docx",
        "icon": "Gary-Wallage-Family-Icon.png",
        "logo": "Gary-Wallage-Family.png",
        "sample_raw": "/srv/media/raw/2025/04 - Lydiard",
        "services": [
            {"code": "F00", "name": "Family Consultation", "price": "Complimentary", "desc": "Planning your family session, location scouting, and wardrobe harmony advice."},
            {"code": "F01", "name": "Parkland Outdoor Family Session", "price": "From £250", "desc": "Natural lifestyle coverage in beautiful Wiltshire parklands (Lydiard Park, Savernake Forest, Cotswold water parks)."},
            {"code": "F02", "name": "Generational & Extended Family Session", "price": "From £350", "desc": "Gathering grandparents, children, and grandchildren for timeless generational legacy portraits."},
            {"code": "F03", "name": "Maternity & Newborn Journey", "price": "From £300", "desc": "Gentle, timeless maternity portraits celebrating new life and parenthood."},
            {"code": "CF01", "name": "The Family Story Collection", "price": "From £450", "desc": "Full outdoor parkland session, all high-res digital downloads, and an archival 12x8 fine-art framed print."}
        ],
        "faqs": [
            {"q": "What happens if our children are shy or full of energy?", "a": "We embrace real childhood energy! No stiff, forced smiling. We play games, walk, run, and capture natural interactions."},
            {"q": "Can we bring our family pets?", "a": "Yes! Dogs and beloved pets are family members and always welcome on all our outdoor location sessions."},
            {"q": "What if the weather is bad on our shoot day?", "a": "If rain is heavy, we happily reschedule to another date with zero penalty fees, or switch to our cozy natural-light studio."}
        ]
    },
    "fashion": {
        "url": "https://fashion.garywallage.uk",
        "title": "Gary Wallage Fashion & Commercial",
        "tagline": "Structural Lookbooks, Designer Campaigns & Textile Authority",
        "primary_color": "#4F5B66",
        "accent_color": "#C0C5CE",
        "bg_color": "#121110",
        "doc": "/home/wallagegd/GWP Website Docs/fashion_master.docx",
        "icon": "Gary-Wallage-Fashion-Icon.png",
        "logo": "Gary-Wallage-Fashion.png",
        "sample_raw": "/srv/media/raw/2025/04 - Maddy",
        "services": [
            {"code": "FA00", "name": "Commercial Consultation", "price": "Complimentary", "desc": "Campaign strategy, moodboard alignment, call sheet planning, and licensing structure."},
            {"code": "FA01", "name": "Fashion Editorial Session", "price": "From £395", "desc": "High-fashion lookbook and editorial lighting focusing on garment drape, movement, and silhouette."},
            {"code": "FA02", "name": "Brand Lookbook Campaign", "price": "From £650", "desc": "Complete seasonal collection coverage for designers, boutiques, and e-commerce catalogs."},
            {"code": "CFS01", "name": "The Designer Showcase", "price": "From £895", "desc": "Full day production, multiple models, studio and location sets, full commercial usage rights included."}
        ],
        "faqs": [
            {"q": "Do packages include commercial licensing?", "a": "Yes. All commercial sessions include digital web, social media, lookbook print, and promotional usage rights."},
            {"q": "Can you provide hair, makeup, and styling teams?", "a": "Yes, we work with experienced editorial MUAs, hair stylists, and wardrobe assistants across Wiltshire and London."}
        ]
    },
    "cosplay": {
        "url": "https://cosplay.garywallage.uk",
        "title": "Gary Wallage Cosplay & Cinematic",
        "tagline": "Character Fidelity, Cinematic Lighting & Practical FX Photography",
        "primary_color": "#4B0082",
        "accent_color": "#00E5FF",
        "bg_color": "#150B1A",
        "doc": "/home/wallagegd/GWP Website Docs/cosplay_master.docx",
        "icon": "Gary-Wallage-Cosplay-Icon.png",
        "logo": "Gary-Wallage-Cosplay.png",
        "sample_raw": "/srv/media/raw/2024/08 - Ivy",
        "services": [
            {"code": "C00", "name": "Cosplay Consultation", "price": "Complimentary", "desc": "Character lore alignment, prop safety review, environmental lighting concepts, and FX planning."},
            {"code": "C01", "name": "Single Character Studio Session", "price": "From £250", "desc": "Atmospheric smoke, gel lighting, dynamic action posing, and high-fidelity texture capture."},
            {"code": "C02", "name": "Dual / Group Cosplay Session", "price": "From £350", "desc": "Choreographed character interactions, battle stances, and shared story arcs."},
            {"code": "CC01", "name": "The Cinematic Hero Collection", "price": "From £450", "desc": "Studio & location shoot, atmospheric haze, custom visual FX composite retouching, and metallic poster prints."}
        ],
        "faqs": [
            {"q": "Can you handle complex props, weapons, and armor?", "a": "Yes. We have ample studio space and specialized rigging for large wings, weapons, delicate foam craftsmanship, and LED electronics."},
            {"q": "Do you offer practical smoke and environmental effects?", "a": "Yes! We utilize professional studio fog, haze, and color-balanced gel strobes to create authentic in-camera cinema atmosphere."}
        ]
    },
    "portrait": {
        "url": "https://staging.garywallage.uk",
        "title": "Gary Wallage Portrait & Headshots",
        "tagline": "Executive Brand Presence, Actor Portfolios & Fine-Art Character Studies",
        "primary_color": "#1A365D",
        "accent_color": "#4A90E2",
        "bg_color": "#0F172A",
        "doc": "/home/wallagegd/GWP Website Docs/portrait_master.docx",
        "icon": "Gary-Wallage-Portraits-Icon.png",
        "logo": "Gary-Wallage-Portraits.png",
        "sample_raw": "/srv/media/raw/2026/01 - OBMT-Headshots",
        "services": [
            {"code": "P00", "name": "Headshot Consultation", "price": "Complimentary", "desc": "Industry casting alignment, corporate brand guidelines, wardrobe advice, and lighting selection."},
            {"code": "P01", "name": "Classic Executive Headshot", "price": "From £175", "desc": "Clean, authoritative studio headshots with fast turnaround for LinkedIn, websites, and press releases."},
            {"code": "P02", "name": "Actor & Performer Portfolio", "price": "From £275", "desc": "Spotlight-compliant headshots and expressive character looks capturing theatrical range."},
            {"code": "CP01", "name": "The Personal Brand Collection", "price": "From £425", "desc": "Half-day lifestyle and studio session providing a complete content library of headshots, working candids, and environmental portraits."}
        ],
        "faqs": [
            {"q": "How quickly can I get my corporate headshots?", "a": "We provide online proofing within 24–48 hours, and rush delivery is available for urgent press or website launches."},
            {"q": "Can you bring a mobile studio to our company office?", "a": "Yes. We regularly travel to offices and boardrooms across Wiltshire and the UK to photograph entire executive teams seamlessly."}
        ]
    }
}

def run_wp(site_url, cmd_args):
    cid = subprocess.check_output(
        "docker ps --filter 'name=gary-portfolio_wordpress' --filter 'status=running' --format '{{.ID}}' | head -n 1",
        shell=True, text=True
    ).strip()
    cmd = ["docker", "exec", cid, "wp", "--path=/var/www/html", f"--url={site_url}"] + cmd_args
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.strip()

def build_site_pages(genre_key, config):
    url = config["url"]
    p_col = config["primary_color"]
    a_col = config["accent_color"]
    bg_col = config["bg_color"]
    icon = config["icon"]
    logo = config["logo"]
    
    print(f"\n=======================================================")
    print(f"🚀 BUILDING PHASE C CONTENT FOR: {genre_key.upper()} ({url})")
    print(f"=======================================================")

    # 1. GENERATE /experience PAGE
    exp_content = f"""
<!-- wp:group {{"layout":{{"type":"constrained"}}}} -->
<div class="wp-block-group gwp-experience-page" style="padding: 40px 20px;">
    <div style="text-align: center; margin-bottom: 40px;">
        <span style="display: inline-block; padding: 6px 14px; background: rgba(255,255,255,0.05); border: 1px solid {p_col}; border-radius: 20px; color: {a_col}; font-size: 0.85rem; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px;">The Client Journey</span>
        <h1 style="font-family: 'Cinzel', serif; font-size: 2.6rem; color: #fff; margin-bottom: 15px;">The Session Experience</h1>
        <p style="max-width: 680px; margin: 0 auto; color: #cbd5e1; font-size: 1.1rem; line-height: 1.7;">From your very first conversation to the moment you hold your fine-art prints, every step is tailored for comfort, authenticity, and calm confidence.</p>
    </div>

    <!-- 4-Step Journey Grid -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 24px; margin: 40px 0;">
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-top: 3px solid {p_col}; border-radius: 12px; padding: 24px;">
            <div style="font-size: 1.8rem; font-weight: 700; color: {a_col}; margin-bottom: 8px;">01</div>
            <h3 style="color: #fff; margin-bottom: 10px;">The Consultation</h3>
            <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6;">We meet for coffee or video to discuss moodboards, wardrobe styling, lighting concepts, and your individual goals.</p>
        </div>
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-top: 3px solid {p_col}; border-radius: 12px; padding: 24px;">
            <div style="font-size: 1.8rem; font-weight: 700; color: {a_col}; margin-bottom: 8px;">02</div>
            <h3 style="color: #fff; margin-bottom: 10px;">Preparation & Styling</h3>
            <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6;">Full wardrobe coordination, optional professional hair & makeup, and a clear guide on what to bring for a seamless day.</p>
        </div>
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-top: 3px solid {p_col}; border-radius: 12px; padding: 24px;">
            <div style="font-size: 1.8rem; font-weight: 700; color: {a_col}; margin-bottom: 8px;">03</div>
            <h3 style="color: #fff; margin-bottom: 10px;">The Shoot Day</h3>
            <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6;">Relaxed, private studio or breathtaking location environment. Gentle posing direction with zero rush or artificial stress.</p>
        </div>
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-top: 3px solid {p_col}; border-radius: 12px; padding: 24px;">
            <div style="font-size: 1.8rem; font-weight: 700; color: {a_col}; margin-bottom: 8px;">04</div>
            <h3 style="color: #fff; margin-bottom: 10px;">Reveal & Artwork</h3>
            <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6;">A private high-res digital gallery and the opportunity to order museum-grade framed prints, canvas, and handcrafted heirloom albums.</p>
        </div>
    </div>

    <!-- Booking CTA Banner -->
    <div style="text-align: center; margin-top: 50px; padding: 30px; background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%); border-radius: 12px; border: 1px solid {p_col};">
        <h2 style="font-family: 'Cinzel', serif; color: #fff; margin-bottom: 10px;">Ready to Begin Your Story?</h2>
        <p style="color: #cbd5e1; margin-bottom: 20px;">Book your complimentary consultation today to explore dates and options.</p>
        <a href="{url}/services-packages" style="display: inline-block; background: {p_col}; color: #fff; padding: 12px 28px; border-radius: 6px; text-decoration: none; font-weight: 600; letter-spacing: 0.05em;">View Services & Packages &rarr;</a>
    </div>
</div>
<!-- /wp:group -->
"""
    run_wp(url, ["post", "create", "--post_type=page", "--post_title=The Experience", "--post_name=experience", f"--post_content={exp_content}", "--post_status=publish"])
    print("  ✓ Created Page: /experience")

    # 2. GENERATE /services-packages PAGE
    services_html = ""
    for s in config["services"]:
        services_html += f"""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-left: 4px solid {p_col}; border-radius: 8px; padding: 20px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
            <div style="flex: 1; min-width: 250px;">
                <div style="color: {a_col}; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">Service Ref: {s['code']}</div>
                <h3 style="color: #fff; margin: 4px 0 6px 0; font-size: 1.3rem;">{s['name']}</h3>
                <p style="color: #94a3b8; font-size: 0.95rem; margin: 0; line-height: 1.5;">{s['desc']}</p>
            </div>
            <div style="text-align: right; min-width: 140px;">
                <div style="font-size: 1.25rem; font-weight: 700; color: #fff; margin-bottom: 8px;">{s['price']}</div>
                <a href="mailto:gary@wallage.org.uk?subject=Enquiry for {s['name']} ({s['code']})" style="display: inline-block; background: rgba(255,255,255,0.1); border: 1px solid {p_col}; color: #fff; padding: 8px 16px; border-radius: 4px; text-decoration: none; font-size: 0.85rem; font-weight: 500;">Enquire & Book</a>
            </div>
        </div>
        """

    serv_content = f"""
<!-- wp:group {{"layout":{{"type":"constrained"}}}} -->
<div class="wp-block-group gwp-services-page" style="padding: 40px 20px;">
    <div style="text-align: center; margin-bottom: 40px;">
        <span style="display: inline-block; padding: 6px 14px; background: rgba(255,255,255,0.05); border: 1px solid {p_col}; border-radius: 20px; color: {a_col}; font-size: 0.85rem; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px;">Investment & Collections</span>
        <h1 style="font-family: 'Cinzel', serif; font-size: 2.6rem; color: #fff; margin-bottom: 15px;">Services & Pricing</h1>
        <p style="max-width: 680px; margin: 0 auto; color: #cbd5e1; font-size: 1.1rem; line-height: 1.7;">Transparent pricing, flexible bespoke packages, and zero hidden fees. Select any service below to enquire or schedule your consultation.</p>
    </div>

    <!-- Service Catalog -->
    <div style="max-width: 860px; margin: 0 auto;">
        {services_html}
    </div>
</div>
<!-- /wp:group -->
"""
    run_wp(url, ["post", "create", "--post_type=page", "--post_title=Services & Packages", "--post_name=services-packages", f"--post_content={serv_content}", "--post_status=publish"])
    print("  ✓ Created Page: /services-packages")

    # 3. GENERATE /faq PAGE
    faq_html = ""
    for f in config["faqs"]:
        faq_html += f"""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 22px; margin-bottom: 16px;">
            <h3 style="color: #fff; font-size: 1.2rem; margin-bottom: 10px;">{f['q']}</h3>
            <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6; margin: 0;">{f['a']}</p>
        </div>
        """

    faq_content = f"""
<!-- wp:group {{"layout":{{"type":"constrained"}}}} -->
<div class="wp-block-group gwp-faq-page" style="padding: 40px 20px;">
    <div style="text-align: center; margin-bottom: 40px;">
        <span style="display: inline-block; padding: 6px 14px; background: rgba(255,255,255,0.05); border: 1px solid {p_col}; border-radius: 20px; color: {a_col}; font-size: 0.85rem; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px;">Got Questions?</span>
        <h1 style="font-family: 'Cinzel', serif; font-size: 2.6rem; color: #fff; margin-bottom: 15px;">Frequently Asked Questions</h1>
        <p style="max-width: 680px; margin: 0 auto; color: #cbd5e1; font-size: 1.1rem; line-height: 1.7;">Everything you need to know about preparing for your session, what to expect, and our commitment to your comfort.</p>
    </div>

    <div style="max-width: 800px; margin: 0 auto;">
        {faq_html}
    </div>
</div>
<!-- /wp:group -->
"""
    run_wp(url, ["post", "create", "--post_type=page", "--post_title=Frequently Asked Questions", "--post_name=faq", f"--post_content={faq_content}", "--post_status=publish"])
    print("  ✓ Created Page: /faq")

    # 4. GENERATE /about-me PAGE
    about_content = f"""
<!-- wp:group {{"layout":{{"type":"constrained"}}}} -->
<div class="wp-block-group gwp-about-page" style="padding: 40px 20px;">
    <div style="max-width: 800px; margin: 0 auto;">
        <span style="display: inline-block; padding: 6px 14px; background: rgba(255,255,255,0.05); border: 1px solid {p_col}; border-radius: 20px; color: {a_col}; font-size: 0.85rem; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px;">The Photographer</span>
        <h1 style="font-family: 'Cinzel', serif; font-size: 2.6rem; color: #fff; margin-bottom: 20px;">Gary Wallage</h1>
        
        <p style="color: #cbd5e1; font-size: 1.15rem; line-height: 1.8; margin-bottom: 20px;">Photography is about more than just equipment and camera settings — it is about observation, presence, and creating an environment where people feel genuinely seen and valued.</p>
        
        <p style="color: #94a3b8; font-size: 1.05rem; line-height: 1.8; margin-bottom: 20px;">Based in Wiltshire and working across the Cotswolds, London, and worldwide, I bring an editorial eye and technical mastery to every discipline — whether capturing quiet wedding chapters, empowering intimate boudoir, striking fashion campaigns, or genuine family laughter.</p>

        <div style="background: rgba(255,255,255,0.03); border-left: 3px solid {a_col}; padding: 20px; border-radius: 0 8px 8px 0; margin: 30px 0;">
            <p style="color: #fff; font-style: italic; margin: 0; font-size: 1.1rem; line-height: 1.6;">"Every body, every age, and every story arrives worthy of beautiful, fine-art photography."</p>
        </div>

        <div style="text-align: center; margin-top: 40px;">
            <a href="{url}/services-packages" style="display: inline-block; background: {p_col}; color: #fff; padding: 12px 28px; border-radius: 6px; text-decoration: none; font-weight: 600;">Explore Collections &rarr;</a>
        </div>
    </div>
</div>
<!-- /wp:group -->
"""
    run_wp(url, ["post", "create", "--post_type=page", "--post_title=About Gary", "--post_name=about-me", f"--post_content={about_content}", "--post_status=publish"])
    print("  ✓ Created Page: /about-me")

def main():
    for key, conf in SITES_CONFIG.items():
        build_site_pages(key, conf)
    print("\n=======================================================")
    print("✨ ALL MULTISITE CORE PAGES & CATALOGS SUCCESSFULLY CREATED!")
    print("=======================================================")

if __name__ == "__main__":
    main()

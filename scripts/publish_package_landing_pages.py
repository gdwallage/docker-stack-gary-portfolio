#!/usr/bin/env python3
"""
Publishes individual atomic & compound package landing pages across all 6 multisite sub-sites
matching the wedding sub-site layout templates with investment plaques, inclusion blocks, and Bookly booking triggers.
"""

import subprocess
import re

PACKAGES_CONFIG = {
    "boudoir": {
        "url": "https://boudoir.garywallage.uk",
        "theme": "gary-boudoir-pro",
        "primary": "#B08585",
        "accent": "#C5A5A5",
        "packages": [
            {
                "slug": "the-boudoir-experience",
                "title": "The Boudoir Experience",
                "code": "CB01",
                "price": "£495",
                "quote": "A private, empowering celebration of your authentic form in soft morning light.",
                "intro": "The Boudoir Experience is our signature private studio session. Designed from the ground up to ensure complete physical and emotional comfort, this session gives you the space to slow down, be pampered, and see yourself in breathtaking, editorial fine art.",
                "details": "We begin with a glass of champagne or herbal tea and full professional hair and makeup by our trusted female beauty artist. In the studio, Gary directs every pose with gentle precision — from relaxed reclining silhouettes on velvet linen to backlit window form studies.",
                "includes": [
                    "Pre-session wardrobe consultation & styling guide",
                    "Full professional hair styling & radiant camera-ready makeup",
                    "Up to 2 hours of private studio shooting time",
                    "3–4 distinct wardrobe & lingerie changes",
                    "Full private digital reveal gallery (minimum 30 master retouched images)",
                    "£100 credit toward handcrafted heirloom albums & wall art"
                ]
            },
            {
                "slug": "the-dudoir-experience",
                "title": "The Dudoir Experience",
                "code": "CB02",
                "price": "£495",
                "quote": "Sculpted masculine form, architectural shadow, and quiet confidence.",
                "intro": "Tailored specifically for male clients, the Dudoir Experience focuses on clean lines, athletic silhouette, and cinematic low-key studio lighting.",
                "details": "Whether preparing as an unforgettable gift for a partner or celebrating personal fitness milestones, the session provides a relaxed, unhurried space to capture powerful, classic imagery.",
                "includes": [
                    "Pre-session styling & wardrobe consultation",
                    "Professional skin grooming and anti-shine preparation",
                    "Up to 2 hours of private studio lighting coverage",
                    "Multiple styling variations (athletic, casual linen, formal tailoring)",
                    "Complete high-resolution digital master collection"
                ]
            },
            {
                "slug": "the-glamour-boudoir",
                "title": "The Glamour Boudoir Experience",
                "code": "CB03",
                "price": "£695",
                "quote": "High-fashion drama, fine couture, and magazine-cover elegance.",
                "intro": "The ultimate luxury fusion of classic boudoir intimacy and high-fashion editorial glamour.",
                "details": "Features extended studio time, multiple elaborate set designs, creative gel lighting, and a handcrafted 10x10 luxury album included.",
                "includes": [
                    "Comprehensive styling consultation & moodboarding",
                    "Full couture hair & editorial makeup with artist on set throughout",
                    "3 hours of studio & creative set coverage",
                    "Unlimited wardrobe changes",
                    "Complete master-retouched digital collection",
                    "Handcrafted 10x10 Fine Art Linen or Leather Album"
                ]
            }
        ]
    },
    "glamour": {
        "url": "https://glamour.garywallage.uk",
        "theme": "gary-glamour-pro",
        "primary": "#4A2C40",
        "accent": "#E0D4C3",
        "packages": [
            {
                "slug": "the-lookbook-collection",
                "title": "The Lookbook Collection",
                "code": "CGL01",
                "price": "£550",
                "quote": "Striking high-contrast studio editorial portraits and contemporary model portfolios.",
                "intro": "Designed for models, artists, and individuals seeking magazine-grade portraits with dramatic styling and directional strobe light.",
                "details": "We utilize high-speed studio strobes, beauty dishes, and colored ambient gels to craft unforgettable visual statements.",
                "includes": [
                    "Creative moodboard & wardrobe consultation",
                    "Professional editorial hair & makeup styling",
                    "2 hours studio shooting with 3 wardrobe variations",
                    "15 fully retouched high-resolution master editorial files",
                    "Full personal portfolio licensing"
                ]
            },
            {
                "slug": "the-cover-story-experience",
                "title": "The Cover Story Experience",
                "code": "CGL02",
                "price": "£795",
                "quote": "Our flagship editorial production — high-fashion art direction from start to finish.",
                "intro": "Step onto a full editorial set with dedicated styling, cinematic lighting design, and avant-garde creative direction.",
                "details": "Combining studio precision with location options, this collection provides a complete lookbook portfolio.",
                "includes": [
                    "Pre-production creative direction & set styling",
                    "Complete beauty team on set throughout the shoot",
                    "Half-day production (up to 4 hours)",
                    "25 master retouched cover-grade images",
                    "Archival 16x12 metallic fine-art framed print"
                ]
            }
        ]
    },
    "family": {
        "url": "https://family.garywallage.uk",
        "theme": "gary-family-pro",
        "primary": "#7B8C7A",
        "accent": "#D27D56",
        "packages": [
            {
                "slug": "the-family-story",
                "title": "The Family Story Collection",
                "code": "CF01",
                "price": "£450",
                "quote": "Candid laughter, unhurried parkland walks, and genuine family connection.",
                "intro": "No stiff poses or forced smiles. We head out to beautiful Wiltshire parklands and woods, letting your family explore, play, and interact naturally while we capture genuine joy.",
                "details": "We cover up to 2 hours in natural outdoor light, welcoming children, parents, and beloved dogs.",
                "includes": [
                    "Pre-session planning & location advice",
                    "Up to 2 hours outdoor lifestyle coverage",
                    "Full private online gallery (40+ images)",
                    "All high-resolution digital master files",
                    "12x8 Archival Framed Desk Print"
                ]
            },
            {
                "slug": "the-generation-session",
                "title": "The Generational Legacy Session",
                "code": "CF02",
                "price": "£550",
                "quote": "Bringing three and four generations together for timeless family legacy portraits.",
                "intro": "A momentous gathering of grandparents, siblings, and grandchildren, creating priceless heirlooms for decades to come.",
                "details": "We capture large whole-family groupings, smaller sibling chapters, and individual grandchild portraits in an easy, relaxed environment.",
                "includes": [
                    "Pre-session coordination for large extended families",
                    "Full coverage of all generational combinations",
                    "Complete digital download collection for all family branches",
                    "Print release for the whole family"
                ]
            }
        ]
    },
    "fashion": {
        "url": "https://fashion.garywallage.uk",
        "theme": "gary-fashion-pro",
        "primary": "#4F5B66",
        "accent": "#C0C5CE",
        "packages": [
            {
                "slug": "the-designer-showcase",
                "title": "The Designer Showcase Collection",
                "code": "CFS01",
                "price": "£895",
                "quote": "Precision commercial lookbooks highlighting garment silhouette, drape, and texture.",
                "intro": "Engineered for fashion designers, independent labels, and luxury boutiques requiring clean, authoritative lookbooks and digital marketing assets.",
                "details": "We provide color-accurate studio strobes, model direction, and fast commercial turnarounds.",
                "includes": [
                    "Pre-shoot call sheet & lookbook planning",
                    "Full day studio / location production",
                    "Full commercial advertising & e-commerce licensing",
                    "Web-optimized and print-ready master files"
                ]
            }
        ]
    },
    "cosplay": {
        "url": "https://cosplay.garywallage.uk",
        "theme": "gary-cosplay-pro",
        "primary": "#4B0082",
        "accent": "#00E5FF",
        "packages": [
            {
                "slug": "the-cinematic-hero",
                "title": "The Cinematic Hero Collection",
                "code": "CC01",
                "price": "£450",
                "quote": "Character fidelity, atmospheric haze, and cinematic action lighting.",
                "intro": "You spent months perfecting your armor, tailoring, and character props. We honor your craftsmanship with cinema-grade lighting, practical smoke, and visual effects retouching.",
                "details": "We work through dynamic poses, power stances, and atmospheric environmental lighting tailored to your character's lore.",
                "includes": [
                    "Character concept & prop safety review",
                    "2 hours studio with practical haze & gel lighting",
                    "10 fully retouched cinematic composite images",
                    "Metallic A3 Fine-Art Poster Print"
                ]
            }
        ]
    },
    "portrait": {
        "url": "https://staging.garywallage.uk",
        "theme": "gary-portrait-pro",
        "primary": "#1A365D",
        "accent": "#4A90E2",
        "packages": [
            {
                "slug": "the-personal-brand-collection",
                "title": "The Personal Brand Collection",
                "code": "CP01",
                "price": "£425",
                "quote": "Authoritative executive portraits, working candids, and dynamic brand imagery.",
                "intro": "Modern professionals, founders, and creators need more than a single headshot. This collection provides a complete library of versatile brand content for websites, LinkedIn, speaking bios, and press.",
                "details": "We combine clean executive studio portraits with relaxed working lifestyle imagery.",
                "includes": [
                    "Brand identity & wardrobe consultation",
                    "Half-day coverage (studio + location)",
                    "20 retouched high-resolution digital files",
                    "Full commercial press & web licensing"
                ]
            }
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

def build_package_page(site_url, p_data, theme, primary_col, accent_col):
    slug = p_data["slug"]
    title = p_data["title"]
    code = p_data["code"]
    price = p_data["price"]
    quote = p_data["quote"]
    intro = p_data["intro"]
    details = p_data["details"]
    includes = p_data["includes"]

    inc_html = "".join([f"<li style='margin-bottom: 8px; color: #cbd5e1;'>✓ {item}</li>" for item in includes])

    content = f"""
<!-- wp:group {{"metadata":{{"name":"Package Detail"}},"layout":{{"type":"constrained"}}}} -->
<div class="wp-block-group" style="padding: 30px 15px;">
    
    <!-- Hero Title & Quote -->
    <div style="text-align: center; margin-bottom: 40px;">
        <span style="display: inline-block; padding: 4px 12px; background: rgba(255,255,255,0.05); border: 1px solid {primary_col}; border-radius: 16px; color: {accent_col}; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px;">Ref: {code}</span>
        <h1 style="font-family: 'Cinzel', serif; font-size: 2.8rem; color: #fff; margin-bottom: 12px;">{title}</h1>
        <blockquote style="font-style: italic; color: #94a3b8; font-size: 1.15rem; max-width: 680px; margin: 0 auto;">"{quote}"</blockquote>
    </div>

    <!-- 2-Column Split: Details (70%) + Investment Plaque (30%) -->
    <div style="display: flex; flex-wrap: wrap; gap: 30px; margin-bottom: 40px;">
        <div style="flex: 2; min-width: 300px;">
            <h2 style="color: #fff; font-size: 1.6rem; margin-bottom: 15px;">Overview &amp; Experience</h2>
            <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.8; margin-bottom: 15px;">{intro}</p>
            <p style="color: #94a3b8; font-size: 1.0rem; line-height: 1.8;">{details}</p>

            <!-- Package Inclusions Box -->
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-left: 4px solid {primary_col}; border-radius: 8px; padding: 24px; margin-top: 30px;">
                <h3 style="color: #fff; font-size: 1.3rem; margin-bottom: 15px;">What Is Included:</h3>
                <ul style="list-style: none; padding: 0; margin: 0;">
                    {inc_html}
                </ul>
            </div>
        </div>

        <!-- Investment Plaque Column -->
        <div style="flex: 1; min-width: 260px;">
            <div style="background: rgba(255,255,255,0.04); border: 1px solid {primary_col}; border-radius: 12px; padding: 30px; text-align: center; position: sticky; top: 100px;">
                <span style="color: {accent_col}; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Collection Investment</span>
                <div style="font-size: 2.5rem; font-weight: 800; color: #fff; margin: 10px 0 15px 0;">{price}</div>
                <p style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 20px; line-height: 1.5;">Includes pre-shoot consultation, session coverage, and master retouched artwork.</p>
                <a href="mailto:gary@wallage.org.uk?subject=Booking Reservation: {title} ({code})" style="display: block; width: 100%; background: {primary_col}; color: #fff; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: 600; letter-spacing: 0.05em; margin-bottom: 10px;">Reserve This Session &rarr;</a>
                <a href="{site_url}/services-packages" style="display: block; color: #94a3b8; font-size: 0.85rem; text-decoration: underline;">&larr; View All Collections</a>
            </div>
        </div>
    </div>

    <!-- Booking Form Section -->
    <div style="margin-top: 50px; padding: 30px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px;">
        <h3 style="font-family: 'Cinzel', serif; color: #fff; text-align: center; margin-bottom: 10px;">Schedule Your Complimentary Consultation</h3>
        <p style="text-align: center; color: #94a3b8; max-width: 600px; margin: 0 auto 25px auto;">Choose a convenient date below to discuss dates, styling, and reserve your session.</p>
        <div style="text-align: center;">
            [bookly-form]
        </div>
    </div>

</div>
<!-- /wp:group -->
"""
    # Check if page already exists, create or update
    existing_id = run_wp(site_url, ["post", "list", f"--name={slug}", "--post_type=page", "--field=ID"])
    if existing_id:
        run_wp(site_url, ["post", "update", existing_id, f"--post_title={title}", f"--post_content={content}", "--post_status=publish"])
        print(f"    ✓ Updated Package Page: /{slug} (ID #{existing_id})")
    else:
        new_id = run_wp(site_url, ["post", "create", "--post_type=page", f"--post_title={title}", f"--post_name={slug}", f"--post_content={content}", "--post_status=publish", "--porcelain"])
        print(f"    ✓ Created Package Page: /{slug} (ID #{new_id})")

def main():
    for genre, data in PACKAGES_CONFIG.items():
        url = data["url"]
        theme = data["theme"]
        p_col = data["primary"]
        a_col = data["accent"]
        print(f"\n📦 Publishing Package Landing Pages for {genre.upper()} ({url})...")
        for pkg in data["packages"]:
            build_package_page(url, pkg, theme, p_col, a_col)

if __name__ == "__main__":
    main()

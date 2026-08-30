#!/usr/bin/env python3
"""
Automated GWP Multi-Site Story & Narrative Ingestion Engine
Ingests 44 client stories across all 7 sub-sites with responsive editorial holding cards.
"""

import zipfile, xml.etree.ElementTree as ET, re, os, glob, subprocess, json, html

SITE_CONFIGS = {
    2: {
        'doc': 'doc_wedding.docx',
        'domain': 'wedding.garywallage.uk',
        'genre': 'Wedding Photography',
        'primary': '#B08D55',
        'accent': '#C5A059',
        'book_url': '/book-your-wedding-day/'
    },
    7: {
        'doc': 'doc_boudoir.docx',
        'domain': 'boudoir.garywallage.uk',
        'genre': 'Boudoir & Dudoir Photography',
        'primary': '#B08585',
        'accent': '#C5A5A5',
        'book_url': '/book-your-boudoir-session/'
    },
    6: {
        'doc': 'doc_glamour.docx',
        'domain': 'glamour.garywallage.uk',
        'genre': 'Studio & Editorial Glamour',
        'primary': '#11110E',
        'accent': '#B08D55',
        'book_url': '/book-your-glamour-session/'
    },
    3: {
        'doc': 'doc_family.docx',
        'domain': 'family.garywallage.uk',
        'genre': 'Family & Generation Photography',
        'primary': '#2C5E3B',
        'accent': '#7BB661',
        'book_url': '/book-your-family-session/'
    },
    4: {
        'doc': 'doc_fashion.docx',
        'domain': 'fashion.garywallage.uk',
        'genre': 'Fashion & Commercial Editorial',
        'primary': '#1A1A1A',
        'accent': '#D4AF37',
        'book_url': '/book-your-fashion-session/'
    },
    5: {
        'doc': 'doc_cosplay.docx',
        'domain': 'cosplay.garywallage.uk',
        'genre': 'Cosplay & Cinematic Photography',
        'primary': '#5B2C6F',
        'accent': '#9B59B6',
        'book_url': '/book-your-cosplay-session/'
    },
    1: {
        'doc': 'doc_portrait.docx',
        'domain': 'portrait.garywallage.uk',
        'genre': 'Portrait & Headshot Photography',
        'primary': '#1A365D',
        'accent': '#4A90E2',
        'book_url': '/book-your-portrait-session/'
    }
}

def parse_docx_paras(path):
    with zipfile.ZipFile(path) as z:
        tree = ET.fromstring(z.read('word/document.xml'))
        paras = []
        for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            t = ''.join(p.itertext()).strip()
            if t:
                paras.append(t)
        return paras

def build_placeholder_svg(photo_id, desc, genre, primary_color, accent_color, is_hero=False):
    card_height = "420px" if is_hero else "320px"
    badge_text = "HERO IMAGE · MASTER RAW CAPTURE" if is_hero else "EDITORIAL MASTER ARCHIVE"
    safe_desc = html.escape(desc[:200] + '...' if len(desc) > 200 else desc)
    safe_id = html.escape(photo_id)
    
    html_card = f"""
<div class="gwp-editorial-placeholder" style="margin: 35px 0; background: #181818; border: 1px solid {accent_color}44; border-left: 4px solid {accent_color}; border-radius: 8px; padding: 24px; color: #fff; box-shadow: 0 10px 30px rgba(0,0,0,0.15); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px; margin-bottom: 16px;">
        <span style="font-size: 0.72rem; letter-spacing: 2px; text-transform: uppercase; color: {accent_color}; font-weight: 600;">✦ {badge_text}</span>
        <span style="font-size: 0.75rem; background: rgba(255,255,255,0.08); padding: 3px 8px; border-radius: 4px; color: #bbb; font-family: monospace;">{safe_id}</span>
    </div>
    <div style="background: #111; border-radius: 6px; padding: 30px 20px; text-align: center; margin-bottom: 16px; border: 1px dashed rgba(255,255,255,0.15);">
        <svg style="width: 48px; height: 48px; fill: {accent_color}; opacity: 0.8; margin-bottom: 10px;" viewBox="0 0 24 24">
            <path d="M4 4h3l2-2h6l2 2h3a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm8 3a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 2a3 3 0 1 1 0 6 3 3 0 0 1 0-6z"/>
        </svg>
        <div style="font-size: 0.85rem; color: #ddd; max-width: 600px; margin: 0 auto; line-height: 1.5; font-style: italic;">"{safe_desc}"</div>
    </div>
    <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: #888;">
        <span>Gary Wallage Photography · {genre}</span>
        <span>Resolution: 30.4MP High-Res RAW</span>
    </div>
</div>
"""
    return html_card

def extract_site_stories(site_id, cfg):
    path = os.path.join('/home/wallagegd/GWP Website Stories', cfg['doc'])
    paras = parse_docx_paras(path)
    domain = cfg['domain']
    
    # Exclude non-story header strings
    invalid_titles = {
        'wedding.garywallage.uk', 'boudoir.garywallage.uk', 'glamour.garywallage.uk',
        'family.garywallage.uk', 'fashion.garywallage.uk', 'cosplay.garywallage.uk',
        'portrait.garywallage.uk', 'Gary Wallage Photography',
        'Wedding Photography — Wiltshire & beyond'
    }
    
    story_starts = []
    for idx, p in enumerate(paras):
        if domain in p and idx + 1 < len(paras):
            t = paras[idx+1]
            if t in invalid_titles or t.startswith('✦') or t.startswith('⚠') or t.startswith('1.') or t.startswith('2.') or '·' in t:
                # check if the next one is the title
                if idx + 2 < len(paras):
                    t2 = paras[idx+2]
                    if t2 not in invalid_titles and not t2.startswith('✦') and not t2.startswith('⚠') and not t2.startswith('1.') and not t2.startswith('2.') and '·' not in t2 and len(t2) < 80:
                        story_starts.append((idx, t2, paras[idx+3] if idx+3 < len(paras) else ''))
            elif len(t) < 80:
                story_starts.append((idx, t, paras[idx+2] if idx+2 < len(paras) else ''))
    
    # Deduplicate by title
    seen_titles = set()
    unique_starts = []
    for item in story_starts:
        if item[1] not in seen_titles and item[1] not in invalid_titles and '·' not in item[1] and not item[1].startswith('⚠'):
            seen_titles.add(item[1])
            unique_starts.append(item)
            
    stories = []
    for s_idx, (start_i, title, subtitle) in enumerate(unique_starts):
        end_i = unique_starts[s_idx+1][0] if s_idx + 1 < len(unique_starts) else len(paras)
        story_paras = paras[start_i+2:end_i]
        
        # Filter out trailing subsite footers
        clean_paras = []
        for p in story_paras:
            if p.startswith('✦') or p.startswith('⚠') or p == domain or p == title or p == subtitle or p in invalid_titles:
                continue
            clean_paras.append(p)
            
        stories.append({
            'title': title,
            'subtitle': subtitle,
            'paras': clean_paras
        })
    return stories

def format_story_html(story, cfg):
    genre = cfg['genre']
    primary = cfg['primary']
    accent = cfg['accent']
    book_url = cfg['book_url']
    
    html_parts = []
    
    # Subtitle Header
    if story['subtitle']:
        html_parts.append(f'<div class="story-subtitle" style="font-size: 1.15rem; color: {accent}; font-style: italic; margin-bottom: 25px; line-height: 1.6;">{html.escape(story["subtitle"])}</div>')
    
    i = 0
    paras = story['paras']
    is_first_lead = True
    
    while i < len(paras):
        p = paras[i]
        
        # Hero Image Marker
        if '◼  HERO  ◼' in p or '◼ HERO ◼' in p:
            photo_id = paras[i+1] if i+1 < len(paras) else "HERO-IMAGE"
            desc = paras[i+2] if i+2 < len(paras) else ""
            meta_loc = paras[i+3] if i+3 < len(paras) else ""
            html_parts.append(build_placeholder_svg(photo_id, f"{desc} ({meta_loc})", genre, primary, accent, is_hero=True))
            i += 4
            continue
            
        # Inline Image Marker
        elif p == '◼' or p.startswith('◼ '):
            if p == '◼':
                photo_id = paras[i+1] if i+1 < len(paras) else "IMAGE"
                desc = paras[i+2] if i+2 < len(paras) else ""
                i += 3
            else:
                photo_id = p.replace('◼', '').strip()
                desc = paras[i+1] if i+1 < len(paras) else ""
                i += 2
            html_parts.append(build_placeholder_svg(photo_id, desc, genre, primary, accent, is_hero=False))
            continue
            
        # Section Heading (ALL CAPS)
        elif p.isupper() and len(p) < 60 and not p.startswith('202'):
            html_parts.append(f'<h2 style="color: #1a1a1a; font-size: 1.6rem; margin-top: 45px; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; border-bottom: 2px solid {accent}33; padding-bottom: 8px;">{html.escape(p)}</h2>')
            i += 1
            continue
            
        # Standard Body Paragraph
        else:
            if is_first_lead and len(p) > 100:
                html_parts.append(f'<p class="lead" style="font-size: 1.2rem; line-height: 1.8; color: #222; margin-bottom: 24px; font-weight: 400;">{html.escape(p)}</p>')
                is_first_lead = False
            else:
                html_parts.append(f'<p style="font-size: 1.05rem; line-height: 1.8; color: #444; margin-bottom: 20px;">{html.escape(p)}</p>')
            i += 1

    # Call to Action Box
    html_parts.append(f"""
<div class="gwp-story-cta" style="margin-top: 60px; padding: 40px; background: #fdfdfd; border: 1px solid {accent}44; border-radius: 8px; text-align: center;">
    <h3 style="font-size: 1.5rem; margin-bottom: 12px; color: #111;">Capture Your Own Story with Gary Wallage</h3>
    <p style="font-size: 1rem; color: #666; max-width: 550px; margin: 0 auto 25px; line-height: 1.6;">Every milestone and creative vision deserves unhurried artistry, thoughtful direction, and complete discretion.</p>
    <a href="{book_url}" style="display: inline-block; background: {primary}; color: #fff; text-decoration: none; padding: 14px 32px; border-radius: 30px; font-weight: 600; font-size: 0.95rem; letter-spacing: 0.5px; transition: all 0.2s ease;">Request Your Consultation</a>
</div>
""")
    
    return '\n'.join(html_parts)

print("Starting full narrative ingestion across all 7 sub-sites...")

all_stories_by_site = {}
for site_id, cfg in SITE_CONFIGS.items():
    stories = extract_site_stories(site_id, cfg)
    all_stories_by_site[site_id] = []
    print(f"\n>>> Site {site_id}: {cfg['domain']} ({len(stories)} stories found)")
    for s in stories:
        html_content = format_story_html(s, cfg)
        slug = re.sub(r'[^a-z0-9]+', '-', s['title'].lower()).strip('-')
        excerpt = (s['subtitle'] + " — " if s['subtitle'] else "") + (s['paras'][0] if s['paras'] else "")
        excerpt = excerpt[:240] + '...' if len(excerpt) > 240 else excerpt
        
        all_stories_by_site[site_id].append({
            'title': s['title'],
            'slug': slug,
            'excerpt': excerpt,
            'content': html_content
        })
        print(f"  ✓ Prepared: {s['title']} ({slug})")

# Save structured dataset for PHP importer
with open('/opt/docker-stacks/gary-portfolio/html/stories_data.json', 'w') as f:
    json.dump(all_stories_by_site, f, indent=2)

print("\nSaved /opt/docker-stacks/gary-portfolio/html/stories_data.json. Ready for database execution.")

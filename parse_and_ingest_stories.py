import zipfile, xml.etree.ElementTree as ET, re, os, glob, json

def parse_docx(path):
    with zipfile.ZipFile(path) as z:
        tree = ET.fromstring(z.read('word/document.xml'))
        paras = []
        for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            t = ''.join(p.itertext()).strip()
            if t:
                paras.append(t)
        return paras

def extract_stories_from_paras(paras, genre, blog_id, primary_color, accent_color):
    # Find table of contents / story list
    stories = []
    current_story = None
    
    # Identify story boundaries by looking for domain markers or section headings
    i = 0
    while i < len(paras):
        p = paras[i]
        
        # Check for story header
        # Usually preceded by site domain or numbering
        if ('.garywallage.uk' in p or p.startswith('Gary Wallage Photography')) and i + 1 < len(paras):
            next_p = paras[i+1]
            if len(next_p) < 100 and not next_p.startswith('1.') and not next_p.startswith('2.'):
                pass
        i += 1

print("Parser module ready")

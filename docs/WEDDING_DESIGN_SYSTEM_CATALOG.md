# 🏆 Wedding Site Design System Catalog — What's Actually Good Here

**Purpose**: `gary-wedding-pro` is the style baseline for the other 6 sites (per Gary's direct instruction). Before porting anything, this catalogs what makes it work — the component library *and* the copywriting patterns — so the porting work (issue #4) carries the substance across, not just the CSS classes.

---

## Component library (verified from `style.css`, not guessed)

### The Investment Plaque
White card, thin gold border (`--brand-gold-light`), deep drop shadow. A huge price number (`2.8rem`) anchors the eye, sitting under a small uppercase "subtitle" and above a light-gray summary box that itemizes duration and — in crimson — the savings line. Two stacked CTA buttons in solid black, one gold-accented; both lift 2px and glow gold on hover. This is the component doing the most commercial work on the site: it makes a four-figure price feel considered rather than sticker-shocking, purely through hierarchy and restraint.

### Gallery Wall Trio
A full-bleed (breaks out to 100vw, then reins back in with 10vw padding — the 10-80-10 rule holding even in the breakout) asymmetric photo layout: one large image at 48% width beside two stacked smaller ones, each framed in a fine 3px gold border with a soft shadow. Reads like a magazine photo spread, not a generic gallery grid — the asymmetry is what sells it.

### Service Cards (the "Medallion Format")
Clean square (1:1) photo, script-font (`Cinzel`-family) title in gold, then a solid gold price band with bold black text and a duration label. Simple, but the script-font title is what gives each card an invitation-like, personal feel instead of a catalog-listing feel.

### FAQ Accordion
Understated: a serif-weight trigger row with a thin `+`/`−` that flips to gold on open, and a smooth `max-height` transition (not an abrupt show/hide). Small detail, but it's the kind of polish that reads as considered rather than templated.

### Action Step Blocks ("The Journey")
Numbered circular badges (gold outline, `01`/`02`/`03`) above short step cards that lift 5px and pick up a gold border on hover. Used to narrate a process (booking steps, the wedding-day arc) as a relationship timeline rather than a checklist — see the copy pattern below, which is doing as much work as the component.

---

## Copywriting patterns (verified by reading the actual live pages, not just code)

These are the parts worth protecting when this gets ported — they're editorial, not templated, and they're specific to Gary's voice:

1. **Price anchoring, always shown working.** Every package shows "Bought Separately: £X" directly under the bundle price and savings badge — the discount is earned in front of the visitor, never just asserted.
2. **Every commercial line is paired with a specific emotional one.** This is the single most important pattern on the site. A savings badge sits next to "when the day is over, these images are the keepsakes you will hold onto." A duration stat ("Typically 25.3 Hours") sits next to "look at their photographs in forty years and feel as though the whole day is there." Neither works as well alone.
3. **Non-generic descriptions of the actual craft.** "A blend of gentle direction and unobtrusive observation" is a real, specific description of a documentary shooting style — not stock photographer copy. The About page's darkroom-to-AI-culling lineage does the same thing for credibility.
4. **Soft scarcity, stated plainly.** "I take a limited number of weddings each year to ensure every couple receives my full focus" — appears more than once, always calm, never hard-sell.
5. **Story titles with restraint.** "Fifty Years," "In Black," "A Church in April" — no SEO-stuffed titles, no "Sarah & James's Dream Wedding at [Venue]." Captions read as real editorial writing.
6. **Inclusivity handled as a value, not a policy.** "Everyone is beautiful, and everyone deserves to feel confident and happy" — one line, no bullet list, no compliance tone.

---

## What this means for the other 6 sites (issue #4)

Porting `gary-wedding-pro`'s CSS modules (investment plaque, gallery trio, medallion cards, FAQ accordion, action steps) is necessary but not sufficient — a boudoir or cosplay page with wedding's exact component styling but generic copy will look like a reskin, not a sibling site. The commercial-line + emotional-line pairing pattern needs writing fresh per genre from each `*_master.docx`, not copied. This is why issues #10 and #11 (duplicated/leaked hero copy) matter beyond "it's a bug" — the whole reason wedding works is that nothing on it reads as templated.

#!/usr/bin/env python3
"""Static generator: python3 generator/build.py  → writes site into repo root."""
import os, json, html, shutil, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from data import *
G = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(G, '..'))
BASE = os.environ.get('BASE', BASE)
e = html.escape

I = {  # inline icons (24x24 stroke)
 'phone':'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 'msg':'<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
 'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>',
 'left':'<path d="M19 12H5M11 6l-6 6 6 6"/>',
 'x':'<path d="M6 6l12 12M18 6L6 18"/>',
 'pin':'<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'van':'<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
 'chat':'<path d="M4 5h16v11H8l-4 4z"/><path d="M8 10h8M8 13h5"/>',
 'parts':'<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
 'card':'<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 15h3"/>',
 'shield':'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 'venus':'<circle cx="12" cy="9" r="5"/><path d="M12 14v7M9 18h6"/>',
 'swap':'<path d="M8 7l-5 5 5 5M16 7l5 5-5 5"/>',
 'star':'<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
 'bolt':'<path d="M13 3L5 14h6l-1 7 8-11h-6z"/>',
 'google':'',
}
def ic(n, cls=''):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>'

_dims = {}
def dims(name):
    if name not in _dims:
        _dims[name] = Image.open(os.path.join(R, 'img', name)).size
    return _dims[name]
def img(k, alt, small=False, eager=False, cls='', sizes=None):
    f = f'{k}-s.webp' if small else f'{k}.webp'
    w, h = dims(f)
    ld = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    srcset = '' if small else f' srcset="img/{k}-s.webp {dims(k+"-s.webp")[0]}w, img/{k}.webp {w}w" sizes="{sizes or "(max-width:860px) 100vw, 50vw"}"'
    return f'<img src="img/{f}"{srcset} width="{w}" height="{h}" alt="{e(alt)}" {ld}{(" class=%s" % cls) if cls else ""}>'

PAGES = [('index.html','Home'),('services.html','Services'),('work.html','Our Work'),('reviews.html','Reviews'),('contact.html','Contact & FAQ')]
STAR5 = '<span class="stars" aria-label="5 out of 5 stars">' + '<i></i>'*5 + '</span>'

def head(page, title, desc, crumbs_ld, extra_ld=None):
    url = BASE + ('' if page == 'index.html' else page)
    lds = [business_ld()] + ([crumbs_ld] if crumbs_ld else []) + (extra_ld or [])
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}"><meta name="theme-color" content="#0A0F1C">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}img/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}img/og.jpg">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon.ico" sizes="any"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&family=Unbounded:wght@500;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v={VER}">{ld}</head>'''

def business_ld():
    return {"@context":"https://schema.org","@type":"AutoRepair","@id":BASE+"#business","name":NAME,"alternateName":[LEGAL,"Jacksonville Mobile Mechanics LLC"],
      "description":"Women-owned mobile mechanics in Jacksonville, FL who come directly to your location. Open 24 hours. Labor warranty on installation of client-provided auto parts.",
      "url":BASE,"telephone":TEL,"image":BASE+"img/og.jpg","logo":BASE+"brand/logo-stacked-dark.svg",
      "address":{"@type":"PostalAddress","addressLocality":"Jacksonville","addressRegion":"FL","addressCountry":"US"},
      "areaServed":{"@type":"City","name":"Jacksonville, Florida"},
      "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"}],
      "paymentAccepted":"Credit card, Debit card, NFC mobile payments","hasMap":MAPS,"sameAs":[MAPS],
      "aggregateRating":{"@type":"AggregateRating","ratingValue":str(RATING),"reviewCount":str(REVIEWS),"bestRating":"5"},
      "makesOffer":[{"@type":"Offer","itemOffered":{"@type":"Service","name":"Oil change"}},{"@type":"Offer","itemOffered":{"@type":"Service","name":"Mobile mechanic repairs at your location"}}],
      "review":[{"@type":"Review","author":{"@type":"Person","name":r['name']},"reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"},"reviewBody":r['text']} for r in REVIEWS_LIST]}

def crumbs(page, label):
    items = [{"@type":"ListItem","position":1,"name":"Home","item":BASE}]
    if page != 'index.html': items.append({"@type":"ListItem","position":2,"name":label,"item":BASE+page})
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items}

def nav(page):
    links = ''.join(f'<li><a href="{p}"{" aria-current=page" if p==page else ""}>{l}</a></li>' for p,l in PAGES)
    mlinks = ''.join(f'<a class="l" href="{p}"{" aria-current=page" if p==page else ""}>{l}</a>' for p,l in PAGES)
    return f'''<a class="skip" href="#main">Skip to content</a><div class="progress" aria-hidden="true"></div><div class="grain" aria-hidden="true"></div>
<header class="nav"><div class="wrap bar"><a class="brand" href="index.html" aria-label="{NAME} home"><img src="brand/logo-horizontal-dark.svg" alt="{NAME}" width="372" height="92"></a>
<nav aria-label="Main"><ul>{links}</ul></nav>
<div class="acts"><a class="btn ghost sm" href="sms:{TEL}">{ic('msg')}Text</a><a class="btn sm mag" href="tel:{TEL}">{ic('phone')}Call 24/7</a></div>
<button class="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="mmenu"><span></span><span></span><span></span></button></div></header>
<div class="mmenu" id="mmenu" aria-hidden="true"><nav aria-label="Mobile">{mlinks}</nav>
<div class="mm-acts"><a class="btn" href="tel:{TEL}">{ic('phone')}{PHONE}</a><a class="btn ghost" href="sms:{TEL}">{ic('msg')}Text us</a></div>
<p class="mm-meta"><span class="live"><span class="dot"></span>Open 24 hours</span><br><br>Mobile service across {CITY} — we come to you.</p></div>'''

def footer():
    links = ''.join(f'<li><a href="{p}">{l}</a></li>' for p,l in PAGES)
    return f'''<footer class="foot"><div class="wrap"><div class="foot-grid">
<div class="fbrand"><img src="brand/logo-horizontal-dark.svg" alt="{NAME}" width="372" height="92" loading="lazy"><p>Women-owned mobile mechanics who come directly to your location in {CITY}. Quality work at reasonable prices.</p></div>
<div><h4>Pages</h4><ul>{links}</ul></div>
<div><h4>Hours</h4><ul><li><span class="live"><span class="dot"></span>Open 24 hours</span></li><li style="color:var(--muted);font-size:.9rem">Day, night, weekends — as listed on Google.</li></ul></div>
<div><h4>Reach us</h4><ul><li><a href="tel:{TEL}"><b>{PHONE}</b></a></li><li><a href="sms:{TEL}">Text {PHONE}</a></li><li style="color:var(--muted)">Mobile service · {CITY}<br>(we come to you — no shop address)</li><li><a href="{MAPS}" rel="noopener" target="_blank">Google reviews ↗</a></li></ul></div>
</div><div class="legal"><span>© <span data-year>2026</span> {NAME} · {CITY}</span><span>Design preview by <a href="https://github.com/RGWebD" rel="noopener">RGWebD</a></span></div></div></footer>
<div class="mbar"><a class="btn" href="tel:{TEL}">{ic('phone')}Call now</a><a class="btn ghost" href="sms:{TEL}">{ic('msg')}Text us</a></div>
<div class="demo" role="note"><span>Design preview by <b>RGWebD</b></span><button aria-label="Dismiss preview note">×</button></div>
<script src="script.js?v={VER}" defer></script></body></html>'''

def cta_band(photo='g12', title='Stuck right now? <span class="lime">We\u2019re up.</span>'):
    return f'''<section class="cta-band rv" aria-labelledby="cta-h">{('<div class="bgimg">'+img(photo,"",small=True)+'</div>') if photo else ''}
<div class="cta-in"><div><span class="eyebrow">Open 24 hours</span><h2 id="cta-h">{title}</h2>
<a class="cta-phone" href="tel:{TEL}">{PHONE}</a><div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn lg mag" href="tel:{TEL}">{ic('phone')}Call now</a><a class="btn lg ghost" href="sms:{TEL}">{ic('msg')}Text the details</a></div></div>
<div class="cta-side"><div class="row">{ic('van')}<div><b>We come to you</b>Home, work, a parking lot or a jobsite.</div></div><div class="row">{ic('parts')}<div><b>Got the part already?</b>We install it and warranty the labor.</div></div><div class="row">{ic('card')}<div><b>Easy to pay</b>Credit, debit &amp; tap-to-pay.</div></div></div></div>
<div class="tape" aria-hidden="true"></div></section>'''

def page_hero(page, label, h1, lede, photo, alt, big):
    return f'''<section class="phero"><div class="bigtype" aria-hidden="true" data-px="-.12">{big}</div><div class="wrap phero-grid">
<div><ol class="crumbs" aria-label="Breadcrumb"><li><a href="index.html">Home</a></li><li aria-current="page">{label}</li></ol>
<h1 class="split"><span class="ln"><span>{h1[0]}</span></span><span class="ln"><span>{h1[1]}</span></span></h1><p class="lede rv d1">{lede}</p>
<div class="ctas rv d2"><a class="btn mag" href="tel:{TEL}">{ic('phone')}Call {PHONE}</a><a class="btn ghost" href="sms:{TEL}">{ic('msg')}Text us</a></div></div>
<div class="rv d2"><div class="frame">{img(photo,alt,eager=True)}<div class="shade"></div></div></div></div></section>'''

def ava(n): return ''.join(w[0] for w in n.split()[:2]).upper()

# ---------------- HOME ----------------
def home():
    ticks = ''.join(f'<line class="tk" x1="{50+38*__import__("math").sin(__import__("math").radians(i*15)):.2f}" y1="{50-38*__import__("math").cos(__import__("math").radians(i*15)):.2f}" x2="{50+46*__import__("math").sin(__import__("math").radians(i*15)):.2f}" y2="{50-46*__import__("math").cos(__import__("math").radians(i*15)):.2f}" stroke-width="{3 if i%6==0 else 1.8}" stroke-linecap="round"/>' for i in range(24))
    loader = f'''<div class="loader" aria-hidden="true"><div class="dial"><svg viewBox="0 0 100 100">{ticks}<g class="hand"><mask id="lm"><rect x="0" y="0" width="100" height="100" fill="#fff"/><rect x="47.7" y="10" width="4.6" height="8" rx="1" fill="#000"/></mask><g mask="url(#lm)" fill="#C8F031"><circle cx="50" cy="20" r="6.5"/><rect x="47.3" y="22" width="5.4" height="28" rx="2.7"/></g><circle cx="50" cy="50" r="4.5" fill="#C8F031"/></g></svg><div class="lt"><span data-hr>00:00</span><small>ANY HOUR · JACKSONVILLE</small></div></div></div>'''
    svcs = ['Mobile diagnostics','Starter replacement','Serpentine belts','Oil changes','No-start help','Engine-bay repairs','Parking-lot fixes','Jobsite breakdowns','Your parts, our labor']
    mq = ''.join(f'<li>{s}</li>' for s in svcs)
    feats = [('van','We come to you','Driveway, workplace, grocery-store lot or jobsite \u2014 the shop rolls out to your car.'),
             ('clock','Open 24 hours','Listed as open around the clock. Early morning, late night, Sundays included.'),
             ('chat','Explained, not upsold','Reviewers keep saying it: they walk you through what broke and why.'),
             ('parts','Bring your own parts','We install client-provided parts and warranty the labor portion.')]
    fc = ''.join(f'<div class="fcard rv d{i%3}"><div class="ic">{ic(a)}</div><h3>{b}</h3><p>{c}</p></div>' for i,(a,b,c) in enumerate(feats))
    picks = [REVIEWS_LIST[i] for i in (0,4,2,5,3,8)]
    slides = ''.join(f'<figure class="slide" aria-roledescription="slide" aria-label="{i+1} of {len(picks)}"><blockquote>\u201c{e(r["pull"])}\u201d</blockquote><figcaption><span class="ava" aria-hidden="true">{ava(r["name"])}</span><span><b style="color:var(--chalk)">{e(r["name"])}</b> · {STAR5} <span style="color:var(--muted);font-size:.85rem">Google · {e(r["meta"])}</span></span></figcaption></figure>' for i,r in enumerate(picks))
    dots = ''.join(f'<button aria-label="Show review {i+1}"></button>' for i in range(len(picks)))
    C = 2*3.14159*60
    def gauge(val, frac, dec, label, sub, suffix=''):
        return f'''<div class="gauge rv"><svg viewBox="0 0 150 150" aria-hidden="true"><circle class="trk" cx="75" cy="75" r="60" fill="none" stroke-width="10"/><circle class="val" cx="75" cy="75" r="60" fill="none" stroke-width="10" stroke-dasharray="{C:.2f}" stroke-dashoffset="{C:.2f}" data-frac="{frac}"/></svg>
<div class="num"><span data-to="{val}" data-dec="{dec}">{val:.{dec}f}</span><small>{suffix}</small></div><h3>{label}</h3><p>{sub}</p></div>'''
    gauges = (gauge(RATING, RATING/5, 1, 'Google rating', 'Out of 5 stars', '★') + gauge(REVIEWS, 1, 0, 'Google reviews', 'And counting') + gauge(24, 1, 0, 'Hours a day', 'Open 24 hours', 'h')
              + f'<div class="gauge wo rv">{ic("venus")}<h3>Women-owned</h3><p>Identifies as a women-owned business on Google.</p></div>')
    teas = [('services.html','g03','Services','What we fix','Diagnostics, starters, belts, oil changes &amp; more.','Engine bay with oil filler cap and filter housing'),
            ('work.html','g20','Gallery','Our work','Real jobs, real driveways, any hour.','Mechanic lifting an engine assembly out of a vehicle'),
            ('reviews.html','g16','4.6 ★ · 315','Reviews','What Jacksonville drivers say.','Crew working beside a work truck on a jobsite lot'),
            ('contact.html','g02','24/7','Contact &amp; FAQ','Call, text &amp; common questions.','Mechanic working under a red classic Corvette')]
    tc = ''.join(f'<a class="tcard rv d{i%3}" href="{p}" data-tilt>{img(ph,alt,small=True)}<span class="go">{ic("arrow")}</span><span class="tx"><span class="k">{k}</span><h3>{t}</h3><p>{s}</p></span></a>' for i,(p,ph,k,t,s,alt) in enumerate(teas))
    title = f'{NAME} | 24-Hour Mobile Mechanic in Jacksonville, FL'
    desc = f'Women-owned mobile mechanics who come to you anywhere in Jacksonville, FL. Open 24 hours. Rated {RATING}★ from {REVIEWS} Google reviews. Call {PHONE}.'
    return head('index.html', title, desc, crumbs('index.html','Home')) + '<body>' + loader + nav('index.html') + f'''<main id="main">
<section class="hero"><div class="bigtype" aria-hidden="true" data-px=".18">24/7</div><div class="wrap hero-grid">
<div><span class="live rv"><span class="dot"></span>Open 24 hours <span class="clock" data-clock></span></span>
<h1 class="split"><span class="ln"><span>Broke down?</span></span><span class="ln"><span>We roll out</span></span><span class="ln"><span><em>any hour.</em></span></span></h1>
<p class="lede rv d1">Women-owned mobile mechanics who come straight to your driveway, workplace or parking lot anywhere in Jacksonville \u2014 and warranty the labor on parts you provide.</p>
<div class="ctas rv d2"><a class="btn lg mag" href="tel:{TEL}">{ic('phone')}Call {PHONE}</a><a class="btn lg ghost" href="services.html">See what we fix {ic('arrow')}</a></div>
<div class="trust rv d3"><a class="stars" href="reviews.html" style="text-decoration:none"><span aria-hidden="true" style="display:inline-flex;gap:2px"><i></i><i></i><i></i><i></i><i></i></span>{RATING} · {REVIEWS} Google reviews</a><span class="sep"></span><span class="pill-wo">{ic('venus')}Women-owned</span><span class="sep"></span><span class="pill-wo">{ic('card')}Card &amp; tap-to-pay</span></div></div>
<div class="hero-photo rv d1"><div class="frame">{img('g11','Mechanics working under the open hood of an SUV at night beside a Jacksonville highway',eager=True,sizes="(max-width:860px) 100vw, 520px")}<div class="beam"></div><div class="shade"></div></div>
<button class="hot" style="left:24%;top:30%" aria-expanded="false" aria-label="Under-hood diagnosis"><span class="tip" role="tooltip"><b>Under the hood</b>Diagnosing right where the car stopped.</span></button>
<button class="hot" style="left:58%;top:76%" aria-expanded="false" aria-label="Tools on site"><span class="tip" role="tooltip"><b>Shop on wheels</b>Jacks, stands and tools come to you.</span></button>
<button class="hot" style="left:80%;top:20%" aria-expanded="false" aria-label="Night call-out"><span class="tip" role="tooltip"><b>After dark</b>Open 24 hours \u2014 night calls welcome.</span></button>
<div class="float-card" aria-hidden="true"><span class="n">{RATING}★</span><span class="t">{REVIEWS} reviews<br>on Google</span></div>
<div class="float-card b" aria-hidden="true"><span class="n">24h</span><span class="t">Day or night,<br>we roll out</span></div>
<div class="tape" aria-hidden="true"></div></div></div></section>
<div class="marq-wrap"><div class="marq" aria-label="Services"><div class="track"><ul>{mq}</ul><ul aria-hidden="true">{mq}</ul></div></div>
<div class="marq out" aria-hidden="true"><div class="track"><ul>{mq}</ul><ul>{mq}</ul></div></div></div>

<section class="sec" aria-labelledby="why-h"><div class="wrap why-grid">
<div class="collage rv"><div class="p1 phtilt" data-px="-.03">{img('g06','Two mechanics working under a raised sedan in a parking lot',small=True)}</div><div class="p2">{img('g15','Mechanic repairing a blue car in a parking space',small=True)}</div>
<div class="stamp" aria-hidden="true"><svg viewBox="0 0 120 120"><defs><path id="cp" d="M60,60 m-46,0 a46,46 0 1,1 92,0 a46,46 0 1,1 -92,0"/></defs><circle cx="60" cy="60" r="58" fill="#0A0F1C"/><text font-family="JetBrains Mono,monospace" font-size="10.5" font-weight="700" letter-spacing="3.2" fill="#F4F6EF"><textPath href="#cp">WE COME TO YOU · ANY HOUR · </textPath></text></svg><span class="core">{ic('van')}</span></div></div>
<div><span class="eyebrow rv">Why Jacksonville calls us</span><h2 class="h2 split" id="why-h"><span class="ln"><span>Your driveway</span></span><span class="ln"><span>is <span class="lime">the shop.</span></span></span></h2>
<p class="lede rv d1">No tow, no waiting room. We come directly to your location to repair your vehicle \u2014 quality work at reasonable prices.</p>
<div class="cards4">{fc}</div></div></div></section>

<section class="sec" style="padding-top:0" aria-labelledby="dn-h"><div class="wrap">
<div class="dn-head"><div><span class="eyebrow rv">Same crew · any hour</span><h2 class="h2 split" id="dn-h"><span class="ln"><span>Sunup or</span></span><span class="ln"><span><span class="lime">streetlights.</span></span></span></h2></div><p class="lede rv d1" style="max-width:40ch">Drag the handle. Some jobs happen at noon in the yard, some at night under a porch light \u2014 we show up for both.</p></div>
<div class="dn rv"><img src="img/g01.webp" width="{dims('g01.webp')[0]}" height="{dims('g01.webp')[1]}" alt="Daytime: mechanic in a hi-vis vest working on an engine curbside" loading="lazy" style="object-position:50% 62%"><img class="night" src="img/g07.webp" width="{dims('g07.webp')[0]}" height="{dims('g07.webp')[1]}" alt="Night: mechanic under the hood of a blue car in a driveway" loading="lazy" style="object-position:50% 55%"><span class="lab d">Day</span><span class="lab n">Night</span><span class="handle"></span><button class="knob" role="slider" aria-label="Compare day and night photos" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">{ic('swap')}</button></div></div></section>

<section class="sec" style="padding-top:0" aria-labelledby="num-h"><div class="wrap"><span class="eyebrow rv">By the numbers</span><h2 class="h2 split" id="num-h" style="margin-bottom:40px"><span class="ln"><span>Trusted on the clock.</span></span></h2><div class="gauges">{gauges}</div></div></section>

<section class="sec" style="padding-top:0" aria-labelledby="rev-h"><div class="wrap"><div class="rev-wrap rv car-root" aria-roledescription="carousel"><span class="q" aria-hidden="true">\u201d</span><span class="eyebrow">Straight from Google reviews</span><h2 id="rev-h" class="sr-only">Customer reviews</h2>
<div class="car" aria-live="polite">{slides}</div>
<div class="car-ctl"><button class="arr pv" aria-label="Previous review">{ic('left')}</button><button class="arr nx" aria-label="Next review">{ic('arrow')}</button><div class="dots">{dots}</div><a class="btn ghost g" href="reviews.html">Read more reviews {ic('arrow')}</a></div></div></div></section>

<section class="sec" style="padding-top:0" aria-labelledby="ex-h"><div class="wrap"><span class="eyebrow rv">Explore</span><h2 class="h2 split" id="ex-h" style="margin-bottom:40px"><span class="ln"><span>Pop the hood.</span></span></h2><div class="teasers">{tc}</div></div></section>
{cta_band('g12')}
</main>''' + footer()

# ---------------- SERVICES ----------------
SVC = [
 ('g23','Mobile diagnostics','Can\u2019t tell what\u2019s wrong? Diagnostics come up in our reviews more than any other job. We trace the problem right where the car sits and explain it in plain English before any work starts.',['Check-engine & warning lights','Won\u2019t start / stalling','Strange noises & leaks'],4,'Engine bay with hoses and wiring being traced'),
 ('g12','Starters &amp; no-start problems','Starter replacement is one of the most-mentioned jobs in our Google reviews. Clicking, cranking or dead silence \u2014 call, tell us what you hear, and we\u2019ll come sort it out.',['Starter replacement','No-crank / no-start','Get-you-home fixes'],None,'Mechanics working with a jack stand at night'),
 ('g17','Serpentine belts','Squealing, cracked or snapped belt? Serpentine belt replacement comes up again and again in our reviews \u2014 done in your driveway, no tow required.',['Belt replacement','Squeal & wear checks','Pulley inspection'],None,'Close-up of a serpentine belt and pulleys in an engine bay'),
 ('g03','Oil changes','Oil changes are a listed offering on our Google profile. Skip the lube-shop line \u2014 we bring the oil change to you.',['At home or at work','Quick in-and-out','Ask about your vehicle'],None,'Engine with yellow oil dipstick handle and filter housing'),
 ('g01','Engine-bay &amp; bigger repairs','From a hard-to-reach loose fuel rail to valve-cover work and drive-shaft removal, our reviewers have trusted us with jobs well beyond the basics.',['Hard-to-access repairs','Valve covers & gaskets','Drive-shaft removal'],3,'Mechanic in hi-vis vest working on an engine curbside'),
 ('g15','Breakdowns where you are','Car died in a grocery-store parking lot? Two work trucks down on a jobsite? We come to you and fix it on the spot whenever we can.',['Parking lots','Workplaces & jobsites','Home driveways'],2,'Mechanic repairing a car in a parking lot'),
 ('g10','You bring the parts, we warranty the labor','Already bought the part? We primarily provide and warranty the labor portion of installing client-provided auto parts \u2014 and we\u2019ll help you get the right part for your car.',['Client-provided parts','Labor warranty','Right-part guidance'],6,'Removed valve cover ready for a new gasket'),
]
def services():
    rows = ''
    for i,(ph,t,txt,tags,ri,alt) in enumerate(SVC):
        q = ''
        if ri is not None:
            r = REVIEWS_LIST[ri]; q = f'<blockquote class="mini-q">\u201c{e(r["pull"])}\u201d<cite>{e(r["name"])} · Google review</cite></blockquote>'
        tg = ''.join(f'<li>{e(x)}</li>' for x in tags)
        rows += f'''<article class="svc" id="s{i+1}"><div class="svc-ph rv"><span class="num" aria-hidden="true">{i+1:02d}</span><div class="frame">{img(ph,alt)}</div></div>
<div class="rv d1"><span class="eyebrow">Service {i+1:02d}</span><h2>{t}</h2><p class="lede">{txt}</p><ul class="tags">{tg}</ul>{q}</div></article>'''
    steps = [('Call or text, any hour', f'Reach us at <a href="tel:{TEL}" style="color:var(--lime)">{PHONE}</a> \u2014 we\u2019re listed as open 24 hours.'),
             ('Tell us what\u2019s going on','Describe the problem and your vehicle. Need a part? We\u2019ll help you get the right one.'),
             ('We come to you','Home, work, a parking lot or a jobsite. The tools come with us.'),
             ('Fixed &amp; explained','We repair it on the spot when we can, and walk you through what was done and why.'),
             ('Drive it, make sure it\u2019s right','As one reviewer put it: he \u201cstayed &amp; let me drive the car around a bit to ensure I was satisfied with the results.\u201d')]
    st = ''.join(f'<div class="step"><span class="b">{i+1}</span><h3>{a}</h3><p>{b}</p></div>' for i,(a,b) in enumerate(steps))
    faq = {"@context":"https://schema.org","@type":"ItemList","name":"Mobile mechanic services","itemListElement":[{"@type":"ListItem","position":i+1,"name":html.unescape(s[1])} for i,s in enumerate(SVC)]}
    return head('services.html', f'Mobile Mechanic Services in Jacksonville, FL | {NAME}', f'Mobile diagnostics, starter replacement, serpentine belts, oil changes and roadside repairs at your location in Jacksonville, FL. Open 24 hours. Call {PHONE}.', crumbs('services.html','Services'), [faq]) + '<body>' + nav('services.html') + '<main id="main">' + \
      page_hero('services.html','Services',('What we fix,','<span class="lime">where you are.</span>'),'Every job below is done at your location. The list is drawn from our Google profile and the work customers describe in their reviews \u2014 call to talk through yours.','g18','Engine with the top end opened up, valve train exposed','FIX') + \
      f'''<section style="padding-bottom:40px"><div class="wrap">{rows}<p class="note rv">Not sure if we handle your job? Call or text {PHONE} and describe it \u2014 we\u2019ll tell you straight. Pricing is quoted per job.</p></div></section>
<section class="sec" aria-labelledby="how-h"><div class="wrap"><div style="text-align:center"><span class="eyebrow rv">How it works</span><h2 class="h2 split" id="how-h"><span class="ln"><span>From call to <span class="lime">fixed.</span></span></span></h2></div>
<div class="tl"><div class="rail"><div class="fill"></div></div>{st}</div></div></section>{cta_band('g06','Ready when <span class="lime">you are.</span>')}</main>''' + footer()

# ---------------- WORK ----------------
GAL = [('g11','night'),('g01','engine drive'),('g06','lots'),('g02','drive'),('g07','night drive'),('g15','lots'),('g18','engine'),('g16','lots'),('g12','night'),('g03','engine'),('g17','engine'),('g10','engine'),('g08','engine'),('g23','engine'),('g05','drive'),('g14','lots'),('g09','lots'),('g24','drive')]
def work():
    items = ''
    for k,cat in GAL:
        w,h = dims(k+'.webp'); cls = ' w' if w > h else ''
        items += f'<figure class="gi rv{cls}" data-cat="{cat}"><button data-lb="img/{k}.webp" data-cap="{e(CAP[k])}" aria-label="Open photo: {e(CAP[k])}">{img(k,CAP[k],small=True)}</button><figcaption>{e(CAP[k])}</figcaption></figure>'
    fl = ''.join(f'<button data-f="{a}" aria-pressed="{"true" if a=="all" else "false"}">{b}</button>' for a,b in [('all','All work'),('night','After dark'),('lots','Lots &amp; jobsites'),('engine','Under the hood'),('drive','Driveways')])
    return head('work.html', f'Our Work — Photo Gallery | {NAME}', f'Real photos of mobile mechanic jobs around Jacksonville, FL: night call-outs, parking-lot repairs and engine-bay work. Call {PHONE}.', crumbs('work.html','Our Work')) + '<body>' + nav('work.html') + '<main id="main">' + \
      page_hero('work.html','Our Work',('Real jobs.','<span class="lime">Real driveways.</span>'),'Every photo here is from our own Google profile \u2014 parking lots, jobsites, driveways and plenty of after-dark call-outs. Tap any photo to open it.','g20','Mechanic lifting an engine assembly out of a vehicle','WORK') + \
      f'''<section class="sec" style="padding-top:20px" aria-labelledby="g-h"><div class="wrap"><div class="gal-head"><h2 class="h2" id="g-h" style="font-size:clamp(1.6rem,3vw,2.4rem)">The gallery</h2><div class="filters" role="group" aria-label="Filter photos">{fl}</div></div>
<div class="masonry">{items}</div><p class="note" style="margin-top:20px">License plates and other businesses\u2019 signs have been blurred for privacy.</p></div></section>
<div class="lb" role="dialog" aria-modal="true" aria-label="Photo viewer" aria-hidden="true"><span class="ct"></span><figure><img src="data:," alt=""><figcaption></figcaption></figure><button class="x" aria-label="Close">{ic('x')}</button><button class="pv" aria-label="Previous photo">{ic('left')}</button><button class="nx" aria-label="Next photo">{ic('arrow')}</button></div>
{cta_band(None,'Need us <span class="lime">on site?</span>')}</main>''' + footer()

# ---------------- REVIEWS ----------------
def reviews():
    cards = ''
    for i,r in enumerate(REVIEWS_LIST):
        cards += f'<figure class="rcard rv{" feat" if i in (0,1) else ""}"><div class="top"><span class="ava" aria-hidden="true">{ava(r["name"])}</span><div><b>{e(r["name"])}</b><span>{e(r["meta"])}</span></div><span class="gbadge">Google</span></div><div class="stars" aria-label="5 out of 5 stars">{"<i></i>"*5}</div><blockquote style="margin:0"><p>{e(r["text"])}</p></blockquote></figure>'
    C = 2*3.14159*60
    return head('reviews.html', f'Reviews — {RATING}★ from {REVIEWS} Google Reviews | {NAME}', f'Read what Jacksonville drivers say about {NAME}: rated {RATING} stars from {REVIEWS} Google reviews. Fast, honest mobile repairs at your location.', crumbs('reviews.html','Reviews')) + '<body>' + nav('reviews.html') + '<main id="main">' + \
      page_hero('reviews.html','Reviews',('Jacksonville','<span class="lime">has our back.</span>'),f'Rated {RATING} out of 5 from {REVIEWS} Google reviews. Here are some of them, word for word.','g02','Mechanic working under a red classic Corvette on a brick driveway','★4.6') + \
      f'''<section class="sec" style="padding-top:10px" aria-labelledby="rv-h"><div class="wrap"><div class="rv-top rv cnt"><div class="big-rating"><span data-to="{RATING}" data-dec="1">{RATING}</span></div>
<div><h2 id="rv-h" style="font-size:clamp(1.4rem,2.6vw,2rem);margin-bottom:10px">{RATING} stars · <span data-to="{REVIEWS}">{REVIEWS}</span> Google reviews</h2><p class="lede" style="margin-bottom:18px">Customers keep coming back to the same things: fast arrival, honest explanations and fair pricing.</p><a class="btn ghost" href="{MAPS}" target="_blank" rel="noopener">See all reviews on Google ↗</a></div></div>
<div class="rv-grid">{cards}</div></div></section>{cta_band('g11','Your turn to <span class="lime">get rolling.</span>')}</main>''' + footer()

# ---------------- CONTACT ----------------
FAQ = [
 ('Do you really come to me?', 'Yes. We\u2019re a mobile mechanic \u2014 we come directly to your location to repair your vehicle: home, work, a parking lot or a jobsite.'),
 ('What are your hours?', 'Our Google listing shows us as open 24 hours. Call or text any time \u2014 day, night or weekend.'),
 ('Can I buy my own parts?', 'Yes. We primarily provide and warranty the labor portion of installing client-provided auto parts, and we can help you pick the right part for your car.'),
 ('What areas do you cover?', 'We serve Jacksonville, Florida and the surrounding Duval area. Call with your location and we\u2019ll confirm.'),
 ('How do I pay?', 'We accept credit cards, debit cards and NFC mobile payments (tap-to-pay).'),
 ('What kinds of jobs do you do?', 'Customers most often call us for diagnostics, starter replacement, serpentine belts and oil changes, plus breakdowns at home, work or in a parking lot. Call to describe your job.'),
 ('How much will it cost?', 'Every job is different, so we quote per job. Reviewers regularly describe our pricing as fair and reasonable.'),
]
def contact():
    fq = ''.join(f'<details class="rv"><summary>{e(q)}<span class="pm" aria-hidden="true"></span></summary><p>{e(a)}</p></details>' for q,a in FAQ)
    faqld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
    return head('contact.html', f'Contact & FAQ — Call {PHONE} | {NAME}', f'Call or text {NAME} at {PHONE}. Open 24 hours, mobile service across Jacksonville, FL. Credit, debit and tap-to-pay accepted.', crumbs('contact.html','Contact & FAQ'), [faqld]) + '<body>' + nav('contact.html') + '<main id="main">' + \
      page_hero('contact.html','Contact &amp; FAQ',('Call. Text.','<span class="lime">We roll.</span>'),'Tell us what\u2019s going on and where the car is. We\u2019re listed as open 24 hours.','g07','Mechanic under the hood of a blue car at night','CALL') + \
      f'''<section class="sec" style="padding-top:10px"><div class="wrap ct-grid">
<div class="panel rv"><span class="live"><span class="dot"></span>Open 24 hours <span class="clock" data-clock></span></span><h2 style="margin-top:22px">Fastest way: call</h2><a class="cta-phone" href="tel:{TEL}" style="margin:6px 0 20px">{PHONE}</a>
<ul class="info-list"><li>{ic('van')}<div><b>Mobile service \u2014 we come to you</b><span>Jacksonville, FL &amp; the Duval area. No shop to drive to.</span></div></li>
<li>{ic('clock')}<div><b>Open 24 hours</b><span>As listed on our Google Business Profile.</span></div></li>
<li>{ic('card')}<div><b>Payments</b><span>Credit cards, debit cards, NFC mobile payments.</span></div></li>
<li>{ic('venus')}<div><b>Women-owned</b><span>Identifies as women-owned on Google.</span></div></li></ul>
<div class="map"><iframe title="Map of Jacksonville, FL service area" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Jacksonville,+FL&amp;z=10&amp;output=embed"></iframe></div></div>
<div class="panel rv d1"><h2>Text us the details</h2><p style="color:#B7BFCD">Fill this in and it opens a pre-written text to {PHONE} on your phone \u2014 nothing is sent until you hit send.</p>
<form class="form" id="txtform" data-tel="{TEL}"><div class="two"><label>Your name<input name="name" autocomplete="name" placeholder="First name"></label><label>Vehicle<input name="vehicle" placeholder="Year, make, model"></label></div>
<label>Where is the car?<input name="where" placeholder="Neighborhood or cross streets"></label>
<label>What\u2019s going on?<textarea name="issue" placeholder="e.g. clicks but won\u2019t start, belt squealing, need an oil change\u2026"></textarea></label>
<button class="btn lg mag" type="submit">{ic('msg')}Open text message</button><p class="small">On a computer? Just call <a href="tel:{TEL}" style="color:var(--lime)">{PHONE}</a>.</p></form>
<div class="ph-note">{img('g12','Mechanics working with jack stands at night',small=True)}<span>After-dark call-outs welcome</span></div></div></div></section>
<section class="sec" style="padding-top:20px" aria-labelledby="faq-h"><div class="wrap"><div style="text-align:center;margin-bottom:30px"><span class="eyebrow rv">FAQ</span><h2 class="h2 split" id="faq-h"><span class="ln"><span>Good questions.</span></span></h2></div><div class="faq">{fq}</div></div></section>
{cta_band('g20','Still stuck? <span class="lime">Call now.</span>')}</main>''' + footer()

def nf():
    return head('404.html', f'Page not found | {NAME}', 'This page could not be found.', None).replace('<link rel="canonical"', '<meta name="robots" content="noindex"><link rel="canonical"') + '<body>' + nav('') + f'''<main id="main" class="nf"><div><p class="eyebrow" style="justify-content:center">Wrong turn</p><h1>404</h1><p class="lede" style="margin:10px auto 30px">This page broke down. Good news: we fix things.</p><div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn" href="index.html">Back to home</a><a class="btn ghost" href="tel:{TEL}">{ic('phone')}{PHONE}</a></div></div></main>''' + footer()

VER = '1'
def main():
    global VER
    VER = os.environ.get('VER', '1')
    out = {'index.html':home(),'services.html':services(),'work.html':work(),'reviews.html':reviews(),'contact.html':contact(),'404.html':nf()}
    for f,s in out.items(): open(os.path.join(R,f),'w').write(s)
    shutil.copy(os.path.join(G,'styles.css'), os.path.join(R,'styles.css'))
    shutil.copy(os.path.join(G,'script.js'), os.path.join(R,'script.js'))
    open(os.path.join(R,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
    urls = ''.join(f'<url><loc>{BASE}{"" if p=="index.html" else p}</loc><changefreq>monthly</changefreq><priority>{"1.0" if p=="index.html" else "0.8"}</priority></url>' for p,_ in PAGES)
    open(os.path.join(R,'sitemap.xml'),'w').write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    llm = f"""# {NAME}
> Women-owned mobile mechanics serving Jacksonville, Florida. They come directly to the customer's location (home, work, parking lot or jobsite) to repair vehicles. Listed on Google as open 24 hours. Rated {RATING}/5 from {REVIEWS} Google reviews.

- Google listing name: {LEGAL} (customers also write "Jacksonville Mobile Mechanics LLC")
- Phone / text: {PHONE}
- Hours: Open 24 hours (per Google Business Profile)
- Service area: Jacksonville, FL and the Duval area (service-area business, no public street address)
- Payments: {', '.join(PAYMENTS)}
- Women-owned business (per Google attribute)
- From the owner: "{OWNER_TEXT}"

## Services (from the Google profile and customer reviews)
""" + ''.join(f"- {html.unescape(s[1])}: {html.unescape(s[2])}\n" for s in SVC) + f"""
## Pages
- [Home]({BASE}): overview, rating, why choose us, reviews, contact
- [Services]({BASE}services.html): each service plus how a mobile visit works
- [Our Work]({BASE}work.html): photo gallery of real jobs
- [Reviews]({BASE}reviews.html): customer reviews quoted from Google
- [Contact & FAQ]({BASE}contact.html): phone, text form, hours, service area, payments, FAQ
- [Google reviews]({MAPS})
"""
    open(os.path.join(R,'llms.txt'),'w').write(llm)
    print('built', len(out), 'pages')
if __name__ == '__main__': main()

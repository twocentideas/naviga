#!/usr/bin/env python3
"""Builds the static Naviga Law site into ./site. Edit content here, run `python3 build.py`."""
import json, os, datetime
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')
SITE = 'https://navigalaw.com'
PHONE, PHONE_TEL = '(207) 805-2182', '+12078052182'
EMAIL = 'info@navigalaw.com'
ADDR1, ADDR2 = '201 US Rt. 1, #102', 'Scarborough, ME 04074'
# Where "Schedule a 30-min consultation" goes. Swap for a Calendly / Cal.com link when ready.
SCHEDULE_URL = '/#schedule-consultation'
MER_EMAIL = 'meredith@navigalaw.com'
# TODO: replace with Meredith's LinkedIn profile URL (linkedin.com/in/...)
LINKEDIN_URL = 'https://www.linkedin.com/search/results/people/?keywords=Meredith%20Maller'

SCHEMA = {
  "@context": "https://schema.org", "@type": "LegalService", "name": "Naviga Law",
  "url": SITE + "/", "telephone": PHONE_TEL, "email": EMAIL,
  "image": SITE + "/assets/img/og.jpg",
  "description": "Trusts and estates law firm in Scarborough, Maine: estate planning, wealth transfer, asset protection, prenuptial agreements and family cottage planning.",
  "address": {"@type": "PostalAddress", "addressLocality": "Scarborough", "addressRegion": "ME", "postalCode": "04074", "addressCountry": "US"},
  "areaServed": ["Maine", "District of Columbia"],
  "founder": {"@type": "Person", "name": "Meredith M. Maller", "jobTitle": "Founder & Attorney",
              "alumniOf": ["Georgetown University Law Center", "University of Maryland Francis King Carey School of Law", "Bates College"]},
}

def head(title, desc, path):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Naviga Law">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#22303A">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/cormorant-garamond-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/tinos-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">{json.dumps(SCHEMA)}</script>
<script src="/assets/js/site.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>'''

def header(active):
    def item(key, href, label):
        cur = ' aria-current="page"' if key == active else ''
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    return f'''<header class="site-header">
<div class="wrap bar">
<a class="logo logo-card" href="/" aria-label="Naviga Law, home"><span class="logo-mark">NAVIGA</span></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span class="sr">Menu</span><span class="burger" aria-hidden="true"></span></button>
<nav id="site-nav" class="site-nav" aria-label="Main">
<ul>{item('home','/','Home')}{item('about','/about/','About')}{item('contact','/contact-us/','Contact Us')}</ul>
<a class="btn btn-sm" href="{SCHEDULE_URL}">Schedule a 30-min consultation</a>
</nav>
</div>
</header>
<main id="main">'''

DISCLAIMER = ('Attorney advertising. The information on this website is for general information only and is not legal advice. '
              'Contacting Naviga Law does not create an attorney–client relationship; please do not send confidential information until one has been established. '
              'Meredith M. Maller is licensed in Maine and the District of Columbia.')

def footer(cta=True):
    year = datetime.date.today().year
    btn = '<a class="btn btn-light foot-btn" href="/contact-us/">Get in Touch</a>' if cta else ''
    return f'''</main>
<footer class="site-footer">
<div class="foot-top">
<div class="wrap foot-grid">
<a class="foot-logo" href="/" aria-label="Naviga Law, home"><span class="foot-wordmark">NAVIGA LAW</span><span class="foot-tag">Family Advisor &amp; Asset Protection</span></a>
<figure class="epigraph-fig">
<blockquote><p><span class="q-mark" aria-hidden="true">“</span>I am not afraid of storms, for I am learning how to sail my ship.<span class="q-mark" aria-hidden="true">”</span></p></blockquote>
<figcaption><span class="ep-rule" aria-hidden="true"></span>Louisa May Alcott</figcaption>
</figure>
</div>
</div>
<div class="wrap foot-grid foot-main">
<p class="foot-line">Clients choose <i>Naviga</i> for sophisticated legal work delivered with focus, discretion, and respect—for their time, their resources, and their goals.</p>
<div class="foot-col">
<h2 class="foot-h">Mailing Address</h2>
<address>{ADDR1}<br>{ADDR2}</address>
</div>
<div class="foot-col">
<h2 class="foot-h">Contact</h2>
<a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a>
</div>
<div class="foot-col foot-act">{btn}</div>
</div>
<div class="wrap foot-legal">
<p class="disclaimer">{DISCLAIMER}</p>
<p class="copy">© {year} Naviga Law · <a href="/privacy/">Privacy</a></p>
</div>
</footer>
</body>
</html>
'''

LANDSCAPE = '''<svg class="landscape" aria-hidden="true" viewBox="0 0 1440 260" preserveAspectRatio="none"><rect x="0" y="110" width="1440" height="150" fill="#E6EEF2"/><path d="M560,110 C760,40 1040,28 1220,46 C1320,56 1400,66 1440,70 L1440,110 Z" fill="#394750"/><path d="M0,110 L6,74 L13,96 L19,76 L25,97 L35,33 L46,92 L52,51 L58,99 L64,76 L70,100 L81,36 L92,92 L101,73 L111,99 L120,46 L129,93 L139,81 L149,96 L158,61 L167,102 L175,82 L183,94 L193,61 L203,101 L214,62 L224,95 L234,67 L244,100 L253,72 L262,103 L268,57 L275,104 L281,66 L286,102 L294,73 L302,102 L313,85 L324,102 L330,70 L337,103 L344,67 L351,103 L359,64 L368,105 L373,87 L378,100 L387,88 L396,104 L402,82 L408,106 L417,70 L426,100 L436,71 L445,106 L452,73 L459,102 L466,75 L473,103 L483,92 L493,106 L501,97 L509,105 L519,93 L530,107 L535,98 L541,104 L548,96 L555,107 L566,95 L577,107 L582,102 L588,108 L597,101 L606,108 L640,106 L1440,104 L1440,110 Z" fill="#22303A"/><rect x="0" y="110" width="1440" height="5" fill="#22303A"/><path d="M0,110 L6,133 L13,118 L19,131 L25,118 L35,158 L46,121 L52,147 L58,117 L64,131 L70,116 L81,156 L92,121 L101,133 L111,117 L120,150 L129,121 L139,128 L149,118 L158,141 L167,115 L175,127 L183,120 L193,140 L203,116 L214,140 L224,119 L234,137 L244,116 L253,134 L262,114 L268,143 L275,113 L281,137 L286,115 L294,133 L302,115 L313,126 L324,115 L330,135 L337,114 L344,136 L351,114 L359,139 L368,113 L373,124 L378,116 L387,124 L396,114 L402,127 L408,113 L417,135 L426,116 L436,134 L445,112 L452,133 L459,115 L466,132 L473,114 L483,121 L493,112 L501,118 L509,113 L519,120 L530,112 L535,118 L541,114 L548,119 L555,112 L566,119 L577,112 L582,115 L588,112 L597,116 L606,111 L640,112 L640,110 Z" fill="#394750" fill-opacity="0.85"/><path d="M520,150 L1440,128 L1440,176 L760,166 Z" fill="#3E6881"/><path d="M980,168 L1440,150 L1440,214 Z" fill="#9ABFD2"/><path d="M440,260 L860,198 L1440,248 L1440,260 Z" fill="#C6D8E4"/></svg>'''

def pic(name, alt, cls='', eager=False, w=900, h=1159):
    load = 'eager' if eager else 'lazy'
    return f'<picture><source srcset="/assets/img/{name}.webp" type="image/webp"><img class="{cls}" src="/assets/img/{name}.jpg" alt="{alt}" width="{w}" height="{h}" loading="{load}" decoding="async"></picture>'

FUNERAL = 'I will not come to your funeral and stand off in the distance under a tree visibly crying as your casket is lowered—but if you really want that, I can do the paperwork and help you hire someone who can.'
SERVICES = [
 ('Estate Planning','The core documents every plan rests on.',['Wills','Revocable trusts','Powers of attorney','Advance healthcare directives']),
 ('Trusts &amp; Wealth Transfer','Structures that move wealth efficiently across generations.',['Irrevocable life insurance trusts (ILITs)','Spousal lifetime access trusts (SLATs)','Grantor retained annuity trusts (GRATs)','Domestic asset protection trusts','Asset allocation, risk management &amp; tax minimization']),
 ('Marital &amp; Partnership Agreements','I facilitate the awkward conversations of building a life together. Did you know that 90% of prenuptial agreements that are drafted are never signed? I maintain a 100% success rate.',['Cohabitation agreements','Prenuptial agreements','Postnuptial agreements']),
 ('Family Cottages &amp; Vacation Homes','Keeping the place everyone loves in the family.',['Intelligent trust design','Sustainable, multi-generational planning','Succession planning for shared properties']),
 ('Non-Traditional Assets','Planning for what doesn’t fit in a brokerage statement.',['Art and collectibles','Cryptocurrency','Intellectual property','Yachts and private planes']),
 ('Charitable Planning','Giving that reflects your values and lasts.',['Charitable trusts','Private foundations','Nonprofit and charitable entities']),
 ('Household &amp; Domestic Affairs','Protecting the people who help run your home—and your privacy.',['Employment agreements for household staff','Confidentiality agreements and NDAs','Household technology policies','Child medical directives']),
 ('Next-Generation Education','Preparing heirs to be informed, capable stewards.',['Wealth management and stewardship education for families']),
 ('The Uncomfortable Stuff',FUNERAL,['“In case of” agreements','Digital privacy and postmortem management']),
]

TOPICS = [t for t, _, _ in SERVICES]

def hidden_fields(kind):
    return (f'<input type="hidden" name="form" value="{kind}">'
            '<div class="hp" aria-hidden="true"><label>Leave this empty<input type="text" name="company" tabindex="-1" autocomplete="off"></label></div>')

def consult_form(num='10', extra=''):
    opts = ''.join(f'<option>{t}</option>' for t in TOPICS)
    num_html = f'<p class="svc-n">{num}</p>' if num else ''
    return f'''<form id="schedule-consultation" class="svc svc-form js-form{extra}" action="/api/contact" method="post" aria-labelledby="sc-title">
<div class="svc-form-head">{num_html}<h3 id="sc-title">Schedule a free 30-min consultation</h3></div>
<label>Name<input type="text" name="name" autocomplete="name" required></label>
<label>Email<input type="email" name="email" autocomplete="email" required></label>
<label>Topic<select name="topic">{opts}</select></label>
{hidden_fields('consultation')}
<button type="submit" class="btn btn-light">Find a time</button>
<p class="form-status" role="status" aria-live="polite"></p>
</form>'''

def home():
    cards = []
    for i, (t, d, items) in enumerate(SERVICES, 1):
        extra = ''
        lis = ''.join(f'<li>{x}</li>' for x in items)
        cards.append(f'<article class="svc"><p class="svc-n">{i:02d}</p><h3>{t}</h3><p class="svc-d">{d}</p><ul>{lis}</ul>{extra}</article>')
    form = consult_form()
    body = f'''<section class="sky-hero">
<div class="wrap hero-copy">
<p class="eyebrow">Trusts &amp; Estates · Scarborough, Maine</p>
<h1 class="display"><i>Naviga</i> provides exceptional legal guidance, helping chart a safe course for your life and legacy.</h1>
<p class="hero-links"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{PHONE_TEL}">{PHONE}</a></p>
</div>
{LANDSCAPE}
</section>

<section class="section">
<div class="wrap two-up">
<p class="lede"><i>Naviga</i> is a trusts and estates law firm focused on delivering high-quality planning and advice with clarity, efficiency, and integrity.</p>
<div class="stack">
<p><i>Naviga</i> advises individuals and families on estate planning, wealth transfer, and asset protection, with a focus on clear communication, thoughtful design, and documents that actually work when they are needed — all with transparent pricing.</p>
<a class="btn" href="/about/">Learn more about <i>Naviga</i></a>
</div>
</div>
</section>

<section class="section section-tint" id="services" aria-labelledby="svc-title">
<div class="wrap">
<div class="svc-head">
<div><p class="eyebrow">What we do</p><h2 id="svc-title" class="h-xl">Services</h2></div>
<p class="muted">Transparent pricing on every engagement. Not sure where you fit? Start with a conversation. Those are free.</p>
</div>
<div class="svc-grid" tabindex="0" aria-label="Services, scroll sideways on small screens">
{''.join(cards)}
{form}
</div>
<div class="svc-nav">
<button type="button" class="svc-prev" aria-label="Previous service"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
<span>Swipe or tap the arrows</span>
<button type="button" class="svc-next" aria-label="Next service"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
</div>
</div>
</section>

<section class="section section-rule">
<div class="wrap attorney">
{pic('meredith', 'Meredith M. Maller', 'portrait')}
<div class="stack">
<p class="eyebrow">Meet your attorney</p>
<h2 class="h-lg name-creds">Meredith M. Maller<span class="creds">J.D., LL.M.</span></h2>
<p class="measure">A seasoned trusts and estates attorney, Meredith founded <i>Naviga</i> to guide individuals and families through estate planning with clarity, confidence, and care. She brings a strategic yet deeply personal approach to helping clients protect their assets and prepare for the future.</p>
<a class="btn" href="/about/#meredith">Meet Meredith</a>
</div>
</div>
</section>'''
    return (head('Naviga Law | Trusts & Estates Attorney in Scarborough, Maine',
                 'Naviga Law is a modern trusts and estates firm in Scarborough, Maine. Estate planning, wealth transfer, asset protection and prenuptial agreements with clear guidance and transparent pricing.', '/')
            + header('home') + body + footer())

def about():
    focus = ['Crafting and implementing complex estate plans—revocable trusts, wills, powers of attorney, advance healthcare directives, irrevocable life insurance trusts and charitable trusts.',
             'Aligning asset allocation, risk management and tax minimization with your estate planning goals.',
             'Protecting vacation homes and cottages for multi-generational use.',
             'Drafting and negotiating prenuptial and postnuptial agreements.',
             'Establishing and managing private foundations, nonprofits and other charitable entities.']
    body = f'''<section class="map-hero">
<div class="wrap hero-dark">
<p class="eyebrow eyebrow-light">About</p>
<h1 class="display"><i>Naviga</i> is guided by the same principles that define good seamanship: <i>preparation, precision, and steady navigation through complexity.</i></h1>
</div>
</section>

<section class="section section-tint">
<div class="wrap split">
<div class="stack">
<p class="eyebrow">How I work</p>
<h2 class="h-lg">Strategic, and deeply personal.</h2>
<p>I guide individuals and families through the estate planning process with clarity, confidence, and care. My approach is strategic, but it’s also personal—protecting your assets and preparing for the future starts with understanding the people involved.</p>
{consult_form(num=None, extra=' svc-form--compact')}
</div>
<div>
<h3 class="label">Where I focus</h3>
<ul class="focus">{''.join(f'<li>{x}</li>' for x in focus)}</ul>
</div>
</div>
</section>

<section class="section section-rule" id="meredith">
<div class="wrap split bio-split">
<div class="stack bio-main">
<p class="eyebrow">About Meredith</p>
<div>
<h2 class="h-md name-creds">Meredith M. Maller<span class="creds">J.D., LL.M.</span></h2>
<p class="small muted">Trusts &amp; Estates | Wealth Transfer Strategy | Legacy Planning</p>
</div>
<div class="stack prose bio-prose">
<p>A seventh-generation Mainer with longstanding roots on Mount Desert Island, Meredith pairs her technical skill with genuine understanding. Her background in finance, taxation, and sophisticated wealth transfer structures allows her to craft estate plans that are thoughtful, effective, and uniquely tailored to each client’s goals and values.</p>
<p>Meredith is known for her steady, thoughtful counsel and her ability to guide clients through the complexities of generational wealth planning with clarity and purpose. She works closely with families to design structures that preserve wealth while preparing the next generation to be informed, capable stewards of it.</p>
<p>Clients value Meredith’s calm, measured approach, her talent for distilling complex legal concepts into practical guidance, and her commitment to crafting bespoke solutions that reflect both their values and long-term vision.</p>
<p>Clients choose <i>Naviga</i> for sophisticated legal work delivered with focus, discretion, and respect—for their time, their resources, and their goals.</p>
</div>
</div>
<aside class="resume" aria-label="Experience and education">
<div class="edu">
<h3 class="label">Experience</h3>
<ul class="edu-list exp-list">
<li><span class="edu-deg">2026–</span><span class="edu-body"><span class="edu-school"><i>Naviga</i> Law</span><span class="edu-field">Founder</span></span></li>
<li><span class="edu-deg">2023–25</span><span class="edu-body"><span class="edu-school">Bernstein Shur</span><span class="edu-field">Shareholder</span></span></li>
<li><span class="edu-deg">2022–23</span><span class="edu-body"><span class="edu-school">Mercer Advisors</span><span class="edu-field">Senior Estate Planning Attorney</span></span></li>
<li><span class="edu-deg">2016–22</span><span class="edu-body"><span class="edu-school">Eaton Peabody</span><span class="edu-field">Associate · Senior Counsel</span></span></li>
<li><span class="edu-deg">2014–16</span><span class="edu-body"><span class="edu-school">Brown</span><span class="edu-field">Associate · Washington, D.C.</span></span></li>
</ul>
</div>
<div class="edu">
<h3 class="label">Education</h3>
<ul class="edu-list">
<li><span class="edu-deg">LL.M.</span><span class="edu-body"><span class="edu-school">Georgetown University Law Center</span><span class="edu-field">Master of Laws in Taxation</span></span></li>
<li><span class="edu-deg">J.D.</span><span class="edu-body"><span class="edu-school">University of Maryland Francis King Carey School of Law</span><span class="edu-field">Juris Doctor</span></span></li>
<li><span class="edu-deg">B.A.</span><span class="edu-body"><span class="edu-school">Bates College</span><span class="edu-field">International Trade</span></span></li>
</ul>
</div>
</aside>
</div>
</section>

<section class="section section-rule">
<div class="wrap">
<h2 class="h-xl h-story">Families are difficult enough. Family law shouldn’t be.</h2>
<div class="story">
<div class="story-side">
{pic('meredith', 'Meredith M. Maller', 'portrait')}
<p class="sign-intro">Let’s discuss your legal needs. Shoot me an <a href="mailto:{MER_EMAIL}">email</a>, give me a <a href="tel:{PHONE_TEL}">call</a>, or find me on <a href="{LINKEDIN_URL}" rel="noopener">LinkedIn</a>.</p>
<p class="signature" aria-label="Signed, Mer">Mer</p>
</div>
<div class="stack prose founder-note">
<p>After years of practicing at leading law firms in Washington, D.C. and Maine (<i>Bernstein Shur</i>), I counseled clients, families, and family offices as an independent, global investment management and strategic advisor at a firm with over $160B of assets under management. Then I had a kid, got divorced, and left the big legal world behind.</p>
<p><i>Naviga</i> (the name of the sailboat I don’t own since I’m a sole practitioner law firm) reflects a deliberate departure from the traditional big-firm model—without sacrificing sophistication or rigor. Sometimes a smaller boat reminds us why we learned to sail.</p>
<p>I’ve built <i>Naviga</i> to provide direct access to experienced counsel and practical solutions, tailored to real lives and real families. It allows me to practice and work with clients on my terms, and theirs. Family law, at its best, is a collaboration.</p>
<p>I’ve been on both sides of the table as an Attorney, but my involvement with the legal system as a Parent, Child, Mother, and Partner is what informed and built <i>Naviga</i>. I am a Personal Attorney, because the law and what it impacts is inherently personal.</p>
</div>
</div>
</div>
</section>'''
    return (head('About Naviga Law & Meredith M. Maller, J.D., LL.M.',
                 'Meredith M. Maller founded Naviga Law to give Maine families direct access to experienced trusts and estates counsel. LL.M. in Taxation, Georgetown; seventh-generation Mainer.', '/about/')
            + header('about') + body + footer())

def contact():
    body = f'''<section class="section">
<div class="wrap contact">
<div class="stack">
<h1 class="h-xxl">Contact us.</h1>
<p>Start the conversation by reaching out, via this form, email, or phone. General response time is one business day.</p>
<span class="rule-accent" aria-hidden="true"></span>
<p class="contact-lines"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{PHONE_TEL}">{PHONE}</a></p>
<div class="mail-addr"><p class="mail-label">Mailing Address:</p><address class="muted">{ADDR1}<br>{ADDR2}</address></div>
</div>
<form class="contact-form js-form" action="/api/contact" method="post" aria-label="Contact form">
<div class="row2">
<label>First name<input type="text" name="first" autocomplete="given-name" required></label>
<label>Last name<input type="text" name="last" autocomplete="family-name" required></label>
</div>
<label>Email<input type="email" name="email" autocomplete="email" required></label>
<label>Phone <span class="opt">(optional)</span><input type="tel" name="phone" autocomplete="tel"></label>
<label>How can we help?<textarea name="message" rows="6" required></textarea></label>
<p class="small muted">Please don’t include confidential details yet. Sending this form does not create an attorney–client relationship.</p>
{hidden_fields('contact')}
<button type="submit" class="btn">Send</button>
<p class="form-status" role="status" aria-live="polite"></p>
</form>
</div>
</section>'''
    return (head('Contact Naviga Law | Scarborough, Maine',
                 'Contact Naviga Law in Scarborough, Maine. Call (207) 805-2182, email info@navigalaw.com, or send a message. Free 30-minute consultations.', '/contact-us/')
            + header('contact') + body + footer(cta=False))

def simple(title, path, h1, inner, desc):
    return head(title, desc, path) + header('') + f'''<section class="section"><div class="wrap narrow stack prose">
<h1 class="h-xl">{h1}</h1>{inner}</div></section>''' + footer(cta=False)

def privacy():
    return simple('Privacy | Naviga Law', '/privacy/', 'Privacy', f'''
<p>This website does not use advertising trackers or sell personal information.</p>
<p>When you submit a form, the details you enter (name, email, phone if given, and your message) are sent to Naviga Law by email so we can reply. They are not shared with anyone else.</p>
<p>The site is hosted by Cloudflare, which may keep standard server logs (such as IP address and browser type) for security and performance.</p>
<p>Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>''', 'How Naviga Law handles information submitted through this website.')

def thanks():
    return simple('Thank you | Naviga Law', '/thanks/', 'Thank you.', f'''
<p>Your message is on its way. Our general response time is one business day.</p>
<p>If it’s urgent, call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
<p><a class="btn" href="/">Back to home</a></p>''', 'Message received.')

def formerror():
    return simple('Message not sent | Naviga Law', '/form-error/', 'That didn’t go through.', f'''
<p>Something went wrong sending your message, or a required field was missing. Nothing was sent.</p>
<p>Please email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_TEL}">{PHONE}</a>, or <a href="/contact-us/">try the form again</a>.</p>''', 'Message not sent.')

def notfound():
    return simple('Page not found | Naviga Law', '/404', 'Off the chart.', '''
<p>We couldn’t find that page. It may have moved when the site was redesigned.</p>
<p><a class="btn" href="/">Back to home</a></p>''', 'Page not found.')

PAGES = {'index.html': home, 'about/index.html': about, 'contact-us/index.html': contact,
         'privacy/index.html': privacy, 'thanks/index.html': thanks, 'form-error/index.html': formerror, '404.html': notfound}

if __name__ == '__main__':
    for rel, fn in PAGES.items():
        p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w').write(fn())
    today = datetime.date.today().isoformat()
    urls = ['/', '/about/', '/contact-us/', '/privacy/']
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + ''.join(f'<url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n' for u in urls) + '</urlset>\n')
    print('built', len(PAGES), 'pages')

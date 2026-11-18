#!/usr/bin/env python3
"""Builds a single-file clickable preview of ./site (for the claude.ai preview artifact).
Images are inlined; fonts come from Google Fonts; pages switch by #hash; forms are disabled."""
import re, base64, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site') + '/'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/preview.html'

def b64(p, mime): return f'data:{mime};base64,' + base64.b64encode(open(ROOT + p, 'rb').read()).decode()
IM = {n: b64(f'assets/img/{n}.webp', 'image/webp') for n in ['meredith', 'about-hero', 'chart-hero']}

css = open(ROOT + 'assets/css/site.css').read()
css = re.sub(r'@font-face\{[^}]*\}\n?', '', css)
for n, d in IM.items():
    css = re.sub(rf"image-set\(url\(/assets/img/{n}\.webp\) type\('image/webp'\),url\(/assets/img/{n}\.jpg\) type\('image/jpeg'\)\)", f'url({d})', css)
    css = css.replace(f'url(/assets/img/{n}.jpg)', f'url({d})')
for svg in re.findall(r'url\(/assets/img/([\w-]+\.svg)\)', css):
    css = css.replace(f'url(/assets/img/{svg})', f'url({b64("assets/img/" + svg, "image/svg+xml")})')
css += ('\n.view{display:none}.view.on{display:block}'
        '.pv-banner{background:#3E6881;color:#F3F6F8;font-size:13px;letter-spacing:.04em;text-align:center;padding:8px 16px}'
        '.epigraph+.site-footer{padding-top:0}.epigraph+.site-footer>.wrap{border-top:1px solid var(--mountain);padding-top:48px}')

def grab(path):
    h = open(ROOT + path).read()
    main = re.search(r'<main id="main">(.*)</main>', h, re.S).group(1)
    foot = re.search(r'(<footer class="site-footer">.*?</footer>)', h, re.S).group(1)
    return main.strip() + '\n' + foot

LINKS = [('href="/about/#meredith"', 'href="#meredith"'), ('href="/about/"', 'href="#about"'),
         ('href="/contact-us/"', 'href="#contact"'), ('href="/privacy/"', 'href="#privacy"'),
         ('href="/#schedule-consultation"', 'href="#schedule-consultation"'), ('href="/"', 'href="#home"')]
def fix(h):
    h = re.sub(r'<source srcset="/assets/img/[\w-]+\.webp" type="image/webp">', '', h)
    h = re.sub(r'src="/assets/img/([\w-]+)\.jpg"', lambda m: f'src="{IM[m.group(1)]}"', h)
    for a, b in LINKS: h = h.replace(a, b)
    return h

views = ''.join(f'<div class="view" id="v-{k}" data-view="{k}">{fix(grab(p))}</div>'
                for k, p in [('home', 'index.html'), ('about', 'about/index.html'), ('contact', 'contact-us/index.html'), ('privacy', 'privacy/index.html')])
hdr = re.search(r'(<header class="site-header">.*?</header>)', open(ROOT + 'index.html').read(), re.S).group(1).replace(' aria-current="page"', '')

js = open(ROOT + 'assets/js/site.js').read().replace(
    "if (!window.fetch) return;\n      e.preventDefault();",
    "e.preventDefault();\n      var st=form.querySelector('.form-status'); st.className='form-status'; st.textContent='Preview only — on the live site this sends an email to Meredith.'; return;")
router = '''(function(){var views=[].slice.call(document.querySelectorAll('.view'));
function show(){var h=(location.hash||'#home').slice(1);var v=document.getElementById('v-'+h);var t=null;
if(!v){t=document.getElementById(h);v=t?t.closest('.view'):document.getElementById('v-home');}
views.forEach(function(x){x.classList.toggle('on',x===v)});
document.querySelectorAll('.site-nav ul a').forEach(function(a){if(a.getAttribute('href')==='#'+v.dataset.view)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
if(t){t.scrollIntoView();}else{window.scrollTo(0,0);}}
window.addEventListener('hashchange',show);show();})();'''

html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Naviga Law — Website Preview</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Tinos:ital,wght@0,400;0,700;1,400&family=Mrs+Saint+Delafield&display=swap">
<style>{css}</style></head><body>
<div class="pv-banner">Preview of the new navigalaw.com — links work; forms are disabled in this preview.</div>
{fix(hdr)}<div id="main">{views}</div>
<script>{router}</script><script>{js}</script></body></html>'''
open(OUT, 'w').write(html)
print(OUT, len(html) // 1024, 'KB')

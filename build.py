"""Builds the static pages from src/*.html bodies plus a shared header and footer.

Run: python3 build.py
Each file in src/ starts with three lines:
  title: Page title
  description: Meta description
  nav: index | our-approach | services | cases | (blank)
followed by a blank line and the page body.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
BOOK = "https://calendar.app.google/pUPfxcmEGfwEiBRHA"
EMAIL = "connect@consumerandcommerce.global"

import hashlib
CSS_V = hashlib.md5((ROOT / "assets/site.css").read_bytes()).hexdigest()[:8]
MONOGRAM = (ROOT / "assets/img/monogram.svg").read_text().strip()


def inline_svg(name):
    svg = (ROOT / "assets/img" / name).read_text()
    svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)
    svg = re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2)
    return svg.strip()


NAV = [
    ("our-approach", "our-approach.html", "Our approach"),
    ("services", "services.html", "Services"),
    ("cases", "cases.html", "Cases"),
]


def header(active):
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a>'
        for key, href, label in NAV
    )
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="lockup" href="index.html" aria-label="MLR Consumer&amp;Commerce, home">{MONOGRAM}<span>CONSUMER&amp;COMMERCE</span></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main">{links}<a class="btn btn-quiet" href="{BOOK}" target="_blank" rel="noopener">Book a call</a></nav>
  </div>
</header>"""


FOOTER = f"""<footer class="site-footer">
  <div class="wrap">
    <div class="top">
      <div>
        <a class="lockup" href="index.html" aria-label="MLR Consumer&amp;Commerce, home">{MONOGRAM}<span>CONSUMER&amp;COMMERCE</span></a>
        <p class="tagline">Effort that compounds.</p>
      </div>
      <nav aria-label="Footer">
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="partners.html">Partner with us</a></li>
          <li><a href="https://www.linkedin.com/company/mlr-consumer-and-commerce/" target="_blank" rel="noopener">LinkedIn</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </nav>
    </div>
    <p class="legal">MLR Global SRL · P.IVA IT11868950962 · <a href="legal.html">Legal information</a></p>
  </div>
</footer>
<script>
  const t = document.querySelector('.nav-toggle'), n = document.getElementById('nav');
  t.addEventListener('click', () => {{ const o = n.classList.toggle('open'); t.setAttribute('aria-expanded', o); }});
</script>"""


def page(title, description, active, body):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="preload" href="assets/fonts/montserrat-latin-300-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/montserrat-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css?v={CSS_V}">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{FOOTER}
</body>
</html>
"""


def main():
    for src in sorted(SRC.glob("*.html")):
        text = src.read_text()
        head, body = text.split("\n\n", 1)
        meta = {k.strip(): v.strip() for k, v in (line.split(":", 1) for line in head.splitlines())}
        body = body.replace("{{BOOK}}", BOOK).replace("{{EMAIL}}", EMAIL)
        body = body.replace("{{MONOGRAM}}", MONOGRAM)
        body = re.sub(r"\{\{SVG:([\w.-]+)\}\}", lambda m: inline_svg(m.group(1)), body)
        out = page(meta["title"], meta["description"], meta.get("nav", "").strip(), body)
        (ROOT / src.name).write_text(out)
        print("built", src.name)


if __name__ == "__main__":
    main()

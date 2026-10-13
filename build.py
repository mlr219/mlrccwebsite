"""Builds the static pages from src/*.html bodies plus a shared header and footer.

Run: python3 build.py
Each file in src/ starts with three lines:
  title: Page title
  description: Meta description
  nav: index | how-we-work | work-with-us | cases | (blank)
followed by a blank line and the page body.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
BOOK = "https://calendar.app.google/pUPfxcmEGfwEiBRHA"
EMAIL = "connect@consumerandcommerce.global"

MONOGRAM = (ROOT / "assets/img/monogram.svg").read_text().strip()


def inline_svg(name):
    svg = (ROOT / "assets/img" / name).read_text()
    svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)
    svg = re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2)
    return svg.strip()


NAV = [
    ("how-we-work", "how-we-work.html", "How we work"),
    ("work-with-us", "work-with-us.html", "Work with us"),
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
    <nav class="nav" id="nav" aria-label="Main">{links}<a class="btn btn-small" href="{BOOK}">Book a call</a></nav>
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
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </nav>
    </div>
    <p class="legal">MLR Consumer&amp;Commerce is a brand of MLR Global SRL. Registered office: Viale Abruzzi 31, 20131 Milano (MI), Italy. Registro Imprese di Milano Monza Brianza Lodi and P.IVA IT11868950962, REA MI-2628589. Share capital €10,000, fully paid. This site sets no cookies.</p>
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
<link rel="stylesheet" href="assets/site.css">
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
        meta = dict(line.split(": ", 1) for line in head.splitlines())
        body = body.replace("{{BOOK}}", BOOK).replace("{{EMAIL}}", EMAIL)
        body = body.replace("{{MONOGRAM}}", MONOGRAM)
        body = re.sub(r"\{\{SVG:([\w.-]+)\}\}", lambda m: inline_svg(m.group(1)), body)
        out = page(meta["title"], meta["description"], meta.get("nav", "").strip(), body)
        (ROOT / src.name).write_text(out)
        print("built", src.name)


if __name__ == "__main__":
    main()

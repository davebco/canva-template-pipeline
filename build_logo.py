"""Generate Etsy shop-icon logo concepts for 'TemplateStudio by QB'.

Brand tokens: ivory #F7F3EE, charcoal #3E3A34, terracotta #C0876B, sand #EAE3D9, taupe #A39A8D.
Fonts: Cormorant Garamond (display) + Lato (labels). One concept nods to the QB parent (deep blue).
Renders six 1000x1000 concepts via headless Chrome, plus a contact sheet.

Usage:  py build_logo.py
"""
import subprocess
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ROOT = Path(__file__).parent
OUT = ROOT / "out" / "logo"
OUT.mkdir(parents=True, exist_ok=True)

HEAD = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Lato:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  :root{--ivory:#F7F3EE;--charcoal:#3E3A34;--terracotta:#C0876B;--sand:#EAE3D9;--taupe:#A39A8D;--qblue:#27395B;}
  *{margin:0;padding:0;box-sizing:border-box;}
  html,body{width:1000px;height:1000px;overflow:hidden;}
  body{font-family:'Lato',sans-serif;display:flex;align-items:center;justify-content:center;}
  svg{width:1000px;height:1000px;display:block;}
"""
FOOT = "</style></head><body>{body}</body></html>"


def render(name, css, body):
    html = HEAD + css + FOOT.format(body=body)
    f = OUT / f"{name}.html"
    f.write_text(html, encoding="utf-8")
    png = OUT / f"{name}.png"
    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", "--window-size=1000,1000",
        "--virtual-time-budget=12000", f"--screenshot={png}", f.resolve().as_uri(),
    ], check=True, capture_output=True)
    print(png.name)


# A — circular seal (terracotta ring, curved text)
render("A-seal",
  ".bg{fill:var(--ivory);} .ring{fill:none;stroke:var(--terracotta);} "
  ".ct{fill:var(--charcoal);font-family:'Lato';font-weight:700;font-size:44px;letter-spacing:8px;} "
  ".mono{fill:var(--charcoal);font-family:'Cormorant Garamond';font-weight:600;font-size:300px;} "
  ".star{fill:var(--terracotta);font-size:44px;}",
  '''<svg viewBox="0 0 1000 1000">
    <rect class="bg" width="1000" height="1000"/>
    <circle class="ring" cx="500" cy="500" r="410" stroke-width="4"/>
    <circle class="ring" cx="500" cy="500" r="392" stroke-width="2"/>
    <defs>
      <path id="top" d="M 140 500 A 360 360 0 0 1 860 500"/>
      <path id="bot" d="M 160 500 A 340 340 0 0 0 840 500"/>
    </defs>
    <text class="ct"><textPath href="#top" startOffset="50%" text-anchor="middle">TEMPLATE&#160;&#160;STUDIO</textPath></text>
    <text class="ct"><textPath href="#bot" startOffset="50%" text-anchor="middle">BY&#160;QUANTUM&#160;BLUE</textPath></text>
    <text class="star" x="500" y="215" text-anchor="middle">&#10022;</text>
    <text class="mono" x="500" y="600" text-anchor="middle">TS</text>
  </svg>''')

# B — terracotta monogram badge
render("B-badge",
  "body{background:var(--ivory);} "
  ".badge{width:640px;height:640px;background:var(--terracotta);border-radius:56px;"
  "display:flex;flex-direction:column;align-items:center;justify-content:center;}"
  ".ts{font-family:'Cormorant Garamond';font-weight:600;font-size:340px;color:var(--ivory);line-height:.8;}"
  ".lbl{font-family:'Lato';font-weight:700;font-size:38px;letter-spacing:12px;color:var(--ivory);margin-top:28px;}",
  '<div class="badge"><div class="ts">TS</div><div class="lbl">STUDIO</div></div>')

# C — emblem: open guide/booklet mark
render("C-emblem",
  "body{background:var(--ivory);flex-direction:column;gap:44px;} "
  ".em{width:470px;} "
  ".t1{font-family:'Cormorant Garamond';font-style:italic;font-weight:600;font-size:96px;color:var(--terracotta);line-height:1;}"
  ".t2{font-family:'Lato';font-weight:900;font-size:52px;letter-spacing:18px;color:var(--charcoal);margin-top:8px;}"
  ".t3{font-family:'Lato';font-weight:700;font-size:30px;letter-spacing:8px;color:var(--taupe);margin-top:20px;}"
  ".wrap{text-align:center;}",
  '''<svg class="em" viewBox="0 0 470 300">
    <g fill="none" stroke="#C0876B" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
      <path d="M235 70 C 190 40, 90 40, 45 62 L 45 250 C 90 228, 190 228, 235 258"/>
      <path d="M235 70 C 280 40, 380 40, 425 62 L 425 250 C 380 228, 280 228, 235 258"/>
      <line x1="235" y1="70" x2="235" y2="258"/>
    </g>
    <g stroke="#EAE3D9" stroke-width="7" stroke-linecap="round">
      <line x1="80" y1="110" x2="200" y2="102"/><line x1="80" y1="150" x2="200" y2="142"/><line x1="80" y1="190" x2="200" y2="182"/>
      <line x1="270" y1="102" x2="390" y2="110"/><line x1="270" y1="142" x2="390" y2="150"/><line x1="270" y1="182" x2="390" y2="190"/>
    </g>
  </svg>
  <div class="wrap"><div class="t2">TEMPLATE STUDIO</div><div class="t3">BY&#160;&#160;QUANTUM&#160;&#160;BLUE</div></div>''')

# D — stacked editorial wordmark
render("D-wordmark",
  "body{background:var(--ivory);flex-direction:column;} "
  ".tpl{font-family:'Cormorant Garamond';font-style:italic;font-weight:600;font-size:170px;color:var(--terracotta);line-height:.9;}"
  ".std{font-family:'Lato';font-weight:900;font-size:96px;letter-spacing:34px;color:var(--charcoal);margin:6px 0 6px 34px;}"
  ".rule{width:360px;height:2px;background:var(--taupe);opacity:.6;margin:26px 0;}"
  ".by{font-family:'Lato';font-weight:700;font-size:34px;letter-spacing:12px;color:var(--taupe);}",
  '<div class="tpl">Template</div><div class="std">STUDIO</div><div class="rule"></div><div class="by">BY QUANTUM BLUE</div>')

# E — minimal lettermark
render("E-lettermark",
  "body{background:var(--ivory);flex-direction:column;} "
  ".mk{font-family:'Cormorant Garamond';font-weight:700;font-size:440px;color:var(--charcoal);line-height:.8;}"
  ".mk span{color:var(--terracotta);}"
  ".sub{font-family:'Lato';font-weight:700;font-size:40px;letter-spacing:14px;color:var(--taupe);margin-top:36px;}",
  '<div class="mk">TS<span>.</span></div><div class="sub">TEMPLATE STUDIO &#183; BY QB</div>')

# F — QB parent-forward (deep blue circle)
render("F-qb-blue",
  "body{background:var(--ivory);} "
  ".circ{width:660px;height:660px;border-radius:50%;background:var(--qblue);"
  "display:flex;flex-direction:column;align-items:center;justify-content:center;}"
  ".qb{font-family:'Cormorant Garamond';font-weight:600;font-size:300px;color:var(--ivory);line-height:.8;}"
  ".qb span{color:var(--terracotta);}"
  ".lbl{font-family:'Lato';font-weight:700;font-size:34px;letter-spacing:11px;color:var(--ivory);margin-top:30px;opacity:.9;}",
  '<div class="circ"><div class="qb">Q<span>B</span></div><div class="lbl">TEMPLATE STUDIO</div></div>')

# contact sheet
try:
    from PIL import Image
    import glob
    files = sorted(glob.glob(str(OUT / "*.png")))
    tw = 470
    cols, rows = 3, 2
    sheet = Image.new('RGB', (cols*tw+40, rows*tw+40), '#ffffff')
    for i, f in enumerate(files):
        im = Image.open(f).convert('RGB').resize((tw, tw))
        r, c = divmod(i, cols)
        sheet.paste(im, (10+c*(tw+10), 10+r*(tw+10)))
    sheet.save(str(ROOT / "out" / "logo-contact.png"))
    print("contact sheet ->", ROOT / "out" / "logo-contact.png")
except Exception as e:
    print("contact sheet skipped:", e)

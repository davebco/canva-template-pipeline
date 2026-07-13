"""Etsy shop banners for 'TemplateStudio by QB', matching the F1 shop icon.

Brand: deep-space hero gradient, lowercase 'qb' + electric-blue dot, Inter, cool-white.
Renders the big cover banner (3360x840) and the mini banner (1200x160).
Key content is centered so Etsy's responsive edge-crop never clips it.

Usage:  py build_banner.py
"""
import subprocess
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ROOT = Path(__file__).parent
OUT = ROOT / "out" / "logo"
OUT.mkdir(parents=True, exist_ok=True)

TAGLINE = "Elegant, editable Canva templates for your business"

CSS = """
  :root{--deep:#050B1F;--navy:#0A1F4A;--royal:#1E3A8A;--electric:#3B82F6;--sky:#7DD3FC;
        --white:#F0F4FF;--slate:#94A3B8;}
  *{margin:0;padding:0;box-sizing:border-box;}
  html,body{overflow:hidden;}
  body{font-family:'Inter',sans-serif;display:flex;align-items:center;justify-content:center;
       background:linear-gradient(115deg,#050B1F 0%,#0A1F4A 55%,#1E3A8A 100%);}
  .lockup{display:flex;align-items:center;}
  .mark{position:relative;}
  .qb{font-weight:700;letter-spacing:-.05em;color:var(--white);line-height:.8;}
  .dot{position:absolute;border-radius:50%;background:var(--electric);}
  .divider{background:linear-gradient(180deg,#7DD3FC 0%,#3B82F6 100%);border-radius:6px;}
  .txt{display:flex;flex-direction:column;}
  .word{font-weight:600;color:var(--white);}
  .tag{color:var(--sky);font-weight:500;}
"""


def render(name, w, h, extra, body):
    html = (f'<!DOCTYPE html><html><head><meta charset="utf-8">'
            f'<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700&display=swap" rel="stylesheet">'
            f'<style>html,body{{width:{w}px;height:{h}px;}}{CSS}{extra}</style></head><body>{body}</body></html>')
    f = OUT / f"{name}.html"
    f.write_text(html, encoding="utf-8")
    png = OUT / f"{name}.png"
    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", f"--window-size={w},{h}",
        "--virtual-time-budget=12000", f"--screenshot={png}", f.resolve().as_uri(),
    ], check=True, capture_output=True)
    print(f"{png.name}  {w}x{h}")


# --- big cover banner 3360x840 ---
render("banner-cover", 3360, 840,
  extra="""
    .lockup{gap:90px;}
    .qb{font-size:340px;}
    .dot{top:38px;right:-30px;width:52px;height:52px;box-shadow:0 0 44px rgba(59,130,246,.6);}
    .divider{width:4px;height:210px;}
    .word{font-size:96px;letter-spacing:.2em;padding-left:.2em;}
    .tag{font-size:44px;letter-spacing:.02em;margin-top:26px;}
  """,
  body=f'''<div class="lockup">
    <div class="mark"><span class="qb">qb</span><span class="dot"></span></div>
    <div class="divider"></div>
    <div class="txt"><div class="word">TEMPLATE STUDIO</div><div class="tag">{TAGLINE}</div></div>
  </div>''')

# --- mini banner 1200x160 ---
render("banner-mini", 1200, 160,
  extra="""
    .lockup{gap:34px;}
    .qb{font-size:120px;}
    .dot{top:13px;right:-12px;width:20px;height:20px;box-shadow:0 0 16px rgba(59,130,246,.6);}
    .divider{width:2px;height:78px;}
    .word{font-size:38px;letter-spacing:.18em;padding-left:.18em;}
    .tag{font-size:19px;letter-spacing:.01em;margin-top:8px;}
  """,
  body=f'''<div class="lockup">
    <div class="mark"><span class="qb">qb</span><span class="dot"></span></div>
    <div class="divider"></div>
    <div class="txt"><div class="word">TEMPLATE STUDIO</div><div class="tag">{TAGLINE}</div></div>
  </div>''')

# preview: downscale cover to a readable width for review
from PIL import Image
Image.open(OUT / "banner-cover.png").convert('RGB').resize((1400, 350)).save(ROOT / "out" / "banner-cover-prev.png")
Image.open(OUT / "banner-mini.png").convert('RGB').resize((1200, 160)).save(ROOT / "out" / "banner-mini-prev.png")
print("previews -> out/banner-cover-prev.png, out/banner-mini-prev.png")

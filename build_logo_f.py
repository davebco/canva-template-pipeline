"""Refine logo concept F against the real Quantum Blue brand kit.

Brand (C:\\Claude\\branding\\quantum-blue-ai): deep-space #050B1F, quantum-navy #0A1F4A,
royal #1E3A8A, electric-blue #3B82F6, sky #7DD3FC, cool-white #F0F4FF. Signature: lowercase
'qb' wordmark (Inter), the electric-blue dot 'tell', and the deep-space hero gradient surface.

Renders 3 variants at 1000x1000, exports a 500x500 Etsy icon of each, and a comparison sheet
showing each full-size plus a small circular-cropped avatar (how Etsy displays it).

Usage:  py build_logo_f.py
"""
import subprocess
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ROOT = Path(__file__).parent
OUT = ROOT / "out" / "logo"
OUT.mkdir(parents=True, exist_ok=True)

HEAD = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{--deep:#050B1F;--navy:#0A1F4A;--royal:#1E3A8A;--electric:#3B82F6;--sky:#7DD3FC;
        --white:#F0F4FF;--mist:#F4F6FA;--slate:#94A3B8;}
  *{margin:0;padding:0;box-sizing:border-box;}
  html,body{width:1000px;height:1000px;overflow:hidden;}
  body{font-family:'Inter',sans-serif;display:flex;align-items:center;justify-content:center;}
  .stack{display:flex;flex-direction:column;align-items:center;}
  .mark{position:relative;}
  .qb{font-weight:700;font-size:400px;letter-spacing:-.05em;color:var(--white);line-height:.8;}
  .dot{position:absolute;top:44px;right:-30px;width:60px;height:60px;border-radius:50%;background:var(--electric);
       box-shadow:0 0 40px rgba(59,130,246,.55);}
  .bar{width:150px;height:7px;border-radius:6px;margin:54px 0 30px;
       background:linear-gradient(90deg,#7DD3FC 0%,#3B82F6 100%);}
  .lbl{font-weight:600;font-size:46px;letter-spacing:.34em;color:var(--white);opacity:.82;padding-left:.34em;}
"""
FOOT = "</style></head><body>{body}</body></html>"

MARK = ('<div class="stack"><div class="mark"><span class="qb">qb</span><span class="dot"></span></div>'
        '<div class="bar"></div><div class="lbl">TEMPLATE STUDIO</div></div>')


def render(name, css):
    html = HEAD + css + FOOT.format(body=MARK)
    f = OUT / f"{name}.html"
    f.write_text(html, encoding="utf-8")
    png = OUT / f"{name}.png"
    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", "--window-size=1000,1000",
        "--virtual-time-budget=12000", f"--screenshot={png}", f.resolve().as_uri(),
    ], check=True, capture_output=True)
    print(png.name)
    return png


# F1 — full-bleed deep-space hero gradient (the brand's signature surface)
p1 = render("F1-gradient", "body{background:linear-gradient(135deg,#050B1F 0%,#0A1F4A 58%,#1E3A8A 100%);}")
# F2 — solid quantum navy (flatter, crispest at tiny sizes)
p2 = render("F2-navy", "body{background:#0A1F4A;}")
# F3 — navy mark inside a cool-white square (his original 'circle on light' feel, full-bleed light)
p3 = render("F3-onlight",
  "body{background:var(--mist);} .qb{color:var(--navy);} .lbl{color:var(--navy);opacity:.7;} "
  ".dot{background:var(--electric);box-shadow:none;}")

# ---- export 500x500 Etsy icons + a comparison sheet with tiny circular avatars ----
from PIL import Image, ImageDraw

def circle_thumb(im, size):
    t = im.convert('RGB').resize((size, size))
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    out = Image.new('RGB', (size, size), '#ffffff')
    out.paste(t, (0, 0), mask)
    return out

pages = [("F1", p1), ("F2", p2), ("F3", p3)]
big = 440; av = 130; pad = 30; gap = 40
sheet = Image.new('RGB', (3*(big)+4*pad, big+av+3*pad+50), '#ffffff')
for i, (name, p) in enumerate(pages):
    im = Image.open(p)
    # 500x500 final icon
    im.convert('RGB').resize((500, 500)).save(OUT / f"icon-{name}-500.png")
    # comparison sheet
    x = pad + i*(big+pad)
    sheet.paste(im.convert('RGB').resize((big, big)), (x, pad))
    # tiny circular avatar centered under each
    sheet.paste(circle_thumb(im, av), (x + (big-av)//2, pad+big+20))
sheet.save(str(ROOT / "out" / "logo-f-compare.png"))
print("compare ->", ROOT / "out" / "logo-f-compare.png")
print("icons -> out/logo/icon-F1-500.png, icon-F2-500.png, icon-F3-500.png")

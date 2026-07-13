"""Generate Etsy listing mockup images for Listing 1 from the finished page PNGs.

Reads out/l1-final/page-0N.png (exported from the finished Canva design) and composes
6 brand-styled 2000x2000 marketing images via headless Chrome screenshots.
Output: out/mockups/img-N-*.png

Usage:  py build_mockups.py
"""
import subprocess
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ROOT = Path(__file__).parent
PAGES = (ROOT / "out" / "l1-final").resolve()
OUT = ROOT / "out" / "mockups"
OUT.mkdir(parents=True, exist_ok=True)


def page(n: int) -> str:
    return (PAGES / f"page-{n:02d}.png").as_uri()


BASE = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Lato:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  :root{{--ivory:#F7F3EE;--charcoal:#3E3A34;--terracotta:#C0876B;--sand:#EAE3D9;--taupe:#A39A8D;}}
  *{{margin:0;padding:0;box-sizing:border-box;}}
  html,body{{width:2000px;height:2000px;overflow:hidden;}}
  body{{font-family:'Lato',sans-serif;color:var(--charcoal);background:var(--ivory);
        display:flex;flex-direction:column;}}
  .eyebrow{{font-weight:900;font-size:24px;letter-spacing:.42em;text-transform:uppercase;color:var(--terracotta);}}
  h2{{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:104px;line-height:1.02;letter-spacing:.01em;}}
  h2 em{{font-style:italic;color:var(--terracotta);}}
  .sub{{font-size:30px;line-height:1.5;color:var(--taupe);}}
  .shadow{{box-shadow:0 40px 90px rgba(62,58,52,.20);border-radius:5px;}}
  {css}
</style></head><body>{body}</body></html>"""


def write(name: str, body: str, css: str = "") -> Path:
    html = BASE.format(body=body, css=css)
    f = OUT / f"{name}.html"
    f.write_text(html, encoding="utf-8")
    return f


# ---- Slide 1: cover hero -------------------------------------------------
s1 = write("img-1-cover", css="""
  body{align-items:center;justify-content:center;gap:70px;}
  .cover{height:1420px;}
  .cap{font-weight:700;font-size:26px;letter-spacing:.24em;text-transform:uppercase;color:var(--charcoal);}
""", body=f"""
  <div class="eyebrow">TemplateStudio &nbsp;&middot;&nbsp; by QB</div>
  <img class="cover shadow" src="{page(1)}">
  <div class="cap">Editable Canva Template &nbsp;&middot;&nbsp; Family &amp; Portrait Photographers</div>
""")

# ---- Slide 2: 9-page grid ------------------------------------------------
tiles = "".join(f'<img src="{page(i)}">' for i in range(1, 10))
s2 = write("img-2-grid", css="""
  body{padding:120px 150px 110px;}
  .head{margin-bottom:56px;}
  .head h2{margin:14px 0 16px;}
  .grid{display:grid;grid-template-columns:repeat(3,340px);justify-content:center;gap:38px;}
  .grid img{width:100%;border-radius:4px;box-shadow:0 22px 50px rgba(62,58,52,.16);}
""", body=f"""
  <div class="head">
    <div class="eyebrow">What's inside</div>
    <h2>A complete <em>9-page</em> guide</h2>
    <div class="sub">Everything a client needs — from first hello to booked session.</div>
  </div>
  <div class="grid">{tiles}</div>
""")

# ---- Slide 3: About close-up (split) ------------------------------------
s3 = write("img-3-about", css="""
  body{flex-direction:row;align-items:center;}
  .imgcol{flex:0 0 52%;height:100%;display:flex;align-items:center;justify-content:center;
          background:var(--sand);}
  .imgcol img{height:1500px;}
  .txt{flex:1;padding:0 130px;}
  .txt h2{margin:18px 0 50px;}
  .feat{display:flex;align-items:flex-start;gap:26px;margin-bottom:40px;}
  .dot{flex:none;width:20px;height:20px;border-radius:50%;background:var(--terracotta);margin-top:14px;}
  .feat b{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:44px;display:block;}
  .feat span{font-size:27px;color:var(--taupe);line-height:1.45;}
""", body=f"""
  <div class="imgcol"><img class="shadow" src="{page(3)}"></div>
  <div class="txt">
    <div class="eyebrow">Fully editable</div>
    <h2>Make it <em>your own</em></h2>
    <div class="feat"><div class="dot"></div><div><b>Your headshot &amp; photos</b><span>Drop your images into every frame.</span></div></div>
    <div class="feat"><div class="dot"></div><div><b>Your story &amp; style</b><span>Rewrite the bio and welcome in your voice.</span></div></div>
    <div class="feat"><div class="dot"></div><div><b>Your brand colors &amp; fonts</b><span>Match your look in a few clicks.</span></div></div>
  </div>
""")

# ---- Slide 4: FAQ close-up (split, mirrored) ----------------------------
s4 = write("img-4-faq", css="""
  body{flex-direction:row;align-items:center;}
  .imgcol{flex:0 0 52%;height:100%;display:flex;align-items:center;justify-content:center;
          background:var(--sand);order:2;}
  .imgcol img{height:1500px;}
  .txt{flex:1;padding:0 130px;order:1;}
  .txt h2{margin:18px 0 50px;}
  .feat{display:flex;align-items:flex-start;gap:26px;margin-bottom:40px;}
  .dot{flex:none;width:20px;height:20px;border-radius:50%;background:var(--terracotta);margin-top:14px;}
  .feat b{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:44px;display:block;}
  .feat span{font-size:27px;color:var(--taupe);line-height:1.45;}
""", body=f"""
  <div class="imgcol"><img class="shadow" src="{page(6)}"></div>
  <div class="txt">
    <div class="eyebrow">Set expectations</div>
    <h2>Answer every <em>question</em></h2>
    <div class="feat"><div class="dot"></div><div><b>Pre-written Q&amp;A</b><span>Editable answers to the questions you hear most.</span></div></div>
    <div class="feat"><div class="dot"></div><div><b>Fewer back-and-forth emails</b><span>Clients arrive prepared and confident.</span></div></div>
    <div class="feat"><div class="dot"></div><div><b>A polished first impression</b><span>Look booked-out and professional from hello.</span></div></div>
  </div>
""")

# ---- Slide 5: editable in Canva -----------------------------------------
thumbs = "".join(f'<img src="{page(i)}">' for i in (2, 5, 8))
s5 = write("img-5-canva", css="""
  body{align-items:center;justify-content:center;text-align:center;padding:0 160px;}
  .pill{background:var(--terracotta);color:var(--ivory);font-weight:900;font-size:24px;
        letter-spacing:.2em;text-transform:uppercase;padding:20px 46px;border-radius:60px;margin-bottom:60px;}
  h2{font-size:132px;margin-bottom:34px;}
  .sub{font-size:34px;margin-bottom:90px;}
  .thumbs{display:flex;gap:56px;}
  .thumbs img{height:700px;border-radius:5px;box-shadow:0 34px 70px rgba(62,58,52,.20);}
  .thumbs img:nth-child(1){transform:rotate(-4deg);}
  .thumbs img:nth-child(3){transform:rotate(4deg);}
""", body=f"""
  <div class="pill">No Canva Pro needed</div>
  <h2>Edit it all in <em>Canva</em></h2>
  <div class="sub">Free Canva account &nbsp;&middot;&nbsp; no design skills &nbsp;&middot;&nbsp; ready in minutes</div>
  <div class="thumbs">{thumbs}</div>
""")

# ---- Slide 6: how it works ----------------------------------------------
steps = [
    ("1", "Purchase &amp; download", "Instant PDF the moment you check out."),
    ("2", "Open your Canva link", "One click opens an editable copy in Canva."),
    ("3", "Make it yours", "Swap photos, text, colors, and prices."),
    ("4", "Send or print", "Share digitally or export to print — done."),
]
cards = "".join(
    f'<div class="card"><div class="num">{n}</div><div class="ct"><b>{t}</b><span>{d}</span></div></div>'
    for n, t, d in steps
)
s6 = write("img-6-how", css="""
  body{padding:150px 150px 140px;}
  .head{margin-bottom:80px;}
  .head h2{margin-top:14px;}
  .cards{display:grid;grid-template-columns:1fr 1fr;gap:52px;flex:1;}
  .card{background:var(--sand);border-radius:8px;padding:70px 66px;display:flex;gap:40px;align-items:center;}
  .num{flex:none;width:112px;height:112px;border-radius:50%;background:var(--terracotta);color:var(--ivory);
       font-family:'Cormorant Garamond',serif;font-weight:600;font-size:60px;
       display:flex;align-items:center;justify-content:center;}
  .ct b{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:54px;display:block;margin-bottom:12px;}
  .ct span{font-size:29px;color:var(--taupe);line-height:1.4;}
""", body=f"""
  <div class="head">
    <div class="eyebrow">Simple setup</div>
    <h2>How it <em>works</em></h2>
  </div>
  <div class="cards">{cards}</div>
""")

# ---- render all ----------------------------------------------------------
for f in [s1, s2, s3, s4, s5, s6]:
    png = OUT / f"{f.stem}.png"
    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", "--window-size=2000,2000",
        "--virtual-time-budget=12000", f"--screenshot={png}", f.resolve().as_uri(),
    ], check=True, capture_output=True)
    print(png.name)
print("done ->", OUT)

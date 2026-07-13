"""Generate the 6 Etsy listing mockup images for any listing from its page PNGs.

Reads out/l{N}-final/page-0N.png (exported from the finished Canva design) and
composes 6 brand-styled 2000x2000 marketing images via headless Chrome.
Output: out/mockups/l{N}/img-N-*.png

Per-listing content (cover subtitle, grid headline, the two close-up pages and
their feature copy, and the Canva-thumb pages) lives in CONFIGS below — add or
tweak an entry there, never in the slide code. The visual system (fonts, colors,
layout) is shared across all listings so the whole shop looks like one brand.

Usage:
    py build_mockups.py <listing 1-6> [--closeups A,B] [--pages-dir DIR]

    py build_mockups.py 2                 # uses CONFIGS[2], pages from out/l2-final
    py build_mockups.py 4 --closeups 2,3  # override the two close-up page numbers

Prereq: the listing's pages must be exported to out/l{N}-final/page-01.png ...
(via Canva MCP export-design, PNG, width 1632 height 2112). Listing 1 already has
out/l1-final; 2-6 need their Canva design finished + exported first.
"""
import sys
import argparse
import subprocess
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ROOT = Path(__file__).parent


# ---- per-listing content -------------------------------------------------
# Each: pages (count), cover_sub, grid (eyebrow, h2_html, sub),
#       closeups = [ {page, eyebrow, h2_html, features:[(bold, sub) x3]} x2 ],
#       thumbs = 3 page numbers for the "editable in Canva" slide.
CONFIGS = {
    1: {
        "pages": 9,
        "cover_sub": "Editable Canva Template &nbsp;&middot;&nbsp; Family &amp; Portrait Photographers",
        "grid": ("What's inside", "A complete <em>9-page</em> guide",
                 "Everything a client needs — from first hello to booked session."),
        "closeups": [
            {"page": 3, "eyebrow": "Fully editable", "h2": "Make it <em>your own</em>",
             "features": [
                 ("Your headshot &amp; photos", "Drop your images into every frame."),
                 ("Your story &amp; style", "Rewrite the bio and welcome in your voice."),
                 ("Your brand colors &amp; fonts", "Match your look in a few clicks."),
             ]},
            {"page": 6, "eyebrow": "Set expectations", "h2": "Answer every <em>question</em>",
             "features": [
                 ("Pre-written Q&amp;A", "Editable answers to the questions you hear most."),
                 ("Fewer back-and-forth emails", "Clients arrive prepared and confident."),
                 ("A polished first impression", "Look booked-out and professional from hello."),
             ]},
        ],
        "thumbs": [2, 5, 8],
    },
    2: {
        "pages": 5,
        "cover_sub": "Editable Canva Template &nbsp;&middot;&nbsp; Photographer Pricing &amp; Investment",
        "grid": ("What's inside", "A complete <em>pricing</em> set",
                 "Present prices so clients self-select the right package."),
        "closeups": [
            {"page": 2, "eyebrow": "Frame the value", "h2": "Sell your <em>packages</em>",
             "features": [
                 ("Tiered package guide", "Mini · Signature · Deluxe, value-framed."),
                 ("A 'most popular' highlight", "Nudge clients toward the middle tier."),
                 ("Your prices, your brand", "Swap in figures, colors, and fonts."),
             ]},
            {"page": 3, "eyebrow": "Every price, one place", "h2": "Clear <em>price lists</em>",
             "features": [
                 ("À la carte list", "Clean, itemized session pricing."),
                 ("Print &amp; product menu", "Prints, wall art, albums, digital add-ons."),
                 ("Editable in minutes", "Update prices any season in Canva."),
             ]},
        ],
        "thumbs": [2, 3, 4],
    },
    3: {
        "pages": 6,
        "cover_sub": "Editable Canva Template &nbsp;&middot;&nbsp; Photography Booking Paperwork",
        "grid": ("What's inside", "The <em>paperwork</em> every session needs",
                 "A clean, editable starting point — customize to your business and state."),
        "closeups": [
            {"page": 2, "eyebrow": "Look professional", "h2": "A clear <em>agreement</em>",
             "features": [
                 ("Session, fees &amp; retainer", "Spell out what's booked and what's due."),
                 ("Cancellation &amp; weather", "Set reschedule and no-show terms up front."),
                 ("Copyright &amp; usage", "Define delivery and how images may be used."),
             ]},
            {"page": 3, "eyebrow": "Cover the essentials", "h2": "Releases &amp; <em>consent</em>",
             "features": [
                 ("Model release", "Scope-of-use checkboxes and sign-off."),
                 ("Print &amp; copyright release", "The personal-use license labs ask for."),
                 ("Minor photo consent", "Guardian consent for photographing children."),
             ]},
        ],
        "thumbs": [2, 4, 6],
    },
    4: {
        "pages": 5,
        "cover_sub": "Editable Canva Template &nbsp;&middot;&nbsp; Client Session Prep &amp; Style",
        "grid": ("What's inside", "Everything to send <em>after booking</em>",
                 "Turn nervous clients into camera-ready ones."),
        "closeups": [
            {"page": 2, "eyebrow": "Camera-ready clients", "h2": "A <em>what-to-wear</em> guide",
             "features": [
                 ("Coordinate, don't match", "Palettes and combos that photograph well."),
                 ("Outfit 'look' examples", "Three styled looks to inspire clients."),
                 ("Dressing the kids", "Simple tips for the whole family."),
             ]},
            {"page": 3, "eyebrow": "Smoother sessions", "h2": "Prep &amp; <em>timeline</em>",
             "features": [
                 ("Countdown checklist", "Week-before to morning-of steps."),
                 ("Bring list &amp; location notes", "Parking, arrival, and weather backups."),
                 ("Session-day timeline", "Hour-by-hour of what to expect."),
             ]},
        ],
        "thumbs": [2, 3, 4],
    },
    5: {
        "pages": 5,
        "cover_sub": "Editable Canva Template &nbsp;&middot;&nbsp; Photographer Client Onboarding",
        "grid": ("What's inside", "Onboard every <em>new client</em>",
                 "Answer inquiries in seconds and never miss a detail."),
        "closeups": [
            {"page": 2, "eyebrow": "Know before you shoot", "h2": "A client <em>questionnaire</em>",
             "features": [
                 ("Who's being photographed", "Occasion, group, and must-have shots."),
                 ("Style &amp; vibe", "Capture the look each client wants."),
                 ("Everything in one form", "No detail lost between emails."),
             ]},
            {"page": 3, "eyebrow": "Reply in seconds", "h2": "Ready-to-send <em>emails</em>",
             "features": [
                 ("3 inquiry scripts", "Initial reply, follow-up, referral-out."),
                 ("Booking confirmation", "Date, location, package, balance, next steps."),
                 ("Session reminder", "Arrival, what-to-wear, and weather notes."),
             ]},
        ],
        "thumbs": [2, 3, 4],
    },
    6: {
        "pages": 6,
        "cover_sub": "Editable Canva Template &nbsp;&middot;&nbsp; Client Delivery &amp; Follow-Up",
        "grid": ("What's inside", "A polished <em>goodbye</em>",
                 "Turn one session into repeat bookings and referrals."),
        "closeups": [
            {"page": 2, "eyebrow": "Wow at delivery", "h2": "A gallery-ready <em>send-off</em>",
             "features": [
                 ("'Your gallery is ready'", "Link, download, and print instructions."),
                 ("Heartfelt thank-you card", "Optional future-session credit built in."),
                 ("Keep it on brand", "Add your colors, links, and offers."),
             ]},
            {"page": 3, "eyebrow": "Repeat &amp; refer", "h2": "Reorders &amp; <em>referrals</em>",
             "features": [
                 ("Print-reorder guide", "Why pro prints, plus a product menu."),
                 ("Review request", "Friendly ask with direct-link slots."),
                 ("Referral card", "An incentive that drives new bookings."),
             ]},
        ],
        "thumbs": [2, 4, 6],
    },
}


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


def _feature_html(features):
    return "".join(
        f'<div class="feat"><div class="dot"></div><div><b>{b}</b><span>{s}</span></div></div>'
        for b, s in features)


def build(listing: int, closeup_override=None, pages_dir=None):
    cfg = CONFIGS[listing]
    pages = cfg["pages"]
    src = Path(pages_dir).resolve() if pages_dir else (ROOT / "out" / f"l{listing}-final").resolve()
    out = ROOT / "out" / "mockups" / f"l{listing}"
    out.mkdir(parents=True, exist_ok=True)

    if not src.exists():
        sys.exit(f"Pages not found: {src}\n"
                 f"Export the finished Listing {listing} design to that folder first "
                 f"(Canva MCP export-design -> page-01.png ...).")

    def page(n: int) -> str:
        return (src / f"page-{n:02d}.png").as_uri()

    def write(name: str, body: str, css: str = "") -> Path:
        html = BASE.format(body=body, css=css)
        f = out / f"{name}.html"
        f.write_text(html, encoding="utf-8")
        return f

    co = cfg["closeups"]
    if closeup_override:
        co = [dict(co[0], page=closeup_override[0]), dict(co[1], page=closeup_override[1])]

    # ---- Slide 1: cover hero --------------------------------------------
    s1 = write("img-1-cover", css="""
      body{align-items:center;justify-content:center;gap:70px;}
      .cover{height:1420px;}
      .cap{font-weight:700;font-size:26px;letter-spacing:.24em;text-transform:uppercase;color:var(--charcoal);}
    """, body=f"""
      <div class="eyebrow">TemplateStudio &nbsp;&middot;&nbsp; by QB</div>
      <img class="cover shadow" src="{page(1)}">
      <div class="cap">{cfg['cover_sub']}</div>
    """)

    # ---- Slide 2: page grid ---------------------------------------------
    tiles = "".join(f'<img src="{page(i)}">' for i in range(1, pages + 1))
    g_eyebrow, g_h2, g_sub = cfg["grid"]
    s2 = write("img-2-grid", css="""
      body{padding:120px 150px 110px;}
      .head{margin-bottom:56px;}
      .head h2{margin:14px 0 16px;}
      .grid{display:grid;grid-template-columns:repeat(3,340px);justify-content:center;gap:38px;}
      .grid img{width:100%;border-radius:4px;box-shadow:0 22px 50px rgba(62,58,52,.16);}
    """, body=f"""
      <div class="head">
        <div class="eyebrow">{g_eyebrow}</div>
        <h2>{g_h2}</h2>
        <div class="sub">{g_sub}</div>
      </div>
      <div class="grid">{tiles}</div>
    """)

    # ---- Slide 3: first close-up (image left) ---------------------------
    a = co[0]
    s3 = write("img-3-feature", css="""
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
      <div class="imgcol"><img class="shadow" src="{page(a['page'])}"></div>
      <div class="txt">
        <div class="eyebrow">{a['eyebrow']}</div>
        <h2>{a['h2']}</h2>
        {_feature_html(a['features'])}
      </div>
    """)

    # ---- Slide 4: second close-up (image right, mirrored) ---------------
    b = co[1]
    s4 = write("img-4-feature", css="""
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
      <div class="imgcol"><img class="shadow" src="{page(b['page'])}"></div>
      <div class="txt">
        <div class="eyebrow">{b['eyebrow']}</div>
        <h2>{b['h2']}</h2>
        {_feature_html(b['features'])}
      </div>
    """)

    # ---- Slide 5: editable in Canva -------------------------------------
    thumbs = "".join(f'<img src="{page(i)}">' for i in cfg["thumbs"])
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

    # ---- Slide 6: how it works ------------------------------------------
    steps = [
        ("1", "Purchase &amp; download", "Instant PDF the moment you check out."),
        ("2", "Open your Canva link", "One click opens an editable copy in Canva."),
        ("3", "Make it yours", "Swap photos, text, colors, and prices."),
        ("4", "Send or print", "Share digitally or export to print — done."),
    ]
    cards = "".join(
        f'<div class="card"><div class="num">{n}</div><div class="ct"><b>{t}</b><span>{d}</span></div></div>'
        for n, t, d in steps)
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

    # ---- render all ------------------------------------------------------
    for f in [s1, s2, s3, s4, s5, s6]:
        png = out / f"{f.stem}.png"
        subprocess.run([
            CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", "--window-size=2000,2000",
            "--virtual-time-budget=12000", f"--screenshot={png}", f.resolve().as_uri(),
        ], check=True, capture_output=True)
        print(png.name)
    print("done ->", out)


def main():
    p = argparse.ArgumentParser(description="Etsy listing mockups (per listing)")
    p.add_argument("listing", type=int, choices=range(1, 7),
                   help="listing number 1-6 (selects CONFIGS + out/l{N}-final)")
    p.add_argument("--closeups", help="override the two close-up page numbers, e.g. 2,3")
    p.add_argument("--pages-dir", dest="pages_dir",
                   help="override the page-PNG source dir (default out/l{N}-final)")
    args = p.parse_args()

    override = None
    if args.closeups:
        parts = [int(x) for x in args.closeups.split(",")]
        if len(parts) != 2:
            sys.exit("--closeups needs exactly two page numbers, e.g. 2,3")
        override = parts

    build(args.listing, closeup_override=override, pages_dir=args.pages_dir)


if __name__ == "__main__":
    main()

"""Render buyer-delivery PDFs from a kit manifest.
Usage: py build_delivery.py <slug> [<n>|bundle|all]   (default: all)
"""
import re
import sys
import subprocess
from pathlib import Path
from kitlib import load_kit, ROOT

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DELIV = ROOT / "templates" / "delivery"


def fill_single(template: str, *, listing_name: str, template_link: str,
                support_email: str, keep_legal: bool) -> str:
    html = (template.replace("[LISTING NAME]", listing_name)
                    .replace("[TEMPLATE LINK]", template_link)
                    .replace("[SUPPORT EMAIL]", support_email))
    if not keep_legal:
        html = re.sub(r'\s*<div class="legal">.*?</div>', "", html, flags=re.S)
    return html


def build_link_list(listings: list[dict]) -> str:
    rows = []
    for L in listings:
        rows.append(
            f'<div class="lk"><div class="num">{L["n"]}</div>'
            f'<div class="body"><div class="name">{L["name"]}</div>'
            f'<a class="url" href="{L["template_link"]}">{L["template_link"]}</a>'
            f'</div></div>')
    return "\n".join(rows)


def fill_bundle(template: str, *, name: str, link_list_html: str,
                support_email: str) -> str:
    return (template.replace("[BUNDLE NAME]", name)
                    .replace("[LINK LIST]", link_list_html)
                    .replace("[SUPPORT EMAIL]", support_email))


def _render_pdf(html: str, name: str) -> Path:
    out_dir = ROOT / "out" / name
    out_dir.mkdir(parents=True, exist_ok=True)
    src = out_dir / "index.html"
    src.write_text(html, encoding="utf-8")
    pdf = out_dir / f"{name}.pdf"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=10000", f"--print-to-pdf={pdf}",
                    src.resolve().as_uri()], check=True, capture_output=True)
    print(pdf)
    return pdf


def build_listing(kit: dict, L: dict) -> None:
    tpl = (DELIV / "index.html").read_text(encoding="utf-8")
    html = fill_single(tpl, listing_name=L["name"], template_link=L["template_link"],
                       support_email=kit["support_email"], keep_legal=L["keep_legal"])
    _render_pdf(html, f"delivery-listing-{L['n']}")


def build_bundle(kit: dict) -> None:
    tpl = (DELIV / "bundle.html").read_text(encoding="utf-8")
    html = fill_bundle(tpl, name=kit["bundle"]["name"],
                       link_list_html=build_link_list(kit["listings"]),
                       support_email=kit["support_email"])
    _render_pdf(html, "delivery-bundle")


def main() -> None:
    slug = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else "all"
    kit = load_kit(slug)
    if target == "bundle":
        build_bundle(kit); return
    if target == "all":
        for L in kit["listings"]:
            build_listing(kit, L)
        build_bundle(kit); return
    L = next(l for l in kit["listings"] if l["n"] == int(target))
    build_listing(kit, L)


if __name__ == "__main__":
    main()

"""Emit paste-ready Etsy copy blocks + etsy-cli spec JSON from a kit manifest.
Usage: py emit_copy.py <slug> [--specs-dir out/specs]
"""
import sys
import json
import argparse
from kitlib import load_kit, ROOT

AI_LINE = "Designed by me using AI tools based on my own creative direction."

OPTIONS = ("Type: Digital > Download · Who made it: I did · What: finished product · "
           "When: 2020-2026 · Category: Craft Supplies & Tools > Templates · "
           "Renewal: Automatic · Qty: 999 · tick the 'Made with AI' attribute · Save as DRAFT")


def _description_with_ai(desc: str) -> str:
    return f"{desc}\n\n★ A NOTE ON DESIGN\n{AI_LINE}"


def emit_block(item: dict, kind: str) -> str:
    label = item["name"] if kind == "listing" else item["name"] + " (BUNDLE)"
    tags = ", ".join(item["tags"])
    return (f"## {label}  ·  ${item['price']:.2f}\n\n"
            f"**Options:** {OPTIONS}\n\n"
            f"**Title:**\n```\n{item['title']}\n```\n\n"
            f"**Description:**\n```\n{_description_with_ai(item['description'])}\n```\n\n"
            f"**Tags (13):**\n```\n{tags}\n```\n\n"
            f"**Materials:**\n```\n{item['materials']}\n```\n")


def emit_spec(item: dict, kit: dict, *, images: list[str], digital_file: str) -> dict:
    return {
        "title": item["title"],
        "description": _description_with_ai(item["description"]),
        "price": item["price"],
        "taxonomy_id": kit["taxonomy_id"],
        "tags": item["tags"],
        "materials": [m.strip() for m in item["materials"].split(",")],
        "quantity": 999,
        "who_made": "i_did",
        "when_made": "2020_2025",
        "type": "download",
        "images": images,
        "digital_file": digital_file,
    }


def _paths_for(n_or_bundle) -> tuple[list[str], str]:
    label = "l7" if n_or_bundle == "bundle" else f"l{n_or_bundle}"
    mock = ROOT / "out" / "mockups" / label
    images = [str(mock / f"img-{i}-{s}.png") for i, s in
              enumerate(("cover", "grid", "feature", "feature", "canva", "how"), 1)]
    pdf_name = "delivery-bundle" if n_or_bundle == "bundle" else f"delivery-listing-{n_or_bundle}"
    digital = str(ROOT / "out" / pdf_name / f"{pdf_name}.pdf")
    return images, digital


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("slug")
    p.add_argument("--specs-dir", default="out/specs")
    args = p.parse_args()
    kit = load_kit(args.slug)
    specs_dir = ROOT / args.specs_dir
    specs_dir.mkdir(parents=True, exist_ok=True)

    for L in kit["listings"]:
        print(emit_block(L, "listing"))
        imgs, dfile = _paths_for(L["n"])
        (specs_dir / f"listing-{L['n']}.json").write_text(
            json.dumps(emit_spec(L, kit, images=imgs, digital_file=dfile), indent=2),
            encoding="utf-8")
    print(emit_block(kit["bundle"], "bundle"))
    imgs, dfile = _paths_for("bundle")
    (specs_dir / "bundle.json").write_text(
        json.dumps(emit_spec(kit["bundle"], kit, images=imgs, digital_file=dfile), indent=2),
        encoding="utf-8")
    print(f"\n[specs written to {specs_dir}]", file=sys.stderr)


if __name__ == "__main__":
    main()

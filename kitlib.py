"""Load and validate per-kit manifests (kits/<slug>/kit.json)."""
import json
from pathlib import Path

ROOT = Path(__file__).parent

_LISTING_KEYS = ("n", "name", "canva_design_id", "template_link", "price",
                 "pages", "keep_legal", "title", "description", "tags",
                 "materials", "mockup")
_TOP_KEYS = ("slug", "shop", "support_email", "brand", "listings", "bundle")


def _check_tags(tags, where):
    if len(tags) != 13:
        raise ValueError(f"{where}: must have 13 tags, has {len(tags)}")
    for t in tags:
        if len(t) > 20:
            raise ValueError(f"{where}: tag over 20 chars: {t!r}")


def validate_kit(kit: dict) -> None:
    for key in _TOP_KEYS:
        if key not in kit:
            raise ValueError(f"kit manifest missing '{key}'")
    for L in kit["listings"]:
        where = f"listing {L.get('n', '?')}"
        for key in _LISTING_KEYS:
            if key not in L:
                raise ValueError(f"{where} missing '{key}'")
        _check_tags(L["tags"], where)
    b = kit["bundle"]
    for key in ("name", "price", "title", "description", "tags", "materials", "mockup"):
        if key not in b:
            raise ValueError(f"bundle missing '{key}'")
    _check_tags(b["tags"], "bundle")


def load_kit(slug: str) -> dict:
    path = ROOT / "kits" / slug / "kit.json"
    if not path.exists():
        raise FileNotFoundError(f"kit manifest not found: {path}")
    kit = json.loads(path.read_text(encoding="utf-8"))
    validate_kit(kit)
    return kit


def list_kits() -> list[str]:
    kdir = ROOT / "kits"
    if not kdir.exists():
        return []
    return sorted(p.name for p in kdir.iterdir() if (p / "kit.json").exists())

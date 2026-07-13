import json, pytest
from pathlib import Path
import kitlib

def _minimal_listing(n=1, **over):
    base = dict(n=n, name="X", canva_design_id="DXXXXXXXXXX",
                template_link="https://canva.link/abc", price=10, pages=5,
                keep_legal=False, title="t", description="d",
                tags=[f"tag{i}" for i in range(13)],
                materials="Canva template", mockup={})
    base.update(over); return base

def _minimal_kit(**over):
    base = dict(slug="k", shop="S", support_email="e@x.co", brand={},
                taxonomy_id=None, listings=[_minimal_listing()],
                bundle=dict(name="B", price=20, title="t", description="d",
                            tags=[f"tag{i}" for i in range(13)],
                            materials="m", mockup={}))
    base.update(over); return base

def test_validate_ok():
    kitlib.validate_kit(_minimal_kit())  # no raise

def test_validate_missing_top_key():
    k = _minimal_kit(); del k["listings"]
    with pytest.raises(ValueError, match="listings"):
        kitlib.validate_kit(k)

def test_validate_tag_count():
    k = _minimal_kit(listings=[_minimal_listing(tags=["a", "b"])])
    with pytest.raises(ValueError, match="13 tags"):
        kitlib.validate_kit(k)

def test_validate_tag_length():
    long = "x" * 21
    k = _minimal_kit(listings=[_minimal_listing(tags=[long] + [f"t{i}" for i in range(12)])])
    with pytest.raises(ValueError, match="over 20"):
        kitlib.validate_kit(k)

def test_load_and_list(tmp_path, monkeypatch):
    monkeypatch.setattr(kitlib, "ROOT", tmp_path)
    d = tmp_path / "kits" / "demo"; d.mkdir(parents=True)
    (d / "kit.json").write_text(json.dumps(_minimal_kit(slug="demo")), encoding="utf-8")
    assert kitlib.list_kits() == ["demo"]
    assert kitlib.load_kit("demo")["slug"] == "demo"

def test_load_missing():
    with pytest.raises(FileNotFoundError):
        kitlib.load_kit("nope-not-here")

def test_photographer_family_manifest_valid():
    kit = kitlib.load_kit("photographer-family")   # raises if invalid
    assert len(kit["listings"]) == 6
    assert kit["bundle"]["price"] == 72
    l3 = next(l for l in kit["listings"] if l["n"] == 3)
    assert l3["keep_legal"] is True
    assert all(l["template_link"].startswith("https://canva.link/") for l in kit["listings"])

import build_mockups as bm

KIT = {
    "brand": {"ivory": "#F7F3EE"},
    "listings": [{"n": 2, "pages": 5,
                  "mockup": {"cover_sub": "SUB", "grid": ["a", "b", "c"],
                             "closeups": [{"page": 2}, {"page": 3}], "thumbs": [2, 3, 4]}}],
    "bundle": {"name": "Complete Kit",
               "mockup": {"cover_sub": "BUN", "grid": ["x", "y", "z"],
                          "closeups": [{"page": 1}, {"page": 6}], "thumbs": [1, 3, 5]}},
}

def test_resolve_listing():
    cfg, pages = bm.resolve_mockup(KIT, "2")
    assert pages == 5 and cfg["cover_sub"] == "SUB"

def test_resolve_bundle_has_six_pages():
    cfg, pages = bm.resolve_mockup(KIT, "bundle")
    assert pages == 6 and cfg["cover_sub"] == "BUN"

def test_montage_html_references_all_covers():
    uris = [f"file:///c/x/l{i}.png" for i in range(1, 7)]
    html = bm.montage_html(KIT, uris)
    for u in uris:
        assert u in html
    assert "Complete" in html
    assert "<em>Kit</em>" in html

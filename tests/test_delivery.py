import build_delivery as bd

SINGLE = '<h1>Your <em>[LISTING NAME]</em></h1><a href="[TEMPLATE LINK]">go</a>' \
         '<span>[SUPPORT EMAIL]</span>' \
         '<div class="legal">not legal advice</div><div class="foot">x</div>'

def test_fill_single_replaces_tokens():
    out = bd.fill_single(SINGLE, listing_name="Pricing Guide",
                         template_link="https://canva.link/abc",
                         support_email="e@x.co", keep_legal=True)
    assert "[LISTING NAME]" not in out and "Pricing Guide" in out
    assert "https://canva.link/abc" in out and "e@x.co" in out
    assert 'class="legal"' in out

def test_fill_single_strips_legal_when_false():
    out = bd.fill_single(SINGLE, listing_name="X", template_link="L",
                         support_email="e", keep_legal=False)
    assert 'class="legal"' not in out
    assert 'class="foot"' in out          # only the legal block removed

def test_build_link_list_has_all_rows():
    listings = [{"n": 1, "name": "Welcome", "template_link": "https://canva.link/a"},
                {"n": 2, "name": "Pricing", "template_link": "https://canva.link/b"}]
    html = bd.build_link_list(listings)
    assert html.count('class="lk"') == 2
    assert "https://canva.link/a" in html and "Pricing" in html

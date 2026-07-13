import emit_copy as ec

ITEM = {"n": 2, "name": "Pricing", "title": "T", "description": "Body text.",
        "tags": [f"tag{i}" for i in range(13)],
        "materials": "Canva template, PDF, US Letter", "price": 18}
KIT = {"taxonomy_id": 1234}

def test_block_injects_ai_line():
    block = ec.emit_block(ITEM, "listing")
    assert ec.AI_LINE in block
    assert "T" in block and "tag0" in block

def test_spec_shape_and_materials_split():
    spec = ec.emit_spec(ITEM, KIT, images=["a.png", "b.png"], digital_file="d.pdf")
    assert spec["title"] == "T" and spec["price"] == 18
    assert spec["type"] == "download" and spec["who_made"] == "i_did"
    assert spec["taxonomy_id"] == 1234
    assert spec["materials"] == ["Canva template", "PDF", "US Letter"]
    assert spec["images"] == ["a.png", "b.png"] and spec["digital_file"] == "d.pdf"
    assert ec.AI_LINE in spec["description"]

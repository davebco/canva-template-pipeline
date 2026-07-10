# canva-template-pipeline

Automation pipeline for the Etsy Canva-templates venture (metadata: `C:\Claude\Business\etsy-canva-templates\`).
Claude designs each listing as brand-styled HTML; this repo renders it for review and prepares it for import into Canva as an editable multi-page design.

## The workflow (Model A, automated)

1. **Copy deck** — listing content written/generated per `docs/content-package-*.md` in the Business folder (Canva MCP `generate-design` is a usable copy generator; its visual output is not used).
2. **HTML master** — Claude builds `templates/<listing>/index.html`: fixed 816×1056px (US Letter) pages, brand tokens, free-Canva-font families only (Cormorant Garamond + Lato). Every page element carries `data-document-role="page"` + `data-label` so Canva's import treats it as a paged design.
3. **Render for review** — `py build.py <listing>` → `out/<listing>/<listing>.pdf` + per-page PNGs (headless Chrome + pypdfium2). Dave approves the design here.
4. **Import into Canva** — host the approved HTML at a public HTTPS URL, then Canva MCP `import-design-from-url` converts it into an editable multi-page Canva design (text → real text boxes; fonts map because both families exist in Canva's free library). *Gate: the file must be public before import — confirm hosting with Dave.*
5. **Finish in Canva (manual, small)** — verify font/layout fidelity, swap placeholder rects for Canva photo frames, then share as a **template link** for Etsy delivery.

## Import-safe HTML rules

- Solid fills and 1px borders only — no gradients, shadows, pseudo-element content, or JS.
- Fonts referenced by family name; both must exist in Canva's free font library.
- One top-level element per page, never nested; fixed pixel dimensions (816×1056 = US Letter @96dpi).
- Placeholder images = flat `--sand` rects with a small-caps label the buyer replaces.

## Brand tokens (photographer kit, locked)

ivory `#F7F3EE` · charcoal `#3E3A34` · terracotta `#C0876B` · sand `#EAE3D9` (placeholders) · taupe `#A39A8D` (utility)
Cormorant Garamond (display) + Lato (body).

## Layout

- `templates/<listing>/index.html` — one folder per listing, self-contained.
- `build.py` — HTML → PDF → PNGs. Chrome path is hardcoded for this machine.
- `out/` — renders (gitignored).

# Navigation behavior comparison

Source: `drtforshortaol/MBA-nearby-dining/app.js` (main, inspected 2026-11-14).

Dining `nav(m,id)` maintains its own `navHistory` of view states; `back()` restores prior view, handles lightbox, and falls back to explore; `home()` returns to **Dining app explore**, not the Hub. Its HTML labels `navHome` as `Return to Hub`, so the actual handler must be checked before reuse. This is a concrete reason not to copy labels or handlers blindly.

RCL prototype intentionally uses browser history for same-origin back and an explicit configurable Hub destination. Before publishing, verify the destination and define consistent semantics for app-home vs Hub-home.

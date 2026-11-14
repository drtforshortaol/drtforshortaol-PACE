# RCL — Reusable Component Library

Purpose: assemble a **reviewable working prototype first**, then refine and complete it without rebuilding.

Workflow: Prototype → Owner Review → Refine → Complete → Validate → Publish.

## Initial component contract
- `AppShell`: title, version, content slot.
- `HubNavigation`: Back and Return to Hub with explicit safe fallback.
- `ContentCard`: reusable expandable content.
- `Search`: local text filtering.

## Safety
- Do not alter MBA Hub V1 or production apps.
- Version components; bundle dependencies for offline operation.
- Extract only after comparing working implementations and their licenses.
- No production merge or deployment without owner approval.

## Next milestone
Inspect MBA Hub V2, El Niño, and Nearby Dining sources; extract a minimal template into this branch; demonstrate a working first-review prototype before adding optional features.

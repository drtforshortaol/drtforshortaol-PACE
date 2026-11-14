# RCL component contract v0.1

## Navigation
- `back`: return to previous in-app view if available; otherwise configured Hub destination.
- `appHome`: optional return to the current app root; distinct from Hub.
- `returnToHub`: always navigate to configured Hub URL.

## Cards
- Input `{title,body}` plain text. Render via textContent, native details/summary.

## Search
- Input string; case-insensitive filter over card title and body; empty state shown.

## Source provenance
- MBA Hub V2 README/package.json and Nearby Dining index.html/app.js examined on default branches.
- This contract is a proposed standard, **not yet a copied/extracted production implementation**.

## Gate
Compare Hub V2 actual renderer/nav source before claiming parity. Confirm target Hub URL and deployment environment before owner device review.

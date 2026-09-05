# Product Database Detail Cards — Design QA

## Evidence

- Source visual truth: `artifacts/design-qa/ups-product-database-source-v1.8.16.png` (1854 × 1118 px).
- Browser comparison fixture: `artifacts/design-qa/ups-product-detail-comparison.html`.
- Implementation capture: Codex in-app Browser at 1854 × 1118 CSS pixels, device scale factor 1, with the first product detail dialog open. The browser API exposed the capture inline during QA but did not expose a standalone PNG path.
- Focused states checked: dialog header and key metrics; Product Information cards; Technical Specifications (泰尔参数) cards after dialog scroll; close and keyboard reopen states.

## Comparison state

The source image is the pre-feature Product Database view. The implemented comparison opens the new detail view for `太行 UR-0010SPS`. Because no separate card mockup was supplied, the source is used as the visual-language reference rather than as a pixel-identical target.

## Findings

- Layout: passed. The overlay keeps the two existing tables visible as context and presents one centered, independently scrollable detail surface.
- Visual hierarchy: passed. Model and series lead, six common metrics provide a quick scan, and the complete data follows in two clearly separated sections.
- Visual consistency: passed. Product Information uses the existing navy/blue treatment; Technical Specifications uses the existing green treatment.
- Data completeness: passed. All non-empty values from the selected product and 泰尔 parameter records are rendered; the detail counts were 18 and 19 respectively for the checked model.
- Interaction: passed. Mouse click, Enter, and Space open the same-model detail; Escape, the close button, and backdrop click close it; focus returns to the invoking row; Tab remains inside the modal.
- Existing table behavior: passed. Text remains selectable, column-width dragging remains active, and Shift-drag horizontal panning does not accidentally open the detail dialog.
- Responsive behavior: passed. At the narrow in-app Browser viewport the grids reduce to two columns and remain readable without overflowing the dialog.
- Console: passed. No browser console errors were observed.

## Severity summary

- P0: none
- P1: none
- P2: none
- P3: none requiring remediation

## Final result

passed

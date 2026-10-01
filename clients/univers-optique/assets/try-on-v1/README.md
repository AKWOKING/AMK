# Univers Optique — five-frame 2D overlay asset proof

**Prepared:** 1 October 2026  
**Status:** proof for review; not production-ready and not an application implementation.

## What is included

- `frames/OU-001.png` through `frames/OU-005.png`: transparent PNG derivatives of the five selected front-facing photographs.
- `masks/OU-001.svg` through `masks/OU-005.svg`: reversible hand-authored silhouette masks used for this proof.
- `frame-manifest-2026-10-01.json`: source mapping, dimensions, provisional anchor points, cleanup status and limitations.
- `proof-sheet-2026-10-01.png`: white-background visual review sheet.
- `test/black-test.png`: the earlier experimental derivative; retained as a non-final comparison and not used as the five-frame output.

The original `clients/univers-optique/PXL_*.jpg` photographs were not modified.

## Preparation method

ImageMagick was used to resize each selected source to 1600 pixels wide, render a hand-authored front-frame mask, copy that mask into the PNG alpha channel, trim the transparent bounds and add 20 pixels of transparent padding. The lens interiors are intentionally transparent so the customer photo can show through in a later 2D overlay test. Visible labels, printed lens text and rear temples are excluded where they fall inside the masked areas.

## Important limitations

This is an **asset-preparation proof**, not a claim that these files are ready for a customer-facing pilot. Pale table/background shadows and some reflections remain around parts of several outer edges. The source photos also have small perspective differences. The provisional lens-centre coordinates in the manifest must be calibrated against a real frontal customer photo; they are not validated face-landmark data.

Before Phase 2B tool comparison, please review:

1. whether the five derivatives retain the frame designs well enough for the proof;
2. whether the remaining pale remnants need manual retouching;
3. the real stock-number, brand/model and availability mapping for each technical ID; and
4. whether the requirements draft still reflects the intended Version A catalogue and privacy behaviour.

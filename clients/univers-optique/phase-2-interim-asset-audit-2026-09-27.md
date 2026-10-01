# Univers Optique — interim asset audit
## Work completed while waiting for client answers

**Date:** 27 September 2026  
**Purpose:** Audit the frame photographs already available in the repository.  
**Important:** No new photographs are required before the first technical test.

---

## 1. What was audited

The folder `clients/univers-optique` currently contains:

- 9 original frame photographs.
- 1 existing try-on mockup image.
- The nine photographs are all high-resolution JPEGs at 4624 × 3472 pixels.
- The photographs were taken with a Google Pixel 8a on 25 September 2026.
- The photographs contain front, three-quarter and side/profile views.

The existing images are sufficient to begin preparing a first five-frame technical test. The original photographs should remain untouched; any cropped or transparent versions should be generated as separate derivative assets.

---

## 2. What the photographs provide

The current set appears to cover approximately six distinct frames:

- Thick black square frame.
- Black frame with visible side branding.
- Tortoiseshell/brown frame with gold details.
- Black frame with gold details.
- Purple patterned Prada frame.
- Thin pink/gold round frame.

The photographs also show the existing numbered/price labels. Those labels are useful for connecting a prepared digital asset to Univers Optique’s physical stock, although the exact numbers should be confirmed with the clinic before they become the application’s official stock IDs.

### Front-facing candidates

The following five files are the strongest candidates for the first try-on test because they show a front or near-front view:

| File | Candidate use | Preparation required |
|---|---|---|
| `PXL_20260925_095151347.jpg` | Thick black square frame | Crop, remove background, handle visible label/other frame behind it |
| `PXL_20260925_095249623.jpg` | Tortoiseshell/brown frame | Crop and clean background/reflections |
| `PXL_20260925_095352814.jpg` | Black frame with gold details | Crop and clean background/reflections |
| `PXL_20260925_095407691.jpg` | Purple patterned frame | Crop, remove background and avoid placing sticker/text over the lens area |
| `PXL_20260925_095445683.jpg` | Thin pink/gold round frame | Crop and check reflections/thin-edge quality |

These are candidate assets, not final selections. The clinic should confirm that the corresponding frames are still available before they are used in a customer-facing test.

### Profile/reference photographs

The side and three-quarter photographs are still valuable. They can be used for:

- Confirming the frame’s side details.
- Building a future catalogue view.
- Helping prepare a future semi-3D or 3D asset.
- Verifying that the front asset belongs to the correct physical frame.

They should not be used as the primary overlay image on a frontal customer photograph.

---

## 3. Current asset limitations

The images are sufficient for a proof of concept, but they are not all ready to be placed directly over a face.

Observed issues include:

- Other frames visible behind or beneath the selected frame.
- Green stock labels visible inside or behind the lens area.
- Reflections on lenses and thin metal edges.
- Background clutter in some images.
- Side/profile angles that cannot be directly overlaid on a frontal face.

These are preparation tasks for us. They are not a reason to ask the client to return to the shop before the first test.

If one particular frame cannot be prepared convincingly, we can temporarily exclude that frame or ask for a replacement photograph later. The first goal is to prove the workflow with the images already available.

---

## 4. Preparation plan

For the first five candidates, prepare separate derivative assets:

1. Preserve the original JPEG.
2. Crop tightly around the frame while keeping the entire frame visible.
3. Remove or mask the background.
4. Remove labels from the lens area where possible without altering the frame.
5. Export a transparent PNG or another browser-friendly transparent format.
6. Record the original stock number separately rather than embedding it in the overlay.
7. Create an initial default scale and position.
8. Validate the asset against a test face.
9. Record whether manual correction is needed.

The frame image used for a face overlay should not contain visible prices or stock labels. Those values should live in catalogue metadata and be shown only where Univers approves.

---

## 5. Tools currently available in the repository environment

The environment already has enough basic tooling to begin asset preparation:

- ImageMagick `convert` and `identify` for image inspection, cropping and format conversion.
- Node.js and npm for a future browser prototype.
- No additional commercial SDK has been installed.
- No customer photograph is required for the asset-preparation step.

We should not install a commercial AR SDK or commit to a framework until the clinic confirms the device, network and privacy requirements.

---

## 6. What can be done now without client answers

The following work is safe and reversible:

- Prepare the five candidate frame assets locally.
- Create a frame manifest containing filenames, stock numbers, status and calibration values.
- Test whether the current photos can be cropped and made transparent.
- Identify which frame types are difficult for the overlay process.
- Prepare a technical test using a non-client test face or an approved internal image.
- Keep all original photographs and customer data separate.

The following should wait:

- Final database design.
- Offline synchronisation decisions.
- Staff authentication design.
- Commercial SDK purchase.
- Full catalogue onboarding.
- Customer-image storage or sharing.
- Production deployment.

---

## 7. Recommendation

We do not need to ask Dr. Bayang for more frame photographs before starting the first preparation step.

The most useful next action is to prepare the five candidate assets from the existing photographs and review their quality. This will tell us more about the real difficulty of the prototype than another general technology discussion.

After the asset-preparation result is reviewed, we can continue with the tool comparison and technical spike while waiting for the clinic’s answers.

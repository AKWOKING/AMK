# Univers Optique — virtual frame try-on prototype
## Phase 1: research and case study

**Date:** 27 September 2026  
**Status:** Ready for review  
**Scope of this document:** Research only. No product requirements have been finalised and no implementation should begin until this phase is reviewed.

---

## 1. Confirmed problem

Univers Optique described the following workflow:

1. A customer arrives looking for eyeglass frames.
2. Staff take a picture of the customer.
3. The customer swipes through pictures of themselves wearing the available frames one at a time.
4. The customer chooses a shortlist.
5. Staff bring out the physical frames for final fitting and purchase.

The business value is not simply that the experience looks modern. It should reduce:

- The number of physical frames handled during the initial search.
- The time spent taking frames from the display and returning them afterwards.
- The time required for a customer to find a few frames that suit them.

The folder `clients/univers-optique` contains sample frame photographs. The visible samples confirm that the shop already uses numbered labels and price tags. Those numbers can probably serve as the internal stock IDs, subject to confirmation from the shop.

The stock appears to contain more than 50 frames. That makes the catalogue and asset-preparation workflow as important as the face overlay itself.

---

## 2. The closest existing products

### 2.1 Fittingbox Standard for In-Store — closest business analogue

Fittingbox explicitly offers an in-store product for opticians. Its stated workflow includes a frame catalogue, a management interface, frame descriptions and prices, multiple frame renderings, live and photo try-on, filters, search, and a wishlist. It is designed to let customers explore frames while staff assist other customers. It supports PC, tablet and phone-style browser environments.

This is the closest analogue to the Univers Optique idea because it is not merely an online shopping widget. It combines:

- A private frame catalogue.
- Frame availability and merchandising.
- Customer photo/live try-on.
- Shortlisting and comparison.
- In-store staff assistance.

**Lesson for Univers:** the product should be designed as a small optical-store workflow tool, not as a public website and not as a generic camera filter.

Source: [Fittingbox Standard for In-Store](https://fittingbox.com/en/glasses-virtual-try-on/standard-instore)

### 2.2 Cosium + Visage — point-of-sale workflow

Cosium is optical practice and retail software. Its virtual try-on uses face tracking and is intended for both web and point-of-sale systems. The case study specifically describes using the experience in-store so customers can explore frames that may not be physically available at that location. It also states that customers do not need to take glasses from the racks for every virtual try-on.

The system uses a standard camera, facial tracking and frame positioning based on interpupillary distance. The customer still benefits from professional staff and physical fitting after making a selection.

**Lesson for Univers:** the software should accelerate selection, not replace the optician. The final physical fitting remains essential.

Source: [Cosium virtual eyewear try-on case study](https://visagetechnologies.com/case-studies/cosium/)

### 2.3 ZEISS Virtual Try-On — optician-curated catalogue

ZEISS takes a more advanced approach. The customer’s digital avatar is created in the optician’s store, where the customer can try virtual frames selected by that optician. The customer can then continue the experience at home. ZEISS describes the benefit as expanding the range of frames available virtually without keeping every frame physically in the store, while still allowing the optician to perform final lens centering and adjustments.

**Lesson for Univers:** the catalogue should remain controlled by the clinic. A customer should see Univers Optique’s available collection, not a huge generic database. The tool should lead to a staff-assisted final selection.

Source: [ZEISS Virtual Try-On](https://www.zeiss.com/vision-care/en/newsroom/news/articles-and-stories/virtual-try-on-of-glasses.html)

### 2.4 Zenni Optical — live try-on plus photo fallback

Zenni provides both live camera try-on and photo upload. It asks users to enter pupillary distance or use a card as a reference to improve scale. It also allows customers to save or share favourite looks. Zenni explicitly warns that virtual try-on is useful for style and scale but that users should still check frame measurements for fit.

**Lesson for Univers:**

- A captured customer photo is a valid first experience.
- A live camera mode can come later.
- A shortlist/favourites function is useful.
- The interface must clearly say that virtual appearance is not a guarantee of physical comfort or final optical fit.

Source: [Zenni Virtual Try-On help page](https://www.zennioptical.com/help/frames-fitting/virtual-try-on)

### 2.5 Warby Parker — polished consumer experience and privacy model

Warby Parker offers virtual try-on through its web and mobile experiences. Its current product page describes trying frames on a face and calculating a suitable frame width. Its privacy policy says that facial scans and measurements for virtual try-on are processed while the feature is being used and are not stored or shared with third parties for that feature.

The older implementation history is useful because Warby Parker originally used Apple face-mapping and ARKit on supported iPhones. It faced technical difficulties with a simpler web experience and had to improve alignment, scale and stability.

**Lesson for Univers:** even large eyewear companies treat accurate frame alignment and scale as difficult. We should start with a constrained, frontal, photo-based experience instead of promising full 3D realism.

Sources:

- [Warby Parker mobile apps](https://www.warbyparker.com/ios-app)
- [Warby Parker privacy policy](https://www.warbyparker.com/privacy-policy)
- [Warby Parker AR implementation history](https://www.theverge.com/2019/2/4/18205654/warby-parker-ar-iphone-face-id-mapping-glasses-try-on-app)

### 2.6 Walmart Optical Virtual Try-On — enterprise-scale reference

Walmart describes an eyewear try-on system using 3D data and digital twins of frames. Its launch included more than 750 frame options, facial scanning, pupillary-distance measurement and prescription customisation.

This demonstrates the upper end of the market, but it is not an appropriate starting point for Univers Optique. It requires a large catalogue, advanced assets, prescription workflows and broader e-commerce integration.

**Lesson for Univers:** do not copy the feature count of a large retailer. Copy the useful principle: make the frame catalogue and availability accurate, then add advanced fit features only when the basic workflow proves valuable.

Source: [Walmart Optical Virtual Try-On](https://corporate.walmart.com/news/2024/01/30/walmarts-augmented-reality-optical-try-on-lets-customer-visualize-customize-fits)

---

## 3. How similar systems are built

The research shows that a production eyewear try-on system has several separate layers.

### Layer A — camera and session

The application must either:

- Open the device camera and capture a live stream or still image; or
- Allow staff to upload/take a customer photograph.

A browser can request camera access through `getUserMedia`, but this requires HTTPS and explicit user permission. The app must handle permission denial, missing cameras and unsupported devices gracefully.

Source: [MDN getUserMedia documentation](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)

### Layer B — face landmarks and alignment

The system detects facial reference points such as the eyes, nose bridge and face contour. Google’s MediaPipe Face Landmarker for Web can process still images or video and return 3D landmarks, optional blendshapes and facial transformation matrices. Those outputs are intended for effects rendering and object placement.

For a frontal photo-based prototype, we probably need only:

- Left and right eye reference points.
- Nose bridge position.
- Eye distance or face width.
- Head tilt.
- A confidence check that the face is sufficiently frontal and visible.

The application should reject or retake photos that are too dark, too far away, strongly turned sideways or obstructed.

Sources:

- [Google MediaPipe Face Landmarker for Web](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker/web_js)
- [MediaPipe Face Mesh reference](https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/face_mesh.md)

### Layer C — digital frame assets

The system cannot work well with arbitrary frame photographs alone. Each frame needs a digital asset that can be positioned over the face.

Commercial asset pipelines vary:

- Fittingbox describes generating a basic 3D frame from a front and side photograph, then reviewing and validating the result.
- Banuba describes an eyewear workflow using multiple frame views, SKU matching and an admin catalogue.
- Higher-quality systems use actual 3D models, accurate dimensions, materials, lens rendering and occlusion.

Fittingbox also warns that thin or rimless frames, strong reflections, shadows and poor source images reduce the quality of automatic digitisation.

This confirms that the Univers sample photos are useful for inventory reference, but each frame may need a consistent capture process before it becomes try-on-ready.

Sources:

- [Fittingbox 3D from Photo](https://fittingbox.com/en/digital-frames/3d-digitization/3d-from-photo)
- [Banuba: How to build a virtual try-on plugin](https://www.banuba.com/blog/how-to-build-virtual-try-on-plugin)

### Layer D — rendering

There are three practical levels:

#### 1. 2D frontal overlay

A transparent frame image is scaled and positioned over a still customer photo.

- Fastest to prototype.
- Lowest asset-production cost.
- Good for a frontal customer photo and swipe interaction.
- Weak when the head turns.
- Does not provide reliable physical fit information.

#### 2. Live 2D or semi-3D overlay

The system tracks the face continuously and moves the frame as the customer moves.

- More engaging.
- Works with a browser camera.
- Still depends heavily on clean, calibrated frame assets.
- Side views and temple occlusion remain limited.

#### 3. Full 3D AR

A 3D frame model is rendered with head pose, depth, materials, reflections and occlusion.

- Most realistic.
- Better for head movement and size.
- Requires a 3D asset or digitisation pipeline for every frame.
- More expensive and difficult to QA.

The commercial products in this research use level 2 or level 3. The customer’s stated requirement only requires level 1 to prove the business idea.

### Layer E — catalogue and stock status

The try-on engine is only useful if it reflects the actual collection. The catalogue needs:

- Internal stock number/SKU.
- Optional brand and model.
- Price, if the clinic wants it visible.
- Front asset.
- Optional side/profile asset.
- Available, reserved, sold or hidden status.
- Optional location/display position.

A sold frame should normally be deactivated rather than permanently erased. That keeps history and allows the frame to be restored if the status was changed by mistake.

### Layer F — customer shortlist and staff handoff

The strongest repeated pattern in the products researched is not just “try on.” It is:

1. Try many options digitally.
2. Save or compare a few favourites.
3. Bring only those physical frames into the final fitting.
4. Complete the purchase with professional assistance.

That is the correct workflow for Univers Optique.

---

## 4. Build versus buy

### Buy an existing platform

Products such as Fittingbox, Banuba, Camweara and similar services can provide a mature face-tracking or try-on engine. This can reduce computer-vision development, but it introduces questions about:

- Subscription or usage cost.
- Whether their frame asset format accepts Univers’s photographs.
- Whether their system supports a private in-store catalogue.
- Whether stock status can be controlled by Univers staff.
- Whether customer images remain on the device or leave Cameroon.
- Whether the service works reliably on the clinic’s connection and devices.
- Whether the vendor’s UI can be adapted to the clinic workflow.

A commercial service may be useful later if Univers needs high-quality live 3D try-on. It is not automatically the best choice for a five-frame prototype.

### Build a focused custom prototype

A custom prototype can be much smaller than a commercial product. It could use:

- A responsive web/PWA interface.
- Browser camera access or photo upload.
- A client-side face-landmark model.
- Canvas/WebGL compositing.
- A small local/server catalogue.
- Session-only customer images.

This approach lets us test the business workflow before paying for a commercial SDK or digitising the entire inventory.

### Research conclusion on this choice

For the first prototype, a custom photo-based overlay is the most sensible route. It is not because commercial tools are poor; it is because we first need to establish whether the clinic actually saves time when customers shortlist frames digitally.

If the prototype succeeds but the overlay is not realistic enough, we can then evaluate a commercial SDK against real Univers frame photos and real clinic devices.

---

## 5. Privacy and security findings

Virtual try-on products demonstrate two privacy patterns:

- Process the face image locally in the browser and do not upload it.
- If processing outside the device is necessary, make retention, consent and deletion explicit.

Fittingbox says its try-on image is processed live in the browser and is not stored. Zenni says try-on photos and videos are stored locally in the browser cache rather than uploaded. Warby Parker describes virtual try-on facial data as processed only while the feature is in use for that feature.

For Univers, the safest prototype policy is:

- Staff explains the purpose before taking the photo.
- No customer account is required.
- No facial recognition or identity matching is used.
- The photo is processed only for the current session.
- The customer image is deleted when the session ends, with an automatic maximum retention fallback of 24 hours.
- Saved favourites contain frame IDs, not the customer’s face image.
- The system does not send the face photo to an AI image-generation API.
- The clinic can manually delete a session.

Cameroon’s Law No. 2024/017 relates to personal-data protection and includes photographs within personal data; legal summaries also identify biometric and health-related information as sensitive categories. Before production deployment, the clinic should receive appropriate local legal guidance. This report is not a legal opinion.

Sources:

- [Fittingbox data-processing terms](https://fittingbox.com/en/resources/help-center/terms)
- [Zenni Virtual Try-On privacy section](https://www.zennioptical.com/help/frames-fitting/virtual-try-on)
- [Warby Parker privacy policy](https://www.warbyparker.com/privacy-policy)
- [African Law & Business summary of Cameroon Law No. 2024/017](https://www.africanlawbusiness.com/expert-views/key-features-of-cameroons-new-data-protection-law/)

---

## 6. What the case studies teach us

### Finding 1 — The closest product is an in-store digital mirror, not an e-commerce website

Univers’s need is closest to Fittingbox Standard In-Store and Cosium’s point-of-sale workflow. The app should be private, staff-assisted and catalogue-driven.

### Finding 2 — Catalogue quality is as important as face tracking

A beautiful face-tracking demo will fail if frames are badly photographed, incorrectly scaled or unavailable in the shop. The frame onboarding process must be treated as a product feature.

### Finding 3 — Virtual try-on is a shortlist tool, not a final fit guarantee

Customers should still physically test their final choices. The app helps narrow 50-plus frames to a manageable shortlist; it does not replace optical measurements, comfort checks, adjustment or professional advice.

### Finding 4 — Availability must be built into the try-on screen

A frame marked sold or unavailable must disappear from the customer experience immediately. The clinic should not need to edit code or delete files to update stock.

### Finding 5 — Start with a narrow catalogue and measure the operational result

Commercial vendors advise launching with part of the catalogue, measuring usage and business impact, then scaling. For Univers, five real frames are enough for a technical and workflow pilot.

### Finding 6 — Simplicity matters more than a long feature list

The first experience should be:

> Take one photo → swipe through available frames → save favourites → bring out only the favourites.

Filters, face-shape recommendations, 3D rotation, online sharing, customer accounts, prescription simulation and analytics should not delay that test.

---

## 7. Research-derived prototype hypothesis

This is a proposal for review, not an approved requirements document.

> **A tablet-first private web application that lets Univers Optique staff photograph a customer, preview a small catalogue of available frames on the customer’s face, swipe through the options, save a shortlist, and automatically delete the customer image after the session.**

### Proposed first technical level

- Frontal still photograph.
- 2D transparent frame overlays.
- Face landmark detection for scale and positioning.
- Five real Univers frames.
- Numbered frame IDs.
- Available/unavailable toggle.
- Favourites/shortlist.
- Session-only customer image.
- Responsive web interface.

### Deliberately not included in the first prototype

- Full 3D frame modelling.
- Live head-turn tracking.
- Prescription-lens simulation.
- Pupillary-distance measurement for lens fabrication.
- Face-shape recommendations.
- Customer accounts.
- Public website or e-commerce checkout.
- Social sharing.
- Automatic machine-learning style recommendations.
- Full 50-plus-frame catalogue onboarding.

---

## 8. Risks and unanswered questions carried into Phase 2

These should be resolved during requirements and tool selection, not guessed during coding:

1. Which device will be used first: Android phone, tablet, laptop or desktop with webcam?
2. Is internet reliable inside the clinic?
3. Should the first version work fully offline after the catalogue is downloaded?
4. Are the frame numbers unique and stable enough to use as stock IDs?
5. Does Univers want prices visible to customers, visible only to staff, or omitted?
6. Can the clinic provide five clean, front-facing frame photographs for the initial test?
7. Should the customer photo be captured by staff or uploaded from the device gallery?
8. What happens if the face is not frontal or the camera cannot detect it?
9. Who is allowed to add, deactivate or reactivate frames?
10. What baseline measurements will Univers provide for the ROI test?

---

## 9. Phase 1 decision requested

Before moving to requirements, tools or implementation, please review and confirm whether we agree with these conclusions:

1. The closest reference product is an **in-store digital mirror/catalogue**, not a public website.
2. The first prototype should be **tablet-first but browser-based**.
3. The first rendering approach should be **photo-based 2D overlay**, not full 3D AR or generative AI.
4. We should test with **five real Univers frames** before processing the entire stock.
5. The customer photo should be **session-only and automatically deleted**.
6. The prototype should shorten the process to a **digital shortlist followed by final physical fitting**.
7. We should not promise ROI until we measure the current process and the pilot process.

If these conclusions are approved, Phase 2 will be a separate document covering the confirmed requirements, device/network assumptions, technology options and prototype acceptance criteria. No implementation should begin before that review.

---

## Research sources

- [Fittingbox Standard for In-Store](https://fittingbox.com/en/glasses-virtual-try-on/standard-instore)
- [Fittingbox: How 3D glasses simulators work](https://fittingbox.com/en/resources/blog/how-3d-glasses-simulators-work-the-technology-behind-virtual-try-on)
- [Fittingbox: 3D from Photo](https://fittingbox.com/en/digital-frames/3d-digitization/3d-from-photo)
- [Fittingbox: Virtual Try-On data terms](https://fittingbox.com/en/resources/help-center/terms)
- [Cosium case study by Visage Technologies](https://visagetechnologies.com/case-studies/cosium/)
- [ZEISS Virtual Try-On](https://www.zeiss.com/vision-care/en/newsroom/news/articles-and-stories/virtual-try-on-of-glasses.html)
- [Zenni Virtual Try-On help](https://www.zennioptical.com/help/frames-fitting/virtual-try-on)
- [Warby Parker mobile apps](https://www.warbyparker.com/ios-app)
- [Warby Parker privacy policy](https://www.warbyparker.com/privacy-policy)
- [Walmart Optical Virtual Try-On](https://corporate.walmart.com/news/2024/01/30/walmarts-augmented-reality-optical-try-on-lets-customer-visualize-customize-fits)
- [Banuba: How to build a virtual try-on plugin](https://www.banuba.com/blog/how-to-build-virtual-try-on-plugin)
- [Google MediaPipe Face Landmarker for Web](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker/web_js)
- [MDN: getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)
- [African Law & Business: Cameroon Law No. 2024/017](https://www.africanlawbusiness.com/expert-views/key-features-of-cameroons-new-data-protection-law/)

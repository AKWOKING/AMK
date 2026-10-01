# Univers Optique — research addendum
## Warby Parker Virtual Try-On and Webkul video

**Date:** 27 September 2026  
**Phase:** Phase 1 research  
**Status:** For review only — no implementation changes

---

## 1. Sources reviewed

### Warby Parker

- [Warby Parker mobile apps](https://www.warbyparker.com/ios-app)
- [Warby Parker Advisor](https://www.warbyparker.com/advisor)
- [Warby Parker privacy policy](https://www.warbyparker.com/privacy-policy)
- [Warby Parker 2019 Impact Report](https://img.warbyparker.com/PDF/impact-report/Impact-Report-2019.pdf)
- [Wired report on Warby Parker’s AR app](https://www.wired.com/story/warby-parker-augmented-reality-app/)
- [Retail Dive report on the launch](https://www.retaildive.com/news/warby-parker-launches-ar-tool-for-virtual-try-on/547673/)

### Webkul video and supporting documentation

- [Video: Virtual Try On Eyewear Software](https://youtu.be/Pg-uoq45uyk?si=oW3KE7TfKuq-p8_A)
- [Webkul Magento 2 Virtual Try-On product page](https://store.webkul.com/magento2-virtual-try-on.html)
- [Webkul TensorFlow Virtual Try-On documentation](https://webkul.com/blog/magento2-tensor-flow-virtual-try-on/)
- [Webkul PrestaShop Virtual Try-On guide](https://webkul.com/blog/prestashop-virtual-try-on/)
- [Webkul eyewear try-on services](https://webkul.com/sunglasses-virtual-tryon-services/)

The video is a public Webkul video titled **“Virtual Try On Eyewear Software | Online Glasses Try-On for E-Commerce.”** It is approximately 2 minutes and 19 seconds long. The description says the solution uses TensorFlow, Three.js and Blender. The demonstration shows a user selecting different frames, moving their face while the frame follows, and downloading the resulting image.

---

## 2. Warby Parker: what the research reveals

### 2.1 The original public implementation was a premium mobile AR experience

Warby Parker’s public launch material from 2019 describes a virtual try-on feature in its iPhone app. The early version used Apple’s ARKit and TrueDepth camera technology on iPhone X-class devices. The TrueDepth camera supplied a detailed depth representation of the user’s face, while Warby Parker added its own frame-placement and fit system.

The important point is that Warby Parker did not treat the feature as a simple flat image pasted over a face. Its stated goals were:

- Realistic scale.
- Stable placement while the head moves.
- Frame colour and texture that look believable.
- A better estimate of which frame width suits the customer.
- A result that feels closer to wearing the real frame than a normal social-media filter.

Warby Parker publicly described its internal method as **“unique placement”**: an algorithm intended to mimic how a real frame sits on a person’s particular facial structure. Its 2019 Impact Report says the system combined Apple ARKit, TrueDepth, a proprietary frame-placement/fit system and digital frame representations.

Sources:

- [Wired: Warby Parker’s AR app](https://www.wired.com/story/warby-parker-augmented-reality-app/)
- [Retail Dive: Warby Parker AR launch](https://www.retaildive.com/news/warby-parker-launches-ar-tool-for-virtual-try-on/547673/)
- [Warby Parker Impact Report 2019](https://img.warbyparker.com/PDF/impact-report/Impact-Report-2019.pdf)

### 2.2 It is connected to a larger shopping workflow

Virtual try-on was not isolated. Warby Parker’s 2019 report describes a user being able to:

- Try a frame virtually.
- Save favourite frames.
- Add frames to the physical Home Try-On programme.
- Purchase directly.
- Share a try-on image with friends.

This is important because the successful experience is not only the tracking technology. It is the sequence around it: browse, try, compare, save, ask for feedback and continue to purchase.

### 2.3 Warby Parker’s current experience is broader than the 2019 launch

Warby Parker currently promotes Virtual Try-On alongside **Advisor**, which combines a face scan, frame-size information, style preferences and recommendations. Its privacy policy says that, for Virtual Try-On, face scans and measurements are processed while the feature is being used and are not stored or shared with third parties for that feature. It distinguishes this from optional conclusions such as a recommended frame width that may be retained.

This distinction is useful for Univers:

- Temporary face data should be separate from persistent business data.
- A favourite frame ID can be saved without saving the customer’s face photograph.
- If the clinic later wants customer history, that should be an explicit second feature, not an accidental consequence of taking a picture.

Sources:

- [Warby Parker Advisor](https://www.warbyparker.com/advisor)
- [Warby Parker mobile apps](https://www.warbyparker.com/ios-app)
- [Warby Parker privacy policy](https://www.warbyparker.com/privacy-policy)

### 2.4 Warby Parker also shows what not to copy initially

The original AR feature depended on advanced Apple hardware and proprietary frame-placement work. Public reporting also describes technical difficulties and multiple revisions before the feature reached the desired quality. The experience was initially limited to newer iPhones because of the TrueDepth requirement.

Therefore, Warby Parker is a good **quality benchmark**, but a poor first implementation blueprint for Univers Optique. We should not assume that a phone camera plus ordinary frame photographs will immediately reproduce Warby Parker’s 3D quality.

---

## 3. Webkul video: what it actually demonstrates

### 3.1 The visible user journey

The video shows the following pattern:

1. The user opens a virtual try-on experience.
2. The camera captures the user’s face.
3. The user selects a frame from several available options.
4. The frame follows the user’s face as the user moves.
5. The user switches between frame styles.
6. The user downloads a try-on image.

This is very close to the interaction Univers Optique wants: one customer image, then rapid frame switching instead of repeatedly removing frames from the display.

### 3.2 What Webkul’s documentation confirms

Webkul’s Magento and PrestaShop documentation describes a simpler and more transparent pipeline than Warby Parker’s premium AR system:

- The customer uploads a photo or uses the camera.
- The image can be cropped.
- The system detects the eyes or pupils.
- A prepared spectacle image is placed over the face.
- The customer can manually adjust the frame if positioning is imperfect.
- The customer can download the final image.
- The store administrator enables try-on only for selected products and uploads a try-on asset for each product.

The Magento documentation describes configurable products, product-specific try-on assets, automatic pupil detection and manual positioning. It also notes that camera access requires an HTTPS connection.

Sources:

- [Webkul Magento 2 Virtual Try-On](https://store.webkul.com/magento2-virtual-try-on.html)
- [Webkul TensorFlow Virtual Try-On](https://webkul.com/blog/magento2-tensor-flow-virtual-try-on/)
- [Webkul PrestaShop Virtual Try-On](https://webkul.com/blog/prestashop-virtual-try-on/)

### 3.3 Important distinction: the video does not disclose the whole implementation

The video description mentions TensorFlow, Three.js and Blender, but it does not disclose:

- The exact TensorFlow model or landmark model.
- Whether every frame is a 2D transparent asset or a 3D model.
- The exact frame-calibration process.
- Whether images are processed locally or uploaded to a server.
- Accuracy measurements.
- Retention and deletion policy.
- How the catalogue is synchronised with inventory.

Therefore, we should treat the video as a useful **workflow demonstration**, not as complete technical documentation.

---

## 4. Warby Parker versus Webkul versus Univers

| Dimension | Warby Parker | Webkul module | Univers prototype |
|---|---|---|---|
| Primary setting | Consumer e-commerce/app | E-commerce storefront plugin | Private optical-clinic tool |
| Main input | Live camera and face/depth scan | Photo or camera, depending on module | Staff-taken customer photo first |
| Rendering ambition | High-quality live 3D AR | Simpler overlay and/or module-specific 3D mode | Frontal 2D overlay first |
| Frame assets | Carefully digitised/calibrated assets | Admin uploads try-on assets per product | Five prepared assets from real Univers frames |
| Face processing | Proprietary placement and fit system | Eye/pupil detection plus positioning | Face landmarks/eye references plus calibration |
| Manual correction | Intended to feel automatic | Manual adjustment is an explicit fallback | Manual correction should be available during testing |
| Catalogue | Warby’s large product catalogue | Selected enabled products | Available/inactive local stock |
| Favourites | Yes | Download/save image; exact shortlist workflow varies | Yes, store frame IDs only |
| Inventory awareness | Commerce integration | Product configuration | Core feature: available/sold toggle |
| Checkout | Built in | E-commerce checkout | Not in prototype |
| Privacy model | Session processing for try-on; policy-specific | Not established from the video | Session-only image, automatic deletion |
| Best lesson | Quality and UX | Practical MVP workflow | Local operational problem |

---

## 5. What this changes in our prototype thinking

### 5.1 The Webkul model is closer to our first build

The Webkul workflow confirms that a usable first version can be built around:

- A frontal face photo.
- Eye/pupil or facial-landmark detection.
- A prepared frame image.
- Automatic placement.
- Manual adjustment when needed.
- Frame switching.

This is closer to Univers’s exact request than Warby Parker’s hardware-dependent 3D AR system.

### 5.2 Warby Parker gives us the UX principles

We should borrow these interaction ideas from Warby Parker:

- Switch frames quickly without returning to a catalogue page.
- Make favourites easy to save.
- Keep the customer in the face-preview experience.
- Make the frame look stable and properly scaled.
- Keep the final physical fitting in the workflow.
- Separate temporary face processing from persistent frame/favourite data.

### 5.3 Manual correction is not a failure

Webkul makes manual adjustment an explicit part of the workflow. We should include a small adjustment control in the prototype rather than pretending automatic placement will be perfect for every face and every frame photograph.

Possible controls:

- Move left/right.
- Move up/down.
- Increase/decrease scale.
- Reset to automatic position.

The customer should not normally need to use these controls. Staff can use them when preparing a frame asset or correcting a particular session.

### 5.4 Frame asset preparation is confirmed as a major task

Warby Parker’s quality depended on carefully prepared digital frame representations. Webkul also requires a try-on asset for each enabled product. This confirms that “the owner uploads a normal phone photo and everything works automatically” is too optimistic.

For Univers, each pilot frame should have:

- A unique stock number.
- A clean frontal photograph.
- A transparent or background-removed try-on asset.
- A calibration value or default placement.
- Availability status.
- Optional price and brand information.

### 5.5 Downloading the customer image should not be automatic for Univers

The Webkul video presents image download as a feature. For Univers, the business goal is in-store selection, not social sharing. Downloading or storing the customer’s face image creates additional privacy risk and is not necessary for the first pilot.

A better first behaviour is:

- Save favourite **frame IDs** during the session.
- Show the shortlist on the screen.
- Delete the face image when the session ends.

Sharing or downloading can be considered later only if Univers specifically requests it and customers give clear permission.

---

## 6. Technical direction after this addendum

This research supports a two-step technical roadmap:

### Prototype A — Webkul-like photo workflow

- Responsive browser application.
- Camera capture or image upload.
- Frontal-photo guide.
- Face/eye landmark detection.
- 2D transparent frame overlay.
- Automatic scale and placement.
- Manual correction controls.
- Swipe through active frames.
- Favourites stored as frame IDs.
- Session-only customer image.

### Later version — Warby-like live AR workflow

- Live camera preview.
- Stable head-pose tracking.
- 3D or semi-3D frame assets.
- Correct scale based on frame dimensions and facial measurements.
- Occlusion for temples and hair.
- Better lighting, material and lens rendering.
- Optional frame-size recommendations.

We should not start Version B until Version A proves that the staff and customers actually save time and prefer the digital shortlist workflow.

---

## 7. Updated Phase 1 conclusion

The two new references strengthen, rather than weaken, our original recommendation:

- **Warby Parker** is the quality and user-experience benchmark.
- **Webkul** is the more realistic implementation reference for the first prototype.
- **Univers Optique** needs neither a consumer e-commerce app nor a full Warby Parker clone.
- The first prototype should be a private, tablet-friendly, inventory-aware version of the simpler photo/landmark/overlay workflow.

The key product sentence remains:

> **Take one customer photo, let the customer swipe through available Univers frames, save a shortlist, then physically fit only the shortlisted frames.**

No requirements or code should be started until this addendum is reviewed together with the original Phase 1 case study.

---

## Decision requested

Please confirm or correct these conclusions:

1. We should use the Webkul-style photo/overlay workflow as the technical starting point.
2. We should use Warby Parker’s swipe, favourites, stability and privacy principles as UX inspiration.
3. We should include manual adjustment in the prototype.
4. We should not include customer-image download or social sharing in Version A.
5. We should treat full Warby-style 3D AR as a later phase, not the initial build.

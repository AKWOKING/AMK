# Univers Optique — prototype
## Phase 2A: product requirements draft

**Date:** 27 September 2026  
**Status:** Draft for review  
**Previous phase:** Warby/Webkul research approved  
**Scope of this phase:** Define the first prototype’s product behaviour and boundaries. Tool selection, architecture and implementation are intentionally deferred.

---

## 1. Product definition

### Working name

**Univers Optique Try-On**

### Product type

A private, staff-operated, tablet-first web application for previewing available eyeglass frames on a customer’s photograph.

### One-sentence purpose

> Help Univers Optique reduce the number of physical frames customers need to try before creating a shortlist.

### Core workflow

> Take one customer photo → swipe through available frames → save favourites → physically fit only the favourites.

The application is a **shortlisting tool**, not a replacement for:

- Professional optical advice.
- Prescription assessment.
- Physical comfort testing.
- Final frame adjustment.
- Lens measurement or lens fabrication.

---

## 2. Actors and permissions

### 2.1 Staff member

The staff member operates the application with the customer.

Staff should be able to:

- Start a try-on session.
- Take or select the customer photograph.
- Move between available frames.
- Save the customer’s favourite frames.
- End the session.
- Add a frame to the catalogue.
- Edit frame information.
- Mark a frame available or unavailable.
- Correct a frame’s default position during asset preparation.

### 2.2 Catalogue administrator

For the first pilot, the catalogue administrator can be the same person as the staff member. A separate role is not required until Univers has more than one location or needs different staff permissions.

The administrator should be able to:

- Add a frame.
- Edit a frame.
- Hide or deactivate a frame.
- Reactivate a frame.
- View the frame’s stock number and status.

### 2.3 Customer

The customer does not need:

- An account.
- A password.
- A phone number.
- An email address.
- A separate application installation.

The customer interacts through the staff member’s device during the session.

---

## 3. Version A scope

### 3.1 Catalogue management

Each frame record should contain:

| Field | Required in Version A? | Notes |
|---|---:|---|
| Internal stock number | Yes | Use Univers’s existing numbered label if unique |
| Try-on image | Yes | Clean frame asset used over the customer photo |
| Display image | Optional | Can be the same as the try-on image in the prototype |
| Brand | Optional | Only if Univers wants it recorded |
| Model name/description | Optional | Not required if the stock number is sufficient |
| Price | Decision required | May be staff-only or visible during selection |
| Availability status | Yes | Available, hidden/sold, or reserved |
| Created/updated date | Yes, internally | Useful for catalogue maintenance |
| Default position/calibration | Yes, internally | Controls how the frame is placed on the face |

The user interface should hide inactive frames from the customer try-on list immediately.

A frame should be **deactivated**, not permanently deleted, when it is sold or no longer available. This prevents accidental loss of catalogue history and allows reactivation.

### 3.2 Try-on session

The staff member should be able to:

1. Start a new session.
2. See a short privacy notice.
3. Obtain the customer’s agreement before taking the photograph.
4. Take a frontal photograph using the device camera, or select a photograph from the device if camera capture fails.
5. Receive guidance to keep the customer’s face frontal and visible.
6. Run face/eye landmark detection.
7. See the first available frame overlaid on the customer’s photo.
8. Swipe or tap to move between frames.
9. Save a frame to the shortlist.
10. Remove a frame from the shortlist.
11. Finish the session and display the selected frame numbers.
12. Delete the customer image.

The first prototype should show one frame at a time. A comparison grid or side-by-side view can be considered later.

### 3.3 Frame overlay

For Version A:

- The overlay is based on a prepared 2D frame image.
- The frame should be automatically positioned using the detected eyes/face landmarks.
- The frame should scale based on the customer’s face reference points and the frame’s calibration.
- The overlay should rotate slightly if the customer’s head is tilted.
- The application should provide a manual adjustment fallback.

Manual adjustment should include:

- Move left/right.
- Move up/down.
- Increase/decrease size.
- Reset to the automatic position.

The controls should be available for staff during testing, even if they are hidden from the normal customer-facing view later.

### 3.4 Favourites

The shortlist should store frame IDs or stock numbers, not a permanent copy of the customer’s face photograph.

At the end of the session, staff should see something similar to:

```text
Customer shortlist
- N° 47
- N° 30
- N° 18
```

The application should not send a customer image to WhatsApp or download it automatically in Version A.

### 3.5 Availability

The try-on screen must only show frames marked available.

Minimum statuses:

- Available
- Hidden/sold
- Reserved

The customer must not see hidden or sold frames, even if an old browser tab remains open. The application should refresh or revalidate the active frame list when a session starts.

---

## 4. Privacy and security requirements

### 4.1 Customer photograph

The customer photograph must be treated as temporary session data.

Recommended Version A policy:

- Explain the purpose before capture.
- Ask for consent verbally and through a visible notice.
- Do not identify or recognise the customer.
- Do not create a customer profile.
- Process the photo locally where practical.
- Delete the photo when the session ends.
- Apply an automatic maximum deletion fallback of 24 hours if the session is abandoned.
- Do not include the customer image in application logs or analytics.
- Do not use the customer image to train a model.

### 4.2 Staff access

The catalogue management area should not be publicly accessible.

At minimum, the prototype should have a basic staff access boundary. The exact authentication approach is deferred until the tool-selection phase.

### 4.3 Camera behaviour

The application must:

- Request camera permission only when the staff starts capture.
- Explain why camera access is needed.
- Stop the camera stream after capture or when the session ends.
- Show a clear fallback when permission is refused.
- Work only through a secure origin when browser camera access requires HTTPS.

### 4.4 Sensitive information not collected

Version A must not collect:

- Prescription values.
- Medical history.
- Patient/customer names.
- Phone numbers.
- Email addresses.
- Facial identity or biometric identity records.
- Payment details.

---

## 5. Device and environment assumptions

These are provisional assumptions and must be confirmed before implementation.

### Proposed primary device

- One Android tablet or smartphone with a front-facing camera.
- Chrome or another modern browser.
- The device is positioned at the optical counter.
- Staff operates the capture; the customer views and swipes.

### Secondary device

A computer may be used for catalogue management if Univers prefers a larger screen. It should not require a separate desktop application.

### Network

Network reliability has not yet been verified.

The product should ideally support:

- Catalogue access when the network is available.
- Face detection and frame preview without sending the customer photo to a remote service.
- Recovery when the network briefly drops during a session.

Whether the complete prototype must work offline is still an open decision. Offline support affects asset storage, staff authentication, inventory synchronisation and deployment complexity, so it must be confirmed before choosing the architecture.

### Clinic setup

The initial pilot assumes:

- One Univers Optique location.
- One catalogue.
- Approximately five frames in the first technical test.
- More than 50 frames eventually.
- One or a small number of staff operators.
- No integration with an existing point-of-sale or inventory system.

---

## 6. Frame-asset requirements

A normal photograph of a frame is not automatically a finished try-on asset.

For each pilot frame, the preparation process should produce:

1. A clean frontal frame image.
2. A transparent background or a reliable mask.
3. The Univers stock number.
4. A default scale reference.
5. A default position relative to the eyes and nose bridge.
6. A validation result on at least one test face.

The pilot should use five frames selected to test different difficulties:

- Thick dark frame.
- Thin metal frame.
- Round frame.
- Coloured or patterned frame.
- Frame with strong reflections or a distinctive bridge.

This is more useful than selecting five frames that all behave the same way.

### Asset quality checklist

A frame photograph should preferably be:

- Frontal.
- Entirely inside the image.
- Taken at a consistent distance.
- On a simple, light background.
- Free of other frames underneath it.
- Free of strong reflections.
- Clear of stickers over the lenses.
- Taken with the temples open when the image is used for catalogue reference.

---

## 7. Customer capture requirements

The capture screen should guide staff to:

- Place the customer in even light.
- Keep the face frontal.
- Keep both eyes visible.
- Move hair away from the eyes when possible.
- Keep the customer at a consistent distance.
- Avoid strong backlighting.
- Remove the customer’s existing glasses if practical, or clearly communicate that the preview may be less accurate.

The system should display a useful error rather than silently producing a badly placed overlay.

Possible capture states:

- Face not detected.
- More than one face detected.
- Face too small.
- Face turned too far sideways.
- Eyes obscured.
- Image too dark.
- Ready to continue.

---

## 8. Version A non-goals

The following are explicitly outside the first prototype:

- Native iOS application.
- Native Android application.
- Full desktop application.
- Full 3D frame modelling.
- Realistic side-angle rendering.
- Lens-refraction simulation.
- Prescription validation.
- Pupillary-distance measurement for manufacturing lenses.
- Face-shape classification.
- AI style recommendations.
- Customer accounts.
- Online checkout.
- Payment processing.
- Public frame catalogue.
- Social sharing.
- WhatsApp image sending.
- Multi-branch inventory.
- POS integration.
- Automatic sales synchronisation.
- Permanent customer history.

These may become future features, but adding them now would make it harder to test the central business hypothesis.

---

## 9. Prototype acceptance criteria

The prototype should not be considered successful merely because a frame appears on a face. It must demonstrate the complete clinic workflow.

### Catalogue criteria

- Staff can add five test frames.
- Every test frame has a unique stock number.
- Staff can mark a frame unavailable.
- An unavailable frame no longer appears in a new session.
- Staff can reactivate a frame.

### Capture criteria

- Staff can start a session from the main screen.
- The application explains the photo purpose before capture.
- Staff can capture a frontal customer image.
- The application detects whether a usable face is present.
- The application provides a clear retake message when detection fails.
- The camera stops when the session ends.

### Try-on criteria

- The first frame appears automatically after a usable capture.
- Staff/customer can move between all active test frames.
- The frame remains reasonably aligned when the customer photo is frontal.
- The overlay can be manually corrected.
- Switching between frames does not require retaking the customer photo.
- The customer can save and remove favourites.

### Session and privacy criteria

- The final screen displays selected stock numbers.
- The customer face image is not included in the shortlist data.
- The image is deleted when the session is finished.
- An abandoned session is automatically cleared within the agreed retention period.
- No customer account is created.

### Operational criteria

- The application can be used by a staff member without developer assistance.
- The workflow can be demonstrated using Univers’s real frame photographs.
- Staff can explain the value in one sentence.
- The pilot can record the time taken to create a shortlist.

---

## 10. Measurements for the pilot

Before using the prototype with customers, Univers should help us record a baseline for a small sample of sessions:

- Number of customers who try frames.
- Number of physical frames handled per customer.
- Time from first frame to shortlist.
- Time spent returning frames to their places.
- Number of frames in the final physical shortlist.
- Whether staff and customers prefer the digital shortlist workflow.

The prototype should record only operational events that do not identify customers. For example:

- Session started.
- Number of active frames shown.
- Number of frames selected.
- Session duration.
- Frame IDs selected.

It should not record the customer photograph as analytics data.

---

## 11. Decisions required before Phase 2B

The following decisions are still open:

1. Which exact device will Univers provide for the pilot?
2. Is the device Android, iPad, laptop or desktop?
3. Is internet access reliable at the counter?
4. Must the first version work fully offline?
5. Should frame prices be visible to customers, staff only, or not included?
6. Are Univers’s frame numbers unique across the whole stock?
7. Should the customer’s existing glasses be removed before capture?
8. Should the customer shortlist be displayed only on the device or also printed/shared?
9. Who will prepare the five pilot frame assets?
10. Does Univers agree to the proposed session-only photo policy?
11. How many staff members need catalogue-management access?
12. What time period should be used for the pilot measurement?

---

## 12. Phase 2A decision requested

Please review this requirements draft before we select tools or write code.

The most important points to approve or correct are:

- Tablet-first responsive web application.
- Customer has no account.
- Five-frame prototype first.
- Photo-based 2D overlay first.
- Manual adjustment available.
- Active/inactive inventory status.
- Favourites store frame IDs, not face images.
- Session-only customer image with automatic deletion.
- No 3D, prescription or public-commerce features in Version A.

After this document is approved, Phase 2B will compare the technical implementation options and tools against these requirements. No implementation should begin until Phase 2B is reviewed and approved.

# DM OPTIQUE SARL website audit

Date: 2026-10-23
Package: `dmopticsarl.zip` (4.3 MB compressed, 8.9 MB uncompressed)
Site: 97 HTML pages, 48 French, 48 English, plus 404
Method: static analysis of every page, local server on port 8766, headless Chrome at 1366 px and 390 px, axe-core WCAG 2 A/AA and 2.1 A/AA on four key pages, comparison with the live domain.
Deployment: none. The package was not published.

## Verdict

The build is technically strong and close to ready. There are no broken links, no metadata gaps, no missing alt text, no duplicate titles, no sitemap gaps, no JavaScript syntax errors and no automated accessibility violations. The bilingual switch is fully wired, including document language, title, description, canonical, navigation, placeholders, counts, image alt text and WhatsApp links.

Two issues should be fixed before the next public push: there is no mobile navigation, and every image and font is served with `max-age=0`, which forces browsers to revalidate them on every visit.

## Scorecard

| Area | Result |
|---|---|
| HTML pages | 97, with 96 sitemap URLs |
| Internal links and assets | 0 broken |
| Title, description, canonical, og, twitter | 0 missing on indexable pages, 0 duplicates |
| Hreflang | 0 missing, 0 asymmetric |
| Sitemap | 96 of 96 targets present |
| JavaScript | 297 inline scripts, 0 syntax errors |
| Structured data | 0 invalid blocks |
| Images | 490 total, 0 missing width/height, 408 lazy, 0 missing alt |
| Accessibility | 0 axe violations on home, category, product, contact |
| WhatsApp and phone | 572 WhatsApp links and 379 phone links, all +237 656 122 239 |
| Live domain | HTTPS 200, www 301 to apex, 404 returns 404 |
| Mobile navigation | Fail: no menu control |
| Asset caching | Fail: max-age=0 on images and fonts |

## P1, fix before the next public push

### 1. No navigation on mobile and tablet

At 390 px, the shared header hides `nav.nav` (`display:none`) and exposes no menu button: 0 visible navigation links, 0 elements with `aria-expanded` or `aria-controls`, and no hamburger. The same header is used on 91 of 97 pages. The only navigation left on mobile is the footer, after a long scroll, plus the two fixed dock buttons (WhatsApp and phone). A visitor who lands on the home page cannot reach the frame catalogue, the eye examination page or the practice page from the top of the page.

The breakpoint is 980 px, so tablets at 768 or 820 px have the same problem.

Fix:

- Add a 44 px menu button with `aria-expanded`, `aria-controls`, a visible label or `aria-label`, focus management, Escape to close and a focus trap while open.
- Or, as a minimum, keep a "Montures" link and a "Contact" link visible in the header below 980 px.
- Test at 390, 768 and 1024 px.

### 2. Images and fonts are cached for zero seconds

The live response sends:

```
Cache-Control: public, max-age=0, must-revalidate
```

on `.webp` photos, `.woff2` fonts and `og.jpg`. Cloudflare reports `cf-cache-status: HIT` at the edge, but the browser still revalidates each file on every visit. On a 3G connection in Douala, that removes most of the benefit of the responsive images and local fonts.

The `_headers` file is honored by the host: the live security headers match it. Add cache rules there:

```
/*.webp
  Cache-Control: public, max-age=604800

/*.woff2
  Cache-Control: public, max-age=31536000, immutable
```

Keep HTML at `max-age=0, must-revalidate`. Use a shorter image lifetime, seven days, because frame photos may be replaced without hashed filenames. If filenames become hashed, switch images to one year and `immutable`.

## P2, fix soon

### 3. No favicon or Apple touch icon

There is no `favicon.ico`, no `favicon.svg`, no `<link rel="icon">` on any of the 97 pages, and `https://dmoptiquesarl.com/favicon.ico` returns 404. Browsers show a blank tab icon and generate a 404 request.

Fix:

- Add `favicon.svg`, `favicon.ico` and a 180x180 `apple-touch-icon.png` built from `dm-logo.webp`.
- Add the links in the shared head:

```
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
```

### 4. Structured data image and logo URLs contain a double slash

Four occurrences on the French and English home pages:

```
https://dmoptiquesarl.com//cabinet-hero-1080.webp
https://dmoptiquesarl.com//dm-logo.webp
```

The browser may recover, but validators and some consumers treat the URL as malformed. Remove one slash in the `Optician` JSON-LD on `index.html` and `en/index.html`.

### 5. HSTS is missing

The live site has `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options` and `Permissions-Policy`, but no `Strict-Transport-Security`. Add:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

Only add `preload` after the domain and all subdomains are permanently HTTPS.

### 6. Product share images are WebP, not 1200x630 JPEG

17 pages use `og.jpg` (1200x630 JPEG, 75 KB). 80 pages use a product WebP, typically 1600x1200. WhatsApp is the primary sharing channel for this business, and WebP support in link previews is inconsistent across WhatsApp and other scrapers. A 4:3 image is also cropped by some previews.

Fix:

- Test one product link in a real WhatsApp chat. If the preview is blank or badly cropped, generate a 1200x630 JPEG per frame, or use `og.jpg` as the product fallback.
- If product WebP stays, add `og:image:width`, `og:image:height` and `og:image:type`.

### 7. llms.txt covers French only

`llms.txt` lists 49 site URLs, the French home plus 48 French pages. The sitemap has 96 URLs. All 47 English pages are missing. For a bilingual site that explicitly targets English-speaking patients and clinics, add the English URLs or list both languages.

## P3, polish and opportunities

### 8. Product pages have no Product schema

Each frame page has `BreadcrumbList` only. Add a `Product` node with `name`, `image`, `description` and `sku` (the frame reference). Do not add an `Offer` with a fake price. A Product without offers is still useful for entity understanding.

### 9. Copy uses many em dashes and en dashes

Visible copy contains 685 em dashes and 654 en dashes. If the house style that applies to AMK also applies here, this needs a copy pass. If the DM Optique voice intentionally uses them, leave them and document the exception.

### 10. No Content Security Policy

There is no `Content-Security-Policy`. The site has no external scripts, which keeps the risk low, but a conservative policy adds defense in depth:

```
Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'
```

Inline styles and scripts force `'unsafe-inline'`. The policy still restricts external origins, framing and form targets.

### 11. Schema founder name and opening hours

The schema founder is "Domche Noumbi". The ONOC directory lists "DOMCHE NOUMBI Samuel Renaud". Use the full name. The schema says the practice closes at 17:30, while the visible copy says eye examinations end at 13:00 and other needs at 17:30. Consider two `OpeningHoursSpecification` entries or a description that matches the visible hours.

### 12. Shared social images

There are 41 unique `og:image` values for 97 pages. Some frames share the same preview image. This is not a defect, but distinct previews per frame make shared links easier to recognize.

## What is solid

- 0 broken internal references across 97 pages, including srcset and CSS `url()`.
- Every indexable page has one title, one description, one canonical, one absolute `og:image`, one `og:url` and a twitter card. The 404 is intentionally no-index and has no canonical. No duplicate titles or descriptions.
- Hreflang is reciprocal on every French and English page, with `x-default`.
- Sitemap covers all 96 indexable pages and excludes the no-index 404.
- 297 inline scripts parse without error. 0 invalid JSON-LD blocks.
- 490 images: all have width and height, 408 are lazy, all have alt text.
- Language switch changes `html lang`, `title`, meta description, canonical, navigation hrefs, placeholders, result counts, image alt text and WhatsApp message language.
- Category filters work: 24 frames, oval filter 2, search F01 gives 1, a nonsense search gives 0 with a useful empty state, reset restores 24. The mobile filter panel opens and closes correctly.
- axe-core reports 0 WCAG A/AA violations on home, category, product and contact.
- No analytics, no cookies, no forms collecting patient data, no exposed secrets. Privacy-friendly for a medical practice.
- Security headers are live and `_headers` is honored.
- Live domain: HTTPS, gzip, www redirect, 404 status, Cloudflare edge cache. Fonts are local with `font-display: swap`; the hero is preloaded with `fetchpriority=high`; images use srcset.

## Pre-deploy checklist

1. Add the mobile menu and test 390, 768, 1024 px.
2. Add the cache rules to `_headers`.
3. Add favicon, favicon.ico and apple-touch-icon.
4. Fix the double slash in the home schema.
5. Add HSTS.
6. Test one product link in WhatsApp; switch product previews to JPEG if needed.
7. Add the English URLs to llms.txt.
8. Optional: Product schema, CSP, founder name, opening hours, copy polish.
9. Re-run the local and live checks after the fixes.

## Limits of this audit

- axe-core is automated. It does not replace a manual screen reader and keyboard pass.
- No physical Android or iPhone test. Layout was checked in headless Chrome at 390 px and 1366 px.
- WhatsApp, Facebook and TikTok crawler rendering was not tested directly. The WebP preview risk needs a real share test.
- The package differs slightly from production: production does not yet have the "preferred source" link, and one script differs. This audit covers the package, not the live page.
- No payment, booking or form flow exists to test.
- Local transfer sizes are not representative because the local server does not compress. Live HTML is gzip.

## Artifacts

- `qa_home_desktop.png`
- `qa_home_en.png`
- `qa_home_mobile.png`
- `qa_category_desktop.png`
- `qa_product_desktop.png`
- `qa_contact_desktop.png`
- `audit_static2.py`
- `audit_extra.py`
- `qa_dmoptic.js`
- `qa_dmoptic_i18n.js`
- `compare_live.py`

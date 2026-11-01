# FLI-1 funnel: GoHighLevel setup

**Goal:** `myaidoesit.com/fli-1` → opt-in → thank-you page with the download →
email sequence.

| File | What it is |
|---|---|
| `index.html` | Opt-in page (FLI-1) |
| `thank-you.html` | Thank-you / download page |
| `emails.md` | 4-email follow-up sequence |
| `images/hero-mockup.png` | Hero image (transparent background) for a native GHL build |
| `images/og-image.png` | 1200×630 social share image (link previews) |
| `images/promo-1080x1350.png` | Instagram feed / story promo graphic |
| `images/preview-*.png` | Screenshots of how the pages look |
| `../post-autopilot.zip` | The lead magnet file people download |

---

## 1. Upload the files to the Media Library
**Sites → Media** (or Media Storage). Upload:
- `post-autopilot.zip` → copy its URL. This is your **DOWNLOAD_URL**.
- `og-image.png`, `hero-mockup.png`

## 2. Create the form
**Sites → Forms → Builder → + Add Form → "FLI-1 Post Autopilot"**
- Fields: **First Name**, **Email** (required)
- Styling: button color `#2F5CFF`, rounded corners, no form title
- Under form settings, set **On Submit → Open URL** to `https://myaidoesit.com/fli-1-thank-you`
- Save, then copy the **embed code** (iframe)

## 3. Build the funnel
**Sites → Funnels → + New Funnel → "FLI-1 Post Autopilot"**

**Step 1: Opt-in.** Path: `fli-1`
1. Add a step and open the page builder.
2. Add a full-width section, then a **Custom JS/HTML** (Code) element.
3. Paste the full contents of `index.html`.
4. In the pasted code, find both `<form class="optin" …> … </form>` blocks (marked `GHL FORM`) and replace each one with your form **embed code** from step 2.
5. **Settings → SEO meta data:** title `Free Post Autopilot Skill for Claude | AI Does It`, the description from the HTML, and the social image set to `og-image.png`'s Media URL.

**Step 2: Thank you.** Path: `fli-1-thank-you`
1. Add another Custom HTML element and paste `thank-you.html`.
2. Replace `{{DOWNLOAD_URL}}` with the zip's Media URL.

> **Prefer GHL's native builder?** Recreate the page with GHL elements: headline,
> paragraphs, a form element, and an image element using `hero-mockup.png`. Use the
> copy from `index.html`. Native forms submit automatically, and you skip step 4
> above.

**Alternative to swapping forms:** keep the styled HTML form and set
`FORM_WEBHOOK` near the bottom of `index.html` to a workflow's **Inbound Webhook**
URL (see step 4). Map `first_name` and `email` to the contact in the workflow.
Until one of these is done, the HTML form shows a "not connected yet" message and
does **not** capture leads.

## 4. Connect the domain
**Settings → Domains:** make sure `myaidoesit.com` is connected to this funnel, then
publish. Check that `https://myaidoesit.com/fli-1` loads.

## 5. Automation workflow
**Automation → Workflows → + Create → Start from scratch → "FLI-1 Delivery"**
- **Trigger:** Form Submitted → form = *FLI-1 Post Autopilot* (or Inbound Webhook if you chose that option)
- **Add Tag:** `fli-1-post-autopilot`
- **Send Email:** Email 1 (immediately)
- **Wait 2 days → Send Email:** Email 2
- **Wait 2 days → Send Email:** Email 3
- **Wait 3 days → Send Email:** Email 4
- *(Optional)* **Add to Workflow:** your main newsletter or nurture
- Publish the workflow.

## 6. Test before you promote
1. Open `myaidoesit.com/fli-1` on your phone and on desktop.
2. Opt in with a personal email.
3. Confirm: redirect to the thank-you page → download works → Email 1 arrives → contact is tagged.
4. Unzip the download and try "Start Post Autopilot" in Claude.

## 7. Promote it
- **Instagram:** `promo-1080x1350.png`, linked in your bio or a link sticker
- **Professional network posts:** when you mention it, put the link directly in the post or first comment. In keeping with the skill, don't use "comment WORD to get it".
- Add UTM tags to track sources, for example: `myaidoesit.com/fli-1?utm_source=instagram&utm_medium=social&utm_campaign=fli-1`

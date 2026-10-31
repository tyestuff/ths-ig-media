# How posts actually get onto LinkedIn

There are four reliable ways to do it. Explain them simply, recommend one, and set
it up with the user. Whatever they choose, **test with one post first**.

> Note: LinkedIn changes its products and API terms from time to time. If a
> screen, button, or permission name doesn't match these steps, tell the user what
> you expected to see and help them find the current equivalent. Don't guess.

---

## A. LinkedIn's built-in scheduler (free, no setup)

**Good for:** anyone who wants zero setup, or wants to keep their hands on the
final "publish" button.

**How it works:** Claude writes and approves the posts in `queue/`. The user
copies each one into LinkedIn and uses the clock icon to schedule it.

**Steps to give the user:**
1. On LinkedIn (desktop or app), click **Start a post**.
2. To post as a Page, click your name or photo at the top of the post box and switch to the Page (you need to be an admin).
3. Paste the post text from the queue file and add the image from `media/`.
4. Click the **clock icon** next to Post, pick the date and time, then click **Schedule**.
5. Tell Claude when it's done, and Claude will mark it scheduled in the queue.

**Claude's job:** Present each post as a clean, copy-ready block with the date,
time, destination, and image filename right above it. Optionally produce a
one-page "schedule sheet" for the week.

---

## B. Zapier (hands-off, no code)

**Good for:** non-technical users who want Claude to post for them.

Zapier's LinkedIn integration can publish a share update to a personal profile
and to a company Page the user administers. There are two ways to use it:

### B1. Claude's Zapier connector (Claude posts directly)
1. The user connects Zapier to Claude (in Claude: Settings → Connectors → Zapier, or `claude mcp add` for Zapier MCP in Claude Code, following Zapier's current instructions at mcp.zapier.com).
2. In Zapier MCP, enable LinkedIn actions such as **Create Share Update** (personal profile) and **Create Company Update** (Page).
3. Connect the LinkedIn account through Zapier's login popup. Claude never sees the password.
4. When a post is approved, Claude calls the action with the post text, an optional image URL, and visibility settings.
5. For **scheduling**, either:
   - post at the right moment from a scheduled Claude session or task, or
   - use method B2 below to let Zapier fire at the scheduled time.

### B2. A Zap that posts from a queue (set and forget)
1. Create a Google Sheet (or Airtable base) named "LinkedIn Queue" with the columns `publish_at`, `destination`, `text`, `image_url`, `status`.
2. Build a Zap: **Schedule by Zapier** (every hour) → **Google Sheets: Find rows** where `status = approved` and `publish_at` ≤ now → **LinkedIn: Create Share Update** (or Create Company Update) → **Google Sheets: Update row** `status = posted`.
3. Claude adds approved posts to the sheet (directly through the Zapier or Google Sheets connector, or by giving the user rows to paste).

Images need a **public URL** (Google Drive "anyone with link", Dropbox direct link,
Cloudinary, the user's website, and so on).

---

## C. A social media scheduling tool

**Good for:** people who already pay for one, want a visual calendar, or manage
several platforms.

Common options that support LinkedIn profiles and Pages include Buffer, Hootsuite,
Later, Publer, Sprout Social, Metricool, Agorapulse, and **GoHighLevel's Social
Planner** (handy if they already use GoHighLevel).

Ways Claude can feed the tool:
1. **Bulk upload:** Most of these accept a CSV. Claude exports the approved queue in the tool's CSV format (ask the user to download the tool's sample CSV so the columns match exactly).
2. **Connector or automation:** If the tool has a Claude connector, a Zapier or Make integration, or an API the user can access, Claude can add posts directly.
3. **Copy and paste:** Same as Method A, but inside the tool's calendar.

---

## D. LinkedIn's official API plus the included scripts

**Good for:** technical users who want full control, no subscription, and posts
published straight from their own computer, a server, or GitHub Actions.

What the user needs:
- A LinkedIn developer app (free). See `linkedin-api-setup.md`.
- Personal profile posting: the **Share on LinkedIn** product and **Sign In with LinkedIn using OpenID Connect** on the app. Scopes are `openid profile w_member_social`.
- Company Page posting: LinkedIn's **Community Management API** product, which requires an application and approval from LinkedIn, plus the `w_organization_social` scope. The user must also be a Super admin or Content admin of the Page. If approval isn't realistic, use Method A, B, or C for the Page and Method D for the personal profile.

How it works:
1. `scripts/linkedin_auth.py` runs a one-time login in the browser and saves an access token to `linkedin-autopilot/.env`. The token lasts about 60 days, and the script reminds them to re-run it.
2. Approved posts sit in `queue/` with `status: approved` and a `publish_at` time.
3. `scripts/linkedin_post.py` publishes every approved post whose time has come, uploads images, records the post URL, and moves the file to `posted/`.
4. The user can run it on a schedule:
   - **Mac/Linux:** a `cron` entry such as `*/15 * * * * cd /path/to/project && python3 path/to/linkedin_post.py`
   - **Windows:** Task Scheduler, running every 15 minutes
   - **Cloud:** `templates/github-action.yml` (runs on GitHub's servers, with the token stored as a GitHub Secret)
   - **Claude Code:** a scheduled task or `/loop` that runs the script

Always do a `--dry-run` first. It shows what *would* be posted without posting.

---

## Picking one: quick guidance

- "Just tell me what to click" and $0 budget → **A**
- Wants hands-off, non-technical → **B** (Zapier)
- Already uses GoHighLevel, Buffer, Hootsuite, or similar → **C**
- Comfortable with a terminal, wants no subscription → **D** for the profile (plus A, B, or C for a Page unless they get Community Management API access)

## About comments and DMs

This skill never writes "comment [WORD] to get it" posts. It also doesn't automate
replies or DMs. LinkedIn doesn't let ordinary apps read comments on personal
posts or send DMs, and third-party auto-DM tools risk the account. Claude can
suggest replies to comments the user pastes in, and the user sends them
personally.

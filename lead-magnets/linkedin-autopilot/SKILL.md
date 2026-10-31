---
name: linkedin-autopilot
description: Plan, write, schedule, and publish LinkedIn posts for a personal profile and/or a LinkedIn company Page. Starts as a blank slate. It interviews the user about their business, audience, offers, and lead magnets, learns their voice from their own writing, builds a content calendar, and then schedules or publishes posts through whichever method they choose (LinkedIn's built-in scheduler, Zapier, a scheduling tool, or the official LinkedIn API). Use whenever the user says things like "set up my LinkedIn", "schedule LinkedIn posts", "write my LinkedIn content", "post this to LinkedIn", "plan my LinkedIn calendar", "automate LinkedIn", or "post to my company page".
---

# LinkedIn Autopilot

You help a business owner, creator, or professional show up on LinkedIn every week
without having to think about it. You interview them, build a content plan that
serves their business goals, write posts that sound like **them**, and get those
posts scheduled or published.

## Ground rules (read first)

1. **Start from a blank slate.** Do not assume an industry, niche, tone, format,
   emoji style, hook formula, or posting cadence. Everything about voice and
   strategy comes from the interview and from samples the user gives you. If you
   don't know something yet, ask. Don't guess.
2. **Their voice, not yours.** Don't fall back on generic "LinkedIn guru" habits
   (one-line hooks, "Here's the thing:", 🚀 bullet lists, "Agree?") unless the
   user's own samples or stated preferences call for them. When you have no
   samples, write plainly and ask them to react to it.
3. **Nothing goes live without a clear yes.** Drafting, planning, and queuing are
   fine. Before anything is published or scheduled, show the final text, image,
   target (personal profile or Page), and date and time, then wait for explicit
   approval. A batch approval ("approve all 8 for next week") counts. Silence
   doesn't.
4. **Never handle passwords.** Don't ask for a LinkedIn password. Logins happen
   through official OAuth screens, Zapier, or the user's scheduling tool.
   Access tokens live in environment variables or a `.env` file that is git-ignored.
   Never print a token or commit one to a repo.
5. **Stay inside LinkedIn's rules.** No fake engagement, engagement pods, automated
   connection requests, scraping, or mass DMs. Those break LinkedIn's User
   Agreement and can get the account restricted. This skill publishes the user's
   own content to the user's own profile or Page. That's all it does.
6. **Keep a memory.** Everything you learn goes into a `linkedin-autopilot/`
   workspace folder (layout below), so future sessions pick up where the last one
   stopped and the interview never has to be repeated.

## Workspace layout

Create this folder in the user's current project (or their home directory if they
prefer) the first time the skill runs:

```
linkedin-autopilot/
├── profile.md            # business, audience, offers, goals (from the interview)
├── voice.md              # how they write, learned from their samples
├── pillars.md            # 3–5 content pillars + post mix
├── lead-magnets.md       # each free resource, its link, CTA, and email sequence
├── media/                # their photos, logos, brand images, and inspiration
├── media-library.md      # what is in media/ and when to use each item
├── calendar.md           # the rolling content calendar
├── queue/                # one file per post, ready to schedule (see templates/post.md)
├── posted/               # files move here after they are published
├── results.md            # performance notes the user reports back
└── .env                  # tokens if using the API method (git-ignored)
```

Templates for these files are in `templates/` next to this SKILL.md.

## Workflow

Before you start, check whether `linkedin-autopilot/profile.md` exists.

- **It exists:** read `profile.md`, `voice.md`, `pillars.md`, `lead-magnets.md`, and
  `calendar.md`, give the user a two-line summary of where things stand, and ask
  what they want to do: write this week's posts, schedule the queue, add a new
  offer, review results, or update their profile.
- **It doesn't exist:** run the full setup below, in order.

### Phase 1: Interview

Follow `references/interview.md`. Key rules:

- Ask **one round at a time** (3–5 questions max), conversationally. Never dump
  all the questions at once.
- Let them answer loosely. Pull out the details yourself and confirm what you
  heard in one or two lines before moving on.
- Any question can be skipped. Write "unknown, ask later" and keep going.
- When a round is done, write those answers to the right workspace file before
  starting the next round, so nothing is lost if the session ends.

The interview covers, in order:
1. The business: what it is, what they're working on now, what's coming next
2. Who they want to attract: audience, ideal clients, buying triggers
3. Offers: products, services, and pricing they'd tease in content
4. Lead magnets and funnel: free resources, opt-in pages, email platform, sequences
5. Content preferences: post types, topics, things to avoid, frequency
6. Voice: samples of their writing, words they use, words they hate
7. Media: photos, logos, brand assets, inspiration accounts
8. Destinations: personal profile, company Page, or both, and admin access
9. Posting method: how they want posts to actually go out (Phase 3)

### Phase 2: Strategy

Using the interview, draft and confirm with the user:

1. **`voice.md`**: Read their samples and describe what you see: sentence length,
   formality, humor, use of "I" versus "we", emojis, line breaks, signature phrases,
   and how they open and close. Write a short "do / don't" list. Then show them a
   short test post in that voice and adjust until they say it sounds like them.
2. **`pillars.md`**: Propose 3–5 content pillars, each tied to a business goal
   and an audience pain point. Propose a weekly mix (for example: teach, story,
   proof, offer, and engagement posts), but let **them** set the ratio and frequency.
3. **`lead-magnets.md`**: For each free resource, record the link, the CTA style
   they're comfortable with, and the email sequence it feeds. See
   `references/funnels.md`.
4. **`calendar.md`**: Build the first 2–4 weeks: date, time, destination
   (profile/Page), pillar, post type, hook idea, CTA, and the media to use.

Use `references/content-playbook.md` for post formats and structure. It covers
**shapes**, not voice. Voice always comes from `voice.md`.

### Phase 3: Choose how posts go out

Explain the options in `references/posting-methods.md` in plain English,
recommend one based on their answers (tech comfort, budget, tools they already
use, personal versus Page), and set it up with them step by step:

| Method | Best for | Can Claude post on its own? |
|---|---|---|
| A. LinkedIn's built-in scheduler | Free, simplest, zero setup | No. Claude drafts, they paste and schedule |
| B. Zapier (Claude's Zapier connector or a Zap) | Non-technical users who want hands-off posting | Yes, after a one-time connection |
| C. A scheduling tool (Buffer, Hootsuite, GoHighLevel Social Planner, etc.) | People who already pay for one or want a visual calendar | Often, via the tool's integration or a CSV upload |
| D. LinkedIn's official API plus the scripts in `scripts/` | Technical users who want full control and no extra subscription | Yes |

Make sure they test with **one** low-stakes post before trusting any method with a
full calendar.

### Phase 4: Produce and schedule (the weekly loop)

1. Read the calendar and pick the next batch (usually one week).
2. Write each post into `queue/` using `templates/post.md`. Include final text,
   destination, publish date and time with time zone, image path (if any),
   first-comment text (if any), and the lead magnet or offer it supports.
3. Check every draft against the pre-flight list below.
4. Present the batch for approval. Edit until approved.
5. Schedule or publish using their chosen method. Record the result (post URL or
   scheduled confirmation) in the post file and move it to `posted/` once it's live.
6. Update `calendar.md`.

**Pre-flight check for each post:**
- Sounds like `voice.md` (read it back against their samples)
- Under 3,000 characters (LinkedIn's limit for a post)
- One clear idea, one clear CTA
- Every link works and has UTM tags if they track them (see `references/funnels.md`)
- Images exist in `media/`, with alt text written
- No claims, numbers, testimonials, or client names they haven't confirmed are real and okay to share
- Destination is correct (personal or Page) and they have rights to post there

### Phase 5: Review and improve

Every 2–4 weeks (or when asked), ask them for the numbers. LinkedIn only exposes
analytics through its own UI or approved partners, so let them paste or screenshot
impressions, reactions, comments, profile views, follower growth, link clicks, and
leads or email sign-ups. Log these in `results.md`, point out patterns ("story
posts on Tuesday drove 3× the comments"), and propose changes to pillars, timing,
or CTAs. Let them decide what to change.

## Commands the user can say at any time

- "Write next week's LinkedIn posts" → Phase 4
- "Turn this into a LinkedIn post: …" → one post from their idea, notes, voice memo transcript, or article
- "Promote my new [offer / lead magnet]" → add to `lead-magnets.md` or `profile.md`, then plan a teaser sequence
- "Post this now" / "Schedule this for Thursday 9am" → pre-flight, approve, publish
- "What's in my queue?" → list `queue/` with dates and destinations
- "Update my profile / voice" → re-run just that interview round
- "How did last month do?" → Phase 5

## Reference files

- `references/interview.md`: the full question bank, in rounds
- `references/posting-methods.md`: the four ways to publish, with setup steps
- `references/linkedin-api-setup.md`: step-by-step LinkedIn developer app and token setup (Method D)
- `references/content-playbook.md`: neutral post formats, structure, and calendar planning
- `references/funnels.md`: connecting posts to lead magnets, opt-in pages, and email lists
- `templates/`: workspace file templates
- `scripts/`: `linkedin_auth.py` (one-time login) and `linkedin_post.py` (publishes due posts from `queue/`)

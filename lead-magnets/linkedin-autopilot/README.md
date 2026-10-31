# LinkedIn Autopilot: a Claude skill

Teach Claude to plan, write, schedule, and post your LinkedIn content for your
personal profile, your company Page, or both, so you show up consistently
without writing every post from scratch.

It starts as a **blank slate**. On first use, Claude interviews you about your
work, who you want to reach, what's happening in your business now and next,
how you write, and how often (if ever) you want to promote something. Then it builds a content plan and posts that sound like *you*, not
like a template.

## What it does

- Interviews you (in short rounds) about your work, goals, audience, and what's coming up
- Learns your voice from your own writing samples
- Uses your photos, brand assets, and marketing materials
- Builds content pillars and a rolling content calendar
- Writes **value-first** posts: real how-tos, checklists, stories, and lessons, each ending with an easy call to action like "try this before your next Monday team meeting"
- Promotes your services, free resources, or booking link **only if you want to and only as often as you choose**, and always after at least 3 value posts
- Schedules or publishes to your **personal profile** and/or **company Page** using the method you pick:
  - **A.** LinkedIn's built-in scheduler (free, copy and paste)
  - **B.** Zapier (hands-off, no code)
  - **C.** A scheduler you already use (Buffer, Hootsuite, GoHighLevel Social Planner, and others)
  - **D.** LinkedIn's official API with the included scripts (no subscription)
- Never posts anything without your approval, and never asks for your password

## Install

### Claude Code (terminal, desktop app, or IDE)
1. Unzip this folder.
2. Move the `linkedin-autopilot` folder to:
   - **All projects:** `~/.claude/skills/linkedin-autopilot/`
   - **One project only:** `<your-project>/.claude/skills/linkedin-autopilot/`
3. Start Claude Code and say: **"Set up my LinkedIn."**

### Claude.ai / Claude desktop app
1. Go to **Settings → Capabilities** (or **Skills**) and make sure Skills are turned on.
2. Click **Upload skill** and choose the `.zip` file.
3. Start a new chat and say: **"Set up my LinkedIn."**

> Automatic posting with Method D (the scripts) needs Claude Code or a computer
> that can run Python 3. Methods A–C work anywhere.

## First run

Plan on 15–20 minutes for the interview. Have these handy:
- Your website or LinkedIn "About" text
- (Optional) anything you might occasionally promote: services, free resources, a booking link
- 3–10 things you've written (past posts, emails, newsletters)
- A folder of photos or brand assets you like

Everything Claude learns is saved to a `linkedin-autopilot/` folder, so you only
do the interview once.

## Everyday prompts

- "Write next week's LinkedIn posts"
- "Turn this voice memo into a LinkedIn post"
- "I have a new service. Work it into the calendar, but keep it light"
- "Schedule the approved posts"
- "What's in my LinkedIn queue?"
- "Here are last month's numbers. What should we change?"

## What's inside

```
linkedin-autopilot/
├── SKILL.md                      # instructions Claude follows
├── references/
│   ├── interview.md              # the onboarding questions
│   ├── posting-methods.md        # the 4 ways to publish
│   ├── linkedin-api-setup.md     # step-by-step API setup (Method D)
│   ├── content-playbook.md       # post formats & calendar planning
│   └── ctas-and-offers.md        # soft calls to action + optional, limited promotion
├── templates/                    # profile, voice, calendar, post, results, GitHub Action
└── scripts/
    ├── linkedin_auth.py          # one-time LinkedIn login (official OAuth)
    └── linkedin_post.py          # publishes approved posts when they're due
```

## Good to know

- **Your account, your rules.** The skill only publishes your own content to your own profile or Page. No engagement pods, scraping, auto-connecting, or mass DMs, because those break LinkedIn's terms.
- **No pushy posts.** Posts never say "comment WORD to get it" and never hold value back. At least 3 value posts come before any promotional post, and you decide how often promotion happens (including never).
- **Company Page posting through the API** requires LinkedIn to approve your developer app for its Community Management API. Until then, use Method A, B, or C for your Page.
- LinkedIn updates its screens and API now and then. If a step looks different, tell Claude what you see and it'll help you through it.

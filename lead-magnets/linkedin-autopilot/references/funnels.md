# Turning posts into leads: lead magnets, opt-ins, and email

The goal: someone sees a post → takes one small step → lands on an opt-in page →
gets the free resource → joins the email list → gets a sequence that leads to an
offer.

```
LinkedIn post ─► CTA (link / comment / profile) ─► Opt-in page ─► Freebie delivered
                                                          │
                                                          └─► Email sequence ─► Offer / call
```

## 1. Record each lead magnet in `lead-magnets.md`

For each one: name, format, who it's for, the problem it solves, the opt-in page
URL, the email platform and list or tag, the sequence name and its final offer,
the CTA keyword (if using comment-to-get), and the UTM link.

If they don't have an opt-in page yet, help them choose a platform they already pay
for (GoHighLevel, Kit, Mailchimp, Beehiiv, Systeme, Kajabi, HubSpot, Flodesk, and
so on). Draft the page copy and a 3–5 email welcome sequence **in their voice**:
1. Deliver the freebie, plus one quick win
2. Their story / why this matters
3. A common mistake, plus how to fix it
4. Proof (a client result)
5. Invitation to the offer or a call

## 2. Pick a CTA style

| CTA style | Pros | Cons | Automatable? |
|---|---|---|---|
| Link in the post | Simplest, fewest steps | Some creators feel link posts get less reach. Test it on your account | Yes |
| Link in the first comment | Keeps the post clean | An extra step for the reader | Zapier or a scheduler can sometimes add a first comment. Otherwise the user posts it right after |
| "Comment WORD and I'll send it" | High engagement, starts conversations | Someone has to send each DM by hand | **No.** Reading comments and auto-DMing isn't available through LinkedIn's standard API, and third-party auto-DM tools risk the account |
| "Link in my Featured section / profile" | Drives profile visits | Lower click-through | N/A |
| "DM me WORD" | Opens a 1:1 conversation | Manual replies | No |

For comment-to-get, Claude prepares:
- a short, friendly DM template with the link, written in their voice
- a reminder in `calendar.md` to check comments 1, 4, and 24 hours after posting
- an optional "reply to comment" template ("Sent! Check your DMs")

Remind users: DM people who asked, and only once. No unsolicited follow-up blasts.

## 3. Track it

Add UTM tags to every link so they can see which posts drive sign-ups:

```
https://their-site.com/freebie?utm_source=linkedin&utm_medium=social&utm_campaign=<lead-magnet-slug>&utm_content=<post-date-or-id>
```

Use `utm_medium=organic_personal` vs `organic_page` if they post to both and
want to compare. In `results.md`, log sign-ups per post when they share numbers
from their email platform.

## 4. Teaser sequences for offers and lead magnets

When the user adds a new offer or freebie, propose a 1–3 week sequence such as:
1. **Problem post:** the pain the freebie or offer solves (no pitch)
2. **Value post:** one real insight from it (soft CTA)
3. **Story or proof post:** how it helped someone (CTA)
4. **Direct post:** what it is, who it's for, how to get it (clear CTA)
5. **Reminder or last call:** only if there's a real deadline

Never invent scarcity, deadlines, numbers, or testimonials.

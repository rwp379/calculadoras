# Handoff prompt: continue the PlanWellHome Pinterest work locally

Paste everything below the line into Claude Code (or Claude) on your local machine, opened in your clone of `rwp379/calculadoras`.

---

I'm continuing work on the Pinterest marketing for my Etsy shop **PlanWellHome**, which was started in a cloud session.

**Setup first:**
```
git fetch origin claude/pinterest-planwellhome-strategy-ns47ww
git checkout claude/pinterest-planwellhome-strategy-ns47ww
```
Read `marketing/pinterest-planwellhome-strategy.md` in full before doing anything. It has the research, the strategy and the account setup walkthrough. Keep everything in `marketing/`. Don't put anything in `docs/`: that's the public GitHub Pages site for my Portuguese calculators, and `build.py` deletes and regenerates it.

**What's been established (don't re-research these):**
- Pinterest **removed the option to claim Etsy shops in Feb 2022**, and `etsy.com` can't be claimed as a website. Any guide describing an Etsy claim flow is out of date. The working approach: pin specific Etsy listing URLs (Etsy listings usually show as product/rich pins with the price), put the shop URL in my Pinterest profile, and later claim my own domain (e.g. `planwellhome.com`) that links out to Etsy.
- Etsy Offsite Ads: 15% fee under $10k trailing 12-month sales (I can opt out), 12% and mandatory once I pass $10k.
- Pin specs: 1000×1500 (2:3), title up to 100 characters (keyword in the first ~40), description up to 500 characters, board names up to 50 characters, always fill in alt text.
- Strategy: new images matter more than re-pins. Start at 1–2 new pins a day and work up to 3–5. Plan seasonal content 45–60 days ahead. Turn each product into 10 pins using reusable Canva templates. Use 10 keyword-named boards (listed in section 2.3). It's late October 2026, so **New Year / "home reset" content comes first** and should be live by mid-December.
- Assumed product line: printable home planners (cleaning schedules, household budget, meal planning, home maintenance, moving checklists, routines/habit trackers). Another agent is building the actual products.

**My situation:**
- I **don't have a Pinterest business account yet**. My Etsy shop is PlanWellHome (shop URL: _fill in_).
- Final product list: _paste it here, or say "not ready yet"_.

**What I want from this session:**
1. **Walk me through creating and setting up the Pinterest business account live**, following section 3 of the strategy file one step at a time. Wait for me to confirm each step before moving on, and adjust if my screen doesn't match the instructions (Pinterest's menus change often). Check *Settings → Claimed accounts* with me in case an Etsy option appears.
2. Write the actual profile copy: display name, About text, and the 10 board names and descriptions, ready to paste.
3. Once I share the product list, map each product to boards and keywords and write 10 pin titles, descriptions and alt texts per product. Save them to `marketing/pins/<product>.md`.
4. Build a 4-week posting calendar starting with New Year content. Save it to `marketing/pinterest-calendar.md`.
5. Commit to the branch above with clear messages and push when I say so.

Before giving a click path, check it against Pinterest's help center if you can reach it. In the cloud session, help.pinterest.com and community.pinterest.biz were blocked, so the walkthrough is based on third-party guides.

# From nothing to a practice that brings in sellers

The formatted version of this runbook, with progress checkboxes, is at
<https://claude.ai/code/artifact/87c72972-63ef-45bc-8794-35cca97da751>.
This file is the same content, kept in the repo so it survives.

Thirty-eight steps in seven phases: the profiles people actually search, then the
website, then somewhere to keep the people who get in touch, then the wiring that
carries a lead from the form to her phone, and finally the campaigns that reach the
sellers who are not looking yet.

## Why this order

The two slowest steps are not technical. A Google Business Profile takes days to
verify, and Margie has to answer four questions before anything can be published.
Both are at the front, so the waiting happens while you build instead of after.

- **Accounts you will create:** Google Business Profile, a Facebook Page, Vercel,
  HubSpot and Resend. Every one is free at this scale. The domain is the only thing
  you pay for.
- **Two are hers, not yours.** The Google and Facebook profiles represent a licensed
  agent, so Margie creates them and adds you as a manager. Doing it under your own
  name breaks their rules and is a licensing problem for her.
- **The one blocker:** two brokerages are on file and one is wrong. Step 1 asks her.
- **Where the work is:** `~/north-shore-site`, already pushed. Every command runs
  from that folder.

---

## Phase 1: the profiles people actually search (~45 min, then days of waiting)

Nobody types a domain to find an agent. They search her name, or they search
"realtor near me" and look at the map. These two profiles answer both, they outrank
a new website for months, and one of them takes days to approve.

### 1. Have the one conversation with Margie

Everything that blocks this project blocks it because only she can answer. Ask for
all of it in one message rather than discovering each gap at the step it stops.

| Ask for | Because |
|---|---|
| **Which brokerage** | Berkshire Hathaway HomeServices Laffey lists her in Williston Park. The public record and her Bayville listing say Americana Realty Group in Syosset. New York requires the broker's name and office address on advertising, so nothing publishes until this is settled. |
| **Her direct phone and email** | The number on the page came off the public record, not from her. It is about to go on a Google listing. |
| **Manager access** | She creates the Google and Facebook profiles from her own accounts, then adds you as a manager. |
| **A portrait** | The slot on the site is deliberately empty rather than filled with a generated headshot. Google and Facebook want one too. |
| **Three testimonials** | No public reviews of her exist anywhere. First name, last initial, town, and her permission. |
| **Two photo sets** | 22 Lincoln Ave and 44 Tyrconnell Ave are not indexed on Zillow or Redfin, so they cannot be recovered any other way. |

**Watch out:** do not create either profile under your own name to save time. Google
requires the business owner to verify, Facebook Pages belong to a personal account,
and a listing that misrepresents who holds the licence is a problem for her. The
manager route takes her about two minutes.

### 2. Start the Google Business Profile, because it is the long pole

For a local agent this outranks the website itself, and verification can take
several days.

1. Margie goes to <https://business.google.com>, **Manage now**. If a listing
   already exists she claims it rather than making a second one.
2. Business name: **her own name**, e.g. *Margie Horowitz, Real Estate
   Salesperson*. Not the brokerage's name: it has its own listing and a duplicate
   gets both suppressed.
3. Category: **Real Estate Agent**, with **Real Estate Consultant** secondary.
4. Choose **service area** rather than a storefront unless clients visit an office
   she staffs. Add Syosset, Glen Cove, Glen Head, Jericho, Woodbury.
5. Phone: the number from step 1. Website: leave it, step 12 fills it.
6. Verification: postcard, phone, or video. Video is normally fastest for agents.
7. Once approved she adds you under **Business Profile settings**, **People and
   access**, as a **Manager**.

*Check:* search her name plus "Syosset" incognito. The profile shows on the right
with no "Claim this business" prompt.

### 3. Create the Facebook Page

Long Island sellers over fifty are on Facebook, and local town groups are where a
recommendation actually spreads.

1. From **her** personal account: <https://www.facebook.com/pages/create>.
2. Page name: the same string as the Google profile, character for character.
   Category: **Real Estate Agent**.
3. Bio, phone, service area. Leave the website field for step 12.
4. Profile picture: her portrait. Cover: `img/hero.jpg` from the repo, or one of her
   own listing photos.
5. She adds you at **Settings**, **Page access**, **Add New**, with full control.
6. Set the page button to **Book now** or **Learn more** once step 12 is done.

**Watch out:** most brokerages require agent pages to carry the broker's name and
follow their branding rules. Ask her compliance contact before the page goes public.

### 4. Connect an Instagram account to the Page

Optional, about twenty minutes. Listing photography is the one thing a real estate
practice generates constantly.

1. Create the account, or convert her existing one to a **Business** account under
   **Settings**, **Account type**.
2. Link it to the Page through <https://business.facebook.com> so one post reaches
   both.
3. Website in the bio link once step 12 is done.

If she will not post regularly, skip it. An account with four posts from last spring
reads worse than no account.

---

## Phase 2: the website (~35 min plus DNS)

The repository is already pushed and already carries a `vercel.json`. The site stays
closed to search engines throughout, which gets undone in phase 6.

### 5. Create the Vercel account

<https://vercel.com/signup>, **Continue with GitHub**, authorise against
`workflo17`. Pick **Hobby**: free, and it covers a site at this scale with a wide
margin.

*Check:* you land on a dashboard at `vercel.com/<your-username>` with an empty
project list.

### 6. Import the repository

1. Top right, **Add New…** then **Project**.
2. Under *Import Git Repository*, find `north-shore-site`.
3. Not listed? **Adjust GitHub App Permissions**, grant access to that repository,
   come back.
4. **Import**.

### 7. Set it up as a static site with functions

The one screen where a wrong default costs a failed deploy. There is no build step
in this project, so anything Vercel guesses about compiling it will be wrong.

| Field | What to set |
|---|---|
| Project Name | `north-shore-site`, which becomes `north-shore-site-workflo17.vercel.app` |
| Framework Preset | **Other**. Not Next.js, not Vite. |
| Root Directory | `./`, leave it alone |
| Build Command | empty, override off |
| Output Directory | empty |
| Install Command | empty |
| Environment Variables | skip, phase 4 handles these |

**Watch out:** `project.vercel.app` is claimed globally, first come first served, and
`north-shore-site.vercel.app` already belongs to an unrelated consulting firm. When
the short name is taken Vercel silently gives the project a longer alias instead, in
the shape `project-scope.vercel.app`. Read the real URL off the deployment rather
than assuming it, and use that one in step 11, or the canonical tag ends up pointing
at a stranger's website.

Click **Deploy**.

### 8. Confirm the deploy, including the function

    https://north-shore-site-workflo17.vercel.app/              # the page, concept bar on top
    https://north-shore-site-workflo17.vercel.app/robots.txt    # must say Disallow: /
    https://north-shore-site-workflo17.vercel.app/api/lead      # must answer, not 404

*Check:* opening `/api/lead` in a browser sends a GET, and the function answers
`{"ok":false,"error":"Use POST."}`. That refusal is the proof it is alive. A 404
means the function did not deploy: open the deployment, **Functions** tab, confirm
`api/lead.js` is listed.

### 9. Buy the domain

Her name is the strongest choice, because the people most likely to search already
got her name from a neighbour: `margiehorowitz.com`. A keyword domain like
`northshorehomevalue.com` reads like an ad and ages badly.

| Where | Roughly | Trade-off |
|---|---|---|
| Vercel Domains | $20/yr | DNS configures itself, costs a few dollars more |
| Cloudflare | $10/yr | at cost, but you add the records yourself |
| Namecheap, Porkbun | $11/yr | cheap first year, watch the renewal |

Have **her** buy it, or transfer it later. An agent whose personal domain is
registered to her marketing guy has a problem the day they part ways.

### 10. Point the domain at the project

1. Vercel, project, **Settings**, **Domains**, type the domain, **Add**.
2. Bought through Vercel: already done.
3. Bought elsewhere: Vercel prints the exact records. Usually an `A` record on the
   apex at `76.76.21.21` and a `CNAME` on `www` at `cname.vercel-dns.com`. Copy them
   off Vercel's screen rather than off this page, since those values are Vercel's to
   change.
4. Wait for the green check. Minutes usually, occasionally hours.
5. Pick one form as primary, apex or `www`, and let Vercel redirect the other.

### 11. Tell the code its own address

The address is written into eight places: the canonical tag, three Open Graph tags,
two structured-data blocks, the sitemap, and the `Sitemap:` line in `robots.txt`.
Miss one by hand and Google indexes the `vercel.app` preview instead.

```bash
python tools/configure.py --url https://margiehorowitz.com
python tools/configure.py --status
git commit -am "Point the site at its own domain"
git push
```

*Check:* view source on the live site, `<link rel="canonical">` carries the real
domain.

### 12. Put the address back on the profiles

Phase 1 left three website fields empty because there was nothing to put in them.

- **Google Business Profile:** the website field, and the primary action.
- **Facebook Page:** the website field, and the page button.
- **Instagram:** the bio link.

Use the exact primary form you chose in step 10, with or without `www`, everywhere.
Consistency across listings is the most common thing a local profile gets wrong.

---

## Phase 3: somewhere to keep the people who get in touch (~30 min)

This is the part most agent websites skip, and it is the part that turns a form into
commission. Build it before the form starts firing.

### 13. Understand what the CRM is actually for

No clicking. It is the argument for the whole phase, and it is written to be read
aloud or turned around on a laptop, because the person who has to believe it is
Margie. Everything from here to the next heading is for her.

#### The leak

Every agent has a version of the same one. Somebody calls in March asking what their
house is worth. Margie talks to them, sends comps, they say they are thinking about
spring next year. In September they list with somebody else.

Not because that agent was better. Because that agent called in July.

Nothing about that story is a lead-generation problem. The lead was already hers. It
was a memory problem, and it is the single most expensive one in the business,
because the deal was closer to signed than any cold call will ever be.

#### The question worth asking her, rather than a statistic

**"How many people asked you what their house was worth last year and then never
listed with anyone at all?"**

She will have a number. It is usually larger than the person saying it expects, and
it is a better argument than anything an industry report can supply, because it is
hers. Some of those people genuinely changed their minds. Some went quiet because
nobody stayed in front of them.

Then the arithmetic, which only has to be run once. The Nassau median single-family
price was $875,000 in June 2026. At a negotiated rate around two and a half per cent,
the listing side of a median sale is roughly $22,000 before the brokerage split.
Commission rates are negotiable and that figure is illustrative, but the shape holds:
**recovering one deal a year that would otherwise have drifted is worth more than
every other item on this runbook combined.** The tool costs nothing, so there is no
break-even to reach.

#### What the thing actually is

Three jobs, and they are not equally important. The first two are the ones people
think of, and the ones a notebook already half-solves.

| Job | In practice | Her phone and a notebook |
|---|---|---|
| A list of everyone | Every person who ever asked, with the address and how to reach them | Fine |
| A record of what was said | Calls, emails and notes on one timeline, so month four does not start from nothing | Badly, and only if she wrote it down |
| **A reminder of what is next** | "Call the Cedar Lane seller on the 14th" appearing on the 14th, without anyone remembering to look | **Not at all** |

The third one is the entire reason to do this. A CRM is not a database of people. She
already has that, and after nineteen years she has it in better shape than any
software will. What she does not have is a system that surfaces the right name on the
right morning without her thinking about it. That is what she is being handed.

#### One lead, all the way through

The part to walk through slowly. It is the whole product in eight rows.

| When | What happens | Who does it |
|---|---|---|
| Tue 9:14 | A homeowner on Split Rock Road fills in the valuation form | the website |
| Tue 9:14 | Her phone buzzes with the name, the address and what they said | automatic |
| Tue 9:14 | The same person appears in the CRM, marked New | automatic |
| Tue 9:22 | She calls while they are still on the website. Six minutes. Books a walkthrough for Thursday. | Margie |
| Tue 9:29 | Two taps: log the call, set the next task for Thursday | Margie |
| Thu 8:00 | "Split Rock walkthrough" is sitting at the top of her task list | automatic |
| Thu | Walkthrough, CMA and net sheet sent. They say spring, maybe. She sets a task for 1 February. | Margie |
| 1 Feb | The name comes back up on its own. She calls. They are ready. | automatic |

The competing agent who spoke to them that same week never called back in February.
That is the only difference between the two of them, and it is worth the whole
commission.

Note what is in the "Margie" column: two calls and about thirty seconds of tapping.
Everything else happens whether she remembers it or not. That ratio is the pitch.

#### What her mornings look like

She opens one screen. It shows the tasks due today, which on a normal week is two or
three names. She makes those calls, which she was going to make anyway, and sets the
next date before closing each one. Twenty minutes.

No data entry, no weekly review, nothing to maintain. If it ever feels like more than
that, it has been set up wrong, and step 15 is where that gets fixed.

#### What it will not do, said plainly

- It will not call anyone for her, or write anything for her.
- It will not tell her anything about a person that she does not put in.
- It does not replace her memory of people. It replaces her memory of dates, which is
  the part that fails.
- The free tier has no marketing automation and no mass email, which is deliberate.
  Sellers on the North Shore do not want a drip campaign from their neighbour's agent.

#### The objections she will actually raise

| She says | The honest answer |
|---|---|
| "I keep it all in my head." | She keeps the *people* in her head, and she is better at that than any software. Nobody keeps forty follow-up dates in their head. This is a calendar for the ones that are not appointments yet. |
| "I tried one and stopped." | Almost everyone does, usually because they were handed thirty fields to fill in per contact. This one is eight stages and a date. If it ever takes more than ten seconds a lead, it is set up wrong. |
| "I don't have time to learn software." | Fifteen minutes once, to see the screen. After that it is the twenty minutes of calls she was making anyway. |
| "What does it cost?" | Nothing. No time limit, no card, no trial that expires. The paid tiers are marketing automation she does not need at this volume. |
| "Whose is it?" | Hers. The account is in her name and her email. Add yourself as a user so you can set it up, and she can remove you in one click. |
| "What if I want out?" | Contacts export to a spreadsheet in two clicks and there is no contract. Worth saying out loud, because an agent should never be handed a system her marketing guy controls. |
| "My brokerage has one." | Then use theirs, and the website can point at it instead. Worth checking before step 14, because a brokerage CRM she already logs into beats a better one she does not. Ask what happens to those contacts if she ever changes brokerage; that answer often decides it. |

#### The one habit that makes or breaks it

**Never close a record without setting the next date.** That is the whole discipline.
Do that and the system works on its own. Skip it and the pipeline quietly turns back
into a list, and a list has never reminded anyone of anything.

#### Two things for you, not for her

**Why HubSpot rather than a real estate CRM.** Follow Up Boss, kvCORE and Sierra are
built for this industry and cost between $69 and $500 a month. What they add over
HubSpot is IDX search, drip campaigns and lead-source routing, none of which matter
until she has more leads than she can personally call. HubSpot's free tier has no time
limit, no card, a million contacts, tasks with reminders, a deal pipeline, email
logging, and an API the website can write to. Move to the industry tools when the
volume justifies the bill.

**Contact against deal,** because the vocabulary trips people up and you need it in
step 15. A **contact** is a person. A **deal** is one potential transaction. The same
contact can carry several deals over the years. The form creates contacts. You create
the deal when the lead turns into a real conversation.

### 14. Create the HubSpot account

1. <https://www.hubspot.com/products/get-started-free>, take the free CRM. No card.
2. **Whose email signs up matters.** If she has already agreed, use hers and have her
   add you at **Settings**, **Users and Teams**. If you are still building this to
   show her, use yours: a portal is handed over later by adding her as a super admin
   and stepping down, which takes two minutes and does not touch the data.
3. Answer the onboarding questions and skip every optional step. It will offer to
   connect an inbox and import contacts; both can wait.
4. Note which region your portal is in, `app.hubspot.com` or `app-eu1.hubspot.com`.

*Check:* **CRM**, **Contacts** loads and shows an empty table.

### 15. Build the pipeline around a seller, not a sales team

HubSpot ships with a generic sales pipeline whose stages are meaningless here.
Replace them, because the stage names are what you look at every morning.

1. **Settings** (gear, top right), **Objects**, **Deals**, **Pipelines**.
2. Rename the default pipeline to **Seller pipeline**.
3. Replace the stages. Each one is a thing that either happened or did not, which is
   what makes a pipeline honest.

| Stage | Means | The next action |
|---|---|---|
| New | The form fired. Nobody has spoken to them. | Call within the hour |
| Contacted | She reached them and they talked | Book the walkthrough |
| Valuation booked | A date is in the calendar | Pull the comps |
| CMA delivered | They have the number and the net sheet | Ask for the listing appointment |
| Listing appointment | The presentation is scheduled | Prepare, then ask for the signature |
| Listing signed | Signed agreement | Photography and go live |
| Closed won | It sold | Ask for the review, step 32 |
| Closed lost | Listed elsewhere, or not selling after all | Note why, follow up in six months |

Leads from the form land as **contacts** with status New, not as deals. Dragging a
contact into the pipeline yourself takes ten seconds and forces you to look at each
one. Automating it needs paid Workflows and is not worth the money at this volume.

**The habit that makes this work:** every time a deal moves, set the next task with
a date before you close the record. A pipeline with no tasks on it is a list, and a
list will not remind anyone of anything.

### 16. Create the private app token

How the website writes into the CRM. HubSpot's free tier includes private apps and
the contacts API, so no paid Workflow is needed.

1. **Settings**, **Integrations**, **Private Apps**.
2. **Create a private app**. Name it `north-shore-site`.
3. **Scopes** tab, search `contacts`, tick **crm.objects.contacts.write**. Ticking
   write usually selects read too, which is fine. Tick nothing else.
4. **Create app**, confirm, **Show token**, copy it. It starts `pat-`.

**Watch out:** that token can read and write your contacts. It goes into Vercel's
environment variables in step 20 and nowhere else. Never into the repository, never
into a message. If it leaks, delete the private app and make a new one.

### 17. Add the spreadsheet backup

Optional, ten minutes. A Google Sheet gives you a plain record that outlives any
account decision. Full recipe in appendix B. It produces a URL for
`LEAD_WEBHOOK_URL` in step 20, so a lead lands in both places at once.

---

## Phase 4: make the leads arrive (~25 min)

The form posts to a real function. That function writes every lead to the Vercel log
*before* it tries to deliver anywhere, so an outage at Resend or HubSpot cannot lose
one. On top of that log there are three independent channels.

### 18. Create a Resend key

Email is the channel that gets Margie to call someone back the same afternoon. The
CRM is where the lead lives; the email is what makes her look.

1. <https://resend.com>. Free tier is 3,000 emails a month, 100 a day.
2. **API Keys**, **Create API Key**. Name `north-shore-site`, permission **Sending
   access**, domain: all domains.
3. Copy the `re_…` key the moment it appears. Resend shows it once.

**Watch out:** until you verify a domain you can only send *from*
`onboarding@resend.dev` and only *to* the address that owns the Resend account.

### 19. Verify the sending domain

You have the domain now, from step 9.

Resend, **Domains**, **Add Domain**. It lists an MX and two TXT records (SPF and
DKIM). Add them in the same DNS panel you used in step 10, wait, **Verify**. Once
green, `LEAD_FROM` can be a real address on the domain, which is what keeps the
notification out of spam.

### 20. Add the environment variables

Vercel, project, **Settings**, **Environment Variables**. Tick all three
environments for each one.

| Name | Value | From |
|---|---|---|
| `RESEND_API_KEY` | the `re_…` key | step 18 |
| `LEAD_TO` | your email while testing. Comma-separate for two people. | you |
| `LEAD_FROM` | `Margie Horowitz Website <leads@yourdomain.com>`, or `onboarding@resend.dev` if step 19 is not done | step 19 |
| `HUBSPOT_TOKEN` | the `pat-…` token | step 16 |
| `LEAD_WEBHOOK_URL` | the Apps Script `/exec` URL, if you did step 17 | appendix B |

### 21. Redeploy, because saving the variables is not enough

The step almost everyone skips. The symptom is a form that looks like it worked
while nothing arrives anywhere. Variables are baked in at deploy time, so the
deployment currently live still has none of them.

**Deployments**, the top one, the `⋯` menu, **Redeploy**. Or push any commit.

### 22. Send a real lead and follow it to all four places

Open the live site and fill the form in as a seller would. **Take more than three
seconds over it**: a faster submission is treated as a bot and silently dropped.

*Check, in four places:*

1. **The page.** The button changes to "Thank you, I will be in touch" and the
   fields lock.
2. **The inbox.** The email arrives. Look in spam the first time.
3. **HubSpot.** Contacts shows the new person, with the address filled in and the
   timing and notes in the Message property.
4. **Vercel.** The **Logs** tab (newer accounts file it under **Observability**),
   filtered to `/api/lead`, has a line beginning `{"tag":"LEAD"`.

*If something is missing:* the lead is still in the log. DevTools, **Network**, the
`lead` request, **Response**. The `delivery` array names all three channels with
either `ok`, an `error`, or `"skipped":"not configured"`, which means a variable is
missing or you did not redeploy.

Then drag that test contact into the Seller pipeline and back out, so you have seen
the shape of the thing before a real one arrives. Then delete it.

---

## Phase 5: Margie's answers, applied (needs step 1 answered)

Everything up to here works without her. This is where her answers go into the page,
and it is the gate on publishing.

### 23. Set the brokerage everywhere it appears

New York requires a salesperson's advertising to carry the broker's name and
business address (19 NYCRR 175.25). It also has to match on the Google profile and
the Facebook Page.

```bash
grep -n tofill index.html   # lists all six spots waiting on her
```

The contact block and the footer both carry a note explaining the conflict between
the two brokerages. Delete those notes once the answer is in, or the page tells
every visitor about a problem that no longer exists.

### 24. Add the New York disclosures

The footer already carries the Equal Housing Opportunity mark and the "deemed
reliable" language. Two things still have to go beside them, taken from her
brokerage's own compliance materials rather than written fresh:

- The Fair Housing notice and the brokerage's fair housing disclosure.
- The Standard Operating Procedures, which New York requires a broker to publish.

### 25. Switch on the brokerage structured data

The page carries a second structured-data block, deliberately commented out, holding
the brokerage and office address. Search engines treat a wrong address worse than a
missing one, which is why it ships disabled.

1. In `index.html`, search for `BROKERAGE:BEGIN`.
2. Delete the `<!--` on the opening line and the `-->` on the closing line.
3. Replace `BROKERAGE NAME`, `STREET`, `TOWN` and `ZIP`.

*Check:* paste the live URL into <https://validator.schema.org>. One
`RealEstateAgent` with the address attached, no errors.

### 26. Drop in the portrait, the testimonials and the two photo sets

- **Portrait:** into the empty slot in the about section, and onto the Google and
  Facebook profiles at the same time so all three match.
- **Testimonials:** the three quotes replace the placeholders in "What clients say".
- **Photographs** for 22 Lincoln Ave and 44 Tyrconnell Ave go into `img/real/` as
  `p-glen-head.jpg` and `p-tyrconnell.jpg`, then run the sync so their
  "Representative image" badges disappear:

```bash
python tools/sync_real_photos.py
```

---

## Phase 6: open it to search, then keep it running (~20 min, then monthly)

### 27. Throw the switch

Three things change together: the `noindex` meta tag, the `Disallow` in
`robots.txt`, and the concept bar. Doing them by hand means eventually doing two of
the three.

```bash
python tools/configure.py --live
git commit -am "Publish"
git push
```

The command prints the compliance reminder from phase 5 and the count of `.tofill`
spots still on the page. If that count is not zero, stop and go back.

*Check:* no concept bar; view source shows
`content="index, follow, max-image-preview:large"`; `/robots.txt` says `Allow: /`.

To reverse at any point: `python tools/configure.py --concept`.

### 28. Look at the link before anyone else does

The social card is already built at `/og.jpg`. Paste the URL into
<https://www.opengraph.xyz>, or text the link to yourself and look at the preview.

**Watch out:** Facebook and LinkedIn cache the card hard. If you change `og.jpg`
later, run the URL through Facebook's Sharing Debugger and LinkedIn's Post Inspector
to force a refresh.

### 29. Register with Google Search Console

1. <https://search.google.com/search-console>, **Add property**, **URL prefix**,
   paste the full `https://` address.
2. Verification: **HTML tag** method, copy the
   `<meta name="google-site-verification" …>` line.
3. Paste it into `index.html` between the markers already waiting for it:

       <!-- SEARCHCONSOLE:BEGIN … -->
       <meta name="google-site-verification" content="…" />
       <!-- SEARCHCONSOLE:END -->

4. Commit, push, wait for the deploy, click **Verify**.
5. **Sitemaps**, enter `sitemap.xml`, **Submit**.
6. **URL Inspection**, paste the homepage, **Request Indexing**. This is the
   difference between appearing in days and appearing in weeks.

### 30. Add Bing, which takes one click

<https://www.bing.com/webmasters>, sign in, **Import from Google Search Console**.
It carries the verification and the sitemap across.

Worth the sixty seconds for a reason beyond Bing's own traffic: it is the index
behind ChatGPT's search.

### 31. Turn on analytics

The tracking scripts are already on the page. They set no cookies, so no consent
banner is needed.

1. Vercel, project, **Analytics** tab, **Enable**.
2. Vercel, project, **Speed Insights** tab, **Enable**.
3. Give it a day, then look at referrers. That is what tells you whether the leads
   came from Google, from the Facebook Page, or from a link she texted someone.

### 32. Set the two recurring habits

**Monthly, five minutes.** Submit a test lead through the live form and confirm it
reaches the inbox and HubSpot. An expired API key or a plan change fails silently,
and a form that quietly stopped working is worse than no form. The Vercel log is the
backstop, but only if someone looks.

**After every closing.** Ask the seller for a Google review, with a link straight to
the review form. For a local agent, review count moves the map ranking harder than
anything you can change on the website. That is why step 15's last pipeline stage
has "ask for the review" as its next action: it belongs in the process, not in
someone's memory.

Once three or four reviews exist they can come back onto the site and replace the
testimonial placeholders from step 26 with something checkable.

---

## Phase 7: campaigns, and the one Margie already thought of (a season's work)

Everything before this makes her findable by people already looking. This phase is
about the people who are not looking yet, which on the North Shore is most of the
sellers she wants.

### 33. Anchor every campaign to the thing only she has

Before any of the fun starts, the filter. Margie's difference is not that she is
friendly or local or hardworking, because every agent on the Island says that and
sellers have stopped hearing it. Her difference is on the website already: **she
publishes the four sales that closed under asking.** Nobody else in Nassau does that.

So every campaign gets one test. **Does this make somebody believe she tells sellers
the truth?** A funny flier that does not is a wasted December. A funny flier that does
is worth more than a year of boosted posts, because it is the one claim her
competitors cannot copy without publishing their own misses.

*Use this on every idea below:* ask what a seller knows about her after seeing it that
they did not know before. If the answer is "she is fun on the internet", cut it or fix
it. If the answer is "she will tell me the truth about my house", ship it.

### 34. The December campaign: "You're going to sell your home. Alone?"

Margie's own idea, and a good one. It earns its place for three reasons that have
nothing to do with the joke.

- **The timing is the strategy.** Almost nobody lists in December, so almost nobody
  markets in December. It is also the exact month a homeowner planning a spring
  listing starts thinking about it. Cheapest attention of the year, aimed at people
  who are three months from a decision.
- **The pun does real work.** "Alone" is not just the gag, it is the pitch: it names
  for-sale-by-owner without saying anything insulting about the seller. The line asks
  a question rather than making a claim, so it lands as a raised eyebrow, not a
  lecture.
- **The geography is a gift.** The most famous house in the film sits on the North
  Shore, the one outside Chicago, and it is a big center-hall colonial that could pass
  for Glen Head. She can say *"the most famous house on any North Shore"* and every
  adult who reads it gets it, without a single protected word.

**Where the legal line sits, and it matters more than usual here.** This is commercial
advertising for a service, which is the weakest possible ground for a fair use or
parody argument. The safe version is easy, so take it.

*Fine to use:* the sentence "You're going to sell your home. Alone?", because those are
ordinary English words. A snowy center-hall colonial at dusk with warm windows. Red and
green. String lights. Anything shot or drawn from scratch.

*Do not use:* the film's title as a headline, caption or hashtag; the poster's
hands-to-cheeks pose; any still, clip or frame; the score; character or family names;
the quotable lines; a photograph of the actual house in Winnetka. Do not imply any
studio connection.

Her brokerage's compliance people have to approve the piece anyway, which is another
reason step 23 has to land before this does.

### 35. Write and place the flier

One side, 5.5 by 8.5 inches so four fit on a sheet, or a 6 by 9 postcard for mail.
Copy first, design second.

| Slot | What it says |
|---|---|
| Headline | **You're going to sell your home. Alone?** |
| Subhead | Five of my last nine listings sold above the asking price. Four did not. Both numbers are on my website. |
| Body | Selling it yourself saves the commission and costs you the pricing, the marketing, the negotiation and every hour of it. Before you decide, get the real number for your street. It is free, and I will tell you if you should wait. |
| Call to action | See the whole record, misses included, plus a free valuation. A QR code, and the domain printed underneath for the people who will not scan it. |
| Footer | Name, licence number, brokerage name and office address, and the Equal Housing Opportunity mark. New York requires the broker details on advertising, and this is advertising. |

**The last line of the body is the whole campaign.** "I will tell you if you should
wait" is a listing agent volunteering to talk someone out of a listing. It is the
flier's proof of the thing the website argues, and it is what makes the joke land as
confidence rather than as a gimmick.

**Where it goes,** in order of how well it pays:

1. **Every for-sale-by-owner sign in her towns.** Drive the routes on a Sunday. These
   people have already decided to sell alone, which makes them the only audience the
   headline is literally about. Hand delivered, not mailed.
2. **Expired and withdrawn listings** from the last six months, off the MLS. They
   tried, it did not work, and they are deciding what to do in spring right now.
3. **The five streets around each of her nine past sales.** She has a real result to
   point at within walking distance, which is the only mailing list where a cold piece
   is not cold.

Blanket-mailing a zip code is how this money gets wasted. The three lists above are a
few hundred pieces, not a few thousand.

### 36. Build the video engine, not the viral video

Worth saying plainly to her: nobody can make a video go viral on purpose. What is
buildable is a format that pays even when it does not, and a back catalogue that keeps
working. Seven that fit a listing agent on this stretch of Long Island, roughly in
order of how reliably they perform.

| Format | What it is | Why it works for her |
|---|---|---|
| **The honest walkthrough** | She films one of her own listings and says out loud what is wrong with it. The bathroom is dated. The driveway is short. Here is what it will cost you. | The flagship. It is the closing record in video form, and almost no agent will do it, which is exactly why it travels. |
| What $875,000 buys | One price, three towns, forty-five seconds. Syosset against Glen Cove against Massapequa Park. | The most dependable performer in real estate video, and she has sales in all three to pull from. |
| "I told them not to" | Renovations that lose money on the North Shore. The wrong kitchen, the pool, the converted garage. | Sellers search this before they spend $40,000. It positions her as the person who saves you money before she makes any. |
| The net sheet reveal | "It sold for $661,500. Here is what they actually walked away with." Real numbers, real deductions. | The site already has the calculator. Almost nobody publishes the gap between sale price and cheque. |
| The thirty-day house | One listing, one clip a week, photography day through closing. | Serialised, so the audience comes back. Also the best listing-presentation asset she will ever own. |
| Local knowledge | Which Syosset streets are in which school district. What the LIRR run really costs in time. Which blocks took water. | Nineteen years is the moat. An agent parachuting in from Queens cannot fake any of it. |
| Reading the FSBO listing | She reads a real for-sale-by-owner ad and gently explains what it is going to cost them. | The December campaign as a running series, and the two feed each other. |

Start with three formats, not seven. Run them for eight weeks, keep the two that get
saved and shared, and drop the rest without ceremony.

### 37. Set up the kit and the batching day

The reason agents stop posting is never the camera. It is that every video is a
separate act of will. Batching removes that.

- **The kit:** her phone, a $20 clip-on microphone, and daylight. Nothing else. A $600
  camera makes the video look more like an advert, which is worse.
- **Vertical, thirty to sixty seconds,** with the point in the first three seconds. No
  slow intro, no logo sting, no "hi guys".
- **Burned-in captions, always.** Most people watch on mute. The editing app does this
  automatically now; check the spelling of the town names, which it will get wrong.
- **One file, three places:** Instagram Reels, TikTok, YouTube Shorts, posted natively
  to each rather than sharing a link. Facebook gets it too through the page from step 3.
- **The batching day:** one afternoon a month, six videos, at whichever listing she has
  access to. Change her jacket between a couple so they do not look like one sitting.

Six a month is one a week with two in hand for the week something goes wrong. That
buffer is the difference between a channel that survives March and one that does not.

### 38. Measure the right thing, and carry the required line

**Views are the number that will mislead her.** A video seen by forty thousand people
in Arizona is worth nothing. A video seen by nine hundred people in Syosset that gets
thirty saves is worth a listing.

| Watch | Ignore |
|---|---|
| **Saves and shares.** A save is somebody bookmarking her for spring. | View count on its own |
| **Direct messages,** especially "are you taking listings" | Follower count |
| **Where the viewers are.** Nassau or nothing. | Likes |
| **Referrers in Vercel Analytics** from step 31, and leads in the CRM tagged to the campaign | Watch time on a thirty-second clip |

The honest measurement window is a full season. Content compounds slowly and then all
at once, and judging it at three weeks is how people quit at week four.

**Two lines every single piece has to carry.**

*The broker.* New York requires her advertising to carry the broker's name and office
address, and that includes video captions and end cards, not just the flier. This is
the same blocker as step 23, which is why the campaign cannot ship before it clears.

*Fair Housing.* Never describe a neighbourhood by the people who live in it. Not the
schools "being a certain kind", not "family area", not "safe", not who the buyers
usually are. Talk about the houses, the taxes, the commute and the lot sizes. This is
the trap that catches agents making town-comparison videos, and it is the one mistake
in this phase with real consequences.

---

## Appendix A: every environment variable

All optional. With none set, the form still validates, still screens bots, and still
records every lead in the Vercel runtime log.

| Name | Example | Missing means |
|---|---|---|
| `RESEND_API_KEY` | `re_ab12…` | no email is sent |
| `LEAD_TO` | `margie@…, don@…` | no email is sent |
| `LEAD_FROM` | `Website <leads@…>` | no email is sent |
| `HUBSPOT_TOKEN` | `pat-na1-…` | no contact is created |
| `LEAD_WEBHOOK_URL` | `https://script.google…/exec` | no webhook is posted |

The three delivery channels are independent. One failing does not stop the others,
and none of them can stop the log write, which happens first.

## Appendix B: the spreadsheet backup, at no cost

The CRM is where a lead gets worked. The sheet is a plain record that outlives any
account decision and answers "how many came in last quarter" in one glance.

1. New Google Sheet. Rename the first tab to `Leads`.
2. Row 1 headers: `Received`, `Name`, `Contact`, `Address`, `Timing`, `Note`, `Page`.
3. **Extensions**, **Apps Script**. Delete what is there and paste:

```javascript
function doPost(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Leads');
  const lead = JSON.parse(e.postData.contents);
  sheet.appendRow([
    new Date(), lead.name, lead.contact, lead.address,
    lead.timing, lead.note, lead.page
  ]);
  return ContentService
    .createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

4. **Deploy**, **New deployment**, type **Web app**.
5. Execute as **Me**. Who has access **Anyone**. It has to be "Anyone" or Vercel
   cannot reach it. The URL is unguessable and the script only ever appends.
6. Authorise. Google warns the script is unverified, which is normal for your own
   script: **Advanced**, then **Go to (project name)**.
7. Copy the deployment URL ending in `/exec`. That is `LEAD_WEBHOOK_URL`.
8. Add it in Vercel, redeploy (step 21 again), send a test lead.

*Check:* a new row appears within a second or two, and the form's network response
shows `{"channel":"webhook","ok":true}`.

The same variable takes a Zapier catch hook, a Make webhook, or a Slack incoming
webhook. Anything that accepts a JSON POST works.

## Appendix C: what the CRM channel actually sends

| Form field | HubSpot property | Note |
|---|---|---|
| Your name | `firstname`, `lastname` | split at the first space |
| Phone or email | `email` or `phone` | whichever it looks like, never both |
| Property address | `address` | omitted when blank |
| Timing and notes | `message` | combined, with the page it came from |
| (always) | `lifecyclestage`, `hs_lead_status` | set to Lead and New |

Two behaviours worth knowing. If a portal does not have the default `message`
property, the write is retried without it rather than failing, so the contact is
never lost to a schema difference. And if the email is already a contact, HubSpot
answers 409 and the function counts that as delivered, because already knowing
someone is not an error.

## Appendix D: working on it locally

```bash
node tools/dev_server.mjs            # site + working API on :5130
node tools/test_lead_api.mjs         # 26 checks on the lead function
python tools/configure.py --status   # indexing state, site URL, tofill count
python tools/build_brand_assets.py   # rebuild og.jpg and the icon set
```

To test real delivery locally, pass the keys on the command line rather than putting
them in a file:

```bash
RESEND_API_KEY=re_… LEAD_TO=you@example.com \
  LEAD_FROM=onboarding@resend.dev HUBSPOT_TOKEN=pat-na1-… \
  node tools/dev_server.mjs
```

Run `test_lead_api.mjs` before any push that touches the form.

## Appendix E: when something goes wrong

| Symptom | Almost always |
|---|---|
| `/api/lead` returns 404 | Framework Preset was not **Other**, or a build command overwrote the output. Step 7. |
| Form says sent, nothing arrives anywhere | You did not redeploy after adding the variables. Step 21. |
| Email in spam | `LEAD_FROM` is still `onboarding@resend.dev`. Step 19. |
| Resend: "can only send to your own address" | Domain not verified. Expected. Step 19. |
| Email arrives, HubSpot stays empty | The `delivery` array names the reason. A `401` is a bad or deleted token; a `403` is a missing scope, so re-check `crm.objects.contacts.write` in step 16. |
| HubSpot contact has no address or notes | The portal is missing a default property and the retry dropped the extras. Appendix C. |
| Submitting does nothing at all | Open the console. Fetch failing means the function is down; nothing firing means a JS error stopped the handler binding. |
| Nothing recorded, no error shown | Under three seconds from page load, so it scored as a bot. Reload and take your time. |
| Google shows the vercel.app URL | `configure.py --url` was never run. Step 11. |
| Nothing indexed after two weeks | Search Console, URL Inspection, read the coverage reason. Usually `robots.txt` is still closed. |
| Google profile will not verify | Service-area businesses often fail the postcard and pass the video. The video has to show signage or office, a work tool, and you logged into the profile. |
| Old social card keeps appearing | Facebook or LinkedIn cache. Their debuggers force a refresh. Step 28. |

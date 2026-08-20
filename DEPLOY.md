# Putting this site online

The formatted version of this runbook, with progress checkboxes, is at
<https://claude.ai/code/artifact/87c72972-63ef-45bc-8794-35cca97da751>.
This file is the same content, kept in the repo so it survives.

Twenty-four steps in six phases. Phases 1 to 3 can run today. Phase 5 cannot start
until Margie answers the questions in phase 4.

**Before you start:** a Vercel account (free), a Resend account (free), the GitHub
account `workflo17`, and a domain (roughly $12 to $20 a year). Every command below
runs from `~/north-shore-site`.

---

## Phase 1: get it on Vercel (~15 min)

The repository is already pushed and already carries a `vercel.json`, so this phase
is mostly clicking. Nothing here is public to search engines yet, by design.

### 1. Create the Vercel account

<https://vercel.com/signup>, choose **Continue with GitHub**, authorise against
`workflo17`. Pick the **Hobby** plan: free, and it covers a site at this scale with
a wide margin.

*Check:* you land on a dashboard at `vercel.com/<your-username>` with an empty
project list.

### 2. Import the repository

1. Top right, **Add New…** then **Project**.
2. Under *Import Git Repository*, find `north-shore-site`.
3. Not listed? Click **Adjust GitHub App Permissions**, grant access to that one
   repository, come back.
4. Click **Import**.

### 3. Set it up as a static site with functions

The one screen where a wrong default costs a failed deploy. There is no build step
in this project, so anything Vercel guesses about compiling it will be wrong.

| Field | What to set |
|---|---|
| Project Name | `north-shore-site`, which becomes `north-shore-site.vercel.app` |
| Framework Preset | **Other**. Not Next.js, not Vite. |
| Root Directory | `./`, leave it alone |
| Build Command | empty, override off |
| Output Directory | empty |
| Install Command | empty |
| Environment Variables | skip, phase 2 handles these |

Click **Deploy**.

### 4. Confirm the deploy, including the function

Thirty to sixty seconds. Then check three URLs by hand:

    https://north-shore-site.vercel.app/              # the page, concept bar on top
    https://north-shore-site.vercel.app/robots.txt    # must say Disallow: /
    https://north-shore-site.vercel.app/api/lead      # must answer, not 404

*Check:* opening `/api/lead` in a browser sends a GET, and the function answers
`{"ok":false,"error":"Use POST."}`. That refusal is the proof it is alive. A 404
instead means the function did not deploy: open the deployment, click the
**Functions** tab, confirm `api/lead.js` is listed.

---

## Phase 2: make the leads arrive somewhere (~20 min)

The form posts to a real function. That function writes every lead to the Vercel log
*before* it tries to send anything, so a mail outage cannot lose one. On top of that
log there are two independent delivery channels.

### 5. Pick where leads go

| Channel | Good for | Set up in |
|---|---|---|
| Email (Resend) | Margie reading a lead on her phone within seconds | steps 6 to 8 |
| Webhook | A permanent record: a Google Sheet, Zapier, a CRM later | appendix B |
| Runtime log | The backstop. Always on, nothing to configure. | already working |

Start with email. Add the webhook once leads are actually coming in.

### 6. Create a Resend key

1. Sign up at <https://resend.com>. Free tier is 3,000 emails a month, 100 a day.
2. Sidebar, **API Keys**, **Create API Key**.
3. Name `north-shore-site`. Permission **Sending access**. Domain: all domains.
4. Copy the `re_…` key the moment it appears. Resend shows it once.

**Watch out:** until you verify a domain in Resend you can only send *from*
`onboarding@resend.dev` and only *to* the address that owns the Resend account.
Fine for testing. Sending to Margie's inbox needs step 7.

### 7. Verify a sending domain

Skip if the domain is not bought yet; come back after phase 3.

Resend, **Domains**, **Add Domain**. It lists an MX and two TXT records (SPF and
DKIM). Add them at your DNS host, wait, click **Verify**. Once green, `LEAD_FROM`
can be a real address on the domain, which is what keeps the notification out of
spam.

### 8. Add the environment variables

Vercel, project, **Settings**, **Environment Variables**. Tick all three
environments for each one.

| Name | Value |
|---|---|
| `RESEND_API_KEY` | the `re_…` key from step 6 |
| `LEAD_TO` | your email while testing. Comma-separate for two people. |
| `LEAD_FROM` | `onboarding@resend.dev` until step 7, then `Margie Horowitz Website <leads@yourdomain.com>` |
| `LEAD_WEBHOOK_URL` | optional, appendix B |

### 9. Redeploy, because saving the variables is not enough

The step almost everyone skips. The symptom is a form that looks like it worked
while no email ever arrives. Variables are baked in at deploy time, so the
deployment currently live still has none of them.

**Deployments**, the top one, the `⋯` menu, **Redeploy**. Or push any commit.

### 10. Send yourself a real lead

Open the live site and fill the form in as a seller would. **Take more than three
seconds over it**: a faster submission is treated as a bot and silently dropped.

*Check, in three places:*

1. The button changes to "Thank you, I will be in touch" and the fields lock.
2. The email arrives. Look in spam the first time.
3. Vercel, project, **Logs** tab (newer accounts file it under **Observability**).
   Filter for `/api/lead`. There is a line beginning `{"tag":"LEAD"` with every
   field in it.

*If the email never came:* the lead is still in the log, so nothing is lost. Open
DevTools, **Network**, click the `lead` request, **Response**. The `delivery` array
names each channel and its error. `"skipped":"not configured"` means a variable is
missing or you did not redeploy.

---

## Phase 3: give it an address of its own (~20 min plus DNS)

### 11. Buy the domain

Her name is the strongest choice, because the people most likely to search already
got her name from a neighbour: `margiehorowitz.com`. A keyword domain like
`northshorehomevalue.com` reads like an ad and ages badly.

| Where | Roughly | Trade-off |
|---|---|---|
| Vercel Domains | $20/yr | DNS configures itself, costs a few dollars more |
| Cloudflare | $10/yr | at cost, but you add the records yourself |
| Namecheap, Porkbun | $11/yr | cheap first year, watch the renewal |

If it is Margie's own name, have **her** buy it, or transfer it to her later. An
agent whose personal domain is registered to her marketing guy has a problem the day
they part ways.

### 12. Point the domain at the project

1. Vercel, project, **Settings**, **Domains**, type the domain, **Add**.
2. Bought through Vercel: already done.
3. Bought elsewhere: Vercel prints the exact records. Usually an `A` record on the
   apex at `76.76.21.21` and a `CNAME` on `www` at `cname.vercel-dns.com`. Copy them
   off Vercel's screen rather than off this page, since those values are Vercel's to
   change.
4. Wait for the green check. Minutes usually, occasionally hours.
5. Pick one form as primary, apex or `www`, and let Vercel redirect the other.

### 13. Tell the code its own address

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

---

## Phase 4: the four things only Margie can supply (blocked)

Phases 1 to 3 can all happen today because the site stays closed to search engines
throughout. This phase is the gate on phase 5.

### 14. Settle which brokerage she is with

Berkshire Hathaway HomeServices Laffey lists her in Williston Park. The public sale
record and her active Bayville listing put her at Americana Realty Group in Syosset,
where she does not appear on the public team page. One of those is stale.

Not a cosmetic gap: New York requires a salesperson's advertising to carry the
broker's name and business address (19 NYCRR 175.25).

```bash
grep -n tofill index.html   # lists all six spots waiting on her
```

### 15. Add the New York disclosures

The footer already carries the Equal Housing Opportunity mark and the "deemed
reliable" language. Two things still have to go beside them, taken from her
brokerage's own compliance materials rather than written fresh:

- The Fair Housing notice and the brokerage's fair housing disclosure.
- The Standard Operating Procedures, which New York requires a broker to publish.

### 16. Switch on the brokerage structured data

The page carries a second structured-data block, deliberately commented out, holding
the brokerage and office address. Search engines treat a wrong address worse than a
missing one, which is why it ships disabled.

1. In `index.html`, search for `BROKERAGE:BEGIN`.
2. Delete the `<!--` on the opening line and the `-->` on the closing line.
3. Replace `BROKERAGE NAME`, `STREET`, `TOWN` and `ZIP`.

*Check:* paste the live URL into <https://validator.schema.org>. One
`RealEstateAgent` with the address attached, no errors.

### 17. Collect the portrait and three testimonials

The portrait slot is deliberately empty rather than filled with a generated
headshot, and there are no public reviews of her anywhere to quote.

- One portrait, landscape or square, as large as she has it.
- Three seller testimonials with first name, last initial, town, and permission.
- Photographs for **22 Lincoln Ave** and **44 Tyrconnell Ave**, the two sales not
  indexed on Zillow or Redfin, which cannot be recovered any other way.

She should also confirm the phone number, which came from the public record rather
than from her.

---

## Phase 5: open it to search (~15 min)

### 18. Throw the switch

Three things change together: the `noindex` meta tag, the `Disallow` in
`robots.txt`, and the concept bar. Doing them by hand means eventually doing two of
the three.

```bash
python tools/configure.py --live
git commit -am "Publish"
git push
```

The command prints the compliance reminder from phase 4 and the count of `.tofill`
spots still on the page. If that count is not zero, stop and go back.

*Check:* no concept bar; view source shows
`content="index, follow, max-image-preview:large"`; `/robots.txt` says `Allow: /`.

To reverse at any point: `python tools/configure.py --concept`.

### 19. Look at the link before anyone else does

The social card is already built at `/og.jpg`. Paste the URL into
<https://www.opengraph.xyz>, or text the link to yourself and look at the preview.

**Watch out:** Facebook and LinkedIn cache the card hard. If you change `og.jpg`
later, run the URL through Facebook's Sharing Debugger and LinkedIn's Post Inspector
to force a refresh.

### 20. Register with Google Search Console

1. <https://search.google.com/search-console>, **Add property**, **URL prefix**,
   paste the full `https://` address.
2. Verification: **HTML tag** method, copy the `<meta name="google-site-verification"
   …>` line.
3. Paste it into `index.html` between the markers already waiting for it:

       <!-- SEARCHCONSOLE:BEGIN … -->
       <meta name="google-site-verification" content="…" />
       <!-- SEARCHCONSOLE:END -->

4. Commit, push, wait for the deploy, click **Verify**.
5. **Sitemaps** in the sidebar, enter `sitemap.xml`, **Submit**.
6. **URL Inspection**, paste the homepage, **Request Indexing**. This is the
   difference between appearing in days and appearing in weeks.

### 21. Add Bing, which takes one click

<https://www.bing.com/webmasters>, sign in, **Import from Google Search Console**.
It carries the verification and the sitemap across.

Worth the sixty seconds for a reason beyond Bing's own traffic: it is the index
behind ChatGPT's search.

---

## Phase 6: the presence that is not the website (~40 min, then ongoing)

A brand new domain ranks for almost nothing for months. Everything here borrows
authority from places that already rank, which is where the early leads come from.

### 22. Claim the Google Business Profile

For a local agent this outranks the website itself, and it is free.

1. <https://business.google.com>, **Manage now**.
2. Business name: **her own name**, e.g. *Margie Horowitz, Real Estate
   Salesperson*. Not the brokerage's name: the brokerage has its own listing and
   duplicating it gets both suppressed.
3. Category: **Real Estate Agent**.
4. Choose **service area** rather than a storefront unless clients visit an office
   she staffs. Add Syosset, Glen Cove, Glen Head, Jericho, Woodbury.
5. Website: the new domain. Phone: the number she confirmed in step 17.
6. Verification: postcard, phone, or video. Video is normally fastest for agents.

Once live, add photos and set the website action. Then ask past clients for reviews.
For a local agent, review count moves rankings harder than anything on the site.

### 23. Link the site from every profile that already ranks

Search her name today and you get Homes.com and FastExpert, not this site. Adding
the website link to each one sends real traffic and tells Google the new domain
belongs to the person on those established profiles.

| Profile | Do this |
|---|---|
| Homes.com | claim it if she has not, add the website link |
| FastExpert | add the link, correct the $38M figure if stale |
| Zillow | claim the agent profile, add the link, ask for reviews |
| Realtor.com | same |
| Her brokerage page | ask the office to add the link to her bio |
| LinkedIn, Facebook | website field, pin one post about the valuation offer |

Keep the name, phone and address identical everywhere, character for character.
Inconsistency across listings is the most common reason a local profile
underperforms.

### 24. Turn on analytics and set a monthly reminder

The tracking scripts are already on the page. They do nothing until the products are
switched on, and they set no cookies, so no consent banner is needed.

1. Vercel, project, **Analytics** tab, **Enable**.
2. Vercel, project, **Speed Insights** tab, **Enable**.
3. Give it a day, then look at referrers.

**The one recurring task:** once a month, submit a test lead through the live form
and confirm the email lands. An expired API key or a plan change fails silently, and
a form that quietly stopped working is worse than no form. The Vercel log is the
backstop, but only if someone looks.

---

## Appendix A: every environment variable

All optional. With none set, the form still validates, still screens bots, and still
records every lead in the Vercel runtime log.

| Name | Example | Missing means |
|---|---|---|
| `RESEND_API_KEY` | `re_ab12…` | no email is sent |
| `LEAD_TO` | `margie@…, don@…` | no email is sent |
| `LEAD_FROM` | `Website <leads@…>` | no email is sent |
| `LEAD_WEBHOOK_URL` | `https://script.google…/exec` | no webhook is posted |

## Appendix B: leads into a Google Sheet, at no cost

Email gets Margie to call someone back the same afternoon, but a year of leads
buried in an inbox cannot be sorted or counted.

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
8. Add it in Vercel, redeploy (step 9 again), send a test lead.

*Check:* a new row appears within a second or two, and the form's network response
shows `{"channel":"webhook","ok":true}`.

The same variable takes a Zapier catch hook, a Make webhook, or a Slack incoming
webhook. Anything that accepts a JSON POST works.

## Appendix C: working on it locally

```bash
node tools/dev_server.mjs            # site + working API on :5130
node tools/test_lead_api.mjs         # 17 checks on the lead function
python tools/configure.py --status   # indexing state, site URL, tofill count
python tools/build_brand_assets.py   # rebuild og.jpg and the icon set
```

To test real email delivery locally, pass the key on the command line rather than
putting it in a file:

```bash
RESEND_API_KEY=re_… LEAD_TO=you@example.com \
  LEAD_FROM=onboarding@resend.dev node tools/dev_server.mjs
```

Run `test_lead_api.mjs` before any push that touches the form.

## Appendix D: when something goes wrong

| Symptom | Almost always |
|---|---|
| `/api/lead` returns 404 | Framework Preset was not **Other**, or a build command overwrote the output. Step 3. |
| Form says sent, no email | You did not redeploy after adding the variables. Step 9. |
| Email in spam | `LEAD_FROM` is still `onboarding@resend.dev`. Step 7. |
| Resend: "can only send to your own address" | Domain not verified. Expected. Step 7. |
| Submitting does nothing at all | Open the console. Fetch failing means the function is down; nothing firing means a JS error stopped the handler binding. |
| Nothing recorded, no error shown | Under three seconds from page load, so it scored as a bot. Reload and take your time. |
| Google shows the vercel.app URL | `configure.py --url` was never run. Step 13. |
| Nothing indexed after two weeks | Search Console, URL Inspection, read the coverage reason. Usually `robots.txt` is still closed. |
| Old social card keeps appearing | Facebook or LinkedIn cache. Their debuggers force a refresh. Step 19. |

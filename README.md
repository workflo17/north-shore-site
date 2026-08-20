# North Shore seller site: a design concept

A one-page seller-facing site for Margie Horowitz, a listing agent working Syosset and the
North Shore of Long Island. The page has one job: get a homeowner who is thinking about
selling to ask for a valuation.

Live at <https://workflo17.github.io/north-shore-site/>. It carries `noindex, nofollow` and a
concept bar at the top, so it is safe to send to Margie without it turning up in search.

## Where every number on the page comes from

Nothing on this page is invented. Two sources, and the page marks which is which, because a
seller who checks and finds the claim holds is worth more than a seller who is impressed.

### From the public sale record

Margie's [Homes.com profile](https://www.homes.com/real-estate-agents/margie-horowitz/k2g7gxc/)
carries her transaction history for the last five years, drawn from public records: twelve
closed sales, $8.8M in total value, eleven of them seller-side. Nine are itemised with an
address, a closing price, days on market, and the percentage against the asking price. Those
nine are the carousel and the list underneath it.

| Property | Town | Closed | vs ask | Days | Date |
|---|---|---|---|---|---|
| 22 Lincoln Ave | Glen Head | $1,500,000 | +7% | 16 | Dec 2022 |
| 1542 84th St | Brooklyn | $988,000 | −14% | 75 | Mar 2023 |
| 2631 Irene Ln | Seaford | $950,000 | +6% | 9 | Jun 2022 |
| 6 Wood Ave | Albertson | $830,000 | +4% | 17 | Oct 2022 |
| 98 Cortelyou St | Islip | $670,000 | +3% | 107 | Apr 2024 |
| 214 Lawrence Ln | Glen Cove | $661,500 | −5% | 31 | Nov 2022 |
| 44 Tyrconnell Ave | Massapequa Park | $562,000 | +2% | 17 | Jul 2022 |
| 8 Bryce Ave | Glen Cove | $560,000 | −5% | 56 | Dec 2022 |
| 61 Robinwood Ave | Hempstead | $525,000 | −4% | 35 | Sep 2023 |

Five of the nine closed at or above asking. Median days on market across the nine is 31. The
Nassau County average was 42 days in June 2026, with a median single-family price of $875,000
([Molloy University / OneKey market data](https://www.molloy.edu/news/rising-long-island-home-prices-nassau-hits-835,000-suffolk-700,000)).
That comparison is the hero claim, and it is the honest version of the line the old page ran.

The old page led with *"most of my listings sell in under thirty days."* The record does not
support that: four of nine were under 30 days, five were over. What the record does support,
and what sells harder to a seller anyway, is that she lands above ask more often than not.
The four that missed are on the page too. Showing them is the point, because the page argues that
she tells sellers the truth, so it has to.

### Two things for Margie to eyeball

Data providers disagree slightly on sale dates, which is normal: one records the contract
date, another the closing, another when the deed was recorded. 8 Bryce Ave reads as December
2022 here and January 2023 on Redfin; 22 Lincoln Ave reads as December 2022 here and mid
November elsewhere. Nothing worth chasing.

**44 Tyrconnell Ave is worth chasing.** The Homes.com record has it at $562,000 in July 2022,
2 bed, 1 bath, 978 sq ft. Public property data elsewhere describes the same address as 5 bed,
1 bath, built 1927, last sold in 2013 for $247,600. One of those is about a different parcel
or a different transaction. Margie will know in a second which, and it is the only row on the
page with that kind of conflict behind it.

Also from the record: an active listing at 44 Perry Ave, Bayville ($599,000, 3 bed, 811 sq ft),
her licence number NY 40HO1125819, the phone number (516) 586-0245, and Hofstra University.

### From Margie's own profile

The career figures on her [FastExpert profile](https://www.fastexpert.com/agents/margie-horowitz-23671/)
are self-reported and are marked on the page as hers: 19 years in the business, $38M in sales
in the last year, a multi-million dollar producer award every year since her first, and the
number one selling agent spot in The Groves in 2017. Her bio text on that profile matches the
bio on Homes.com word for word, so it is the same agent.

Note the two profiles disagree with each other. FastExpert says $38M last year; the public
record shows $8.8M across five years. Public records only capture the deals where the feed
recorded her as the agent, so an undercount is expected. But the page never adds them
together, and it never prints a career volume as if it were verified.

## Four things that have to be settled before this goes live

1. **Which brokerage.** Berkshire Hathaway HomeServices Laffey lists her in Williston Park.
   The public sale record and her active Bayville listing put her at Americana Realty Group,
   375 Jericho Turnpike, Syosset. She is not on Americana's public team page. One of the two
   is stale and only Margie can say which. Every spot this affects is marked `.tofill` in the
   markup and shows in verdigris on the page.

2. **A portrait.** The About section holds a 3:4 slot for a real photograph of her. It is
   deliberately empty. A generated headshot on an agent's own site is the fastest way to lose
   a seller's trust, so it stays a slot until she sends one.

3. **Three testimonials.** There are no public reviews to pull from anywhere, not Zillow,
   not FastExpert, not her brokerage. These have to come from her directly. Ask for ones that
   carry a first name and a town; an anonymous quote reads like it was written in-house.

4. **Two listing photo sets**, for 22 Lincoln Ave and 44 Tyrconnell Ave. See the photography
   section below for why those two could not be retrieved.

Her email address and office address are also unset.

## The photography

Margie and her brokerage granted rights to use her listing photography, so the property
photographs on this page are the real ones: the OneKey MLS photo sets her listings carried,
watermark and all. `tools/fetch_listing_photos.py` retrieves them and drops them in
`img/real/`; `tools/sync_real_photos.py` compresses them and rewrites the `REAL` set in
`index.html` from whatever is actually in that folder.

That last part matters. Any sale without a real photograph on disk falls back to a generated
stand-in and shows a *Representative image* badge on its slide. Because the badge is driven by
the folder rather than by anyone's memory, it cannot end up claiming more than the site holds.
Run the sync after adding any photo:

```bash
python tools/fetch_listing_photos.py     # everything still missing
python tools/sync_real_photos.py         # compress, then update the REAL set
```

### Where the photos come from, and what is still missing

Homes.com holds the best masters at 1900px, but it blocks every non-browser client at the edge
and refuses cross-origin reads, so it cannot be scripted. Zillow (`cc_ft_1536`) and Redfin
(`bigphoto`, about 1280px) both work. Both throttle hard after roughly eight quick requests,
which is why `PAGE_DELAY` is set to 75 seconds. Leave it slow.

Six of the ten properties have their real photograph on the page. Four do not, and each of
those four shows a *Representative image* badge:

| Property | Why not |
|---|---|
| 22 Lincoln Ave, Glen Head | MLS #3430002. The listing page on Berkshire Hathaway HomeServices Laffey came down after the sale, and the address is not indexed on Zillow or Redfin. |
| 44 Tyrconnell Ave, Massapequa Park | Not indexed on Zillow or Redfin either. See the data conflict noted above. |
| 98 Cortelyou St, Islip | Zillow only (zpid 82666298), and Zillow was throttling this IP by the time its turn came round. Retry later; it should come through. |
| 61 Robinwood Ave, Hempstead | Same as Islip. Zillow only (zpid 31218306), throttled. |

The last two are a matter of waiting out a rate limit. Run
`python tools/fetch_listing_photos.py islip robinwood` again after an hour and they will
almost certainly land. The first two need Margie: they are her own listings, so asking her
for the two photo sets is faster than any amount of scraping. Drop them in `img/real/` as
`p-glen-head.jpg` and `p-tyrconnell.jpg`, run the sync, and their badges disappear.

The hero, shoreline and village images are generated, not photographs of real places. They are
atmosphere rather than property, and none of them claims to be a specific address.

### One thing that came off the page

Earlier drafts labelled each sale with an architectural style: "Center-hall colonial",
"Expanded cape", and so on. Those were read off the bed, bath and square-foot figures rather
than taken from the record, and the real photograph of 214 Lawrence Lane turned out to be a
ranch where the page had guessed a cape. A page whose argument is that every figure on it can
be checked cannot carry a guess, so the style labels are gone. Each row now shows the town,
the bed count, and the square footage, all of which are in the record.

## Running it

```bash
python -m http.server 5140 --directory .
```

Single file, no build step. `index.html` holds the markup, the styles, and the nine sales as a
JS array. The only external dependency is Google Fonts (Fraunces and Archivo).

## The design

Deep harbour navy against warm ivory, with the verdigris that Gold Coast copper roofs go after
eighty years. Fraunces carries the display type and every figure, because money set in a serif reads
engraved rather than printed. Archivo does the body and the labels.

The signature is the **ask-versus-sold line** under each sale. The tick in the middle is the
asking price; the bar shows where the house actually closed, right of the tick for over, left
for under. It appears once per carousel slide and again on all nine rows of the list, so the
shape of her record is readable without reading a single number. The scale runs −15% to +15%.

Auto-advance stops on hover, on focus, on any manual control, when the tab is hidden, and
never starts at all under `prefers-reduced-motion`.

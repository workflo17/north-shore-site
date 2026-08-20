/* Lead capture for the valuation form.
   Runs on Vercel's Node runtime. No dependencies, no build step.

   A lead is never dropped: it is written to the runtime log first, then pushed
   to whichever delivery channels are configured. Configure with env vars:

     RESEND_API_KEY     re_xxx from resend.com. Absent: no email is sent.
     LEAD_TO            where the email goes. Comma-separated for more than one.
     LEAD_FROM          verified sender, e.g. Margie Horowitz <leads@example.com>
     HUBSPOT_TOKEN      private app token. Absent: no contact is created.
     LEAD_WEBHOOK_URL   optional POST target: Zapier, Make, Slack, Apps Script.

   With none of them set the function still validates and logs, so the form
   works from the first deploy and the leads sit in the Vercel runtime logs. */

const LIMITS = { name: 80, address: 160, contact: 120, note: 2000 };
const TIMINGS = [
  "As soon as possible",
  "Within 3 months",
  "6 to 12 months",
  "Just want to know the value",
];

/* Best-effort throttle. Serverless instances are recycled and there can be
   several at once, so this stops a loop from one browser, not a real flood.
   Vercel's own WAF / Attack Challenge Mode is the answer for that. */
const RATE = new Map();
const RATE_MAX = 5;
const RATE_WINDOW_MS = 10 * 60 * 1000;

function rateLimited(ip) {
  const now = Date.now();
  const hits = (RATE.get(ip) || []).filter((t) => now - t < RATE_WINDOW_MS);
  hits.push(now);
  RATE.set(ip, hits);
  if (RATE.size > 500) {
    for (const [k, v] of RATE) if (!v.some((t) => now - t < RATE_WINDOW_MS)) RATE.delete(k);
  }
  return hits.length > RATE_MAX;
}

function clean(v, max) {
  return typeof v === "string" ? v.replace(/\s+/g, " ").trim().slice(0, max) : "";
}

function looksReachable(contact) {
  if (/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(contact)) return "email";
  if ((contact.match(/\d/g) || []).length >= 7) return "phone";
  return null;
}

async function readBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  if (typeof req.body === "string" && req.body) {
    try { return JSON.parse(req.body); } catch { return null; }
  }
  const chunks = [];
  for await (const chunk of req) {
    chunks.push(chunk);
    if (chunks.reduce((n, c) => n + c.length, 0) > 64 * 1024) return null;
  }
  if (!chunks.length) return null;
  try { return JSON.parse(Buffer.concat(chunks).toString("utf8")); } catch { return null; }
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function emailBody(lead) {
  const rows = [
    ["Name", lead.name],
    ["Property", lead.address || "not given"],
    ["Reach them at", lead.contact],
    ["Timing", lead.timing],
    ["Notes", lead.note || "none"],
    ["Came from", lead.page],
    ["Received", lead.receivedAt],
  ];
  const text = rows.map(([k, v]) => `${k}: ${v}`).join("\n");
  const html = `<div style="font:15px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;color:#14232C">
<p style="margin:0 0 18px"><strong>${escapeHtml(lead.name)}</strong> asked for a valuation${
    lead.address ? ` on <strong>${escapeHtml(lead.address)}</strong>` : ""}.</p>
<table cellpadding="0" cellspacing="0" style="border-collapse:collapse">${rows
    .map(([k, v]) => `<tr>
<td style="padding:6px 18px 6px 0;color:#6F8189;vertical-align:top;white-space:nowrap">${escapeHtml(k)}</td>
<td style="padding:6px 0;vertical-align:top">${escapeHtml(v)}</td></tr>`).join("")}</table>
<p style="margin:22px 0 0;color:#6F8189;font-size:13px">Sent by the valuation form on the website.</p></div>`;
  return { text, html };
}

async function sendEmail(lead) {
  const key = process.env.RESEND_API_KEY;
  const to = (process.env.LEAD_TO || "").split(",").map((s) => s.trim()).filter(Boolean);
  const from = process.env.LEAD_FROM;
  if (!key || !to.length || !from) return { channel: "email", ok: false, skipped: "not configured" };

  const { text, html } = emailBody(lead);
  const payload = {
    from,
    to,
    subject: `Valuation request: ${lead.name}${lead.address ? ` · ${lead.address}` : ""}`,
    text,
    html,
  };
  if (lead.contactKind === "email") payload.reply_to = lead.contact;

  try {
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(8000),
    });
    if (!res.ok) return { channel: "email", ok: false, error: `resend ${res.status}: ${(await res.text()).slice(0, 200)}` };
    return { channel: "email", ok: true };
  } catch (err) {
    return { channel: "email", ok: false, error: String(err && err.message || err) };
  }
}

/* HubSpot's free tier includes private apps and the contacts API, which is
   enough to land a lead as a real contact without paying for Workflows. */
async function sendCrm(lead) {
  const token = process.env.HUBSPOT_TOKEN;
  if (!token) return { channel: "crm", ok: false, skipped: "not configured" };

  const [first, ...rest] = lead.name.split(" ");
  const props = {
    firstname: first,
    lastname: rest.join(" "),
    lifecyclestage: "lead",
    hs_lead_status: "NEW",
  };
  props[lead.contactKind === "email" ? "email" : "phone"] = lead.contact;
  if (lead.address) props.address = lead.address;

  const detail = [
    `Timing: ${lead.timing}`,
    lead.note ? `Notes: ${lead.note}` : "",
    `From the valuation form on ${lead.page}`,
  ].filter(Boolean).join("\n");

  const post = (properties) => fetch("https://api.hubapi.com/crm/v3/objects/contacts", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ properties }),
    signal: AbortSignal.timeout(8000),
  });

  try {
    let res = await post({ ...props, message: detail });
    /* A portal missing the default `message` property rejects the whole write.
       Retry with the properties every portal has rather than lose the contact. */
    if (res.status === 400) res = await post(props);
    /* 409 is HubSpot saying the email is already a contact. Already known is fine. */
    if (res.status === 409) return { channel: "crm", ok: true, note: "already a contact" };
    if (!res.ok) return { channel: "crm", ok: false, error: `hubspot ${res.status}: ${(await res.text()).slice(0, 200)}` };
    return { channel: "crm", ok: true };
  } catch (err) {
    return { channel: "crm", ok: false, error: String(err && err.message || err) };
  }
}

async function sendWebhook(lead) {
  const url = process.env.LEAD_WEBHOOK_URL;
  if (!url) return { channel: "webhook", ok: false, skipped: "not configured" };
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lead),
      signal: AbortSignal.timeout(8000),
    });
    if (!res.ok) return { channel: "webhook", ok: false, error: `webhook ${res.status}` };
    return { channel: "webhook", ok: true };
  } catch (err) {
    return { channel: "webhook", ok: false, error: String(err && err.message || err) };
  }
}

module.exports = async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");

  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Use POST." });
  }

  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "unknown";
  if (rateLimited(ip)) {
    return res.status(429).json({ ok: false, error: "Too many requests. Please call instead." });
  }

  const body = await readBody(req);
  if (!body) return res.status(400).json({ ok: false, error: "Could not read the form." });

  /* Two silent spam gates. The honeypot is a field hidden from people; a form
     filled in under three seconds was not filled in by a person. Both answer
     200 so a bot cannot tell it was caught. */
  if (clean(body.company, 100)) {
    console.log(JSON.stringify({ tag: "LEAD_SPAM", reason: "honeypot", ip }));
    return res.status(200).json({ ok: true });
  }
  const elapsed = Number(body.elapsed);
  if (Number.isFinite(elapsed) && elapsed >= 0 && elapsed < 3000) {
    console.log(JSON.stringify({ tag: "LEAD_SPAM", reason: "too fast", elapsed, ip }));
    return res.status(200).json({ ok: true });
  }

  const name = clean(body.name, LIMITS.name);
  const contact = clean(body.contact, LIMITS.contact);
  const fields = {};
  if (name.length < 2) fields.name = "Please add your name so Margie knows who to call back.";
  const contactKind = looksReachable(contact);
  if (!contactKind) fields.contact = "Please add a phone number or an email address.";
  if (Object.keys(fields).length) return res.status(422).json({ ok: false, fields });

  const timingRaw = clean(body.timing, 60);
  const lead = {
    name,
    contact,
    contactKind,
    address: clean(body.address, LIMITS.address),
    timing: TIMINGS.includes(timingRaw) ? timingRaw : TIMINGS[3],
    note: clean(body.note, LIMITS.note),
    page: clean(body.page, 200) || "unknown",
    receivedAt: new Date().toISOString(),
    ip,
  };

  /* The log is written before any network call, so a lead survives an email
     outage. `vercel logs` and the dashboard's Runtime Logs both show it. */
  console.log(JSON.stringify({ tag: "LEAD", ...lead }));

  const delivery = await Promise.all([sendEmail(lead), sendCrm(lead), sendWebhook(lead)]);
  delivery.filter((d) => d.error).forEach((d) =>
    console.error(JSON.stringify({ tag: "LEAD_DELIVERY_FAILED", ...d })));

  return res.status(200).json({ ok: true, delivery });
};

module.exports.__test = { clean, looksReachable, emailBody, sendCrm, TIMINGS };

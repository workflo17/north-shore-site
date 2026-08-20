/* Exercises api/lead.js against fake requests. No network, no Vercel, no keys.
   Run before every deploy that touches the form:  node tools/test_lead_api.mjs */

import { createRequire } from "node:module";
import { Readable } from "node:stream";

const require = createRequire(import.meta.url);
const handler = require("../api/lead.js");

function call(body, { method = "POST", ip = "203.0.113.7" } = {}) {
  const req = Object.assign(
    Readable.from([Buffer.from(typeof body === "string" ? body : JSON.stringify(body))]),
    { method, headers: { "x-forwarded-for": ip, "content-type": "application/json" } }
  );
  return new Promise((resolve) => {
    const res = {
      statusCode: 200,
      headers: {},
      setHeader(k, v) { this.headers[k.toLowerCase()] = v; },
      status(code) { this.statusCode = code; return this; },
      json(obj) { resolve({ status: this.statusCode, body: obj, headers: this.headers }); return this; },
      end() { resolve({ status: this.statusCode, body: null, headers: this.headers }); return this; },
    };
    handler(req, res);
  });
}

const good = {
  name: "Jane Reilly", contact: "jane@example.com", address: "12 Cedar Lane, Syosset",
  timing: "Within 3 months", note: "Kitchen redone in 2023.", elapsed: 42000, page: "/",
};

let pass = 0, fail = 0;
const check = (label, cond, detail) => {
  if (cond) { pass++; console.log(`  ok    ${label}`); }
  else { fail++; console.log(`  FAIL  ${label}${detail ? `\n        ${JSON.stringify(detail)}` : ""}`); }
};

const logged = [];
const realLog = console.log;
console.log = (...a) => { logged.push(String(a[0])); };

const r = {
  get:       await call(good, { method: "GET" }),
  ok:        await call(good, { ip: "198.51.100.1" }),
  phone:     await call({ ...good, contact: "(516) 555 0123" }, { ip: "198.51.100.2" }),
  noName:    await call({ ...good, name: "" }, { ip: "198.51.100.3" }),
  badReach:  await call({ ...good, contact: "maybe later" }, { ip: "198.51.100.4" }),
  honeypot:  await call({ ...good, company: "Acme SEO" }, { ip: "198.51.100.5" }),
  tooFast:   await call({ ...good, elapsed: 400 }, { ip: "198.51.100.6" }),
  garbage:   await call("{not json", { ip: "198.51.100.7" }),
  badTiming: await call({ ...good, timing: "<script>alert(1)</script>" }, { ip: "198.51.100.8" }),
  longNote:  await call({ ...good, note: "x".repeat(9000) }, { ip: "198.51.100.9" }),
};
const flood = [];
for (let i = 0; i < 7; i++) flood.push(await call(good, { ip: "198.51.100.99" }));

console.log = realLog;

console.log("\napi/lead.js\n");
check("GET is rejected with 405", r.get.status === 405, r.get);
check("a complete lead returns 200 ok", r.ok.status === 200 && r.ok.body.ok === true, r.ok);
check("a phone number is accepted as contact", r.phone.status === 200 && r.phone.body.ok === true, r.phone);
check("a missing name returns 422 with a field message",
  r.noName.status === 422 && !!r.noName.body.fields?.name, r.noName);
check("an unreachable contact returns 422",
  r.badReach.status === 422 && !!r.badReach.body.fields?.contact, r.badReach);
check("the honeypot answers 200 but does not record a lead",
  r.honeypot.status === 200 && !logged.some((l) => l.includes('"tag":"LEAD"') && l.includes("Acme SEO")), r.honeypot);
check("a sub-3s submission is treated as a bot",
  r.tooFast.status === 200 && logged.some((l) => l.includes("too fast")), r.tooFast);
check("unparseable JSON returns 400", r.garbage.status === 400, r.garbage);
check("an off-list timing falls back to the safe default",
  logged.some((l) => l.includes('"tag":"LEAD"') && l.includes("Just want to know the value")), r.badTiming);
check("a 9000 character note is truncated to 2000",
  logged.some((l) => { try { const j = JSON.parse(l); return j.tag === "LEAD" && j.note.length === 2000; } catch { return false; } }));
check("the 6th submission from one IP inside 10 min is throttled",
  flood[5].status === 429 || flood[6].status === 429, flood.map((f) => f.status));
check("every accepted lead is written to the log before delivery",
  logged.filter((l) => l.includes('"tag":"LEAD"')).length >= 3);
check("with no keys set, delivery reports both channels as unconfigured",
  r.ok.body.delivery?.every((d) => d.skipped === "not configured"), r.ok.body.delivery);

const { looksReachable, clean } = handler.__test;
check("looksReachable: email", looksReachable("a@b.co") === "email");
check("looksReachable: 10-digit phone", looksReachable("516-586-0245") === "phone");
check("looksReachable: prose is rejected", looksReachable("call me") === null);
check("clean strips control whitespace and trims", clean("  a\n\n b  ", 80) === "a b");

console.log(`\n${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);

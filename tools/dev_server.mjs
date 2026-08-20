/* Local stand-in for Vercel: serves the static site and routes /api/lead to the
   same handler Vercel runs, so the whole lead flow can be exercised before any
   deploy. Not used in production.

     node tools/dev_server.mjs            → http://localhost:5130
     PORT=5131 node tools/dev_server.mjs

   Env vars are read the same way the deployed function reads them, so
   RESEND_API_KEY=... node tools/dev_server.mjs sends a real test email. */

import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const PORT = Number(process.env.PORT) || 5130;
const require = createRequire(import.meta.url);

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".webmanifest": "application/manifest+json; charset=utf-8",
  ".xml": "application/xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".webp": "image/webp",
};

/* Re-required per request so edits to api/lead.js land without a restart. */
function loadHandler() {
  const path = require.resolve("../api/lead.js");
  delete require.cache[path];
  return require(path);
}

function vercelResponse(res) {
  res.status = (code) => { res.statusCode = code; return res; };
  res.json = (obj) => {
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.end(JSON.stringify(obj));
    return res;
  };
  return res;
}

async function serveFile(res, path) {
  const body = await readFile(path);
  res.statusCode = 200;
  res.setHeader("Content-Type", TYPES[extname(path).toLowerCase()] || "application/octet-stream");
  res.setHeader("Cache-Control", "no-store");
  res.end(body);
}

const server = createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);

  if (url.pathname === "/api/lead") {
    try {
      await loadHandler()(req, vercelResponse(res));
    } catch (err) {
      console.error("handler threw:", err);
      if (!res.writableEnded) { res.statusCode = 500; res.end(JSON.stringify({ ok: false, error: String(err) })); }
    }
    return;
  }

  let rel = decodeURIComponent(url.pathname).replace(/^\/+/, "");
  if (rel === "" || rel.endsWith("/")) rel += "index.html";
  const path = join(ROOT, normalize(rel));
  if (!path.startsWith(ROOT)) { res.statusCode = 403; return res.end("Forbidden"); }

  try {
    if ((await stat(path)).isDirectory()) return await serveFile(res, join(path, "index.html"));
    await serveFile(res, path);
  } catch {
    try {
      res.statusCode = 404;
      res.setHeader("Content-Type", TYPES[".html"]);
      res.end(await readFile(join(ROOT, "404.html")));
    } catch { res.statusCode = 404; res.end("Not found"); }
  }
});

server.listen(PORT, () => console.log(`north-shore-site dev server on http://localhost:${PORT}`));

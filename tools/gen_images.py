"""Render the site photography locally through ComfyUI (DreamShaperXL Turbo).

Every image here is generated, not photographed. That is a deliberate limit: these stand in for
Margie's own listing photography, which is MLS-copyrighted and has to come from her brokerage.
Each property slide carries a visible "representative image" marker in the page for that reason.

No human faces anywhere. Generated faces are the clearest AI tell, and a fake headshot on an
agent's own website is not something to hand a prospect. Margie's portrait stays an empty slot
until she sends a real one.

Usage:  python tools/gen_images.py [key ...]     (no args = everything)
"""
import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.request

HOST = "http://127.0.0.1:8188"
CKPT = "DreamShaperXL_Turbo_v2_1.safetensors"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COMFY_OUT = os.path.expanduser("~/asset-forge/ComfyUI_windows_portable/ComfyUI/output")

NEG = ("text, watermark, signature, logo, letters, words, caption, street sign, house number, "
       "ugly, deformed, warped perspective, crooked walls, melted roofline, blurry, lowres, "
       "jpeg artifacts, oversaturated, hdr halo, cartoon, illustration, 3d render, cgi, "
       "person, face, people, figure, extra windows, floating door")

# Shared look. Real-estate photography has a house style and it is worth matching: wide lens
# held at chest height, late-afternoon sun, clean sky, no cars in the frame.
LOOK = ("professional real estate photography, wide angle architectural exterior, "
        "late afternoon golden light, clear sky, crisp shadows, manicured lawn, "
        "shot on full frame camera, sharp, natural colour, high detail")

# (key, filename, w, h, prompt)
JOBS = [
    # ---------- hero ----------
    ("hero", "hero", 1344, 768,
     "A large white center-hall colonial house on Long Island's North Shore, black shutters, "
     "columned portico, slate roof, mature oak trees, deep green lawn, stone walkway, "
     "autumn late afternoon, " + LOOK),

    # ---------- sold properties: matched to the real specifications ----------
    ("glenhead", "p-glen-head", 1216, 832,
     "A substantial four bedroom center hall colonial house, cream clapboard siding, "
     "black shutters, two storeys, wide front lawn, mature trees, quiet suburban street, "
     "Long Island, " + LOOK),
    ("seaford", "p-seaford", 1216, 832,
     "A wide five bedroom split level suburban house, brick lower facade and pale siding above, "
     "attached garage, wide driveway, trimmed hedges, Long Island suburb, " + LOOK),
    ("brooklyn", "p-brooklyn", 1216, 832,
     "A brick semi-detached two family Brooklyn row house, limestone detail, front stoop, "
     "small iron fence, narrow front garden, tree lined residential street, " + LOOK),
    ("albertson", "p-albertson", 1216, 832,
     "A neat three bedroom expanded cape cod house, white siding, dormer windows, "
     "brick chimney, front path, flowering shrubs, Long Island suburb, " + LOOK),
    ("islip", "p-islip", 1216, 832,
     "A five bedroom two storey village colonial house, grey shingle siding, white trim, "
     "covered front porch, picket fence, large shade tree, Long Island village, " + LOOK),
    ("lawrence", "p-lawrence", 1216, 832,
     "A three bedroom cape cod cottage, pale yellow siding, white shutters, dormers, "
     "detached garage, hydrangeas by the porch, north shore Long Island, " + LOOK),
    ("tyrconnell", "p-tyrconnell", 1216, 832,
     "A small two bedroom cottage style house, white siding, dark green shutters, "
     "compact front garden, low picket fence, narrow driveway, Long Island, " + LOOK),
    ("bryce", "p-bryce", 1216, 832,
     "A long single storey ranch house, brick and pale siding, low pitched roof, "
     "picture window, carport, wide front lawn, Long Island suburb, " + LOOK),
    ("robinwood", "p-robinwood", 1216, 832,
     "A modest three bedroom cape cod house, white siding, black shutters, front dormers, "
     "concrete path, small trimmed lawn, Nassau County, " + LOOK),
    ("perry", "p-perry", 1216, 832,
     "A small shingled beach cottage near the water, weathered cedar shingles, white trim, "
     "screened porch, beach grass and a low fence, boats visible far behind, "
     "Long Island Sound, " + LOOK),

    # ---------- atmosphere ----------
    ("shore", "shore", 1344, 768,
     "Long Island Sound shoreline at golden hour, calm water, moored sailboats, "
     "wooded headland, pebble beach, warm low sun, "
     "landscape photograph, natural colour, sharp, high detail"),
    ("village", "village", 1216, 832,
     "A quiet North Shore Long Island village main street, brick storefronts with awnings, "
     "planted sidewalk trees, lamp posts, empty street, early morning light, "
     "documentary photograph, natural colour, sharp, high detail"),
    ("interior", "interior", 1216, 832,
     "An empty staged living room in a colonial house, oak floors, white walls, "
     "large windows with plantation shutters, neutral sofa, coffee table, brass lamp, "
     "sunlight across the floor, interior real estate photography, sharp, natural colour"),
]


def graph(prompt, w, h, seed, prefix):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CKPT}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": NEG, "clip": ["1", 1]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {
            "seed": seed, "steps": 9, "cfg": 2.0, "sampler_name": "dpmpp_sde",
            "scheduler": "karras", "denoise": 1.0,
            "model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0]}},
        "6": {"class_type": "VAEDecodeTiled", "inputs": {
            "samples": ["5", 0], "vae": ["1", 2],
            "tile_size": 512, "overlap": 64, "temporal_size": 32, "temporal_overlap": 4}},
        "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": prefix}},
    }


def post(path, payload):
    req = urllib.request.Request(HOST + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def wait_for_server(timeout=600):
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(HOST + "/system_stats", timeout=5).read()
            return True
        except Exception:
            time.sleep(4)
    return False


def run(job, index, budget=180):
    """Render one job. Returns (src, dst) or None if the engine stalls past `budget` seconds."""
    key, name, w, h, prompt = job
    pid = post("/prompt", {"prompt": graph(prompt, w, h, 4200 + index * 6421, "ns/" + name)})["prompt_id"]
    deadline = time.time() + budget
    while time.time() < deadline:
        time.sleep(2)
        hist = json.loads(urllib.request.urlopen(f"{HOST}/history/{pid}", timeout=30).read())
        if pid in hist:
            imgs = hist[pid].get("outputs", {}).get("7", {}).get("images")
            if not imgs:
                return None
            src = os.path.join(COMFY_OUT, imgs[0].get("subfolder", ""), imgs[0]["filename"])
            dst_dir = os.path.join(ROOT, "img")
            os.makedirs(dst_dir, exist_ok=True)
            return src, os.path.join(dst_dir, name + ".png")
    try:
        post("/interrupt", {})
    except Exception:
        pass
    return None


if __name__ == "__main__":
    wanted = set(sys.argv[1:])
    jobs = [j for j in JOBS if not wanted or j[0] in wanted]
    print(f"waiting for ComfyUI at {HOST} ...", flush=True)
    if not wait_for_server():
        sys.exit("ComfyUI never came up on 8188")
    print(f"server up, {len(jobs)} images to render", flush=True)
    skipped = []
    for i, job in enumerate(jobs):
        t0 = time.time()
        try:
            got = run(job, i)
        except Exception as exc:
            print(f"  [{i+1}/{len(jobs)}] {job[0]} ERROR {exc}", flush=True)
            skipped.append(job[0])
            continue
        if not got:
            print(f"  [{i+1}/{len(jobs)}] {job[0]} STALLED, skipped", flush=True)
            skipped.append(job[0])
            continue
        src, dst = got
        shutil.copyfile(src, dst)
        print(f"  [{i+1}/{len(jobs)}] {job[0]} -> {os.path.relpath(dst, ROOT)} "
              f"({time.time()-t0:.0f}s)", flush=True)
    print(f"done. skipped: {skipped or 'none'}", flush=True)

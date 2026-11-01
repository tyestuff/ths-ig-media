#!/usr/bin/env python3
"""
Publish approved, due LinkedIn posts from post-autopilot/queue/.

A post is published when its front matter has `status: approved` and its
`publish_at` time is now or in the past. After publishing, the file gets
`status: posted` and `posted_url`, and moves to post-autopilot/posted/.
Failures get `status: failed` and an `error` line, and stay in queue/.

Usage:
    python3 scripts/publish_posts.py --dry-run          # show what would post; posts nothing
    python3 scripts/publish_posts.py                    # publish everything that's due
    python3 scripts/publish_posts.py --file post-autopilot/queue/2026-11-04-hello.md --now
                                                         # publish one file immediately (must be approved)

Reads LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN, optional LINKEDIN_ORG_ID and
LINKEDIN_API_VERSION from environment variables or post-autopilot/.env.
Standard library only.
"""
import argparse
import datetime as dt
import glob
import json
import mimetypes
import os
import re
import shutil
import sys
import urllib.error
import urllib.request

DEFAULT_API_VERSION = "202608"  # LinkedIn supports each monthly version for about a year; override with LINKEDIN_API_VERSION
API = "https://api.linkedin.com/rest"
MAX_CHARS = 3000
MIN_SOFT_BEFORE_ASK = 3  # every "ask" (promotional) post needs at least this many soft-CTA posts before it


# ---------- helpers ----------

def load_env(path):
    env = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    env.update({k: v for k, v in os.environ.items() if k.startswith("LINKEDIN_") and v})
    return env


def parse_value(raw):
    raw = raw.strip()
    if raw[:1] in ('"', "'"):
        q = raw[0]
        end = raw.find(q, 1)
        return raw[1:end] if end != -1 else raw[1:]
    return re.split(r"\s+#", raw, maxsplit=1)[0].strip()


def read_post(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        raise ValueError("missing front matter (--- block at top)")
    meta = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = parse_value(v)
    return meta, m.group(2).strip(), m.group(1), text


def write_meta(path, updates):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^(---\s*\n)(.*?)(\n---\s*\n?)(.*)$", text, re.S)
    head, fm, sep, body = m.groups()
    lines = fm.splitlines()
    for key, val in updates.items():
        val_s = json.dumps(val) if isinstance(val, str) else str(val)
        if key == "status":
            val_s = val
        pat = re.compile(rf"^{re.escape(key)}\s*:")
        for i, line in enumerate(lines):
            if pat.match(line):
                lines[i] = f"{key}: {val_s}"
                break
        else:
            lines.append(f"{key}: {val_s}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + "\n".join(lines) + sep + body)


ESCAPE_CHARS = set("\\|{}@[]()<>#*_~")
HASHTAG = re.compile(r"(?<![\w&])#([A-Za-z][\w]*)")


def to_little_text(text):
    """Escape LinkedIn 'little text' reserved chars; turn #words into real hashtags."""
    out, pos = [], 0
    esc = lambda s: "".join("\\" + c if c in ESCAPE_CHARS else c for c in s)
    for m in HASHTAG.finditer(text):
        out.append(esc(text[pos:m.start()]))
        out.append("{hashtag|\\#|" + m.group(1) + "}")
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out)


def parse_time(s):
    t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    if t.tzinfo is None:
        t = t.astimezone()  # treat naive times as local time
    return t


class LinkedIn:
    def __init__(self, token, version):
        self.token, self.version = token, version

    def _req(self, method, url, body=None, headers=None, raw=None):
        h = {
            "Authorization": f"Bearer {self.token}",
            "LinkedIn-Version": self.version,
            "X-Restli-Protocol-Version": "2.0.0",
        }
        data = raw
        if body is not None:
            data = json.dumps(body).encode()
            h["Content-Type"] = "application/json"
        h.update(headers or {})
        req = urllib.request.Request(url, data=data, method=method, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                payload = r.read()
                return r.status, dict(r.headers), (json.loads(payload) if payload.strip() else {})
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}") from None

    def upload_image(self, owner, path):
        _, _, res = self._req("POST", f"{API}/images?action=initializeUpload",
                              {"initializeUploadRequest": {"owner": owner}})
        val = res["value"]
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            req = urllib.request.Request(val["uploadUrl"], data=f.read(), method="PUT",
                                         headers={"Authorization": f"Bearer {self.token}",
                                                  "Content-Type": ctype})
        try:
            urllib.request.urlopen(req, timeout=120).read()
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Image upload failed HTTP {e.code}: {e.read().decode(errors='replace')[:300]}") from None
        return val["image"]

    def create_post(self, payload):
        _, headers, _ = self._req("POST", f"{API}/posts", payload)
        lower = {k.lower(): v for k, v in headers.items()}
        return lower.get("x-restli-id") or lower.get("x-linkedin-id")


def posted_history(workspace):
    """CTA types of already-published posts, oldest first."""
    rows = []
    for path in glob.glob(os.path.join(workspace, "posted", "*.md")):
        try:
            meta, _, _, _ = read_post(path)
        except Exception:
            continue
        rows.append((meta.get("posted_at") or meta.get("publish_at") or "", (meta.get("cta_type") or "soft").lower()))
    return [cta for _, cta in sorted(rows)]


def soft_since_last_ask(history):
    n = 0
    for cta in reversed(history):
        if cta == "ask":
            break
        n += 1
    return n


# ---------- main ----------

def build(meta, body, env, workspace):
    dest = (meta.get("destination") or "personal").lower()
    if dest == "page":
        org = env.get("LINKEDIN_ORG_ID")
        if not org:
            raise ValueError("destination is 'page' but LINKEDIN_ORG_ID is not set")
        author = org if org.startswith("urn:") else f"urn:li:organization:{org}"
    else:
        author = env.get("LINKEDIN_PERSON_URN")
        if not author:
            raise ValueError("LINKEDIN_PERSON_URN not set. Run scripts/connect_account.py first")
    if not body:
        raise ValueError("post body is empty")
    if len(body) > MAX_CHARS:
        raise ValueError(f"post is {len(body)} characters; LinkedIn's limit is {MAX_CHARS}")
    visibility = (meta.get("visibility") or "PUBLIC").upper()
    if dest == "page" and visibility != "PUBLIC":
        visibility = "PUBLIC"
    image = meta.get("image") or ""
    image_path = os.path.join(workspace, image) if image else ""
    if image_path and not os.path.exists(image_path):
        raise ValueError(f"image not found: {image_path}")
    payload = {
        "author": author,
        "commentary": to_little_text(body),
        "visibility": visibility,
        "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [],
                         "thirdPartyDistributionChannels": []},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    return author, payload, image_path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace", default="post-autopilot")
    ap.add_argument("--file", help="publish just this queue file")
    ap.add_argument("--now", action="store_true", help="ignore publish_at (still requires status: approved)")
    ap.add_argument("--dry-run", action="store_true", help="show what would be posted without posting")
    args = ap.parse_args()

    ws = args.workspace
    env = load_env(os.path.join(ws, ".env"))
    files = [args.file] if args.file else sorted(glob.glob(os.path.join(ws, "queue", "*.md")))
    now = dt.datetime.now(dt.timezone.utc)

    exp = env.get("LINKEDIN_TOKEN_EXPIRES")
    if exp:
        days = (dt.date.fromisoformat(exp) - now.date()).days
        if days <= 7:
            print(f"WARNING: LinkedIn token expires in {days} day(s) ({exp}). Re-run scripts/connect_account.py.")

    token = env.get("LINKEDIN_ACCESS_TOKEN")
    if not token and not args.dry_run:
        sys.exit("LINKEDIN_ACCESS_TOKEN not set. Run scripts/connect_account.py first.")
    li = LinkedIn(token or "", env.get("LINKEDIN_API_VERSION", DEFAULT_API_VERSION))

    history = posted_history(ws)
    posted = failed = 0
    for path in files:
        name = os.path.basename(path)
        try:
            meta, body, _, _ = read_post(path)
        except Exception as e:
            print(f"SKIP {name}: {e}")
            continue
        if meta.get("status", "").lower() != "approved":
            if args.file:
                print(f"SKIP {name}: status is '{meta.get('status')}', not 'approved'")
            continue
        try:
            when = parse_time(meta["publish_at"]) if meta.get("publish_at") else None
        except ValueError:
            print(f"SKIP {name}: publish_at '{meta.get('publish_at')}' isn't a valid ISO date-time")
            continue
        if not args.now and (when is None or when > now):
            if args.dry_run:
                print(f"WAIT {name}: scheduled for {when}")
            continue
        try:
            author, payload, image_path = build(meta, body, env, ws)
            cta_type = (meta.get("cta_type") or "soft").lower()
            if cta_type == "ask" and soft_since_last_ask(history) < MIN_SOFT_BEFORE_ASK:
                raise ValueError(f"promotional (ask) post blocked: only {soft_since_last_ask(history)} "
                                 f"soft-CTA post(s) since the last ask; at least {MIN_SOFT_BEFORE_ASK} are required. "
                                 "Reschedule it later or change it to a soft-CTA value post.")
            if args.dry_run:
                history.append(cta_type)
                print(f"WOULD POST [{cta_type}] {name} → {meta.get('destination', 'personal')} ({author})"
                      f"{' + image ' + image_path if image_path else ''}\n---\n{body}\n---")
                continue
            if image_path:
                payload["content"] = {"media": {"id": li.upload_image(author, image_path),
                                                "altText": meta.get("image_alt", "")[:4000]}}
            urn = li.create_post(payload)
            url = f"https://www.linkedin.com/feed/update/{urn}/" if urn else ""
            write_meta(path, {"status": "posted", "posted_url": url,
                              "posted_at": now.isoformat(timespec="seconds")})
            os.makedirs(os.path.join(ws, "posted"), exist_ok=True)
            shutil.move(path, os.path.join(ws, "posted", name))
            history.append(cta_type)
            posted += 1
            print(f"POSTED {name} → {url or '(no URL returned)'}")
            if meta.get("first_comment"):
                print(f"  Reminder: add the first comment now: {meta['first_comment']}")
        except Exception as e:
            failed += 1
            if not args.dry_run:
                write_meta(path, {"status": "failed", "error": str(e)[:300]})
            print(f"FAILED {name}: {e}")

    if not args.dry_run:
        print(f"Done. Posted {posted}, failed {failed}.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

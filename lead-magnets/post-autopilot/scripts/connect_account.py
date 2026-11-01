#!/usr/bin/env python3
"""
One-time LinkedIn login for Post Autopilot (Method D).

Opens your browser to LinkedIn's official consent screen, receives the
authorization code on http://localhost:8765/callback, exchanges it for an
access token, and saves it to post-autopilot/.env.

Your password is entered only on linkedin.com; this script never sees it.

Usage:
    python3 scripts/connect_account.py                 # personal profile posting
    python3 scripts/connect_account.py --org           # + company Page posting (needs Community Management API)
    python3 scripts/connect_account.py --workspace path/to/post-autopilot

Requires LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET in the .env file
(see references/api-setup.md). Standard library only.
"""
import argparse
import datetime as dt
import http.server
import json
import os
import secrets
import sys
import threading
import urllib.parse
import urllib.request
import webbrowser

REDIRECT_URI = "http://localhost:8765/callback"
AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
USERINFO_URL = "https://api.linkedin.com/v2/userinfo"


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
    return env


def save_env(path, updates):
    lines = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    seen = set()
    for i, line in enumerate(lines):
        key = line.split("=", 1)[0].strip()
        if key in updates and not line.lstrip().startswith("#"):
            lines[i] = f"{key}={updates[key]}"
            seen.add(key)
    for k, v in updates.items():
        if k not in seen:
            lines.append(f"{k}={v}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace", default="post-autopilot")
    ap.add_argument("--org", action="store_true", help="also request w_organization_social for company Page posting")
    args = ap.parse_args()

    env_path = os.path.join(args.workspace, ".env")
    env = {**load_env(env_path), **{k: v for k, v in os.environ.items() if k.startswith("LINKEDIN_")}}
    client_id = env.get("LINKEDIN_CLIENT_ID")
    client_secret = env.get("LINKEDIN_CLIENT_SECRET")
    if not client_id or not client_secret:
        sys.exit(f"Missing LINKEDIN_CLIENT_ID / LINKEDIN_CLIENT_SECRET in {env_path}. "
                 "See references/api-setup.md, step 4.")

    scopes = ["openid", "profile", "w_member_social"]
    if args.org:
        scopes.append("w_organization_social")
    state = secrets.token_urlsafe(24)
    url = AUTH_URL + "?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "scope": " ".join(scopes),
    })

    result = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path != "/callback":
                self.send_response(404)
                self.end_headers()
                return
            q = urllib.parse.parse_qs(parsed.query)
            result.update({k: v[0] for k, v in q.items()})
            ok = "code" in result and result.get("state") == state
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            msg = ("You're connected. You can close this tab and go back to Claude."
                   if ok else "Something went wrong. Go back to the terminal for details.")
            self.wfile.write(f"<html><body style='font-family:sans-serif;padding:40px'><h2>{msg}</h2></body></html>".encode())
            threading.Thread(target=self.server.shutdown, daemon=True).start()

        def log_message(self, *a):
            pass

    server = http.server.HTTPServer(("localhost", 8765), Handler)
    print("Opening LinkedIn in your browser to approve access...")
    print("If it doesn't open, paste this URL into your browser:\n\n" + url + "\n")
    webbrowser.open(url)
    server.serve_forever()

    if "error" in result:
        sys.exit(f"LinkedIn returned an error: {result.get('error')}: {result.get('error_description', '')}")
    if result.get("state") != state or "code" not in result:
        sys.exit("Login was not completed (state mismatch or no code). Please try again.")

    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": result["code"],
        "redirect_uri": REDIRECT_URI,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            tok = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Token exchange failed ({e.code}): {e.read().decode(errors='replace')}")

    access_token = tok["access_token"]
    expires = dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=int(tok.get("expires_in", 0)))

    req = urllib.request.Request(USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        me = json.load(r)

    save_env(env_path, {
        "LINKEDIN_ACCESS_TOKEN": access_token,
        "LINKEDIN_PERSON_URN": f"urn:li:person:{me['sub']}",
        "LINKEDIN_TOKEN_EXPIRES": expires.date().isoformat(),
    })
    print(f"Connected as {me.get('name', 'your LinkedIn account')}.")
    print(f"Token saved to {env_path}. It expires on {expires.date().isoformat()}. Re-run this script before then.")
    print("Make sure .env is listed in your .gitignore. Never share or commit it.")


if __name__ == "__main__":
    main()

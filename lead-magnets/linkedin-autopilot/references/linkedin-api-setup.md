# LinkedIn API setup (Method D)

Walk the user through this one step at a time, confirming each step before the
next. Budget about 15 minutes. LinkedIn sometimes renames screens. If something
doesn't match, ask them what they see.

## 1. Create a LinkedIn developer app

1. Go to **https://www.linkedin.com/developers/apps** and click **Create app**.
2. **App name:** anything, such as "My LinkedIn Autopilot".
3. **LinkedIn Page:** LinkedIn requires every app to be associated with a company Page. Use their business Page. If they don't have one, they can create a free Page first. For personal-profile posting, the Page is only a requirement and nothing gets posted to it.
4. Upload any logo, accept the terms, and click **Create app**.
5. On the **Settings** tab, the Page admin may need to **verify** the app (LinkedIn generates a verification link for the Page admin to approve).

## 2. Add products

On the **Products** tab, request:
- **Sign In with LinkedIn using OpenID Connect** (usually instant)
- **Share on LinkedIn** (usually instant), which gives `w_member_social` for posting as the person
- *(Optional, for company Pages)* **Community Management API**, which requires an application, a business use case, and LinkedIn's approval. It gives `w_organization_social`. If it's denied or pending, post to the Page with Method A, B, or C.

## 3. Set the redirect URL

On the **Auth** tab, under **Authorized redirect URLs for your app**, add exactly:

```
http://localhost:8765/callback
```

Copy the **Client ID** and **Client Secret** from the same tab.

## 4. Save credentials locally

Create `linkedin-autopilot/.env` (and make sure `.env` is in `.gitignore`):

```
LINKEDIN_CLIENT_ID=paste_here
LINKEDIN_CLIENT_SECRET=paste_here
# Optional: only if you have Community Management API access
# LINKEDIN_ORG_ID=12345678
```

The Page's numeric org ID is in the Page admin URL:
`linkedin.com/company/12345678/admin/`.

## 5. Log in once

```
python3 scripts/linkedin_auth.py            # personal profile only
python3 scripts/linkedin_auth.py --org      # also request company Page permission
```

A browser opens, they approve, and the script saves `LINKEDIN_ACCESS_TOKEN`,
`LINKEDIN_PERSON_URN`, and the token's expiry date to `.env`.

Tokens last about **60 days**. Put a reminder in `calendar.md` a week before
`LINKEDIN_TOKEN_EXPIRES` to re-run the login.

## 6. Test

```
python3 scripts/linkedin_post.py --dry-run
python3 scripts/linkedin_post.py --file linkedin-autopilot/queue/test-post.md
```

For the first real test, use a harmless post. If they want to keep the test private,
they can set `visibility: CONNECTIONS` in the post file.

## 7. Automate

Choose one:
- **cron** (Mac/Linux): `crontab -e` → `*/15 * * * * cd /full/path/to/project && /usr/bin/python3 /full/path/to/scripts/linkedin_post.py >> linkedin-autopilot/post.log 2>&1`
- **Windows Task Scheduler:** create a basic task that runs every 15 minutes, with program `python`, arguments `C:\path\to\scripts\linkedin_post.py`, and the project folder as the start directory.
- **GitHub Actions:** copy `templates/github-action.yml` to `.github/workflows/linkedin.yml` in a **private** repo and add `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_PERSON_URN` (and `LINKEDIN_ORG_ID` if used) under Settings → Secrets and variables → Actions. The workflow commits the moved post files back to the repo.

## Troubleshooting

| Error | Likely cause | Fix |
|---|---|---|
| `401 Unauthorized` / `EXPIRED_ACCESS_TOKEN` | Token expired | Re-run `linkedin_auth.py` |
| `403 ACCESS_DENIED` posting as Page | No Community Management API access, or not a Page admin | Use Method A, B, or C for the Page, or check the admin role |
| `redirect_uri does not match` | Redirect URL missing or typo'd | Add exactly `http://localhost:8765/callback` on the Auth tab |
| `unauthorized_scope_error` | Product not added to the app | Add "Share on LinkedIn" and "Sign In with LinkedIn using OpenID Connect" |
| `426` or a version error | LinkedIn retired the API version the script uses | Set `LINKEDIN_API_VERSION=YYYYMM` in `.env` to a current month (see LinkedIn's API versioning docs) |
| `422` duplicate | The same text was posted recently | Edit the text slightly |

## API reference (for Claude)

- OAuth authorize: `https://www.linkedin.com/oauth/v2/authorization`
- Token: `https://www.linkedin.com/oauth/v2/accessToken`
- Who am I: `GET https://api.linkedin.com/v2/userinfo` (`sub` → `urn:li:person:{sub}`)
- Create post: `POST https://api.linkedin.com/rest/posts` with headers `Authorization: Bearer …`, `LinkedIn-Version: YYYYMM`, `X-Restli-Protocol-Version: 2.0.0`, `Content-Type: application/json`. The new post's URN comes back in the `x-restli-id` response header.
- Image upload: `POST https://api.linkedin.com/rest/images?action=initializeUpload` → `PUT` the bytes to `uploadUrl` → reference the returned `urn:li:image:…` in `content.media.id`.
- Post commentary uses LinkedIn's "little text" format, so the characters `| { } @ [ ] ( ) < > # \ * _ ~` must be backslash-escaped. Real hashtags and mentions require special syntax. The script escapes everything and converts plain `#hashtags` into LinkedIn hashtag syntax.

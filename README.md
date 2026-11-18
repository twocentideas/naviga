# navigalaw.com

Static site for Naviga Law, hosted on Cloudflare Pages. No framework, no build dependencies.

```
build.py            ← page content + templates. Edit here, then run: python3 build.py
site/               ← the website Cloudflare serves (generated HTML + assets)
  assets/css, js, img, fonts
  _headers          ← security + caching headers
  _redirects        ← old Squarespace URLs → new pages (301)
functions/api/contact.js   ← form handler (emails submissions via Resend)
wrangler.toml       ← tells Cloudflare the output folder is ./site
```

## 1. Preview on a .pages.dev address

**Option A — GitHub (recommended; every push redeploys)**
1. Push this folder to a private GitHub repo (e.g. `navigalaw-site`).
2. Cloudflare dashboard → Workers & Pages → Create → Pages → *Connect to Git* → pick the repo.
3. Build settings: Framework preset **None**, build command **(leave empty)**, output directory **`site`**.
4. Deploy. You'll get `https://<project>.pages.dev`.

**Option B — from a terminal**
```
npx wrangler login
npx wrangler pages deploy        # reads wrangler.toml, uploads ./site + ./functions
```

> Don't use the dashboard's drag-and-drop upload — it skips the `functions/` folder, so the forms won't work.

Every branch other than `main` gets its own preview URL, so drafts never touch the live site.

## 2. Connect the forms (≈10 min)

1. Create a free account at resend.com, add the domain `navigalaw.com`, and add the DNS records it shows (easy once DNS is on Cloudflare — see step 3).
2. Create an API key.
3. Cloudflare → the Pages project → Settings → Variables and Secrets (Production *and* Preview):
   - `RESEND_API_KEY` = the key (type: Secret)
   - `CONTACT_TO` = `meredith@navigalaw.com` (comma-separate for more than one)
   - `CONTACT_FROM` = `Naviga Law website <web@navigalaw.com>`
4. Redeploy. Submissions arrive by email with Reply-To set to the client.

Until this is done, the forms politely tell visitors to email or call instead.

## 3. Go live on navigalaw.com (replacing Squarespace)

1. **Check email first.** Note where navigalaw.com email is hosted (Google Workspace / Microsoft 365 / Squarespace). The MX records must be copied exactly or email breaks.
2. Add `navigalaw.com` to Cloudflare (free plan). Cloudflare imports existing DNS records — confirm the MX, SPF/TXT and any DKIM records match the current ones.
3. At the registrar (Squarespace Domains if bought there), change the nameservers to the two Cloudflare gives you. Takes minutes to a few hours.
4. Pages project → Custom domains → add `navigalaw.com` and `www.navigalaw.com`. Cloudflare swaps the old Squarespace A/CNAME records for you.
5. Add a redirect so `www` → bare domain (Rules → Redirect Rules, or a Bulk Redirect).
6. Test: home, about, contact, both forms, `/our-team` (should land on Meredith's bio), email still arriving.
7. Submit `https://navigalaw.com/sitemap.xml` in Google Search Console and update the website link on her Google Business Profile.
8. Keep Squarespace a couple of weeks as a fallback, then cancel the site plan (not the domain, unless it's been transferred).

## Editing content

Text lives in `build.py` (services list, bios, contact details). After editing:
```
python3 build.py
```
To change where "Schedule a 30-min consultation" goes (e.g. a Calendly or Cal.com link), set `SCHEDULE_URL` near the top of `build.py`.

Images: replace files in `site/assets/img/` keeping the same names (`.webp` + `.jpg` pair).

## Before launch — open items
- [ ] Meredith to review all copy, especially About (a few small edits were made — see notes).
- [ ] Confirm the attorney-advertising disclaimer wording in the footer meets Maine Bar rules.
- [ ] Decide on a scheduling tool (Calendly / Cal.com / Acuity) or keep the request-a-time form.
- [ ] Connect forms (step 2) and send a test submission from both forms.
- [ ] Optional: Cloudflare Web Analytics (privacy-friendly, no cookie banner needed).

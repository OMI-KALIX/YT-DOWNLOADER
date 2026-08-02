# 🛠️ YouTube Bot-Check & Render Deployment Troubleshooting Guide

This guide explains how YouTube's anti-bot verification challenge (`Sign in to confirm you're not a bot`) and Render deployment issues (such as `[Errno 30] Read-only file system`) were diagnosed and resolved step-by-step.

---

## 1. Summary of Issues Identified

| Issue / Error | Root Cause | Technical Fix Applied |
| :--- | :--- | :--- |
| **`Sign in to confirm you're not a bot`** | YouTube requires Proof-of-Origin (PO) tokens or session cookies on datacenter IPs (e.g. Render). | 1. Installed Deno JS runtime.<br>2. Configured `player_client: ["android", "web"]` fallback.<br>3. Enabled `youtube_cookies.txt` support. |
| **`[Errno 30] Read-only file system`** | Render mounts Secret Files (`/etc/secrets/`) as read-only, but `yt-dlp` attempts to write session updates back to the cookie file. | Added automatic copying of read-only cookie mounts to a writable temp directory (`/tmp/active_youtube_cookies.txt`). |
| **4K/2K Quality Degradation** | `yt-dlp` skipped high-resolution VP9/AV1 streams without JavaScript runtime challenge solvers. | Configured `js_runtimes: {"node": {}, "deno": {}}` and `format_sort: ["res", "fps", "vbr"]`. |

---

## 2. Step-by-Step Fix Implementation

### Step 1: Export Netscape-Format `youtube_cookies.txt`

1. Install the free browser extension **[Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)** (or use Firefox/Edge equivalents).
2. Open **[YouTube.com](https://www.youtube.com)** while logged into your YouTube account.
3. Click the extension icon and select **Export cookies for this domain**.
4. Save the file as **`youtube_cookies.txt`**.

---

### Step 2: Configure Render Secret Files & Environment Variables

1. Log into **[Render Dashboard](https://dashboard.render.com/)** and select your Web Service.
2. Go to **Environment** $\rightarrow$ **Secret Files** $\rightarrow$ Click **Add Secret File**:
   - **Filename**: `youtube_cookies.txt`
   - **Contents**: Paste the full text of your exported `youtube_cookies.txt` file.
   - Click **Save Changes**.
3. Under **Environment Variables**, click **Add Environment Variable**:
   - **Key**: `COOKIES_FILE`
   - **Value**: `/etc/secrets/youtube_cookies.txt`
   - Click **Save Changes**.

---

### Step 3: Writable Cookie File Resolution (Handling `[Errno 30]`)

Because `/etc/secrets/` is a read-only filesystem, the backend in `app/probe.py` and `app/downloader.py` automatically detects read-only mounts and copies the cookie file to writable temp storage:

```python
if path and os.path.exists(path):
    target_path = path
    if not os.access(path, os.W_OK):
        # Copy from read-only mount (Render /etc/secrets/) to writable temp storage
        writable_path = os.path.join(tempfile.gettempdir(), "active_youtube_cookies.txt")
        try:
            shutil.copyfile(path, writable_path)
            target_path = writable_path
        except Exception as e:
            print(f"[yt-dlp] Warning copying read-only cookies file: {e}")
    options["cookiefile"] = target_path
```

---

### Step 4: JavaScript Runtime Engine & Player Client Fallback

YouTube's anti-bot system requires executing JavaScript challenges to resolve `n` signature tokens. The container `Dockerfile` installs Deno:

```dockerfile
# Install Deno JS runtime for yt-dlp YouTube challenge solving
RUN curl -fsSL https://deno.land/x/install/install.sh | sh \
    && mv /root/.deno/bin/deno /usr/local/bin/deno
```

And `yt-dlp` options are configured with client fallbacks:

```python
options: Dict[str, Any] = {
    "quiet": True,
    "no_warnings": True,
    "js_runtimes": {"node": {}, "deno": {}},
    "format_sort": ["res", "fps", "vbr"],
    "extractor_args": {
        "youtube": {
            "player_client": ["android", "web"]
        }
    }
}
```

---

## 3. How to Verify Deployment Health

Open your deployed service's `/healthz` endpoint:

```http
GET https://your-service.onrender.com/healthz
```

Expected JSON response when correctly configured:

```json
{
  "status": "ok",
  "cookies_env": "/etc/secrets/youtube_cookies.txt",
  "active_cookie_file": "/tmp/active_youtube_cookies.txt",
  "cookies_exist": true
}
```

If `cookies_exist` is `true`, your deployment is fully authenticated and protected against YouTube's anti-bot verification challenges!

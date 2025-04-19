from flask import Flask, request, redirect, render_template_string
import logging
from datetime import datetime

app = Flask(__name__)

# === Config ===
REDIRECT_AFTER_SECONDS = 30
LOG_FILE = "visitor_log.txt"

# === OnClick Ad Scripts with Priority Logic ===
ad_scripts = """
<!-- OnClick Ads with Chaining -->
<script>
  function loadAd(zoneId) {
    const script = document.createElement('script');
    script.src = 'https://shebudriftaiter.net/tag.min.js';
    script.setAttribute('data-zone', zoneId);
    (document.body || document.documentElement).appendChild(script);
  }

  // Load first ad
  loadAd(9233373);

  // Setup ad chaining after user interaction
  document.addEventListener('click', () => {
    setTimeout(() => {
      loadAd(9233412);
    }, 1000); // 1s delay after first interaction

    document.removeEventListener('click', arguments.callee);
  });
</script>
"""

# === Home Page ===
@app.route("/")
def home():
    return f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <meta name="monetag" content="28d87cfad14ca2c792a76293e20949f6">
        <title>MyClicks Store</title>
      </head>
      <body>
        <h1>Welcome to MyClicks Store</h1>
        <p>Stay on the page to support us by viewing ads.</p>
        {ad_scripts}
      </body>
    </html>
    """

# === Redirect Page Template ===
page_template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="{{ delay }};url={{ target }}">
  <meta name="monetag" content="28d87cfad14ca2c792a76293e20949f6">
  <title>Redirecting...</title>
</head>
<body>
  {{ ad_code|safe }}
  <p style="text-align:center;margin-top:20px;">You will be redirected in {{ delay }} seconds...</p>
</body>
</html>
"""

# === Logger ===
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# === /go Route ===
@app.route('/go')
def redirect_view():
    target = request.args.get('url', 'https://example.com')
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    ref = request.headers.get('Referer', 'Direct')
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Log the visit
    logging.info(f"{now} | IP: {ip} | UA: {ua} | From: {ref} => {target}")

    return render_template_string(page_template, delay=REDIRECT_AFTER_SECONDS, target=target, ad_code=ad_scripts)

# === Run App ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

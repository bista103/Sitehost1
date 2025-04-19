from flask import Flask, request, redirect, render_template_string
import time
import logging
from datetime import datetime

app = Flask(__name__)

# === Config ===
REDIRECT_AFTER_SECONDS = 5
LOG_FILE = "visitor_log.txt"

# === Ad Placeholder (Replace with real ad code later) ===
ad_html = """
<div style='width: 100%; padding: 20px; text-align: center; background: #f9f9f9;'>
  <h3>Advertisement</h3>
  <p>This is a placeholder. Insert your ad network script here.</p>
</div>
"""

# === Landing Page Template ===
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

# === Route ===
@app.route('/go')
def redirect_view():
    target = request.args.get('url', 'https://example.com')
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    ref = request.headers.get('Referer', 'Direct')
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Log the visit
    logging.info(f"{now} | IP: {ip} | UA: {ua} | From: {ref} => {target}")

    return render_template_string(page_template, delay=REDIRECT_AFTER_SECONDS, target=target, ad_code=ad_html)

# === Run App ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

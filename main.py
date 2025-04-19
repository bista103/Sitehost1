from flask import Flask, request, redirect, render_template_string
import logging
from datetime import datetime

app = Flask(__name__)

# === Config ===
REDIRECT_AFTER_SECONDS = 30
LOG_FILE = "visitor_log.txt"

# === Ad Code Injection ===
ad_html = """
<!-- Bright Tag -->
<script>(function(d,z,s){s.src='https://'+d+'/400/'+z;try{(document.body||document.documentElement).appendChild(s)}catch(e){}})('vemtoutcheeg.com',9233249,document.createElement('script'))</script>

<!-- Positive Tag -->
<script>(function(s,u,z,p){s.src=u,s.setAttribute('data-zone',z),p.appendChild(s);})(document.createElement('script'),'https://shebudriftaiter.net/tag.min.js',9233225,document.body||document.documentElement)</script>

<!-- Optional: PropellerAds Push Script -->
<script data-cfasync="false" type="text/javascript" src="https://upgulpinon.com/1?z=6027370"></script>
"""

# === Landing Page Template ===
page_template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Redirecting...</title>
  <script type="text/javascript">
    setTimeout(function() {
      window.location.href = "{{ target }}";
    }, {{ delay * 1000 }}); // Delay in milliseconds
  </script>
</head>
<body>
  {{ ad_code|safe }}
  <p style="text-align:center;margin-top:20px;">
    Please wait... You will be redirected in {{ delay }} seconds.
  </p>
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

    logging.info(f"{now} | IP: {ip} | UA: {ua} | From: {ref} => {target}")

    return render_template_string(
        page_template,
        delay=REDIRECT_AFTER_SECONDS,
        target=target,
        ad_code=ad_html
    )

# === Run App ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

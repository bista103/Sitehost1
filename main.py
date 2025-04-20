from flask import Flask, request, redirect, render_template_string
import logging
from datetime import datetime

app = Flask(__name__)

# === Config ===
REDIRECT_AFTER_SECONDS = 30
LOG_FILE = "visitor_log.txt"

# === New Ad Scripts ===
ad_scripts = """
<!-- Banner Ad -->
<script type=\"text/javascript\">
\tatOptions = {
\t\t'key' : '9169a46ee81b0140c7551d9cd809ca0c',
\t\t'format' : 'iframe',
\t\t'height' : 90,
\t\t'width' : 728,
\t\t'params' : {}
\t};
</script>
<script type=\"text/javascript\" src=\"//www.highperformanceformat.com/9169a46ee81b0140c7551d9cd809ca0c/invoke.js\"></script>

<!-- Social Bar Ad -->
<script type='text/javascript' src='//pl26427786.profitableratecpm.com/53/4d/3c/534d3c4331b30b66cd259fbb1e426246.js'></script>

<!-- Additional Ad Unit -->
<script async=\"async\" data-cfasync=\"false\" src=\"//pl26427849.profitableratecpm.com/32303644a088d2160e9900739bf884b8/invoke.js\"></script>
<div id=\"container-32303644a088d2160e9900739bf884b8\"></div>
"""

# === Home Page ===
@app.route("/")
def home():
    return f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset=\"UTF-8\">
        <meta name=\"monetag\" content=\"28d87cfad14ca2c792a76293e20949f6\">
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
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta http-equiv=\"refresh\" content=\"{{ delay }};url={{ target }}\">
  <meta name=\"monetag\" content=\"28d87cfad14ca2c792a76293e20949f6\">
  <title>Redirecting...</title>
</head>
<body>
  {{ ad_code|safe }}
  <p style=\"text-align:center;margin-top:20px;\">You will be redirected in {{ delay }} seconds...</p>
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


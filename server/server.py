from bottle import get, post, request, abort, run, static_file
import time
import os

index_template = """
<!DOCTYPE html>
<html>
    <head>
        <title>Tater Timer</title>
        <link rel="icon" href="/tater"/>
        <meta http-equiv="refresh" content="10"/>
        <style>
            * {
                font-family: sans-serif;
            }

            body {
                font-size: 32px;
                text-align: center;
            }
        </style>
    </head>
    <body>%s</body>
</html>
"""

last_time = time.time()
password = os.getenv("TATER_PASSWORD", "tater")

@get('/')
def index():
    time_since = time.time() - last_time
    h = time_since/3600
    m = time_since/60
    s = time_since%60
    message = "<p>the boy last went out %d:%02d:%02d ago.</p>" % (h,m,s)
    if time_since > 7200:
        message += "<p>take the boy outside!</p>"
    return index_template % (message,)

@get('/tater')
def tater():
    return static_file("tater.jpg", ".")

@post('/reset')
def reset():
    p = request.forms.get("password")
    if p != password:
        abort(401, "that ain't the password, bub")
    global last_time
    last_time = time.time()
    return "boop"

run(host='0.0.0.0', port=80, debug=False)

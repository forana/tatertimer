from bottle import get, post, request, abort, run, static_file, template
import time
import os

index_template = """
<!DOCTYPE html>
<html>
    <head>
        <title>Tater Timer</title>
        <link rel="icon" href="/tater">
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
    <body>
        {{body}}
    </body>
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
    message = "The boy last went out %d:%02d:%02d ago." % (h,m,s)
    return template(index_template, body = message)

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
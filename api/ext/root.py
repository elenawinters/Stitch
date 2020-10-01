from ..api import app, loop, base
from flask import render_template


@app.route("/")
def root():
    msg = 'Stitch API Root\n\n' \
          'This API exists to assist programmers in optimizing certain functions of their bot.\n' \
          'When running multiple bots, data management should be handled by the API.'
    return render_template('base.html', render=msg)

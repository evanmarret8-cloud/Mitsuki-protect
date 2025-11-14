from flask import Flask
from threading import Thread
import logging

app = Flask('')

# Désactiver les logs de Flask
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def home():
    return "Bot Online"

def run():
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=False,
        use_reloader=False
    )

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

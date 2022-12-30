from flask import *
from datetime import datetime, date
import time
from threading import Thread
import logging

resname = ""
restsec = 0

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def sleeper():
    time.sleep(1)
    global restsec
    restsec = restsec - 1
    if restsec > 0:
        t = Thread(target=sleeper)
        t.start()

app = Flask(__name__)

@app.route('/treppe/sta')
def sta():
    global restsec
    global resname
    di = {}
    di["name"] = resname
    di["restsec"] = restsec
    return Response(json.dumps(di), mimetype='text/json')

@app.route('/treppe/res/<name>')
def res(name):
    global resname
    global restsec
    if restsec <= 0:
        logging.warning("Reservierung von " + name + " um " + str(datetime.now()))
        resname = name
        restsec = 20
        t = Thread(target=sleeper)
        t.start()
    return ""

@app.route('/treppe/gui/<name>')
def gui(name):
    return render_template('gui.html', name=name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


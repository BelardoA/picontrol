#!/usr/bin/python 
#app.py
import os, psutil, json, logging
from flask import Flask, render_template, jsonify, request, session, redirect
from flask_httpauth import HTTPBasicAuth
from flask_api import status

from user import User
from config import Config
from game import Game
from settings import Settings
from nfc import NFC
from profile import Profile

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

auth = HTTPBasicAuth()

fan = 'Off'

## flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890' #os.urandom(12)

@auth.verify_password
def verify_password(token, password):
    session['username'] = ''
    # authenticate by token
    sessionUser = User.verify_auth_token(token, app.config['SECRET_KEY'])
    if sessionUser != None:
        session['username'] = sessionUser.username
        return True
    # authenticate with username/password
    config = Config.loadConfig()        
    appUsername = config.get("user","username")
    appPassword = config.get("user","password")
    if token == appUsername and password == appPassword:
        sessionUser = User()
        sessionUser.username = token
        session['username'] = sessionUser.username
        return True
    # unable to authenticate
    return False

@app.route('/')
def index():
    return render_template('index.html')

## auth calls
@app.route('/token', methods=['POST'])
def get_auth_token():
    if verify_password(request.form['username'], request.form['password']) == True:
        if 'username' in session:
            sessionUser = User()
            sessionUser.username = session['username']
            if sessionUser.username != '':
                token = sessionUser.generate_auth_token(app.config['SECRET_KEY'])
                response_data = {'access_token': token.decode('ascii')}
                return json.dumps(response_data), 200, {'Content-Type': 'application/json'}
    return "Unauthorized", 401

@app.route('/api/test')
@auth.login_required
def get_test():
    return jsonify({'test': 'success'})

## api calls
@app.route('/api/pi/shutdown', methods=['GET','POST'])
def shutdown():
    os.system("sudo shutdown -h now")
    return jsonify(True)

@app.route('/api/pi/reboot', methods=['GET','POST'])
def reboot():
    os.system("sudo reboot")
    return jsonify(True)

@app.route('/api/pi/info')
@auth.login_required
def getPiInfo():
    global fan

    res = os.popen('vcgencmd measure_temp').readline()
    temp1 = float(res.replace("temp=","").replace("'C\n",""))
    temp2 = float(temp1 * 1.8) + 32.0
    temp1 = "{0:.2f}".format(temp1)
    temp2 = "{0:.2f}".format(temp2)

    thresholdOff = 50
    thresholdOn = 60

    try:
        fanConfig = Config.loadConfig()
        thresholdOff = float(fanConfig.get("fan", "thresholdOff")) 
        thresholdOn = float(fanConfig.get("fan", "thresholdOn")) 
    except:
        pass

    if float(temp1) >= thresholdOn:
        fan = 'On'
    if fan == 'On' and float(temp1) <= thresholdOff:
        fan = 'Off'

    cpuUsage = psutil.cpu_percent(interval=1)
    cpuUsage = "{0:.2f}".format(cpuUsage)

    memUsage = psutil.virtual_memory()
    memUsage = "{0:.2f}".format(memUsage[2])

    info = {'celsius':temp1, 'fahrenheit':temp2, 'fan':fan, 'cpuUsage':cpuUsage, 'memUsage':memUsage}
    return jsonify(info)

@app.route('/api/profile/user/update', methods=["POST"])
@auth.login_required
def setUser():
    user = json.loads(request.data)
    return jsonify(Profile.setUser(user))

@app.route('/api/profile/user', methods=["GET"])
@auth.login_required
def getUser():
    return jsonify(Profile.getUser())

@app.route('/api/profile/theme/update', methods=["POST"])
@auth.login_required
def updateTheme():
    theme = json.loads(request.data)
    return jsonify(Profile.setTheme(theme))

@app.route('/api/profile/theme', methods=["GET"])
def getTheme():
    return jsonify(Profile.getTheme())

@app.route('/api/pi/settings/fan/update', methods=["POST"])
@auth.login_required
def updateFanSettings():
    fanSettings = json.loads(request.data)
    return jsonify(Settings.setFanSettings(fanSettings))

@app.route('/api/pi/settings/fan', methods=["GET"])
@auth.login_required
def getFanSettings():
    return jsonify(Settings.getFanSettings())

@app.route('/api/pi/settings/button/update', methods=["POST"])
@auth.login_required
def updateButtonSettings():
    buttonSettings = json.loads(request.data)
    return jsonify(Settings.setButtonSettings(buttonSettings))

@app.route('/api/pi/settings/version', methods=["GET"])
@auth.login_required
def getVersion():
    return jsonify(Settings.getVersion())

@app.route('/api/pi/settings/version/check', methods=["GET"])
@auth.login_required
def checkUpdates():
    return jsonify(Settings.checkUpdates())

@app.route('/api/pi/settings/version/update', methods=["GET"])
@auth.login_required
def updateVersion():
    return jsonify(Settings.updateVersion())

@app.route('/api/pi/settings/button', methods=["GET"])
@auth.login_required
def getButtonSettings():
    return jsonify(Settings.getButtonSettings())

@app.route('/api/game/consoles', methods=["GET"])
@auth.login_required
def getConsoleList():
    return jsonify(Game.getConsoleList())

@app.route('/api/game/games', methods=["POST"])
@auth.login_required
def getGameList():
    consoleInfo = json.loads(request.data)
    return jsonify(Game.getGameList(consoleInfo))

@app.route('/api/game/upload', methods=["POST"])
@auth.login_required
def uploadGames():
    return jsonify(Game.uploadGames(request))

@app.route('/api/game/delete', methods=["POST"])
@auth.login_required
def deleteGame():
    return jsonify(Game.deleteGame(request.data))

@app.route('/api/game/run', methods=["POST"])
@auth.login_required
def runGame():
    return jsonify(Game.runGame(request.data))

@app.route('/api/nfc/read', methods=["GET"])
@auth.login_required
def readNFC():
    return jsonify(NFC.readNFC())

@app.route('/api/nfc/write', methods=["POST"])
@auth.login_required
def writeNFC():
    return jsonify(NFC.writeNFC(request.data))

## init app
if __name__ == '__main__':
    app.run(debug=False, threaded=True, host='0.0.0.0', port=8080)
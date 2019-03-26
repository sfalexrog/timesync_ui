from flask import Flask, request, render_template, jsonify
import ntplib
from datetime import datetime

from chrony_conf.chrony_conf import ChronyConf

app = Flask(__name__)

@app.route('/')
def echo():
    ip = request.remote_addr
    return render_template('timesync_params.html', ip=ip)


@app.route('/try_time_sync')
def try_time_sync():
    ntp = ntplib.NTPClient()
    ip = request.remote_addr
    try:
        response = ntp.request(ip, version=4, timeout=5)
    except ntplib.NTPException:
        return 'Could not retrieve data from remote ip; ntp server is not active', 500
    return str(datetime.fromtimestamp(response.tx_time)), 200


@app.route('/get_timesync_config')
def get_timesync_config():
    try:
        config = ChronyConf.readConfig(configfile='/etc/chrony/chrony.conf')
        lines = []
        for option, value in config.config.iteritems():
            optlist = [option]
            optlist.extend(str(val) for val in value)
            optline = ' '.join(optlist)
            lines.append(optline)
        return '\n'.join(lines)
    except:
        return 'Could not read Chrony config', 500


@app.route('/set_timesync_config')
def set_timesync_config():
    ip = request.remote_addr
    config = ChronyConf(configfile='/etc/chrony/chrony.conf')
    config.config['server'] = [ip, 'iburst']
    config.config['driftfile'] = ['/var/lib/chrony/drift']
    config.config['makestep'] = ['1.0', '3']
    config.config['rtcsync'] = ['']
    try:
        config.writeConfig()
    except:
        return 'Could not write config', 500
    return 'Config written successfully', 200


app.run(host='0.0.0.0', port=12345)

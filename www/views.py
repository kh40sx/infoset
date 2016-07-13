import yaml
import time
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from infoset.db.agent import Get, GetDataPoint, GetData
from flask import render_template, jsonify, send_file, request
from www import infoset
from os import listdir, walk, path, makedirs, remove
from infoset.utils.rrd.rrd_xlate import RrdXlate


@infoset.route('/')
def index():
    hosts = getHosts()
    return render_template('index.html',
                           hosts=hosts)


@infoset.route('/hosts')
def hosts():
    hosts = getHosts()
    return jsonify(hosts)


@infoset.route('/hosts/<host>')
def host(host):
    filename = host + ".yaml"
    filepath = path.join("./www/static/yaml/", filename)
    yaml_dump = {}
    with open(filepath, 'r') as stream:
        try:
            yaml_dump = yaml.load(stream)
        except Exception as e:
            raise e
    return jsonify(yaml_dump)


@infoset.route('/hosts/<host>/layer1')
def layerOne(host):
    filename = host + ".yaml"
    filepath = path.join("./www/static/yaml/", filename)
    yaml_dump = {}
    with open(filepath, 'r') as stream:
        try:
            yaml_dump = yaml.load(stream)
        except Exception as e:
            raise e
    layer1 = yaml_dump['layer1']
    return jsonify(layer1)


@infoset.route('/hosts/<host>/layer2')
def layerTwo(host):
    filename = host + ".yaml"
    filepath = path.join("./www/static/yaml/", filename)
    yaml_dump = {}
    with open(filepath, 'r') as stream:
        try:
            yaml_dump = yaml.load(stream)
        except Exception as e:
            raise e
    layer2 = yaml_dump['layer2']
    return jsonify(layer2)


@infoset.route('/devices')
def devices():
    hosts = getHosts()
    devices = getDevices()
    return render_template('devices.html',
                           hosts=hosts,
                           devices=devices)


@infoset.route('/receive/<uid>', methods=["POST"])
def receive(uid):
    # TODO replace with config obj
    config = infoset.config['GLOBAL_CONFIG']
    cache_dir = config.ingest_cache_directory()
    # Get Json from incoming POST
    data = request.json
    timestamp = data['timestamp']
    data_uid = data['uid']
    json_path = cache_dir + ("/%s_%s.json") % (timestamp, str(data_uid))
    with open(json_path, "w+") as temp_file:
        json.dump(data, temp_file)
        temp_file.close()
    print("Agent:%s recieved" % uid)
    return "Recieved"


@infoset.route('/fetch/agent/<uid>', methods=["GET", "POST"])
def fetch_agent_dp(uid):
    config = infoset.config['GLOBAL_CONFIG']
    agent = Get(uid, config)
    idx = agent.idx()
    # Gets all associated datapoints
    datapoints = GetDataPoint(idx, config)
    return jsonify(datapoints.everything())


@infoset.route('/fetch/agent/<uid>/<datapoint>', methods=["GET", "POST"])
def fetch_dp(uid, datapoint):
    # TODO implement start and stop times
    config = infoset.config['GLOBAL_CONFIG']
    data = GetData(datapoint, config)
    data_values = data.everything()
    # Gets all associated datapoints
    """
    x_axis = []
    y_axis = []
    for key, value in data_values.items():
        x_axis.append(key)
        y_axis.append(value)
    np_x_axis = np.asarray(x_axis)
    np_y_axis = np.asarray(y_axis)
    plt.plot(np_x_axis, np_y_axis)
    plt.savefig("/home/proxima/public_html/graph.png")
    """
    return jsonify(data_values)

def getHosts():
    hosts = {}
    for root, directories, files in walk('./www/static/yaml'):
        for filename in files:
            filepath = path.join(root, filename)
            hosts[filename[:-5]] = filepath  # Add it to the list.
    return hosts


def getDeviceDetails(uid):
    active_yaml = {}
    filepath = "./www/static/devices/linux/" + str(uid) + "/active.yaml"
    with open(filepath, 'r') as stream:
        try:
            active_yaml = yaml.load(stream)
        except Exception as e:
            raise e
    return active_yaml


def getDevices():
    active_yamls = {}
    devices = []
    root = "./www/static/devices/linux/"
    directories = [d for d in listdir(root) if path.isdir(path.join(root, d))]

    for directory in directories:
        filepath = "./www/static/devices/linux/" + directory + "/active.yaml"
        active_yamls[directory] = filepath

        with open(filepath, 'r') as stream:
            try:
                yaml_dump = yaml.load(stream)
            except Exception as e:
                raise e
        devices.append(yaml_dump)
    return devices

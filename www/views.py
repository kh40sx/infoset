import yaml
import time
import json
from infoset.db.agent import Get, GetDataPoint
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
    cache_dir = "/tmp/infoset_cache/"
    # Get Json from incoming POST
    data = request.json
    json_path = cache_dir + ("%s_%s.json") % (int(time.time()), str(uid))
    with open(json_path, "w+") as temp_file:
        json.dump(data, temp_file)
        temp_file.close()
    print("Agent:%s recieved" % uid)
    return "Recieved"


@infoset.route('/fetch/agent/<uid>', methods=["GET", "POST"])
def fetch_agent_dp(uid):
    db_config = infoset.config['DB_CONFIG']
    agent = Get(uid, db_config)
    idx = agent.idx()
    # Gets all associated datapoints
    datapoints = GetDataPoint(idx, db_config)
    print(datapoints.everything())
    return "PONG"


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

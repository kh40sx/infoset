from flask import render_template, jsonify, send_file
from www import infoset
from os import listdir, walk, path
import yaml
import requests
from infoset.utils.rrd import rrdagent
import time
import threading
import os.path


@infoset.route('/')
def index():
    hosts = getHosts()
    agent = rrdagent.RrdAgent('cpu.rrd', 5)
    agent.create()
    t = threading.Thread(target=chartCPU, args=(agent,))
    t.daemon = True
    t.start()
    return render_template('index.html',
                           hosts=hosts)


def chartCPU(agent):
    count = 0
    while True:
        time.sleep(5)
        agent.update()
        agent.graph()


@infoset.route('/hosts/<host>/cpu')
def getCpu(host):
    return send_file('static/img/cpu.png', mimetype='image/gif')


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


def getHosts():
    hosts = {}
    for root, directories, files in walk('./www/static/yaml'):
        for filename in files:
            filepath = path.join(root, filename)
            hosts[filename[:-5]] = filepath  # Add it to the list.
    return hosts

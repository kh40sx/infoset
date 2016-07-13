"""Module of infoset webserver routes.

Contains all routes that infoset's Flask webserver uses

"""
import yaml
import time
import json
from infoset.db.agent import Get, GetDataPoint, GetData
from flask import render_template, jsonify, send_file, request
from www import infoset
from os import listdir, walk, path, makedirs, remove

# Matplotlib imports, Do not edit order
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
# End of Imports



@infoset.route('/')
def index():
    """Function for handling home route.

    Args:
        None

    Returns:
        Home Page

    """
    return render_template('index.html')


@infoset.route('/hosts/<host>')
def host(host):
    """Function for handling /hosts/<host> route.

    Args:
        host: IP address of a local host

    Returns:
        JSON response of different layers of specified host

    """
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
    """Function for handling /hosts/<host>/layer1 route.

    Args:
        host: IP address of a local host

    Returns:
        JSON response of layer1 of the OSI model of the specified host

    """
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
    """Function for handling /hosts/<host>/layer2 route.

    Args:
        host: IP address of a local host

    Returns:
        JSON response of layer2 of the OSI model of the specified host

    """    
    filename = host + ".yaml"
    filepath = path.join("./www/static/yaml/", filename)
    yaml_dump = {}

    with open(filepath, 'r') as stream:
        try:
            yaml_dump = yaml.load(stream)
        except Exception as e:
            raise e
    # Gets layer2 from loaded yaml
    layer2 = yaml_dump['layer2']

    return jsonify(layer2)


@infoset.route('/receive/<uid>', methods=["POST"])
def receive(uid):
    """Function for handling /receive/<uid> route.

    Args:
        uid: Unique Identifier of an Infoset Agent

    Returns:
        Text response of Received

    """    
    # TODO replace with config obj
    config = infoset.config['GLOBAL_CONFIG']
    cache_dir = config.ingest_cache_directory()
    
    # Get Json from incoming agent POST
    data = request.json
    timestamp = data['timestamp']
    data_uid = data['uid']
    json_path = cache_dir + ("/%s_%s.json") % (timestamp, str(data_uid))

    with open(json_path, "w+") as temp_file:
        json.dump(data, temp_file)
        temp_file.close()
    
    print("Agent:%s recieved" % uid)
    return "Received"


@infoset.route('/fetch/agent/<uid>', methods=["GET", "POST"])
def fetch_agent_dp(uid):
    """Function for handling /fetch/agent/<uid> route.

    Args:
        uid: Unique Identifier of an Infoset Agent

    Returns:
        JSON response of all datapoints

    """  
    config = infoset.config['GLOBAL_CONFIG']

    # Fetches agent from mysql by uid
    agent = Get(uid, config)
    idx = agent.idx()
    
    # Gets all datapoints associated with agent
    datapoints = GetDataPoint(idx, config)
    return jsonify(datapoints.everything())


@infoset.route('/fetch/agent/<uid>/<datapoint>', methods=["GET", "POST"])
def fetch_dp(uid, datapoint):
    """Function for handling /fetch/agent/<uid>/<datapoint> route.

    Args:
        uid: Unique Identifier of an Infoset Agent

    Returns:
        JSON response of all data under specific datapoint

    """ 
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

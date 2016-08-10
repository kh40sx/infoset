"""Module of infoset webserver routes.

Contains all routes that infoset's Flask webserver uses

"""
# Standard imports
import yaml
import time
import json
import pprint
from os import listdir, walk, path, makedirs, remove

# Pip imports
from flask import render_template, jsonify, send_file, request, make_response

# Infoset imports
from infoset.db.db_agent import Get
from infoset.db.db_data import GetIDX
from infoset.db.db_agent import GetDataPoint
from infoset.db.db_orm import Agent
from infoset.db.db_datapoint import GetSingleDataPoint
from infoset.db.db_chart import StackedChart
from infoset.db.db_chart import Chart
from infoset.db.db import Database
from infoset.utils import TimeStamp
from infoset.utils import ColorWheel
from infoset.utils import jm_general
from infoset.language import language
from www import infoset
# Matplotlib imports, Do not edit order
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
# End of Imports
"""


@infoset.template_filter('strftime')
def _jinja2_filter_datetime(timestamp, fmt=None):
    timestamp = time.strftime('%H:%M (%d-%m-%Y) ', time.localtime(timestamp))
    return timestamp


@infoset.route('/')
def index():
    """Function for handling home route.

    Args:
        None

    Returns:
        Home Page

    """
    # Get UID of _infoset agent
    database = Database()
    session = database.session()
    record = session.query(Agent.id).filter(Agent.idx == 1).one()
    uid = record.id
    session.close()

    # Get agent information
    agent = Get(uid)
    host = agent.hostname()
    agent_list = [agent.everything()]
    datapoints = GetDataPoint(agent.idx())
    data_point_dict = datapoints.everything()

    # Render the home page
    return render_template('index.html',
                           data=data_point_dict,
                           agent_list=agent_list,
                           uid=uid,
                           hostname=host)


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


@infoset.route('/graphs/<uid>/<datapoint>', methods=["GET", "POST"])
def graphs(uid, datapoint):
    """Create graphs.

    Args:
        uid: Agent uid
        datpoint: Datapoint idx

    Returns:
        None

    """
    preset = TimeStamp()
    timestamps = preset.get_times()
    return render_template('graphs.html',
                           timestamps=timestamps,
                           uid=uid,
                           datapoint=datapoint)


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
    uid = data['uid']
    hostname = data['hostname']

    # Create a hash of the hostname
    host_hash = jm_general.hashstring(hostname, sha=1)
    json_path = ('%s/%s_%s_%s.json') % (cache_dir, timestamp, uid, host_hash)

    with open(json_path, "w+") as temp_file:
        json.dump(data, temp_file)
        temp_file.close()

    return "Received"


@infoset.route('/fetch/agent/<uid>', methods=["GET", "POST"])
def fetch_agent_dp(uid):
    """Function for handling /fetch/agent/<uid> route.

    Args:
        uid: Unique Identifier of an Infoset Agent

    Returns:
        JSON response of all datapoints

    """
    # Fetches agent from mysql by uid
    agent = Get(uid)
    idx = agent.idx()

    # Gets all datapoints associated with agent
    datapoints = GetDataPoint(idx)
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
    data = GetIDX(datapoint)
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


@infoset.route('/fetch/agent/graph/<uid>/<datapoint>', methods=["GET", "POST"])
def fetch_graph(uid, datapoint):
    """Create graph.

    Args:
        uid: Agent uid
        datpoint: Datapoint idx

    Returns:
        None

    """
    filename = uid + '_' + datapoint
    filepath = './www/static/img/' + filename

    # Getting start and stop parameters from url
    start = request.args.get('start')
    stop = request.args.get('stop')

    # Config object
    config = infoset.config['GLOBAL_CONFIG']
    if start and stop:
        chart = Chart(datapoint,
                      image_width=12,
                      image_height=4,
                      text_color='#272727',
                      start=int(start),
                      stop=int(stop))
    else:
        chart = Chart(datapoint,
                      image_width=12,
                      image_height=4,
                      text_color='#272727')

    # create specific chart
    single_datapoint = GetSingleDataPoint(datapoint)
    agent_label = single_datapoint.agent_label()
    color_palette = ColorWheel(agent_label)

    #########################################################################
    #########################################################################
    #########################################################################
    # URL issue needs to be fixed.
    #########################################################################
    #########################################################################
    #########################################################################

    # Get the label for the chart from the language class
    # Start with the agent name
    # For some reason we are posting urls that appear to be bytes
    # but are in fact strings. This strips the extraneous characters
    uid_fixed= uid[2:-1].encode()
    agent_name = Get(uid_fixed).name()
    lang = language.Agent(agent_name)
    chart_label = lang.label_description(agent_label)

    # Print the chart
    # chart_label = agent_label.decode()
    png_output = chart.api_single_line(
        chart_label, 'Data',
        color_palette.get_scheme(), filepath,
    )
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


@infoset.route(
    '/fetch/agent/graph/stacked/<uid>/<datapoint>', methods=["GET", "POST"])
def fetch_graph_stacked(uid, datapoint):
    """Process stacked charts.

    Args:
        uid: Agent uid
        datpoint: Datapoint idx

    Returns:
        None

    """
    # Initialize key variables
    filename = str(uid) + '_' + str(datapoint)
    filepath = './www/static/img/' + filename

    # Getting start and stop parameters from url
    start = request.args.get('start')
    stop = request.args.get('stop')

    # Config object
    config = infoset.config['GLOBAL_CONFIG']

    datapoint_list = [86, 82]
    values = []
    for datapoint in datapoint_list:
        get_idx = GetIDX(datapoint)
        data = get_idx.everything()
        values.append(data)
    new_chart = StackedChart(values)
    """
    if start and stop:
        chart = Chart(datapoint, config,
                      image_width=12,
                      image_height=4,
                      text_color='#272727',
                      start=int(start),
                      stop=int(stop))
    else:
        chart = Chart(datapoint, config,
                      image_width=12,
                      image_height=4,
                      text_color='#272727')
    """
    # create specific chart
    single_datapoint = GetSingleDataPoint(datapoint)
    agent_label = single_datapoint.agent_label()
    color_palette = ColorWheel(agent_label)

    png_output = new_chart.create_stacked(
        'Stacked', 'test', '#000000', filepath)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

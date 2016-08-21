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
from infoset.db.db_agent import GetUID
from infoset.db.db_data import GetIDX
from infoset.db.db_agent import GetDataPoint
from infoset.db.db_orm import Agent
from infoset.db.db_datapoint import GetSingleDataPoint
from infoset.db.db_chart import Chart
from infoset.db.db import Database
from infoset.utils import TimeStamp
from infoset.utils import ColorWheel
from infoset.utils import jm_general
from infoset.metadata import language
from www import infoset
from infoset.web import ws_device
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
    uid = record.id.decode('utf-8')
    session.close()

    # Get agent information
    agent = GetUID(uid)
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
@infoset.route('/<uid>')
def overview(uid):
    # Get agent information
    agent = Get(uid_fixed)
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

@infoset.route('/<uid>/datapoints')
def datapoints(uid):
    # Get agent information
    uid_fixed= uid[2:-1].encode()
    agent = Get(uid_fixed)
    host = agent.hostname()
    agent_list = [agent.everything()]
    datapoints = GetDataPoint(agent.idx())
    data_point_dict = datapoints.everything()
    
    return render_template('datapoints.html',
                           data=data_point_dict,
                           agent_list=agent_list,
                           uid=uid,
                           hostname=host)

@infoset.route('/search')
def search():
    database = Database()
    session = database.session()
    agent_list = []
    for agent in session.query(Agent):
        print(agent)
        agent_list.append(agent)
    return render_template('search.html',
                            agent_list=agent_list)

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
    agent = GetUID(uid)
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
    filename = str(uid) + '_' + str(datapoint)
    filepath = './www/static/img/' + filename

    # Getting start and stop parameters from url
    start = request.args.get('start')
    stop = request.args.get('stop')
        # Get data as dict

    datapointer = GetIDX(datapoint, start=start, stop=stop)
    data = datapointer.everything()

    # Config object
    config = infoset.config['GLOBAL_CONFIG']

    if start and stop:
        chart = Chart(data,
                      image_width=12,
                      image_height=4,
                      text_color='#272727',
                      start=int(start),
                      stop=int(stop))
    else:
        chart = Chart(data,
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
    # URL issue needs to be fixed. It is affecting png filenames too
    #########################################################################
    #########################################################################
    #########################################################################

    # Get the label for the chart from the language class
    # Start with the agent name
    # For some reason we are posting urls that appear to be bytes
    # but are in fact strings. This strips the extraneous characters
    agent_name = GetUID(uid).name()
    lang = language.Agent(agent_name)
    chart_label = lang.label_description(agent_label)

    # Print the chart
    png_output = chart.api_single_line(
        chart_label, 'Data',
        color_palette.get_scheme(), filepath,
    )
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


@infoset.route(
    '/fetch/agent/graph/stacked/<uid>/<stack_type>', methods=["GET", "POST"])
def fetch_graph_stacked(uid, stack_type):
    """Process stacked charts.

    Args:
        uid: Agent uid
        datpoint: Datapoint idx

    Returns:
        Image of Stacked Chart

    """
    # Initialize key variables
    filename = str(uid) + '_' + str(stack_type)
    filepath = './www/static/img/' + filename

    # Getting start and stop parameters from url
    start = request.args.get('start')
    stop = request.args.get('stop')

    # Config object
    config = infoset.config['GLOBAL_CONFIG']
    # Determine what kind of stacked chart to make
    # Memory, Load, Bytes In/Out, CPU
    if "memory" in stack_type:
        #Do memory
        datapoint_list = [128, 129, 131, 133, 135]
        colors = ['#71D5C3', '#009DB2', '#21D5C3', '#98e1d4', '#f0e0a0']
    elif "cpu" in stack_type:
        #Do cpu
        pass
    elif "load" in stack_type:
        #Do load
        colors = ['#F37372','#FA9469','#FDBB5D']
        datapoint_list = [124,125,126]
        pass
    elif "network" in stack_type:
        #Do network
        colors = ['#F37372','#FA9469', '#FDBB5D']
        datapoint_list = [124,125,126]        
        pass
    elif "disk" in stack_type:
        #Do disk
        pass 


    values = []
    for datapoint in datapoint_list:
        get_idx = GetIDX(datapoint)
        data = get_idx.everything()
        values.append(data)
    
    if start and stop:
        chart = Chart(values,
                      image_width=12,
                      image_height=4,
                      text_color='#272727',
                      start=int(start),
                      stop=int(stop))
    else:
        chart = Chart(values,
                      image_width=12,
                      image_height=4,
                      text_color='#272727')    

    # create specific chart
    single_datapoint = GetSingleDataPoint(datapoint)
    agent_label = single_datapoint.agent_label()
    color_palette = ColorWheel(agent_label)

    plt, fig, png_output = chart.create_stacked(
        'Stacked', 'test', colors, [], filepath)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    plt.clf()
    return response


@infoset.route('/fetch/agent/<ip>/table', methods=["GET"])
def fetch_table(ip):
    """Return Network Layout tables.

    Args:
        ip: Host IP

    Returns:
        HTML string of host table

    """    
    # Config Object
    config = infoset.config['GLOBAL_CONFIG']
    
    html = ws_device.api_make(config, ip, True)

    return html


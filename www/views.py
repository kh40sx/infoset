"""Module of infoset webserver routes.

Contains all routes that infoset's Flask webserver uses

"""
# Standard imports
from datetime import datetime
import time
import json
import operator
from os import path
from os import walk

# Pip imports
import yaml
from flask import render_template, jsonify, request

# Infoset imports
from infoset.utils import Config
from infoset.db.db_agent import GetUID
from infoset.db.db_data import GetIDX
from infoset.db.db_agent import GetDataPoint
from infoset.db.db_orm import Agent
from infoset.db import db_hostagent
from infoset.db.db_host import GetIDX as GetHostIDX
from infoset.db.db import Database
from infoset.charts import TimeStamp
from infoset.charts import ColorWheel
from infoset.utils import jm_general
from infoset.metadata import language
from infoset.db import db_datapoint
from infoset.db import db_agent
from infoset.db import db_host
from infoset.topology import pages
from www import infoset


@infoset.template_filter('strftime')
def _jinja2_filter_datetime(timestamp):
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
    idx_agent = agent.idx()
    host = _infoset_hostname()

    agent_list = [agent.everything()]
    datapoints = GetDataPoint(idx_agent)
    data_point_dict = datapoints.everything()

    # Render the home page
    return render_template('index.html',
                           data=data_point_dict,
                           agent_list=agent_list,
                           uid=uid,
                           hostname=host)
@infoset.route('/<uid>')
def overview(uid):
    """Function for showing UID related data for agent.

    Args:
        uid: UID of agent

    Returns:
        overview page

    """
    # Get agent information
    agent = GetUID(uid)
    host = _infoset_hostname()
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
    """Function for showing datapoint related data for agent.

    Args:
        uid: UID of agent

    Returns:
        overview page

    """
    # Get agent information
    agent = GetUID(uid)
    host = _infoset_hostname()
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
    """Function for showing list of hosts on search page.

    Args:
        None

    Returns:
        overview page

    """
    # Initialize key variables
    data = []

    # Get list of all host indices
    host_idx_list = db_hostagent.all_host_indices()

    for idx_host in host_idx_list:
        # Get names for host
        hostname = db_host.GetIDX(idx_host).hostname()

        # Create list of enabled agents
        all_agent_indices = db_hostagent.agent_indices(idx_host)
        enabled_agent_idx_list = []
        for idx_agent in all_agent_indices:
            enabled = db_agent.GetIDX(idx_agent).enabled()
            if enabled is True:
                enabled_agent_idx_list.append(idx_agent)

        # Append agent data to list
        for idx_agent in enabled_agent_idx_list:
            agent_name = db_agent.GetIDX(idx_agent).name()
            # Append to data
            data.append(
                (hostname, idx_host, agent_name, idx_agent)
            )

    # Render data on screen
    return render_template('search.html', agent_list=data)


@infoset.route('/search/<idx_host>/<idx_agent>')
def search_host(idx_host, idx_agent):
    """Function for showing all data for all DIDs.

    Args:
        idx_host: IDX of Host
        idx_agent: IDX of Agent

    Returns:
        overview page

    """
    # Initialize key variables
    data = []

    # Get Hostname
    hostname = db_host.GetIDX(idx_host).hostname()

    # Get agent details
    agent_name = db_agent.GetIDX(idx_agent).name()
    uid = db_agent.GetIDX(idx_agent).uid()

    # Get a description of the datapoint
    lang = language.Agent(agent_name)

    # Get datapoints charting host metrics
    metadata = db_datapoint.datapoint_host_agent(idx_host, idx_agent)
    for data_dict in metadata:
        # Create datapoint object
        idx_datapoint = data_dict['idx']
        timestamp = data_dict['last_timestamp']
        source = data_dict['agent_source']
        agent_label = data_dict['agent_label']

        final_description = ''

        # Get a description of the datapoint
        label_description = lang.label_description(agent_label)
        if bool(label_description) is True:
            final_description = label_description
        else:
            final_description = agent_label

        # Get datapoint source
        datex = datetime.fromtimestamp(
            timestamp).strftime('%H:%M %d-%b-%Y')

        # Append to data
        data.append(
            (hostname, agent_name, source,
             final_description, idx_datapoint, uid, datex)
        )

    # Sort list by label_description and source
    data = sorted(data, key=operator.itemgetter(3, 2))

    # Render data on screen
    return render_template(
        'search-host.html', idx_host=idx_host, agent_list=data)


@infoset.route('/tables/<idx_host>/<idx_agent>')
def tables(idx_host, idx_agent):
    """Function for creating host tables.

    Args:
        idx_host: Index of host
        idx_agent: Index of agent

    Returns:
        HTML

    """
    hostname = _infoset_hostname()
    hosts = _get_yaml_hosts()
    return render_template('network-topo.html',
                           hostname=hostname,
                           hosts=hosts)


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
        except Exception as error:
            raise error
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
        except Exception as error:
            raise error

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
        except Exception as error:
            raise error

    # Gets layer2 from loaded yaml
    layer2 = yaml_dump['layer2']

    return jsonify(layer2)


@infoset.route('/graphs/<idx_agent>/<idx_datapoint>', methods=["GET", "POST"])
def graphs(idx_agent, idx_datapoint):
    """Create graphs.

    Args:
        uid: Agent uid
        idx: Datapoint idx

    Returns:
        None

    """
    # Get agent details
    agent_name = db_agent.GetIDX(idx_agent).name()
    uid = db_agent.GetIDX(idx_agent).uid()

    # Get a description of the datapoint
    lang = language.Agent(agent_name)

    single_datapoint = db_datapoint.GetIDX(idx_datapoint)
    agent_label = single_datapoint.agent_label()

    agent_description = lang.label_description(agent_label)
    colorwheel = ColorWheel(agent_label)
    fill = colorwheel.get_scheme()
    preset = TimeStamp()
    timestamps = preset.get_times()
    return render_template('graphs.html',
                           timestamps=timestamps,
                           uid=uid,
                           datapoint=idx_datapoint,
                           fill=fill,
                           description=agent_description,
                           agent_source=agent_name)


@infoset.route('/receive/<uid>', methods=["POST"])
def receive(uid):
    """Function for handling /receive/<uid> route.

    Args:
        uid: Unique Identifier of an Infoset Agent

    Returns:
        Text response of Received

    """
    # Read configuration
    config = Config()
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

    # Return
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
    # Getting start and stop parameters from url
    start = request.args.get('start')
    stop = request.args.get('stop')

    # Get data as dict
    datapointer = GetIDX(datapoint, start=start, stop=stop)
    data = datapointer.chart_everything()

    # Return
    return jsonify(data)


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
    # Define key variables
    # We are only interested in the infoset server host idx for now.
    idx_host = 1
    labels = {}

    # Define label values
    labels['cpu'] = [
        'cpu_times_percent_iowait',
        'cpu_times_percent_irq',
        'cpu_times_percent_ctx_switches',
        'cpu_times_percent_syscalls',
        'cpu_times_percent_interrupts',
        'cpu_times_percent_soft_interrupts',
        'cpu_times_percent_softirq',
        'cpu_times_percent_steal',
        'cpu_times_percent_user',
        'cpu_times_percent_nice',
        'cpu_times_percent_system',
        'cpu_times_percent_idle',
        'cpu_times_percent_guest',
        'cpu_times_percent_guest_nice'
    ]
    labels['memory'] = [
        'memory_buffers',
        'memory_cached',
        'memory_shared',
        'memory_available',
        'memory_free'
    ]
    labels['load'] = [
        'load_average_01min',
        'load_average_05min',
        'load_average_15min'
    ]
    labels['network'] = [
        'network_bytes_recv',
        'network_bytes_sent'
    ]

    # Get Agent data
    idx_agent = db_agent.GetUID(uid).idx()

    # Determine what kind of stacked chart to make
    # Memory, Load, Bytes In/Out, CPU
    if 'memory' in stack_type:
        # Do memory
        datapoint_list = _datapoint_labels(
            idx_host, idx_agent, labels['memory'])
    elif 'cpu' in stack_type:
        # Do cpu
        datapoint_list = _datapoint_labels(
            idx_host, idx_agent, labels['cpu'])
    elif 'load' in stack_type:
        # Do load
        datapoint_list = _datapoint_labels(
            idx_host, idx_agent, labels['load'])
    elif 'network' in stack_type:
        # Do network
        datapoint_list = _datapoint_labels(
            idx_host, idx_agent, labels['network'])
    elif 'disk' in stack_type:
        # Do disk
        pass

    values = []
    for datapoint in datapoint_list:
        get_idx = GetIDX(datapoint)
        data = get_idx.chart_everything()
        values.extend(data)

    return jsonify(values)


@infoset.route('/fetch/agent/<ip_address>/table', methods=["GET"])
def fetch_table(ip_address):
    """Return Network Layout tables.

    Args:
        ip_address: Host IP

    Returns:
        HTML string of host table

    """
    # Config Object
    config = Config()
    html = pages.create(config, ip_address)

    return html


def _datapoint_labels(idx_host, idx_agent, labels):
    """Get datapoint IDXes for a host / agent with specific labels.

    Args:
        idx_host: Host index
        idx_agent: Agent index
        labels: Labels to match

    Returns:
        listing: List of datap

    """
    # Initialize key variables
    listing = []

    # Get datapoints the agent is tracking for the host
    metadata = db_datapoint.datapoint_host_agent(idx_host, idx_agent)
    for data_dict in metadata:
        agent_label = data_dict['agent_label']
        idx_datapoint = data_dict['idx']
        if agent_label in labels:
            listing.append(idx_datapoint)

    # Return
    return listing

def _infoset_hostname():
    """Get hostname for _infoset agent.

    Args:
        None

    Returns:
        host: Hostname

    """
    # host_indices = db_hostagent.host_indices(1)
    # host_idx = host_indices[0]
    host_object = GetHostIDX(1)
    host = host_object.hostname()
    return host

def _get_yaml_hosts():
    """Get hosts listed in toplogy YAML files.

    Args:
        None

    Returns:
        hosts: Dict of hostnames

    """
    # Read configuration
    config = Config()
    topology_directory = config.topology_directory()

    hosts = {}
    for root, _, files in walk(topology_directory):
        for filename in files:
            filepath = path.join(root, filename)
            hosts[filename[:-5]] = filepath  # Add it to the list.
    return hosts

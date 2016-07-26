from flask import render_template, jsonify, send_file, request
from www import infoset
from os import listdir, walk, path, makedirs, remove
from infoset.utils.rrd.rrd_xlate import RrdXlate
import yaml


@infoset.route('/')
def index():
    hosts = getHosts()
    return render_template('index.html',
                           hosts=hosts)
                    
@infoset.route('/search')
def search():
    return render_template('search.html', results=[])


@infoset.route('/search/<query>')
def searchq(query):
    info = getInfo() #This is a list of dictionaries
    hosts = getHosts()
    results = [] #results of search query

    #if query is a mac address since ips normally start with one
    if query[0] != '1':
        query = query.replace('.',"")
        query = query.replace(':',"")
        query = query.replace('-',"")

    for data in info:
        for ip, mac in data.items():
            if ip == query:
                #print("%s | %s | %s" %(data['host'],ip,mac))
                results.append(("Host: %s | IP Address: %s | MAC Address: %s"
                                +" | DNS: | Port Label: ")
                                %(data['host'],ip,mac))
            elif mac == query:
                #print("%s | %s | %s" %(data['host'],ip,mac))
                results.append(("Host: %s | IP Address: %s | MAC Address: %s"
                                +" | DNS: | Port Label: ")
                                %(data['host'],ip,mac))

    if results == []:
        results.append("No Results Found")

    return render_template('search.html', results=results)


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

@infoset.route('/devices/<uid>')
def device_details(uid):
    devices = getDevices()
    device_details = getDeviceDetails(uid)
    device_path = "./www/static/devices/linux/" + str(uid)
    rrd_root = RrdXlate(device_path)
    rrd_root.rrd_graph()
    return render_template('device.html',
                           uid=uid,
                           devices=devices,
                           details=device_details)

@infoset.route('/receive/<uid>', methods=["POST"])
def receive(uid):
    device_path = "./www/static/devices/linux/" + str(uid)
    content = request.json
    if not path.exists(device_path):
        makedirs(device_path)

    active_yaml_path = device_path + "/active.yaml"
    # Out with the old
    remove(active_yaml_path)
    # In with the new
    with open(active_yaml_path, "w+") as active_file:
        active_file.write(yaml.dump(content, default_flow_style=False))
        active_file.close()

    rrd_root = RrdXlate("./www/static/devices/linux/")

    rrd_root.rrd_update()
    return "Recieved"


def getHosts():
    hosts = {}
    for root, directories, files in walk('./www/static/yaml'):
        for filename in files:
            filepath = path.join(root, filename)
            hosts[filename[:-5]] = filepath  # Add it to the list.
    return hosts

def getDeviceDetails(uid):
    active_yaml = {}
    filepath="./www/static/devices/linux/" + str(uid) + "/active.yaml"
    with open(filepath, 'r') as stream:
        try:
            active_yaml = yaml.load(stream)
        except Exception as e:
            raise e
    return active_yaml

def getDevices():
    active_yamls = {}
    devices = []
    root="./www/static/devices/linux/"
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
    
def getLayer(host, layer):
    filename = host + ".yaml"
    filepath = path.join("./www/static/yaml/", filename)
    yaml_dump = {}
    with open(filepath, 'r') as stream:
        try:
            yaml_dump = yaml.load(stream)
        except Exception as e:
            raise e
    layer = yaml_dump['layer'+str(layer)]
    return layer

def getInfo():
    hosts = getHosts()
    info = []
    for host in hosts.keys():
        for val in getLayer(host, 3).values():
            val['host'] = host
            info.append(val)
    return info

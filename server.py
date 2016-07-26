#! /usr/bin/env python3
from www import infoset
from infoset.utils import Daemon
infoset.run(debug=True, host='0.0.0.0', threaded=True)

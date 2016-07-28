#! /usr/bin/env python3
from www import infoset
import os
import argparse
import sys
import time
from infoset.utils import jm_configuration
from infoset.utils import Daemon
from infoset.utils import hidden
from infoset.utils import log


infoset.run(debug=True, host='0.0.0.0', threaded=True, port=5000)

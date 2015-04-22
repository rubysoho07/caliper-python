# -*- coding: utf-8 -*-
# Caliper-python package
#
# This file is part of the IMS Caliper Analytics(tm) and is licensed to IMS
# Global Learning Consortium, Inc. (http://www.imsglobal.org) under one or more
# contributor license agreements.
#
# IMS Caliper is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, version 3 of the License.
#
# IMS Caliper is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#

"""
Caliper library
~~~~~~~~~~~~~~~

Caliper is a library, written in python, to help you implement an IMS
Caliper-compliant sensor or endpoint for you learning services.

:license: GPLv3 or LPGLv3. See LICENSE for more details.
"""
from __future__ import absolute_import

__title__ = 'caliper_python'
__version__ = '0.9.0'
__build__ = 0x000900
__author__ = 'IMS Global Learning Consortium, Inc.'
__license__ = 'LGPLv3'

from caliper.sensor import Sensor as Sensor
import caliper.base as base


def build_default_sensor():
    return Sensor.fashion_default_sensor_with_config(config_options=base.HttpOptions())

def build_sensor_from_config(config_options):
    return Sensor.fashion_default_sensor_with_config(config_options=config_options)

def build_sensor_for_client(client):
    return Sensor.fashion_default_sensor_with_client(client=client)

## set default logging handler to avoid "No handler found" warnings.
## Thanks to Kenneth Reitz' requests library for this pattern

import logging
try: # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


logger = logging.getLogger(__name__).addHandler(NullHandler())



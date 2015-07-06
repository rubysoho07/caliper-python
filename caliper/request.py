# -*- coding: utf-8 -*-
# Caliper-python package, request module
#
# This file is part of the IMS Caliper Analytics(tm) and is licensed to IMS
# Global Learning Consortium, Inc. (http://www.imsglobal.org) under one or more
# contributor license agreements. See the NOTICE file distributed with this
# work for additional information.
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
from __future__ import (absolute_import, division, print_function, unicode_literals)
from future.standard_library import install_aliases
install_aliases()
from builtins import *

import collections
import datetime
import json
import requests
import uuid

from caliper.base import CaliperSerializable, HttpOptions

class Envelope(CaliperSerializable):

    def __init__(self,
            data = None,
            send_time = None,
            sensor_id = None,
            **kwargs):
        CaliperSerializable.__init__(self)
        self._set_list_prop('data',data,t=CaliperSerializable)
        self._set_str_prop('sendTime', send_time)
        self._set_str_prop('sensor', sensor_id)

    @property
    def data(self):
        return self._get_prop('data')
    @data.setter
    def data(self, new_data):
        self._set_list_prop('data',data,t=CaliperSerializable)        

    @property
    def sendTime(self):
        return self._get_prop('sendTime')
    @sendTime.setter
    def sendTime(self, v):
        self._set_str_prop('sendTime', v)

    @property
    def sensor(self):
        return self._get_prop('sensor')


class EventStoreRequestor(object):

    def send(self, caliper_object=None, sensor_id=None):
        raise NotImplementedError('Instance must implement EventStoreRequester.send()')

    def send_batch(self, caliper_object_list=None, sensor_id=None):
        raise NotImplementedError('Instance must implement EventStoreRequester.send_batch()')

    def _get_time(self):
        return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'        

    def _generate_payload(self,
            caliper_object_list = None,
            send_time = None,
            sensor_id = None):
        st = send_time if send_time else self._get_time()
        payload = self._get_payload_json(caliper_object_list, st, sensor_id)
        return {'type':'application/json',
                'data': payload}

    def _get_payload_json(self,
            caliper_object_list = None,
            send_time = None,
            sensor_id = None):
        envelope = Envelope(
            data = caliper_object_list,
            send_time = send_time,
            sensor_id = sensor_id)
                
        return envelope.as_json()

class HttpRequestor(EventStoreRequestor):

    def __init__(self,
            options = None,
            **kwargs):
        if not options:
            self._options = HttpOptions()
        elif not( isinstance(options, HttpOptions)):
            raise TypeError('options must implement base.HttpOptions')
        else:
            self._options = options

    def send(self, caliper_object=None, sensor_id=None):
        return self.send_batch(caliper_object_list=[caliper_object],sensor_id=sensor_id)[0]

    def send_batch(self, caliper_object_list=None, sensor_id=None):
        results = []

        if isinstance(caliper_object_list, collections.MutableSequence):
            s = requests.Session()
            payload = self._generate_payload(caliper_object_list=caliper_object_list,sensor_id=sensor_id)
            r = s.post(self._options.HOST,
                       data=payload['data'],
                       headers={'Content-Type':payload['type']} )
            if (r.status_code is requests.codes.ok):
                v = True
            else:
                v = False
            results += len(caliper_object_list) * [v]
            s.close()

        return results

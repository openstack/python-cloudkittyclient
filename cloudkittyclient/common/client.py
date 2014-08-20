# -*- coding: utf-8 -*-
# Copyright 2014 Objectif Libre
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# @author: François Magimel (linkid)

"""
OpenStack Client interface. Handles the REST calls and responses.
Override the oslo-incubator one.
"""

import logging
import time

from cloudkittyclient.common import exceptions
from cloudkittyclient.openstack.common.apiclient import client


_logger = logging.getLogger(__name__)


class HTTPClient(client.HTTPClient):
    """This client handles sending HTTP requests to OpenStack servers.
    [Overrider]
    """
    def request(self, method, url, **kwargs):
        """Send an http request with the specified characteristics.

        Wrapper around `requests.Session.request` to handle tasks such as
        setting headers, JSON encoding/decoding, and error handling.

        :param method: method of HTTP request
        :param url: URL of HTTP request
        :param kwargs: any other parameter that can be passed to
             requests.Session.request (such as `headers`) or `json`
             that will be encoded as JSON and used as `data` argument
        """
        kwargs.setdefault("headers", kwargs.get("headers", {}))
        kwargs["headers"]["User-Agent"] = self.user_agent
        if self.original_ip:
            kwargs["headers"]["Forwarded"] = "for=%s;by=%s" % (
                self.original_ip, self.user_agent)
        if self.timeout is not None:
            kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("verify", self.verify)
        if self.cert is not None:
            kwargs.setdefault("cert", self.cert)
        self.serialize(kwargs)

        self._http_log_req(method, url, kwargs)
        if self.timings:
            start_time = time.time()
        resp = self.http.request(method, url, **kwargs)
        if self.timings:
            self.times.append(("%s %s" % (method, url),
                               start_time, time.time()))
        self._http_log_resp(resp)

        if resp.status_code >= 400:
            _logger.debug(
                "Request returned failure status: %s",
                resp.status_code)
            raise exceptions.from_response(resp, method, url)

        return resp

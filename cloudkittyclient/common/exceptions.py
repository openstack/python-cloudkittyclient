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
Exception definitions.
See cloudkittyclient.openstack.common.apiclient.exceptions.
"""

from cloudkittyclient.openstack.common.apiclient.exceptions import *


# _code_map contains all the classes that have http_status attribute.
_code_map = dict(
    (getattr(obj, 'http_status', None), obj)
    for name, obj in six.iteritems(vars(sys.modules[__name__]))
    if inspect.isclass(obj) and getattr(obj, 'http_status', False)
)


def from_response(response, method, url):
    """Returns an instance of :class:`HttpError` or subclass based on response.

    :param response: instance of `requests.Response` class
    :param method: HTTP method used for request
    :param url: URL used for request
    """

    req_id = response.headers.get("x-openstack-request-id")
    # NOTE(hdd) true for older versions of nova and cinder
    if not req_id:
        req_id = response.headers.get("x-compute-request-id")
    kwargs = {
        "http_status": response.status_code,
        "response": response,
        "method": method,
        "url": url,
        "request_id": req_id,
    }
    if "retry-after" in response.headers:
        kwargs["retry_after"] = response.headers["retry-after"]

    content_type = response.headers.get("Content-Type", "")
    if content_type.startswith("application/json"):
        try:
            body = response.json()
        except ValueError:
            pass
        else:
            if isinstance(body, dict):
                if isinstance(body.get("error"), dict):
                    error = body["error"]
                    kwargs["message"] = error.get("message")
                    kwargs["details"] = error.get("details")
                elif "faultstring" in body and "faultcode" in body:
                    # WSME
                    kwargs["message"] = "%(faultcode)s: %(faultstring)s" % body
                    kwargs["details"] = body.get("debuginfo", "")
    elif content_type.startswith("text/"):
        kwargs["details"] = response.text

    try:
        cls = _code_map[response.status_code]
    except KeyError:
        if 500 <= response.status_code < 600:
            cls = HttpServerError
        elif 400 <= response.status_code < 500:
            cls = HTTPClientError
        else:
            cls = HttpError
    return cls(**kwargs)

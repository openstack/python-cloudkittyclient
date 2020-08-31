# -*- coding: utf-8 -*-
# Copyright 2018 Objectif Libre
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from string import Formatter as StringFormatter
from urllib.parse import urlencode

from cloudkittyclient import utils


class HttpDecoratorMeta(type):

    ignore = ('get_url', )

    def __new__(cls, *args, **kwargs):
        return utils.format_http_errors(HttpDecoratorMeta.ignore)(
            super(HttpDecoratorMeta, cls).__new__(cls, *args, **kwargs)
        )


class BaseManager(object, metaclass=HttpDecoratorMeta):
    """Base class for Endpoint Manager objects."""

    url = ''

    def __init__(self, api_client):
        self.api_client = api_client
        self._formatter = StringFormatter()

    def _get_format_kwargs(self, **kwargs):
        it = self._formatter.parse(self.url)
        output = {i[1]: '' for i in it}
        for key in output.keys():
            if kwargs.get(key):
                output[key] = kwargs[key]
        if 'endpoint' in output.keys():
            output.pop('endpoint')
        return output

    def get_url(self,
                endpoint,
                kwargs,
                authorized_args=[]):
        """Returns the required url for a request against CloudKitty's API.

        :param endpoint: The endpoint on which the request should be done
        :type endpoint: str
        :param kwargs: kwargs that will be used to build the query (part after
                       '?' in the url) and to format the url.
        :type kwargs: dict
        :param authorized_args: The arguments that are authorized in url
                                parameters
        :type authorized_args: list
        """
        query_kwargs = {
            key: kwargs[key] for key in authorized_args
            if kwargs.get(key, None)
        }
        kwargs = self._get_format_kwargs(**kwargs)
        url = self.url.format(endpoint=endpoint, **kwargs)
        query = urlencode(query_kwargs)
        if query:
            url += '?' + query
        return url

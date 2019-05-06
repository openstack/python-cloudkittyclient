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
#
from oslo_log import log

from cloudkittyclient.common import base
from cloudkittyclient import exc


LOG = log.getLogger(__name__)


class CollectorManager(base.BaseManager):
    """Class used to handle /v1/collector/mappings endpoint"""
    url = '/v1/collector/{endpoint}/{service_id}'

    def get_mapping(self, **kwargs):
        """Returns a service to collector mapping.

        If the service is not specified, returns a list of mappings for the
        given collector.

        :param service: Name of the service to filter on.
        :type service: str
        :param collector: Name of the collector to filter on.
        :type collector: str
        """
        LOG.warning('WARNING: Collector mappings are deprecated and will '
                    'be removed in a future release')
        kwargs['service_id'] = kwargs.get('service') or ''
        authorized_args = ['collector']
        url = self.get_url('mappings', kwargs, authorized_args)
        return self.api_client.get(url).json()

    def create_mapping(self, **kwargs):
        """Creates a service to collector mapping.

        :param service: Name of the service to filter on.
        :type service: str
        :param collector: Name of the collector to filter on.
        :type collector: str
        """
        LOG.warning('WARNING: Collector mappings are deprecated and will '
                    'be removed in a future release')
        for arg in ('collector', 'service'):
            if not kwargs.get(arg):
                raise exc.ArgumentRequired(
                    "'{arg}' argument is required.".format(arg=arg))
        url = self.get_url('mappings', kwargs)
        body = dict(
            collector=kwargs['collector'],
            service=kwargs['service'])
        return self.api_client.post(url, json=body).json()

    def delete_mapping(self, **kwargs):
        """Deletes a service to collector mapping.

        :param service: Name of the service of which the mapping
                        should be deleted.
        :type service: str
        """
        LOG.warning('WARNING: Collector mappings are deprecated and will '
                    'be removed in a future release')
        if not kwargs.get('service'):
            raise exc.ArgumentRequired("'service' argument is required.")
        body = dict(service=kwargs['service'])
        url = self.get_url('mappings', kwargs)
        self.api_client.delete(url, json=body)

    def get_state(self, **kwargs):
        """Returns the state of a collector.

        :param name: Name of the collector.
        :type name: str
        """
        LOG.warning('WARNING: Collector mappings are deprecated and will '
                    'be removed in a future release')
        if not kwargs.get('name'):
            raise exc.ArgumentRequired("'name' argument is required.")
        authorized_args = ['name']
        url = self.get_url('states', kwargs, authorized_args)
        return self.api_client.get(url).json()

    def set_state(self, **kwargs):
        """Sets the state of the collector.

        :param name: Name of the collector
        :type name: str
        :param enabled: State of the collector
        :type name: bool
        """
        LOG.warning('WARNING: Collector mappings are deprecated and will '
                    'be removed in a future release')
        if not kwargs.get('name'):
            raise exc.ArgumentRequired("'name' argument is required.")
        kwargs['enabled'] = kwargs.get('enabled') or False
        url = self.get_url('states', kwargs)
        body = dict(
            name=kwargs['name'],
            enabled=kwargs['enabled'],
        )
        self.api_client.put(url, json=body)
        return self.get_state(**kwargs)

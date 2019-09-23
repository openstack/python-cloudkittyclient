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
from keystoneauth1 import adapter
from keystoneauth1 import session as ks_session


class BaseClient(object):

    def __init__(self,
                 session=None,
                 adapter_options={},
                 cacert=None,
                 insecure=False,
                 **kwargs):
        adapter_options.setdefault('service_type', 'rating')
        adapter_options.setdefault('additional_headers', {
            'Content-Type': 'application/json',
        })

        if insecure:
            verify_cert = False
        else:
            if cacert:
                verify_cert = cacert
            else:
                verify_cert = True

        self.session = session
        if self.session is None:
            self.session = ks_session.Session(
                verify=verify_cert, **kwargs)

        self.api_client = adapter.Adapter(
            session=self.session, **adapter_options)

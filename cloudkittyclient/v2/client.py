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
from cloudkittyclient.v1 import client
from cloudkittyclient.v2 import dataframes
from cloudkittyclient.v2.rating import modules
from cloudkittyclient.v2 import reprocessing
from cloudkittyclient.v2 import scope
from cloudkittyclient.v2 import summary


# NOTE(peschk_l) v2 client needs to implement v1 until the v1 API has been
# completely ported to v2
class Client(client.Client):

    def __init__(self,
                 session=None,
                 adapter_options={},
                 cacert=None,
                 insecure=False,
                 **kwargs):
        super(Client, self).__init__(
            session=session,
            adapter_options=adapter_options,
            cacert=cacert,
            insecure=insecure,
            **kwargs
        )

        self.dataframes = dataframes.DataframesManager(self.api_client)
        self.scope = scope.ScopeManager(self.api_client)
        self.summary = summary.SummaryManager(self.api_client)
        self.rating = modules.RatingManager(self.api_client)
        self.reprocessing = reprocessing.ReprocessingManager(self.api_client)

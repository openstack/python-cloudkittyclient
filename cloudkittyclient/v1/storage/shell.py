# Copyright 2015 Objectif Libre
#
# All Rights Reserved.
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

from cloudkittyclient.common import utils


@utils.arg('-b', '--begin',
           help='Starting date/time (YYYY-MM-DDTHH:MM:SS)',
           required=False)
@utils.arg('-e', '--end',
           help='Ending date/time (YYYY-MM-DDTHH:MM:SS)',
           required=False)
@utils.arg('-t', '--tenant',
           help='Tenant ID',
           required=False,
           default=None)
@utils.arg('-r', '--resource-type',
           help='Resource type (compute, image, ...)',
           required=False,
           default=None)
def do_storage_dataframe_list(cc, args):
    """List dataframes."""
    data = cc.storage.dataframes.list(begin=args.begin, end=args.end,
                                      tenant_id=args.tenant,
                                      resource_type=args.resource_type)
    fields = ['begin', 'end', 'tenant_id', 'resources']
    fields_labels = ['Begin', 'End', 'Tenant ID', 'Resources']
    utils.print_list(data, fields, fields_labels, sortby=0)

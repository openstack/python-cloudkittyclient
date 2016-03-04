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
from __future__ import print_function

from cloudkittyclient.common import utils


def do_report_tenant_list(cc, args):
    """List tenant report."""
    tenants = cc.reports.list_tenants()
    out_table = utils.prettytable.PrettyTable()
    out_table.add_column("Tenant UUID", tenants)
    print(out_table)


@utils.arg('-t', '--tenant-id',
           help='Tenant id',
           required=False,
           dest='total_tenant_id')
@utils.arg('-b', '--begin',
           help='Begin timestamp',
           required=False)
@utils.arg('-e', '--end',
           help='End timestamp',
           required=False)
@utils.arg('-s', '--service',
           help='Service Type',
           required=False)
def do_total_get(cc, args):
    """Get total reports."""
    begin = utils.ts2dt(args.begin) if args.begin else None
    end = utils.ts2dt(args.end) if args.end else None
    total = cc.reports.get_total(tenant_id=args.total_tenant_id,
                                 begin=begin,
                                 end=end,
                                 service=args.service)
    utils.print_dict({'Total': total or 0.0})

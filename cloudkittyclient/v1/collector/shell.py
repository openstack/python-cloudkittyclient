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


@utils.arg('-c', '--collector',
           help='Collector name to filter on.',
           required=False,
           default=None)
def do_collector_mapping_list(cc, args):
    """List collector mapping."""
    data = cc.collector.mappings.list(collector=args.collector)
    fields = ['service', 'collector']
    fields_labels = ['Service', 'Collector']
    utils.print_list(data, fields, fields_labels, sortby=0)


@utils.arg('-s', '--service',
           help='Which service to get the mapping for.',
           required=True)
def do_collector_mapping_get(cc, args):
    """Show collector mapping detail."""
    data = cc.collector.mappings.get(mapping_id=args.service)
    utils.print_dict(data.to_dict())


@utils.arg('-c', '--collector',
           help='Map a service to this collector.',
           required=True)
@utils.arg('-s', '--service',
           help='Map a collector to this service.',
           required=True)
def do_collector_mapping_create(cc, args):
    """Create collector mapping."""
    out = cc.collector.mappings.create(service=args.service,
                                       collector=args.collector)
    utils.print_dict(out.to_dict())


@utils.arg('-s', '--service',
           help='Filter on this service.',
           required=True)
def do_collector_mapping_delete(cc, args):
    """Delete collector mapping."""
    # TODO(sheeprine): Use a less hacky way to do this
    cc.collector.mappings.delete(mapping_id=args.service)


@utils.arg('-n', '--name',
           help='Name of the collector.',
           required=True)
def do_collector_state_get(cc, args):
    """Show collector state."""
    data = cc.collector.states.get(state_id=args.name)
    utils.print_dict(data.to_dict())


@utils.arg('-n', '--name',
           help='Name of the collector.',
           required=True)
def do_collector_state_enable(cc, args):
    """Enable collector state."""
    new_state = cc.collector.states.update(name=args.name, enabled=True)
    utils.print_dict(new_state.to_dict())


@utils.arg('-n', '--name',
           help='Name of the collector.',
           required=True)
def do_collector_state_disable(cc, args):
    """Disable collector state."""
    new_state = cc.collector.states.update(name=args.name, enabled=False)
    utils.print_dict(new_state.to_dict())

# Copyright 2015 Objectif Libre
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

from cloudkittyclient.apiclient import exceptions
from cloudkittyclient.common import utils
from cloudkittyclient import exc


def do_module_list(cc, args):
    '''List the samples for this meters.'''
    try:
        modules = cc.modules.list()
    except exceptions.NotFound:
        raise exc.CommandError('Modules not found')
    else:
        field_labels = ['Module', 'Enabled', 'Priority']
        fields = ['module_id', 'enabled', 'priority']
        utils.print_list(modules, fields, field_labels,
                         sortby=0)


@utils.arg('-n', '--name',
           help='Module name',
           required=True)
def do_module_enable(cc, args):
    '''Enable a module.'''
    try:
        module = cc.modules.get(module_id=args.name)
        module.enable()
    except exceptions.NotFound:
        raise exc.CommandError('Module not found: %s' % args.name)
    else:
        field_labels = ['Module', 'Enabled', 'Priority']
        fields = ['module_id', 'enabled', 'priority']
        modules = [cc.modules.get(module_id=args.name)]
        utils.print_list(modules, fields, field_labels,
                         sortby=0)


@utils.arg('-n', '--name',
           help='Module name',
           required=True)
def do_module_disable(cc, args):
    '''Disable a module.'''
    try:
        module = cc.modules.get(module_id=args.name)
        module.disable()
    except exceptions.NotFound:
        raise exc.CommandError('Module not found: %s' % args.name)
    else:
        field_labels = ['Module', 'Enabled', 'Priority']
        fields = ['module_id', 'enabled', 'priority']
        modules = [cc.modules.get(module_id=args.name)]
        utils.print_list(modules, fields, field_labels,
                         sortby=0)


@utils.arg('-n', '--name',
           help='Module name',
           required=True)
@utils.arg('-p', '--priority',
           help='Module priority',
           required=True)
def do_module_set_priority(cc, args):
    '''Set module priority.'''
    try:
        module = cc.modules.get(module_id=args.name)
        module.set_priority(args.priority)
    except exceptions.NotFound:
        raise exc.CommandError('Module not found: %s' % args.name)
    else:
        field_labels = ['Module', 'Enabled', 'Priority']
        fields = ['module_id', 'enabled', 'priority']
        modules = [cc.modules.get(module_id=args.name)]
        utils.print_list(modules, fields, field_labels,
                         sortby=0)


def do_info_config_get(cc, args):
    '''Get cloudkitty configuration.'''
    utils.print_dict(cc.config.get_config(), dict_property="Section")


@utils.arg('-n', '--name',
           help='Service name',
           required=False)
def do_info_service_get(cc, args):
    '''Get service info.'''
    if args.name:
        try:
            services_info = [cc.service_info.get(service_id=args.name)]
        except exceptions.NotFound:
            raise exc.CommandError('Service not found: %s' % args.name)
    else:
        try:
            services_info = cc.service_info.list()
        except exceptions.NotFound:
            raise exc.CommandError('ServiceInfo not found')

    field_labels = ['Service', 'Metadata', 'Unit']
    fields = ['service_id', 'metadata', 'unit']
    utils.print_list(services_info, fields, field_labels, sortby=0)

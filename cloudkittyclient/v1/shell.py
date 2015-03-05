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

from cloudkittyclient.common import utils
from cloudkittyclient import exc


def do_module_list(cc, args):
    '''List the samples for this meters.'''
    try:
        modules = cc.modules.list()
    except exc.HTTPNotFound:
        raise exc.CommandError('Modules not found: %s' % args.counter_name)
    else:
        field_labels = ['Module', 'Enabled']
        fields = ['module_id', 'enabled']
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
    except exc.HTTPNotFound:
        raise exc.CommandError('Modules not found: %s' % args.counter_name)
    else:
        field_labels = ['Module', 'Enabled']
        fields = ['module_id', 'enabled']
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
    except exc.HTTPNotFound:
        raise exc.CommandError('Modules not found: %s' % args.counter_name)
    else:
        field_labels = ['Module', 'Enabled']
        fields = ['module_id', 'enabled']
        modules = [cc.modules.get(module_id=args.name)]
        utils.print_list(modules, fields, field_labels,
                         sortby=0)

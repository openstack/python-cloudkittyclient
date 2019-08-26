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
import json
import os
import shlex
import subprocess

from cloudkittyclient.tests import utils


class BaseFunctionalTest(utils.BaseTestCase):

    def _run(self, executable, action,
             flags='', params='', fmt='-f json', stdin=None, has_output=True):
        if not has_output:
            fmt = ''
        cmd = ' '.join([executable, flags, action, params, fmt])
        cmd = shlex.split(cmd)
        p = subprocess.Popen(
            cmd, env=os.environ.copy(), shell=False,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            stdin=subprocess.PIPE if stdin else None,
        )
        stdout, stderr = p.communicate(input=stdin)
        if p.returncode != 0:
            raise RuntimeError('"{cmd}" returned {val}: {msg}'.format(
                cmd=' '.join(cmd), val=p.returncode, msg=stderr))
        return json.loads(stdout) if has_output else None

    def openstack(self, action,
                  flags='', params='', fmt='-f json',
                  stdin=None, has_output=True):
        return self._run('openstack rating', action,
                         flags, params, fmt, stdin, has_output)

    def cloudkitty(self, action,
                   flags='', params='', fmt='-f json',
                   stdin=None, has_output=True):
        return self._run('cloudkitty', action, flags, params, fmt,
                         stdin, has_output)

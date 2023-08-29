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
import subprocess

from cloudkittyclient.tests import utils

from oslo_log import log

LOG = log.getLogger(__name__)


class BaseFunctionalTest(utils.BaseTestCase):

    # DevStack is using VENV by default. Therefore, to execute the commands,
    # we need to activate the VENV. And, to do that, we need the VENV path.
    # This path is hardcoded here because we could not find a variable in this
    # Python code to retrieve the VENV variable from the test machine.
    # It seems that because of the stack TOX -> stestr -> this python code, and
    # so on, we are not able to access the DevStack variables here.
    #
    # If somebody finds a solution, we can remove the hardcoded path here.
    DEV_STACK_VENV_BASE_PATH = "/opt/stack/data/venv"

    BASE_COMMAND_WITH_VENV = "source %s/bin/activate && %s "

    def _run(self, executable, action,
             flags='', params='', fmt='-f json', stdin=None, has_output=True):
        if not has_output:
            fmt = ''

        does_venv_exist = not os.system("ls -lah /opt/stack/data/venv")
        LOG.info("Test to check if the VENV file exist returned: [%s].",
                 does_venv_exist)

        system_variables = os.environ.copy()
        LOG.info("System variables [%s] found when executing the tests.",
                 system_variables)

        cmd = ' '.join([executable, flags, action, params, fmt])

        actual_command_with_venv = self.BASE_COMMAND_WITH_VENV % (
            self.DEV_STACK_VENV_BASE_PATH, cmd)

        LOG.info("Command being executed: [%s].", actual_command_with_venv)

        p = subprocess.Popen(
            ["bash", "-c", actual_command_with_venv],
            env=os.environ.copy(), shell=False, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, stdin=subprocess.PIPE if stdin else None
        )
        stdout, stderr = p.communicate(input=stdin)
        LOG.info("Standard output [%s] and error output [%s] for command "
                 "[%s]. ", stdout, stderr, actual_command_with_venv)
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

# Copyright 2019 Objectif Libre
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
import os
import uuid

from cloudkittyclient.tests.functional import base


class CkDataframesTest(base.BaseFunctionalTest):
    dataframes_data = """
    {
        "dataframes": [
            {
                "period": {
                    "begin": "20190723T122810Z",
                    "end": "20190723T132810Z"
                },
                "usage": {
                    "metric_one": [
                        {
                            "vol": {
                                "unit": "GiB",
                                "qty": 1.2
                            },
                            "rating": {
                                "price": 0.04
                            },
                            "groupby": {
                                "group_one": "one",
                                "group_two": "two"
                            },
                            "metadata": {
                                "attr_one": "one",
                                "attr_two": "two"
                            }
                        }
                    ],
                    "metric_two": [
                        {
                            "vol": {
                                "unit": "MB",
                                "qty": 200.4
                            },
                            "rating": {
                                "price": 0.06
                            },
                            "groupby": {
                                "group_one": "one",
                                "group_two": "two"
                            },
                            "metadata": {
                                "attr_one": "one",
                                "attr_two": "two"
                            }
                        }
                    ]
                }
            },
            {
                "period": {
                    "begin": "20190823T122810Z",
                    "end": "20190823T132810Z"
                },
                "usage": {
                    "metric_one": [
                        {
                            "vol": {
                                "unit": "GiB",
                                "qty": 2.4
                            },
                            "rating": {
                                "price": 0.08
                            },
                            "groupby": {
                                "group_one": "one",
                                "group_two": "two"
                            },
                            "metadata": {
                                "attr_one": "one",
                                "attr_two": "two"
                            }
                        }
                    ],
                    "metric_two": [
                        {
                            "vol": {
                                "unit": "MB",
                                "qty": 400.8
                            },
                            "rating": {
                                "price": 0.12
                            },
                            "groupby": {
                                "group_one": "one",
                                "group_two": "two"
                            },
                            "metadata": {
                                "attr_one": "one",
                                "attr_two": "two"
                            }
                        }
                    ]
                }
            }
        ]
    }
    """

    def __init__(self, *args, **kwargs):
        super(CkDataframesTest, self).__init__(*args, **kwargs)
        self.runner = self.cloudkitty

    def setUp(self):
        super(CkDataframesTest, self).setUp()

        self.fixture_file_name = '{}.json'.format(uuid.uuid4())
        with open(self.fixture_file_name, 'w') as f:
            f.write(self.dataframes_data)

    def tearDown(self):
        files = os.listdir('.')
        if self.fixture_file_name in files:
            os.remove(self.fixture_file_name)

        super(CkDataframesTest, self).tearDown()

    def test_dataframes_add_with_no_args(self):
        self.assertRaisesRegex(
            RuntimeError,
            'error: the following arguments are required: datafile',
            self.runner,
            'dataframes add',
            fmt='',
            has_output=False,
        )

    def test_dataframes_add(self):
        self.runner(
            'dataframes add {}'.format(self.fixture_file_name),
            fmt='',
            has_output=False,
        )

    def test_dataframes_add_with_hyphen_stdin(self):
        with open(self.fixture_file_name, 'r') as f:
            self.runner(
                'dataframes add -',
                fmt='',
                stdin=f.read().encode(),
                has_output=False,
            )

    def test_dataframes_get(self):
        # TODO(jferrieu): functional tests will be added in another
        # patch for `dataframes get`
        pass


class OSCDataframesTest(CkDataframesTest):
    def __init__(self, *args, **kwargs):
        super(OSCDataframesTest, self).__init__(*args, **kwargs)
        self.runner = self.openstack

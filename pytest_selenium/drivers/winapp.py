# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import os


def pytest_addoption(parser):
    group = parser.getgroup('selenium', 'selenium')
    group._addoption('--host',
                     default=os.environ.get('APPIUM_HOST', 'localhost'),
                     metavar='str',
                     help='host that the WinAppDriver server is listening on. '
                          '(default: %default)')
    group._addoption('--port',
                     type='int',
                     default=os.environ.get('APPIUM_PORT', 4723),
                     metavar='num',
                     help='port that the WinAppDriver server is listening on. '
                          '(default: %default)')


def driver_kwargs(request, test, capabilities, **kwargs):
    capabilities.setdefault('app', request.config._capabilities['app'])
    kwargs = {
        'command_executor': 'http://{0}:{1}'.format(request.config.getoption('host'),
                                                    request.config.getoption('port')
                                                    ),
        'desired_capabilities': capabilities}
    return kwargs

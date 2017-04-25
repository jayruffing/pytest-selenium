# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import pytest


def pytest_addoption(parser):
    group = parser.getgroup('selenium', 'selenium')
    group._addoption('--host',
                     default=os.environ.get('APPIUM_HOST', 'localhost'),
                     metavar='str',
                     help='host that the Appium server is listening on. '
                          '(default: %default)')
    group._addoption('--port',
                     type='int',
                     default=os.environ.get('APPIUM_PORT', 4723),
                     metavar='num',
                     help='port that the Appium server is listening on. '
                          '(default: %default)')


def driver_kwargs(request, test, capabilities, **kwargs):
    capabilities.setdefault('app', request.config._capabilities['app'])

    if request.config._capabilities['browserName'] is None and request.config._capabilities['app'] is None:
        raise pytest.UsageError('either --browserName or --app capability must be specified.')

    if request.config.getoption('browserName') and request.config._capabilities['app']:
        raise pytest.UsageError('--browserName and --app capabilities cannot both be specified.')

    capabilities = {
        'platformName': request.config._capabilities['platformName'],
        'platformVersion': request.config._capabilities['platformVersion'],
        'deviceName': request.config._capabilities['deviceName'],
    }

    capabilities.setdefault('platformName', 'iOS')  # default to iOS platform
    capabilities.setdefault('platformVersion', '10.3')  # default to iOS 10.3 version
    capabilities.setdefault('deviceName', 'iPhone 7')  # default to iPhone

    kwargs = {
        'command_executor': 'http://{0}:{1}'.format(request.config.getoption('host'),
                                                    request.config.getoption('port')
                                                    ),
        'desired_capabilities': capabilities}
    return kwargs

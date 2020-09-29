#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import re
import sys
import time
from subprocess import CalledProcessError

from workflow import ICON_INFO, Workflow3
from workflow.notify import notify
from workflow.util import run_command, set_config

GITHUB_SLUG = 'bmunoz89/alfred-wf-bluetooth-manager'
UPDATE_FREQUENCY = 7  # days

# TODO: it would be great to improve this regex
DEVICE_REGEX = re.compile(
    r'^address: ([a-z0-9\-\:]*), '  # address
    r'(.*(\(.*\))?), '  # connected
    r'(.*), '  # favorite
    r'(.*), '  # paired
    r'name: "(.*)", '  # name
    r'recent access date: (.*)'  # last access
    r'$',
    flags=re.M | re.I)

log = None


class BluetoothManager:

    __BREW_COMMAND_PATH = '/usr/local/bin/brew'
    __BLUETOOTH_COMMAND_PATH = '/usr/local/bin/blueutil'

    def __init__(self, wf):
        self._wf = wf
        log.debug('Args: %s' % wf.args)
        self._args = wf.args
        if len(self._args) < 1:
            raise Exception('At least the action must be passed')
        self._action = self._args[0]
        self._action_args = self._args[1:]

        self._set_bluetooth_command_path()

        self.main()

    def _set_bluetooth_command_path(self):
        if os.path.exists(self.__BLUETOOTH_COMMAND_PATH):
            log.debug('blueutil command path exists')
            return

        bluetooth_command_path = self._wf.stored_data('bluetooth_command_path')
        if bluetooth_command_path is not None:
            log.debug(
                'blueutil command path stored in "%s" was restored from stored data' %
                bluetooth_command_path)
            self.__BLUETOOTH_COMMAND_PATH = bluetooth_command_path
            return

        if not os.path.exists(self.__BREW_COMMAND_PATH):
            log.error('brew command path not found')
            return

        bluetooth_command_path = self._run_command([
            self.__BREW_COMMAND_PATH,
            '--prefix',
        ])

        if bluetooth_command_path is None:
            log.error('blueutil command path not found')
            return

        bluetooth_command_path += os.path.join(bluetooth_command_path, '/bin/blueutil')
        if os.path.exists(bluetooth_command_path):
            log.debug('blueutil command path stored in "%s"' % bluetooth_command_path)
            self._wf.store_data('bluetooth_command_path', bluetooth_command_path)
            self.__BLUETOOTH_COMMAND_PATH = bluetooth_command_path

    def _run_command(self, command):
        log.debug('Command: "%s"' % ' '.join(command))
        output = self._wf.decode(run_command(command)).strip()
        log.debug('Command result: "%s"' % output)
        return output

    def _is_on(self):
        output = self._run_command([
            self.__BLUETOOTH_COMMAND_PATH,
            '--power',
        ])
        return output == '1'

    def main(self):
        action_method = getattr(self, 'action_%s' % self._action, None)
        if action_method is None:
            raise Exception('Action does not exists: "%s"' % self._action)

        is_on = self._is_on()

        if self._action == 'manager':
            action_method(is_on, *self._action_args)
        elif not is_on:
            log.info('Bluetooth is not activated')
            self._wf.add_item(
                title='Bluetooth is not activated',
                icon=ICON_INFO,
                valid=False)
            notify('Bluetooth is not activated')
            self._wf.send_feedback()
        else:
            action_method(*self._action_args)

        return 0

    def action_manager(self, is_on, selected_option=None):
        if selected_option is None:
            if is_on:
                self._wf.add_item(
                    title='Turn off Bluetooth',
                    arg='turn_off',
                    valid=True, )
            else:
                self._wf.add_item(
                    title='Turn on Bluetooth',
                    arg='turn_on',
                    valid=True, )

            if os.getenv('can_update', 'true') == 'true':
                self._wf.add_item(
                    title='Disable update',
                    subtitle='Is performed every %d days' % UPDATE_FREQUENCY,
                    arg='disable_update',
                    valid=True, )
            else:
                self._wf.add_item(
                    title='Activate update',
                    subtitle='Is performed every %d days' % UPDATE_FREQUENCY,
                    arg='activate_update',
                    valid=True, )
        else:
            selected_option_method = getattr(self, 'manager_%s' % selected_option, None)
            if selected_option_method is not None:
                selected_option_method()
            else:
                raise Exception('"bm" action not')
        self._wf.send_feedback()

    def _parse_device(self, raw_device):
        return {
            'name': raw_device[5],
            'mac_address': raw_device[0],
            'connected': raw_device[1] != 'not connected',
            'paired': raw_device[4] != 'not paired',
            'favorite': raw_device[3] != 'not favourite',
            'last_access': raw_device[6],
        }

    def _get_devices(self):
        output = self._run_command([
            self.__BLUETOOTH_COMMAND_PATH,
            '--paired',
        ])
        output_devices = DEVICE_REGEX.findall(output)
        log.info(output_devices)

        devices = []
        for raw_device in output_devices:
            devices.append(self._parse_device(raw_device))
        return devices

    def action_list_devices(self):
        devices = self._get_devices()
        if len(devices) == 0:
            self._wf.add_item(
                title='No device found',
                icon=ICON_INFO,
                valid=False)
        else:
            for device in devices:
                self._wf.add_item(
                    uid=device['mac_address'],
                    title=device['name'],
                    subtitle='Connected' if device['connected'] else 'Disconnected',
                    arg=json.dumps(device),
                    valid=True, )
        self._wf.send_feedback()

    def action_set_device(self, device):
        set_config('default_device', device)
        device_json = json.loads(device)
        set_config('default_device_name', device_json['name'])
        notify('Default device stored', device_json['name'])
        self._wf.send_feedback()

    def _device_is_connected(self, mac_address):
        output = self._run_command([
            self.__BLUETOOTH_COMMAND_PATH,
            '--is-connected',
            mac_address,
        ])
        return output == '1'

    def action_connect(self, device=None):
        if device is None:
            device = os.getenv('default_device')
        device_json = json.loads(device)
        if not self._device_is_connected(device_json['mac_address']):
            try:
                self._run_command([
                    self.__BLUETOOTH_COMMAND_PATH,
                    '--connect',
                    device_json['mac_address'],
                ])
            except CalledProcessError as exc:
                log.error(exc)
                notify('"%s" was not possible to connect' % device_json['name'])
            else:
                # TODO: find a better way to wait until the device is connected
                time.sleep(1)
                if self._device_is_connected(device_json['mac_address']):
                    notify('"%s" connected' % device_json['name'])
                else:
                    notify(
                        '"%s" not connected' % device_json['name'],
                        'Make sure the device is on')
        else:
            notify('"%s" is already connected' % device_json['name'])
        self._wf.send_feedback()

    def action_disconnect(self, device=None):
        if device is None:
            device = os.getenv('default_device')
        device_json = json.loads(device)
        if self._device_is_connected(device_json['mac_address']):
            try:
                self._run_command([
                    self.__BLUETOOTH_COMMAND_PATH,
                    '--disconnect',
                    device_json['mac_address'],
                ])
            except CalledProcessError as exc:
                log.error(exc)
                notify('"%s" is already disconnected' % device_json['name'])
            else:
                if self._device_is_connected(device_json['mac_address']):
                    notify(
                        '"%s" disconnected' % device_json['name'],
                        'Something goes wrong')
                else:
                    notify('"%s" disconnected' % device_json['name'])
        else:
            notify('"%s" is already disconnected' % device_json['name'])
        self._wf.send_feedback()

    def action_notification(self, title, text=''):
        notify(title, text)

    def manager_turn_off(self):
        self._run_command([
            self.__BLUETOOTH_COMMAND_PATH,
            '--power',
            '0',
        ])
        notify('Bluetooth off')

    def manager_turn_on(self):
        self._run_command([
            self.__BLUETOOTH_COMMAND_PATH,
            '--power',
            '1',
        ])
        notify('Bluetooth on')

    def manager_disable_update(self):
        set_config('can_update', 'false')
        notify('Update disabled')

    def manager_activate_update(self):
        set_config('can_update', 'true')
        notify('Update activated')


if __name__ == '__main__':
    wf = Workflow3(update_settings={
        'github_slug': GITHUB_SLUG,
        'frequency': UPDATE_FREQUENCY,
    })
    log = wf.logger

    can_update = os.getenv('can_update', 'true') == 'true'
    if can_update and wf.update_available:
        wf.start_update()

    exit_status = wf.run(BluetoothManager)
    sys.exit(exit_status)

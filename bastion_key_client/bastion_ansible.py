#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2020 FABRIC Testbed
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Author: Ilya Baldin (ibaldin@renci.org)
from typing import List

import enum
import json
import os
from dataclasses import dataclass

from swagger_client.models.ssh_key_bastion import SshKeyBastion


class BastionKeyStatus(enum.Enum):
    active = enum.auto()
    deactivated = enum.auto()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class AnsibleStatus(enum.Enum):
    present = enum.auto()
    absent = enum.auto()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


@dataclass
class BastionAnsibleKey:
    key: str
    state: str

    def to_jsonobj(self):
        return self.__dict__.copy()

    def __str__(self):
        parts = self.key.split(' ')
        if len(parts) == 3:
            return parts[2] + ": " + self.state
        else:
            return self.key[-40:] + ": " + self.state

    def __repr__(self):
        return str(self)


class BastionAnsibleUser:
    """
    Single user within ansible JSON
             {
            "username": "jdoe",
            "name": "John Doe,,,,jdoe@email.com",
            "shell": "/sbin/nologin",
            "groups": "",
            "state": "present",
            "remove": "yes",
            "force": "yes",
            "create_home": "yes",
            "ssh_key": [
               {
                  "key": "ssh-rsa <key> <key comment>"
                  "state": "present",
               },
               {
                  "key": "ssh-rsa <key> <key comment>"
                  "state": "absent",
               }
            ]
         }
    """
    def __init__(self, username: str, name: str,
                 shell: str = "/sbin/nologin", groups: str = ""):
        self.username = username
        # note that even when removing keys username and name/gecos
        # have to match the original entry, otherwise Ansible will edit /etc/passwd
        self.name = name
        self.shell = shell
        self.groups = groups
        # we always do 'present' state for users
        self.state = AnsibleStatus.present.name
        self.remove = "yes"
        self.force = "yes"
        self.create_home = "yes"
        self.ssh_key = list()

    def add_key(self, bastion_key: SshKeyBastion):
        """
        Add key to a person
        :param bastion_key:
        :return:
        """
        if bastion_key.login != self.username:
            raise BastionAnsibleException(f'Attempting to add key of user {bastion_key.login} '
                                          f'to the record of user {self.username}')
        encoded_key1 = bastion_key.public_openssh.split()[1]

        for existing_key in self.ssh_key:
            # check for duplicates (although shouldn't really happen)
            encoded_key2 = existing_key.key.split()[1]
            if encoded_key1 == encoded_key2:
                # deactivated keys always win
                if existing_key.state == AnsibleStatus.present.name and \
                        bastion_key.status == BastionKeyStatus.deactivated.name:
                    existing_key.state = AnsibleStatus.absent.name
                return

        if bastion_key.status == BastionKeyStatus.active.name:
            ansible_status = AnsibleStatus.present
        else:
            ansible_status = AnsibleStatus.absent

        self.ssh_key.append(BastionAnsibleKey(bastion_key.public_openssh, ansible_status.name))

    def to_jsonobj(self):
        odict = self.__dict__.copy()
        odict['ssh_key'] = [x.to_jsonobj() for x in self.ssh_key]
        return odict

    def __str__(self):
        return self.username + ": " + ", ".join([str(k) for k in self.ssh_key])

    def __repr__(self):
        return str(self)


class BastionAnsibleUserList:
    """
    This maps onto a JSON object consumed by the Ansible playbooks, for
    each user we have their login info and key info.
    There are different scenarios for adding a key to this list
    - Key is active - returned from UIS, login and gecos provided by UIS
    - Key is deactivated - returned from UIS, login and gecos provided by UIS
    - Key is expired/deactivated - found in /home/<login>/.ssh/authorized_keys,
      login is known, gecos needs to be looked up by getent
    """
    def __init__(self, bastion_key_list: List[SshKeyBastion]):
        """
        Convert a list of keys into a Bastion User list, checking for key duplicates (just in case).
        A deactivated key always wins over an active key if fingerprints match.
        :param bastion_key_list:
        """
        # organize users by username/login
        self.users = dict()
        for bk in bastion_key_list:
            self.add_key(bk)

    def add_key(self, key: SshKeyBastion) -> None:
        """
        Add a new key (potentially creating a dictionary entry and new user)
        :param key:
        :return:
        """
        assert key.login is not None
        assert key.gecos is not None and len(key.gecos) > 0
        if self.users.get(key.login, None) is None:
            self.users[key.login] = BastionAnsibleUser(key.login, key.gecos)
        self.users[key.login].add_key(key)

    @property
    def usercount(self):
        return len(self.users)

    @property
    def usernames(self):
        return list(self.users.keys())

    def to_json(self) -> str:
        jsondict = {"community": {"experimenter": [x.to_jsonobj() for x in self.users.values()]}}
        return json.dumps(jsondict, indent=2)

    @staticmethod
    def get_package_path():
        return os.path.dirname(__file__)

    def __str__(self):
        return "\n".join([str(u) for u in self.users.values()])


class BastionAnsibleException(Exception):
    def __init__(self, msg: str):
        assert(msg is not None)
        super().__init__(f'BastionAnsible Exception: {msg}')
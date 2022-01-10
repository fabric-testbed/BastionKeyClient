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
import datetime
from typing import List

import os
import pwd
import re
from datetime import datetime, timezone
from swagger_client.models.ssh_key_bastion import SshKeyBastion

KEYTSREGEX = r"^.*_\(([\d]{4}-[\d]{2}-[\d]{2}_[\d]{2}:[\d]{2}:[\d]{2}\+0000)\)_$"
TSFORMAT = "%Y-%m-%d_%H:%M:%S%z"


def keyfilter(pubkey) -> bool:
    """
    Check if comment in the key means the key is expired or not. Return True
    for keys that don't have a comment.
    Return false for 0-length keys.
    :param pubkey:
    :return:
    """
    if len(pubkey) == 0:
        return False
    now = datetime.now(timezone.utc)
    match = re.match(KEYTSREGEX, pubkey)
    if match is not None:
        pdate = datetime.strptime(match[1], TSFORMAT)
        return pdate < now
    return False


def prejudicekeyfilter(pubkey) -> bool:
    """
    Check if comment in the key means the key is expired or not. Return False
    for keys that don't have a comment.
    Return false for 0 length keys.
    :param pubkey
    :return:
    """
    if len(pubkey) == 0:
        return False
    now = datetime.now(timezone.utc)
    match = re.match(KEYTSREGEX, pubkey)
    if match is not None:
        pdate = datetime.strptime(match[1], TSFORMAT)
        return pdate < now
    return True


class HomedirScanner:
    """
    Scans home directories' .ssh/authorized_keys files for any expired keys.
    Keys that have as part of their comment a string indicating their
    expiration date like _(YYYY-MM-DD_HH:MM:SS)_ (in UTC). Those keys that are
    expired are flagged for removal. Depending on the prejudice setting,
    keys that do not have an expiration date set are ignored (False) or
    removed (True).
    Ignores home directories whose users are on the exclude list.
    Uses getent to collect gecos fields matching home directories
    because this is needed by Ansible.
    """
    def __init__(self, exclude_list: List[str], home_prefix: str, prejudice: bool = False):
        self.exclude_list = exclude_list
        self.prejudice = prejudice
        self.home_prefix = home_prefix

    def scan(self) -> List[SshKeyBastion]:
        """
        Scan the home directories, locate expired keys and return a list
        of SshKeyBastion structures.
        :return:
        """
        homeiter = os.scandir(self.home_prefix)
        ret = list()
        for homedir in homeiter:
            if not homedir.is_dir():
                continue
            if homedir.name in self.exclude_list:
                continue
            # read matching /etc/passwd getent
            try:
                gecos = pwd.getpwnam(homedir.name).pw_gecos
            except KeyError:
                # unable to find user in password database, exit with error
                raise BastionHomedirException(f'Unable to find user {homedir.name} in password database, '
                                              f'unable to proceed')
            # read home/.ssh/authorized_keys
            try:
                with open(os.path.join(homedir.path, ".ssh", "authorized_keys"),
                          "r", encoding="utf-8") as f:
                    userkeys = f.read()
                # can remove keys with prejudice - i.e. those keys that don't have a timestamp
                # get removed. Or else leave them alone
                if self.prejudice:
                    userkeys_list = filter(prejudicekeyfilter, userkeys.split('\n'))
                else:
                    userkeys_list = filter(keyfilter, userkeys.split('\n'))

                ret.extend([SshKeyBastion(key, homedir.name, gecos, "deactivated") for key in userkeys_list])
            except FileNotFoundError:
                # skipping
                continue

        return ret


class BastionHomedirException(Exception):
    def __init__(self, msg: str):
        assert (msg is not None)
        super().__init__(f'BastionHomedir Exception: {msg}')
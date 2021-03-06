#!/usr/bin/env python
# -*- coding: utf8 ft: python -*-

# Copyright (c) 2012-2013 Svante Kvarnström <sjk@ankeborg.nu>. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import re
import sys
import smtplib
import urllib2
import yaml


class Ipcheck():
    config_file = os.path.expanduser('~/etc/ip-check.yaml')
    ip = None
    config = {}

    def __init__(self):
        pass

    def get_ip(self):
        try:
            f = urllib2.urlopen(self.config["loopia"])
        except urllib2.URLError, e:
            print "Could not open {}: {}".format(self.config["loopia"], e)
            exit()

        data = f.read()
        self.ip = re.search(r'((?:\d{1,3}\.){3}\d{1,3})', data).group(1)

    def is_new_ip(self):
        try:
            f = open(self.config["ipfile"], 'r+')
            oldip = f.read().rstrip()
        except IOError:
            f = open(self.config["ipfile"], 'w')
            f.write(newip)
            f.close()
            return True

        if self.ip == oldip:
            f.close()
            return False
        else:
            f.truncate()
            f.write(self.ip)
            f.close()
            return True

    def email_ip(self):
        msg = r"From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\nMy IP-adress is {}".format(
                self.config["email"]["from_addr"], self.config["email"]["to_addr"], self.ip, self.ip)

        server = smtplib.SMTP_SSL(self.config["email"]["smtp_out"])
        # server.set_debuglevel(1)
        server.sendmail(self.config["email"]["from_addr"], self.config["email"]["to_addr"], msg)
        server.quit()

    def load_config(self):
        try:
            f = open(self.config_file)
        except IOError, e:
            print "Could not read configuration file: {}".format(e)
            sys.exit()

        config = yaml.load(f)
        f.close()
        self.config = config

def main():
    ipcheck = Ipcheck()

    ipcheck.load_config()
    ipcheck.get_ip()

    if ipcheck.is_new_ip():
        ipcheck.email_ip()


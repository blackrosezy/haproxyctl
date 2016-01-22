#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""haproxyctl.

Usage:
  haproxyctl add <url> <container_name> [<port>]
  haproxyctl rm <url>
  haproxyctl sync
  haproxyctl (-h | --help)
  haproxyctl (-v | --version)

Options:
  -h --help     Show this screen.
  -v --version  Show version.

"""

from cStringIO import StringIO
from docker import Client, errors
from docopt import docopt
from jinja2 import Environment, FileSystemLoader, Template
import json
import os
import sys
import tarfile


class Haproxyctl:
    def __init__(self):
        self.__haproxyctl_config_file = '/root/.haproxyctl.cfg'
        self.__haproxy_template_file = 'haproxy.jinja'
        self.__haproxy_config_file = 'haproxy.cfg'
        self.__haproxy_config_path = '/usr/local/etc/haproxy/'
        self.__haproxy_container_id = None
        self.__docker_client = Client(base_url='unix://var/run/docker.sock')

    def get_haproxy_container(self):
        containers = self.__docker_client.containers()
        for container in containers:
            for name in container['Names']:
                if 'haproxy' in name.lower():
                    self.__haproxy_container_id = container['Id']
                    return self.__haproxy_container_id
        return None

    def get_container_ip(self, container_name):
        try:
            container = self.__docker_client.inspect_container(container_name)
            return container['NetworkSettings']['IPAddress']
        except errors.NotFound:
            return None

    def read_config_file(self):
        with open(self.__haproxyctl_config_file) as f_handle:
            try:
                json_data = json.load(f_handle)
                return json_data
            except ValueError:
                return []
        return []

    def write_config_file(self, existing_config):
        with open(self.__haproxyctl_config_file, 'w') as f_handle:
            json.dump(existing_config, f_handle, sort_keys=True, indent=4, ensure_ascii=False)

    def add_url(self, url, container_name, port, existing_config):
        if port is None:
            port = 80

        for item in existing_config:
            if type(item) is dict:
                if 'url' in item:
                    if item['url'] == url:
                        item['container_name'] = container_name
                        item['port'] = port
                        return existing_config

        existing_config.append({'url': url, 'container_name': container_name, 'port': port})
        return existing_config

    def remove_url(self, url, existing_config):
        for item in existing_config:
            if type(item) is dict:
                if 'url' in item:
                    if item['url'] == url:
                        existing_config.remove(item)

        return existing_config

    def generate_haproxy_config(self, new_config):
        env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True)
        template = env.get_template(self.__haproxy_template_file)
        f = open(self.__haproxy_config_file, 'w')
        items = []
        counter = 1
        for item in new_config:
            ip = self.get_container_ip(item['container_name'])
            if ip:
                items.append({'id': counter, 'url': item['url'], 'port': item['port'], 'ip': ip})
                counter += 1
                print " => [ OK ] Url: '%s', Container: '%s', IP:%s, Port:%s" % (
                    item['url'], item['container_name'], ip, item['port'])
            else:
                print " => [SKIP] Url: '%s', Container: '%s'(not found), IP:N/A, Port:%s" % (
                    item['url'], item['container_name'], item['port'])

        f.write(template.render(items=items))
        f.close()

    def update_haproxy_config(self):
        si = StringIO()
        tar = tarfile.open(mode='w', fileobj=si)
        tar.add(self.__haproxy_config_file)
        tar.close()
        tar_content = si.getvalue()
        self.__docker_client.put_archive(self.__haproxy_container_id, self.__haproxy_config_path, tar_content)

    def test_haproxy_config(self):
        cmd = "haproxy -c -f %s%s 2>&1" % (self.__haproxy_config_path, self.__haproxy_config_file)
        res = self.__docker_client.exec_create(container=self.__haproxy_container_id, cmd=['bash', '-c', cmd])
        output = self.__docker_client.exec_start(res)
        output = output.strip()
        if output == "Configuration file is valid":
            print " => Haproxy config is OK"
            return True
        else:
            print " => Haproxy config contains error!"
        return False

    def restart_haproxy_container(self):
        print " => Restarting haproxy..."
        self.__docker_client.restart(container=self.__haproxy_container_id, timeout=0)
        print " => Restarted."


def main():
    arguments = docopt(__doc__, version='haproxyctl 0.1.0')

    if not os.geteuid() == 0:
        sys.exit(' => Script must be run as root!')

    hctl = Haproxyctl()

    if hctl.get_haproxy_container() is None:
        sys.exit(' => Cannot find any Haproxy container, exiting.')

    if arguments['rm'] and arguments['<url>'] is not None:
        config_content = hctl.read_config_file()
        config_content = hctl.remove_url(arguments['<url>'], config_content)
        hctl.write_config_file(config_content)
        hctl.generate_haproxy_config(config_content)
        hctl.update_haproxy_config()
        if hctl.test_haproxy_config():
            hctl.restart_haproxy_container()

    if arguments['add'] and arguments['<url>'] is not None and arguments['<container_name>'] is not None:
        config_content = hctl.read_config_file()
        config_content = hctl.add_url(arguments['<url>'], arguments['<container_name>'], arguments['<port>'],
                                      config_content)
        hctl.write_config_file(config_content)
        hctl.generate_haproxy_config(config_content)
        hctl.update_haproxy_config()
        if hctl.test_haproxy_config():
            hctl.restart_haproxy_container()

    if arguments['sync']:
        config_content = hctl.read_config_file()
        hctl.generate_haproxy_config(config_content)
        hctl.update_haproxy_config()
        if hctl.test_haproxy_config():
            hctl.restart_haproxy_container()

    print " => Done."


if __name__ == '__main__':
    main()

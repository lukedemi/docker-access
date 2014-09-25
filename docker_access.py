#!/usr/bin/env python
import docker
import argparse
from subprocess import call
from distutils import spawn

c = docker.Client(base_url='unix://var/run/docker.sock', version='1.12', timeout=10)

# This app needs nsenter to run, google around to find the easiest way to install
# it on your system - it is probably not available as a package.
if not spawn.find_executable('nsenter'):
    print "Please install nsenter on your system before using this script"

PARSER = argparse.ArgumentParser()
PARSER.add_argument('search_query', help='Search query (id or name)')
PARSER.add_argument('-i', dest='id', action='store_true',
                     help='Will only search docker container ids')
PARSER.add_argument('-n', dest='name', action='store_true',
                     help='Will only search docker container names')
RESULTS = PARSER.parse_args()

def nsenter(container):
    pid = c.inspect_container(container)['State']['Pid']
    call('nsenter --target %s --mount --uts --ipc --net --pid' % pid, shell=True)

for container in c.containers():
    if RESULTS.name and RESULTS.search_query in container['Image']:
        nsenter(container)
        exit(0)
    elif RESULTS.id and RESULTS.search_query in container['Id']:
        nsenter(container)
        exit(0)
    elif not RESULTS.id or RESULTS.name and RESULTS.search_query in container['Id'] + container['Image']:
        nsenter(container)
        exit(0)

print 'container not found.'

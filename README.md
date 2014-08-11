docker-access
=============

I write this guy to help me quickly get in and out of docker containers while I'm debugging environments. It's pretty simple - just call it with a container id or 'name' and it will open up the first match. I added in some simple argparse values in case you want to specifically check only ids or names, but I doubt they'll ever be useful.

## Install

Python Requirements:
```
sudo apt-get install python-pip
pip install -r requirements.txt
```
Nsenter:
```
cd /tmp
curl https://www.kernel.org/pub/linux/utils/util-linux/v2.24/util-linux-2.24.tar.gz \
     | tar -zxf-
cd util-linux-2.24
./configure --without-ncurses
make nsenter
cp nsenter /usr/local/bin
```
Docker API:
```
# Docker-py needs the HTTP API
echo 'DOCKER_OPTS="-H tcp://0.0.0.0:4243 -H unix:///var/run/docker.sock"' >> /etc/default/docker
restart docker
```

## Usage

I usually drop it in /usr/local/bin/ minus .py

```
usage: docker_access.py [-h] [-i] [-n] search_query

positional arguments:
  search_query  Search query (id or name)

optional arguments:
  -h, --help    show this help message and exit
  -i            Will only search docker container ids
  -n            Will only search docker container names
```

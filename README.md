# lcmap-client-py  [![Build Status][travis-badge]][travis][![PyPI Project][pypi-badge]][pypi]

*LCMAP REST Service Client for Python*

[Very WIP ... not ready for use]

## System Requirements
#### Centos 7

Python 2.7
```bash
$ sudo apt-get install python-pip python-devel
                       gcc-c++ gcc-gfortran
                       gdal-devel gdal
```

Python 3.4
```bash
$ sudo apt-get install python3-pip python3-devel
                       gcc-c++ gcc-gfortran
                       gdal-devel gdal
```

#### Ubuntu 14.04
```bash
$ sudo yum install -y python-pip python-dev
                      libgdal1h libgdal1-dev
                      gfortran g++
```

## Installing
```bash
$ pip install lcmap_client
```

If /tmp is mounted noexec:
```bash
$ pip install -b some_dir lcmap_client
```

## Configuration

Client library configuration is done using a Config/INI file. For more
information, visit the client documentation link below -- in particular, the
section "The Client Libraries" > "Configuration".


## Documentation

Full documentation for all LCMAP clients is available here:
 * http://usgs-eros.github.io/lcmap-client-docs/current/

Note that per-client usage and example code is selectable via tabs in the upper-right of that page.


## Example Usage

Starting:

```bash
$ cd lcmap-client-py
$ tox -e py34-shell
```

```python
>>> from lcmap_client import Client
>>> client = Client()
>>> result = client.models.samples.os_process.run(year=2017, delay=10)
>>> result.follow_link()
```

## CLI Tools

Run a query:

```bash
$  lcmap query rod --x -1789425 --y 3073665 --t1 2010-01-01 --t2 2015-01-01
```

Execute the same query against the CCDC model:

```bash
$  lcmap model ccdc --x -1789425 --y 3073665 --t1 2010-01-01 --t2 2015-01-01 \
        --row=2241 --col=1231 --out-dir="stdout" --scene-list="stdin"
```

To see what's available:

```bash
$ lcmap --help
```

And for help on the subcommands:

```bash
$ lcmap query --help
$ lcmap query rod --help
```


## Development

TBD


## License

```
Copyright © 2015 United States Government

NASA Open Source Agreement, Version 1.3.
```

<!-- Named page links below: /-->

[travis]: https://travis-ci.org/USGS-EROS/lcmap-client-py
[travis-badge]: https://travis-ci.org/USGS-EROS/lcmap-client-py.png?branch=master
[lcmap-logo]: resources/images/lcmap-logo-1-250px.png
[lcmap-logo-large]: resources/images/lcmap-logo-1-1000px.png
[pypi]: https://pypi.python.org/pypi/lcmap-client
[pypi-badge]: https://img.shields.io/pypi/v/lcmap-client.svg?maxAge=2592000

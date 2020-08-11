
### Get

```
git clone --recurse-submodules https://github.com/davidlatwe/rez-packages.git
```

### Prerequisite

In `$PATH`
* Git
* Python

### Deploy script

Caveat: The Python executable you used to call `deploy.py` will be used to create Rez core's virtualenv if option `--install-rez` is given.

```bash
$ python deploy.py --install-rez --deploy-package --with-config
```

The *--help*
```bash
$ python deploy.py -h
usage: deploy.py [-h] [--install-rez [INSTALL_REZ]] [--deploy-package]
                 [--with-config [WITH_CONFIG]] [--release] [--yes]
                 [packages [packages ...]]

positional arguments:
  packages              Deploy only these packages. Deploy ALL if no
                        specification.

optional arguments:
  -h, --help            show this help message and exit
  --install-rez [INSTALL_REZ]
                        Rez install path if you want to install it. If enabled
                        but no path given, Rez will be installed in
                        '~/rez/core'. Directory will be removed if exists.
  --deploy-package      Deploy packages from this repository.
  --with-config [WITH_CONFIG]
                        Deploy packages with config ($REZ_CONFIG_FILE). If
                        enabled but no config path(s) given, ./rezconfig.py
                        will be used.
  --release             Deploy to package releasing location.
  --yes                 Yes to all.


```


## Ozark

A production/development environment setup powered by Rez, Allzpark and MongoDB.


### Get

```
git clone --recurse-submodules https://github.com/davidlatwe/rez-ozark.git
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

### Mock Apps

To quickly get started, you can use this tool to mock any apps in any version you want.

```bash
$ python mocks.py --all
```

The output app package is just a Qt app that have a button to press. But you can use them to quickly compose profile for demo.


## Usage

Ozark ships with a MongoDB/MontyDB based Rez package repository plugin which used to store Allzpark profile packages, you may see `ozark/config/rezconfig.py` for configuration details.

* Enter Ozark

    ```bash
    $ rez-env ozark
    ```

* Init profile at current working directory

    ```bash
    $ party --init
    ```

* Enable profile to MongoDB

    ```bash
    $ party --at release
    ```
    
* Or MontyDB
    
    ```bash
    $ party --at install
    ```

* List out all profiles

    ```bash
    $ party --list
    ```

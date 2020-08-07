
### Get

```
git clone --recurse-submodules https://github.com/davidlatwe/rez-packages.git
```

### Prerequisite

In `$PATH`
* Git
* Python >= 3

### Deploy

```shell script
rez-bind --release os
cd ./rez | rez-release
```

```shell script
cd ../_base/default | rez-release
cd ../../miniconda | rez-release
cd ../python | rez-release --version=3.6
cd ../gitz | rez-release
cd ../pipz | rez-release
```

```shell script
rez-env pipz -- install PySide2 PyQt5 --release --yes
cd ../Qt.rez | rez-release
```

```shell script
rez-env pipz -- install rich environs --release --yes
cd ../_base/site | rez-release
```

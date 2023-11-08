
See discussions here: 
[Build Python with ssl module](https://stackoverflow.com/questions/53543477/building-python-3-7-1-ssl-module-failed/77445326#77445326)



## 1.Install Python 3.12 with openssl on ubuntu 20.04:

```
wget https://www.openssl.org/source/openssl-3.1.4.tar.gz
tar zxvf openssl-3.1.4.tar.gz
cp -r openssl-3.1.4 /usr/src/
cd openssl-3.1.4
./config shared --prefix=/usr/local/
sudo make -j32
sudo make install
```

## Install Python 3.12

### Firstly, prepare the library path (for openssl libs to be found on lib64):

``` vim ~/.profile ```

```
export LD_LIBRARY_PATH="/usr/local/lib64:$LD_LIBRARY_PATH"
```

### Install prerequisite packages (the step is important, else many runtime errors may occur):

```bash
apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
```

see: https://stackoverflow.com/questions/50335503/no-module-named-bz2-in-python3

### Then install python 3.12 from source:

```
sudo apt install libffi-dev
export LD_LIBRARY_PATH="/usr/local/lib64:$LD_LIBRARY_PATH"
wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
tar zxvf Python-3.12.0.tgz
cd Python-3.12.0
./configure --with-openssl=/usr/local --prefix=/opt/python-3.12.0  --enable-optimizations
sudo make -j32
sudo make altinstall
```

In case you would like to skip unit test when compiling (for python 3.12), add the skip instructions for configure: ``` --without-tests --disable-tests ```.

And you may make part of the targets if the tests skipping params not work (for python 3.10):
```
make -j32 build_all
make -j32 altinstall
```

### To test it out, run python3.12 and input:

```
import ssl
ssl.OPENSSL_VERSION
```

Plus, currently to Nov 2023, Python 3.10 is recommended to avoid lots of incompatibilities with many packages.

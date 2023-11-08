
See discussions here: 
[Build Python with ssl module](https://stackoverflow.com/questions/53543477/building-python-3-7-1-ssl-module-failed/77445326#77445326)



## 1.Install Python 3.12/3.10.8 with openssl on ubuntu 20.04:

Python 3.10 works with openssl 1.1.1 and 1.1.1w, it does not works with openssl later version other than 1.1.x

```
cd /usr/src
wget https://www.openssl.org/source/openssl-1.1.1w.tar.gz
tar zxvf openssl-1.1.1w.tar.gz
mv openssl-1.1.1w /usr/local/openssl && cd /usr/local/openssl
make distclean 
./config -fPIC -shared 
sudo make -j32
sudo make install
mkdir lib
cp ./*.{so,so.1.*,so.*,a,pc} ./lib
```

## Install Python 3.12/3.10.8

### Firstly, prepare the library path (for openssl libs to be found):

``` vim ~/.profile ```

```
export LD_LIBRARY_PATH="/usr/local/openssl/lib:$LD_LIBRARY_PATH"
```

### Install prerequisite packages (the step is important, else many runtime errors may occur):

```bash
apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
```

see: https://stackoverflow.com/questions/50335503/no-module-named-bz2-in-python3

If you did'nt install the prerequisite packages, and get errors in python program running in a venv environment.
Then you can go back to this step to install these prerequisites. And then reinstall python, recreate venv environment.

### Then install python 3.12.0/3.10.8 from source:

```
export VERSION=3.10.8
export LD_LIBRARY_PATH="/usr/local/openssl/lib:$LD_LIBRARY_PATH"
wget https://www.python.org/ftp/python/$VERSION/Python-$VERSION.tgz
tar zxvf Python-3*.tgz
cd Python-$VERSION
./configure --with-openssl=/usr/local --prefix=/opt/python-$VERSION  --enable-optimizations
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
import ssl, _ssl, bz2
ssl.OPENSSL_VERSION
```

Plus, currently to Nov 2023, Python 3.10 is recommended to avoid lots of incompatibilities with many packages(like torch, transformers).

## Reference for torch and cuda compatibilities

https://gist.github.com/davideuler/8cc6331a88e102c26db6676016e63517

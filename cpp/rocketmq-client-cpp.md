
# Mac Silicon 上面使用 rocketmq-client-cpp 客户端

Mac Sonama 14.5, boost 1.79.0, rocketmq-client-cpp 2.1.0 安装成功。 之后可以使用 rocketmq-client-python==2.0.0。

## 编译安装 boost 1.79.0

brew install cmake automake autoconf libtool

从源代码安装：
https://archives.boost.io/release/1.79.0/source/
https://www.boost.org/doc/libs/1_85_0/more/getting_started/windows.html#simplified-build-from-source

sh ./bootstrap.sh
./b2 install --prefix=
./b2 install --prefix=~/workspace/rocketmq-client-cpp-2.1.0

## 安装 rocketmq-client-python

pip install rocketmq-client-python

依赖于 boost 1.7x 中的 atomic.hpp，1.8.x 及以上版本版本 boost 会报错:

```text
fatal error: 'boost/atomic.hpp' file not found
#include <boost/atomic.hpp>
```

##  安装 rocketmq-client-cpp 2.1.0

cmake 安装 rocketmq-client-cpp

``` bash
wget https://github.com/open-source-parsers/jsoncpp/archive/0.10.6.zip -O jsoncpp-0.10.6.zip
unzip jsoncpp-0.10.6.zip
cd jsoncpp-0.10.6
mkdir -p dest
cd dest 
cmake -DCMAKE_BUILD_TYPE=Release ..
make && make jsoncpp_lib_static && sudo make install

# 编译 rocketmq-client-cpp
cd ../..
wget https://github.com/apache/rocketmq-client-cpp/archive/refs/tags/2.1.0.zip -O rocketmq-client-cpp-2.1.0.zip
unzip rocketmq-client-cpp-2.1.0.zip

cd rocketmq-client-cpp-2.1.0

vim CMakeLists.txt 
# Libevent_USE_STATIC_LIBS, JSONCPP_USE_STATIC_LIBS 两个 option 默认值改成 OFF
# 增加内容： set(BOOST_DIR ${PROJECT_SOURCE_DIR})
# 更新：Boost_INCLUDE_DIR, Boost_LIBRARY_DIRS 目录指向：
#     set(Boost_INCLUDE_DIR ${BOOST_DIR}/include)
#     set(Boost_LIBRARY_DIRS ${BOOST_DIR}/lib)

sh build.sh  # 运行这个命令会报错，自动下载 libevent 包

# 拷贝编译的 libjsoncpp.a 静态库到 bin/lib 目录:
cp tmp_down_dir/jsoncpp-0.10.6/dest/src/lib_json/libjsoncpp.a  bin/lib/

# 编译 libevent
cd tmp_down_dir
cd libevent-release-2.1.11-stable
sh ./autogen.sh
./configure  # --disable-shared --enable-static
make && sudo make install

# 回到 rocketmq-client-cpp 根目录：
cd ../..
mkdir -p tmp_build_dir
cd tmp_build_dir

cmake -DCMAKE_BUILD_TYPE=Release ..
export LIBRARY_PATH=$LIBRARY_PATH:/opt/homebrew/opt/boost@1.76/lib:
/opt/homebrew/opt/jsoncpp/lib/
export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:/opt/homebrew/opt/boost@1.76/include:/usr/local/include/jsoncpp/

make -j8
```

## 发布 librocketmq 库到系统目录

``` bash
cd ..
mkdir -p /usr/local/include/rocketmq
sudo cp bin/* /usr/local/include/rocketmq
sudo cp bin/librocketmq* /usr/local/lib
sudo install_name_tool -id “@rpath/librocketmq.dylib” /usr/local/lib/librocketmq.dylib
```

## FAQ

### 1.如果出现这个错误，说明要用 boost 1.72.0 或者更改代码来修复：

``` text
~/workspace/rocketmq-client-cpp-2.1.0/src/common/ByteOrder.h:23:10: fatal error: 'boost/detail/endian.hpp' file not found
#include <boost/detail/endian.hpp>
```

改代码：vim ~/workspace/rocketmq-client-cpp-2.1.0/src/common/ByteOrder.h，调整如下：

// #include <boost/detail/endian.hpp>
#include <boost/predef/other/endian.h>

https://github.com/boostorg/endian/issues/45


### 2.No rule to make target ~/workspace/rocketmq-client-cpp-2.1.0/bin/lib/libevent.a',

需要安装 libevent 静态库。或者在 CMakeLists.txt 文件中把 libevent 的 static 选项配置为 OFF。

### 3.如果出现这个错误，需要重新安装 arm64 版本 zlib:

ld: warning: ignoring file '/usr/local/lib/libz.1.2.12.dylib': found architecture 'x86_64', required architecture 'arm64'
ld: Undefined symbols:
  _crc32, referenced from:
      boost::iostreams::detail::zlib_base::after(char const*&, char*&, bool) in libboost_iostreams.a[6](zlib.o)
  _deflate, referenced from:
      boost::iostreams::detail::zlib_base::xdeflate(int) in libboost_iostreams.a[6](zlib.o)

arch -arm64 brew reinstall zlib

重新覆盖软链：
sudo ln -sf /opt/homebrew/opt/zlib/lib/libz.1.3.1.dylib /usr/local/lib/libz.dylib

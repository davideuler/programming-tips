
# Include a dependency from local directory instead of a remote dependency. 
Add a dependency section to your executable's Cargo.toml and specify the path:

[dependencies.my_lib]
path = "../my_lib"
or the equivalent alternate TOML:

[dependencies]
my_lib = { path = "../my_lib" }

https://stackoverflow.com/questions/33025887/how-to-use-a-local-unpublished-crate

# Specify a dependecy mirror for Cargo build

cat ~/.cargo/config

```
[source.crates-io]
replace-with = 'tuna'

[source.tuna]
registry = "https://mirrors.tuna.tsinghua.edu.cn/git/crates.io-index.git"
```

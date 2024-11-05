

https://github.com/ibraheemdev/modern-unix?tab=readme-ov-file
https://jvns.ca/blog/2022/04/12/a-list-of-new-ish--command-line-tools/

Tools:
eza bat lsd fd ripgrep delta dust duf mcfly jq bottom glances gtop lazygit


```
wget https://github.com/eza-community/eza/releases/download/v0.20.6/eza_x86_64-unknown-linux-musl.tar.gz
tar -xzf eza_x86_64-unknown-linux-musl.tar.gz
cp eza /usr/local/bin

wget https://github.com/sharkdp/bat/releases/download/v0.24.0/bat-musl_0.24.0_amd64.deb
dpkg -i bat-musl*.deb

wget https://github.com/lsd-rs/lsd/releases/download/v1.1.5/lsd-v1.1.5-aarch64-unknown-linux-musl.tar.gz
tar zxvf lsd-*.tar.gaz

wget https://github.com/sharkdp/fd/releases/download/v10.2.0/fd-v10.2.0-aarch64-unknown-linux-musl.tar.gz
tar zxvf fd-*.tar.gz

wget https://github.com/BurntSushi/ripgrep/releases/download/14.1.1/ripgrep-14.1.1-aarch64-unknown-linux-gnu.tar.gz
tar zxvf ripgrep*.tar.gz


wget https://github.com/dandavison/delta/releases/download/0.18.2/delta-0.18.2-aarch64-unknown-linux-gnu.tar.gz
tar zxvf delta*.tar.gz

wget https://github.com/bootandy/dust/releases/download/v1.1.1/dust-v1.1.1-aarch64-unknown-linux-musl.tar.gz
tar xvf dust*.tar.gz

LAZYGIT_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" | grep -Po '"tag_name": "v\K[^"]*')
curl -Lo lazygit.tar.gz "https://github.com/jesseduffield/lazygit/releases/latest/download/lazygit_${LAZYGIT_VERSION}_Linux_x86_64.tar.gz"
tar xf lazygit.tar.gz lazygit
sudo install lazygit /usr/local/bin

```


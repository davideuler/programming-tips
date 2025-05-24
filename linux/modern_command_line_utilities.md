

https://github.com/ibraheemdev/modern-unix?tab=readme-ov-file
https://jvns.ca/blog/2022/04/12/a-list-of-new-ish--command-line-tools/
https://lnav.org/downloads
https://github.com/dandavison/delta#get-started
https://zaiste.net/posts/shell-commands-rust/
https://github.com/jonas/tig/issues/26#issuecomment-1923835137

## Modern Linux/Mac (maybe also works on Windows) Command line tools

On Mac:
brew install eza bat lsd fd ripgrep delta dust duf mcfly jq bottom glances gtop lazygit lnav

lnav doesn't works with warp now(2025/05).

On Linux:

```
wget https://github.com/eza-community/eza/releases/download/v0.20.6/eza_x86_64-unknown-linux-musl.tar.gz
tar -xzf eza_x86_64-unknown-linux-musl.tar.gz
cp eza /usr/local/bin

wget https://github.com/sharkdp/bat/releases/download/v0.24.0/bat-musl_0.24.0_amd64.deb
dpkg -i bat-musl*.deb

wget https://github.com/lsd-rs/lsd/releases/download/v1.1.5/lsd-musl_1.1.5_amd64.deb
dpkg -i lsd-*.deb

wget https://github.com/sharkdp/fd/releases/download/v10.2.0/fd-musl_10.2.0_amd64.deb
tar zxvf fd-*.tar.gz

wget https://github.com/BurntSushi/ripgrep/releases/download/14.1.0/ripgrep-14.1.0-x86_64-unknown-linux-musl.tar.gz
tar zxvf ripgrep*.tar.gz


wget https://github.com/dandavison/delta/releases/download/0.18.2/delta-0.18.2-x86_64-unknown-linux-musl.tar.gz
tar zxvf delta*.tar.gz

wget https://github.com/bootandy/dust/releases/download/v1.1.1/du-dust_1.1.1-1_amd64.deb
tar xvf dust*.tar.gz

LAZYGIT_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" | grep -Po '"tag_name": "v\K[^"]*')
curl -Lo lazygit.tar.gz "https://github.com/jesseduffield/lazygit/releases/latest/download/lazygit_${LAZYGIT_VERSION}_Linux_x86_64.tar.gz"
tar xf lazygit.tar.gz lazygit
sudo install lazygit /usr/local/bin

```

## A note on delta

### delta as git pager
Delta works as a git pager, configure it at ~/.gitconfig, then git diff, git show works.

$vim ~/.gitconfig

```
[core]
    pager = delta

[interactive]
    diffFilter = delta --color-only

[delta]
    navigate = true  # use n and N to move between diff sections
    light = true      # or dark = true, or omit for auto-detection
    side-by-side = true

[merge]
    conflictstyle = zdiff3
```

### delta as tig diff
For tig diff, configure ~/.tigrc to bind Shift + D, Shift + S for side by side diff,

vim ~/.tigrc
```
# View diffs using `delta`
bind diff D >sh -c "git show %(commit) | delta --paging always"
bind diff S >sh -c "git show %(commit) | delta --paging always --side-by-side"

bind stage  D >sh -c "git diff HEAD -- %(file) | delta --paging always"
bind stage  S >sh -c "git diff HEAD -- %(file) | delta --paging always --side-by-side"
bind status D >sh -c "git diff HEAD -- %(file) | delta --paging always"
bind status S >sh -c "git diff HEAD -- %(file) | delta --paging always --side-by-side"
```

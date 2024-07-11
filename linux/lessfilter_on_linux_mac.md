## Installation of lessfilter

https://github.com/CoeJoder/lessfilter-pygmentize?tab=readme-ov-file

``` bash
# install pipx if needed
sudo apt install pipx

# add pipx-installed binaries to `$PATH` if not already
pipx ensurepath

# install Pygments and GNU awk
pipx install Pygments
sudo apt install gawk
```

## configuration of ~/.zshrc for lessfilter:

``` bash
# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

ZSH_THEME="robbyrussell"
export PYGMENTIZE_STYLE='paraiso-dark'

source $ZSH/oh-my-zsh.sh

# for lessfilter
export LESS='-R'
export LESSOPEN='|~/.lessfilter %s'
export LS_OPTIONS='--color'

plugins=(git macos docker )
git config --global credential.helper store
```

## Copy lessfilter or Generate lessfilter

https://github.com/CoeJoder/lessfilter-pygmentize/blob/master/.lessfilter

``` bash
git clone https://github.com/CoeJoder/lessfilter-pygmentize.git
cd lessfilter-pygmentize/
pipenv install
pipenv run python main.py >/dev/null
```

# pyenv cheatsheet

[pyenv](https://github.com/yyuu/pyenv)

[pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv)

[Command reference](https://github.com/yyuu/pyenv/blob/master/COMMANDS.md)

      $ curl https://pyenv.run | bash
      $ git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv  # if pyenv virtualenv-init not found, clone this repository.


## pyenv
### pyenv install

List available python versions:

        $ pyenv install -l

Install Python 3.10:

        $ PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.10  # enable framework to avoid errors like "ModuleNotFoundError: No module named '_lzma'"
        $ pyenv rehash

### pyenv virtualenv

$ git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

echo 'eval "$(pyenv init -)"' >> ~/.zshrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

### pyenv versions

List installed versions:

        $ pyenv versions

### pyenv local

Sets a local application-specific Python version:

        $ pyenv local 2.7.6  

Unset the local version:

        $ pyenv local --unset

## pyenv-virtualenv
### List existing virtualenvs

        $ pyenv virtualenvs

### Create virtualenv

From current version with name "venv35":

        $ pyenv virtualenv venv35

From version 2.7.10 with name "venv27":

        $ pyenv virtualenv 2.7.10 venv27

### Activate/deactivate

        $ pyenv activate <name>
        $ pyenv deactivate

### Delete existing virtualenv

        $ pyenv uninstall venv27
        
        
## pipenv

### install packages

        $ pipenv install <package_name>

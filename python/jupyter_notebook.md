
## Installation Jupyter
```
$ apt-get install jupyter # or by pip:
$ pip install jupyter  # or pip install jupyter-lab
$ pip install 'python-lsp-server[all]'
$ pip install -U jedi-language-server
$ npm install --save-dev pyright
$ pip install --upgrade notebook==6.4.12
$ jupyter notebook
$ jupyter notebook --ip 0.0.0.0
$ jupyter notebook --allow-root --ip 0.0.0.0 .
```

Reference:
https://jupyter.org/install

If "jupyter notebook" failed with "ModuleNotFoundError: No module named 'jupyter_server.contents' switching to Python kernel", take a look at this page:
https://github.com/microsoft/azuredatastudio/issues/24436

Can update the Python3xx\site-packages\notebook\notebookapp.py to fix the issue, change content from
'jupyter_server.contents.services.managers.ContentsManager'
to
'jupyter_server.services.contents.manager.ContentsManager'

Another option maybe used to specify the version for traitlets (but not work on my m3, python 3.10.6).

## Extensions & Auto complete in jupyter notebook

https://stackoverflow.com/questions/45390326/how-to-get-autocomplete-in-jupyter-notebook-without-using-tab

First, install jupyter contrib nbextensions by running

``` pip install jupyter_contrib_nbextensions ```

Next install js and css file for jupyter by running

``` jupyter contrib nbextension install --user ```

and at the end run,

``` jupyter nbextension enable hinterland/hinterland ```

The output of last command will be

Enabling notebook extension hinterland/hinterland...
      - Validating: OK

If error occurr on install nbextensions: "from notebook.base.handlers import APIHandler, IPythonHandler
ModuleNotFoundError: No module named 'notebook.base'",

Caused by incompatibility of release version between nbextension and jupyter. Then can install an old version of jupyter:

https://stackoverflow.com/questions/76893872/modulenotfounderror-no-module-named-notebook-base-when-installing-nbextension

``` shell
  python -m pip install --upgrade notebook==6.4.12 -i https://pypi.tuna.tsinghua.edu.cn/simple
  pip install -U traitlets==5.9.0
  pip install -U ipython==8.9.0
```


### For Conda installation
Installing nbextension using conda forge channel. Simply run the below command in conda terminal:

``` conda install -c conda-forge jupyter_nbextensions_configurator ```

Next Step enabling the hinterland extension. Run the below command in conda terminal:

``` jupyter nbextension enable hinterland/hinterland ```


## Install Language servers:
https://jupyterlab-lsp.readthedocs.io/en/latest/Language%20Servers.html

Install nvm, node.js and language servers:

``` shell
curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
nvm ls-remote
nvm install v20.10.0
jlpm add --dev  \     bash-language-server \     dockerfile-language-server-nodejs \     pyright \     sql-language-server \     typescript-language-server \     unified-language-server \     vscode-css-languageserver-bin \     vscode-html-languageserver-bin \     vscode-json-languageserver-bin \     yaml-language-server
```


Start by creating a certificate file and a hashed password, as explained in Securing a Jupyter server.
If you don’t already have one, create a config file for the notebook using the following command line:

```shell
$ jupyter server --generate-config 
```

In the ~/.jupyter directory, edit the notebook config file, jupyter_server_config.py. By default, the notebook config file has all fields commented out. The minimum set of configuration options that you should uncomment and edit in jupyter_server_config.py is the following:

```
# Set options for certfile, ip, password, and toggle off # browser auto-opening c.ServerApp.certfile = u'/absolute/path/to/your/certificate/mycert.pem' c.ServerApp.keyfile = u'/absolute/path/to/your/certificate/mykey.key'

# Set ip to '*' to bind on all interfaces (ips) for the public server c.ServerApp.ip = '*' c.ServerApp.password = u'sha1:bcd259ccf...' c.ServerApp.open_browser = False 
# It is a good idea to set a known, fixed port for server access c.ServerApp.port = 9999 
```

You can then start the notebook using the jupyter server command.

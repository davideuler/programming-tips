
## Installation Jupyter
$ apt-get install jupyter
$ pip install jupyter  # or install jupyter by pip
$ pip install 'python-lsp-server[all]'
$ pip install -U jedi-language-server
$ npm install --save-dev pyright
$ jupyter notebook
$ jupyter notebook --ip 0.0.0.0
$ jupyter notebook --allow-root --ip 0.0.0.0 .

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

# Set options for certfile, ip, password, and toggle off # browser auto-opening c.ServerApp.certfile = u'/absolute/path/to/your/certificate/mycert.pem' c.ServerApp.keyfile = u'/absolute/path/to/your/certificate/mykey.key'

# Set ip to '*' to bind on all interfaces (ips) for the public server c.ServerApp.ip = '*' c.ServerApp.password = u'sha1:bcd259ccf...' c.ServerApp.open_browser = False 
# It is a good idea to set a known, fixed port for server access c.ServerApp.port = 9999 


You can then start the notebook using the jupyter server command.

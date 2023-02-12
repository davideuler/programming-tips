Reference:
https://www.vultr.com/docs/how-to-install-node-js--npm-on-debian-11/
https://phoenixnap.com/kb/debian-install-nodejs

## Installing NodeJS with NVM

The Node Version Manager(NVM) is a bash script used to manage multiple active NodeJS versions on the same machine. You can easily switch between different NodeJS versions. Using this method, you will be able to use multiple versions of NodeJS without worrying about compatibility issues.

1.  First, download the installer script from GitHub.
    
    ```
    $ curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
    
    => Downloading nvm as script to '/root/.nvm'
    
    => Appending nvm source string to /root/.bashrc
    
    => Appending bash_completion source string to /root/.bashrc
    ```
    
2.  Run the `source ~/.profile` command to reload the environment variables into your current session.
    
    ```
    $ source ~/.profile
    ```
    
3.  List the available versions of NodeJS.
    
    ```
    $ nvm ls-remote
    ```
    
4.  Once you have decided on the version, run `nvm install <version>` command to download and install it. For example, to install NodeJS 11.6, runs:
    
    ```
    $ nvm install v18.14.0
    
      Downloading and installing node v18.14.0...
      Downloading https://nodejs.org/dist/v18.14.0/node-v18.14.0-linux-x64.tar.xz...
      ################################################################################################################ 100.0%
      Computing checksum with sha256sum
      Checksums matched!
      Now using node v18.14.0 (npm v9.3.1)
      Creating default alias: default -> v18.14.0
    ```
    
5.  The latest version will be used if you don't explicitly specify a version number. You will need to tell NVM which version of NodeJS to use. For example, to use NodeJS 11, run:
    
    ```
    $ nvm use v18.14.0
    
    Now using node v18.14.0 (npm v9.3.1)
    ```
    
6.  Run the `nvm ls` command to list the installed NodeJS versions. NNM will also indicate which version is the default.
    
    ```
     $ nvm ls
    ->     v18.14.0
    default -> v18.14.0
    v11.6.0
    
    v11.7.0
    
    default -> 11.6 (-> v11.6.0)
    ```
    
7.  You can also set a specific version as the default NodeJS version. For example, to set version 11.7 as your default NodeJS version, runs:
    
    ```
    $ nvm alias default 11.7
    
    default -> 11.7 (-> v11.7.0)
    ```
    

## Conclusion

You have installed NodeJS using several methods. At this point, you can use the node command to run your NodeJS application within any of these installed versions. You can also switch between NodeJS versions using NVM.

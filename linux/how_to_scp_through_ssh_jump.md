
https://mperdikeas.github.io/networking.html.files/scp-a-file-through-jump-host.html

## how to scp a file through an intermediate host (a.k.a. jump host)
There's various methods (with or without using an SSH tunnel). More recently I used and settled to method D.

The situation is the following:
A -- ssh --> B -- ssh --> C

* where A is my client machine, 
* B is the jump host and 
* C is the final endpoint of the copy (either source or destination depending on the direction — the other endpoint being A)

### method D - Update (October 2022)
thanks to @moppman for reporting this — I have not had a chance to use this though

A couple of years ago scp gained the ability to use jump hosts in a much more concise and intuitive manner. Using the -J flag, you can now do the following:

```shell
scp -J username@B username@C:/some/path /some/path
```
You can even add more jump hosts seperated by a comma. As scp's manual states, the -J flag is just a shortcut for ssh commands very similar to what I described in the other methods on this page.

### method A

I 've used the following option from the source:

A$ scp -oProxyCommand="ssh -W %h:%p B" thefile C:destination
… and as a matter of fact reversed the copy direction (e.g. I copied from system C to system A). I.e. the incantation I used was:
A$ scp -oProxyCommand = "ssh -W %h:%p username@B" username@C:/some/path/on/macine/C some/path/on/machine/A

### method B

This is the method that I can understand more intuitively.

open an SSH tunnel from A/localmachine to B to C on local port 1234 (or some other unclaimed local port):
``` shell
ssh -L 1234:C:22 username@B
```

Enter password for B.

just bloody copy the file(s) through the local opening of the tunnel (1234) on the localhost:
```shell
scp -P 1234 -pr prj/ username@localhost:/some/remote/path
```

The command copys the project file(s) from the local machine to the remote machine(C).

exit the tunnel you opened on the first step

Be sure to note in the scp invocation above that the uppercase -P flag specifies the port to use whereas the lowercase -p is for preserving permission rights on files.

### method C
Method B has the disadvantage that it requires that you use two shells, one for the tunnel and one for the actual scp. It also requires you to manually set up and tear down the tunnel. Finally you have to guess and reserve a local available port. This method does not suffer from these three problems.

I used the method recommended in this answer without the -o 'Host remote2' part as advised in the comments to this answer.

scp -o 'ProxyCommand ssh username@B nc %h %p' someFile username@C:/some/path
I then improved upon that since modern versions of ssh have netcat-like abilities built-in and do not require nc on the intermediate host as advised in this answer. So I did:

scp -o 'ProxyCommand ssh username@B -W %h:%p' someFile username@C:/some/path
… which also worked — observe that there is now a colon (:) between %h and %p which wasn't there before.
The final improvement was to use sshpass to avoid being prompted (I had setup SSH public key authentication between A and B but was unable to do so between B and C):

sshpass -f password scp -o 'ProxyCommand ssh username@B -W %h:%p' someFile username@C:/some/path

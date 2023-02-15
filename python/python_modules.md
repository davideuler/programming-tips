

## Failed to run file in a submodule 

```
python 
```
ImportError: No module named dirFoo1.foo1



Set your PYTHONPATH environment variable. For example like this PYTHONPATH=.:.. (for *nix family).

Also you can manually add your current directory (src in your case) to pythonpath:

import os
import sys
sys.path.insert(0, os.getcwd())

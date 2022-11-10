
# 1.Update submodule to to a specifiy commit or tag

Use hexsha to specify a commit, or tag to specify a tag.
``` 
[submodule "subprojects/faiss"]
	path = subprojects/faiss
	url = https://github.com/facebookresearch/faiss.git
	hexsha = 0a622d2d78ee691575c50ab62af23147fba453b8 
  ```
  
  https://stackoverflow.com/questions/1777854/how-can-i-specify-a-branch-tag-when-adding-a-git-submodule
  
If you specify a tag, should fetch tags firstly: 
```
git submodule foreach --recursive 'git fetch --tags' 
```

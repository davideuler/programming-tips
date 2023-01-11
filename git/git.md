
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

# 2.discard all uncommitted changes && discard changes on a single file

To discard all uncommited changes:
```
git reset --hard HEAD
git reset --hard <commit id>
```

Use Git reset --hard <commit id> to point the repo to a previous commit.

To discard changes on a single file
```
git checkout -- <file>
```

Also can use "git restore <file>..." to discard changes in working directory
```
git restore <file>...
```

To stash all changes to local temparory storage and restore them later:
```
git stash 
git stash pop
```
Git stash lets you discard changes and save them for later reuse.

Use Git reflog to check commits history.
```
git reflog
```

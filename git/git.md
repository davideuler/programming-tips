
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

## 3.删除一个文件的所有提交记录（一个误上传大文件，或者历史记录中包含敏感信息的配置文件/代码等）

下载 bfg.jar:
https://rtyley.github.io/bfg-repo-cleaner/

切换到 bare 仓库 (git clone --mirror 拉取到的仓库）， 或者本地仓库，删除不要历史记录的文件（如果有最新版本，保留最新版本的文件）：

```
$ java -jar ~/workspace/bfg-1.14.0.jar --delete-files oss_client_with_ak.py SchedulerJob/
$ java -jar ~/workspace/bfg-1.14.0.jar --strip-blobs-bigger-than 100M some-big-repo.git  # for bare repository

# cd SchedulerJob
$ git reflog expire --expire=now --all && git gc --prune=now --aggressive

$ git push --force
```



# Create conda environment

```
conda create -n mlp python=3.10
conda activate mlp
```

# Show conda environment list

```
conda env list
```

or 

```
conda info --envs
```

# Activate environment

conda activate mlp


# Update base Python 

conda activate base
conda install python=3.n

# Using conda and pip to manage dependencies

https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#pip-in-env
https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#setting-environment-variables

https://stackoverflow.com/questions/63381004/best-practice-to-manage-dependencies-between-conda-and-pip

The recommendation in the official documentation for managing a Conda environment that also requires PyPI-sourced or pip-installed local packages is to define all dependencies (both Conda and Pip) in a YAML file. Something like:

env.yaml

```
name: my_env
channels:
 - defaults
dependencies:
 - python=3.8
 - numpy
 - pip
 - pip:
   - some_pypi_only_pkg
   - -e path/to/a/local/pkg
```

# Conda create environment error 

conda_libmamba_solver  
RuntimeError: Unable to read repodata JSON file 'https://repo.anaconda.com/pkgs/main/linux-64'


Config the .condarc:
https://mirror.tuna.tsinghua.edu.cn/help/anaconda/


``` bash
# clean cache
 conda clean -i 

# create new environment
 conda create -n anime-ai-310 python=3.10
```


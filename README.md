# clustering
A clustering experiment


### Packages

Starting with

`conda create --prefix ~/Anaconda3/envs/clustering python=3.7.7`

and

```bash
  conda install -c anaconda dask
  conda install -c anaconda scikit-learn
  conda install -c anaconda matplotlib seaborn
  conda install -c anaconda pytest coverage pytest-cov pylint
  conda install -c anaconda pywin32 jupyterlab nodejs
  conda install -c anaconda python-graphviz
```

Note

* python installs
  * setuptools

* dask installs
  * numpy
  * pandas

* scikit-learn installs
  * scipy
  
* python-graphviz installs
  * graphviz


Exclude

* pywin32
* nodejs
* python-graphviz

from filter.txt

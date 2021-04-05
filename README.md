## Clustering
A clustering experiment

<br>


### Preliminaries

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
  
  # Version 1.3.post1 ... odd
  pip install yellowbrick 
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


### Notes

Time option:

```r
	start <- Sys.time()
	elapsed <- as.integer(difftime(Sys.time(), start, units = "secs")) 
```

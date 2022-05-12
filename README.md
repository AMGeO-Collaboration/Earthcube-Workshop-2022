# AMGeO-Earthcube 2022 Workshop

Welcome! This repository contains various ways of being able to run AMGeO 
for the AMGeO-Earthcube 2022 Workshop

<mark>NOTE:</mark> If you want to generate AMGeO Maps, it is highly recommended to run AMGeO using Docker/VSCode Dev Container

There are 3 exercises for those that don't have something they would like to work on for the workshop:

- Exercise 1: Basic plotting/data manipulation
- Exercise 2: Basic plotting and intermediate data manipulation
- Exercise 3: Intermediate/advanced plotting and advanced data manipulation

There are an array of dates that we have prerun, so you can load on without any generation neeeded.

- 2011-09-26
- 2015-03-17
- 2017-09-07
- 2017-09-08
- 2017-09-09

We have also added some helpful util functions you can use if you want in `util.py`. You can import these into a notebook using

```python
from util import ...
```

## Running AMGeO in Binder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AMGeO-Collaboration/Earthcube-Workshop-2022/HEAD)

If you do not want to run AMGeO locally, you can click the above link to open up a notebook env with AMGeO already setup!

## VS Code Dev container

If you use [VS Code](https://code.visualstudio.com/), there is an extension you can use called [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) that allows for running VS Code in a container environment.

To run this repo in a container environment, follow these steps:

1. clone this repository to your local machine

2. Install the remote conatiners extension

3. Follow [these steps](https://code.visualstudio.com/docs/remote/containers#_quick-start-open-an-existing-folder-in-a-container), and select the directory where this repository is located (which will use this `Dockerfile` to use for your dev env)

## Running with Docker

It is also possible to use Docker to run AMGeO in a container environment.

To do this, 
execute the following commands:

```sh
docker build -t amgeo-earthcube-2022 .
docker run -it --rm -p 8888:8888 amgeo-earthcube-2022 jupyter notebook --ip=0.0.0.0 --port=8888
```

And open `AMGeO-Notebook.ipynb`

## Running AMGeO Locally

<mark>WARNING</mark> only recommended on Linux natively
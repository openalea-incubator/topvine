# Overview

`topvine` is a 3D statistical reconstruction model of grapevine (*Vitis vinifera* L.)
that simulates canopy structure accounting for (cultivar)-(training system) pairs.

# Installation (develop mode)
- Ensure that you have both
  [git](https://git-scm.com/install/) and
  [conda](https://www.anaconda.com/docs/getting-started/miniconda/install/overview)
  installed.
 
- Clone the repo into local machine;
  go to the directory where you would like to have the `topvine` code cloned then type
  (replace `<topvine-parent-directory>` by your directory name):
  ```bash
  cd <topvine-parent-directory>
  git clone git@github.com:openalea-incubator/topvine.git
  conda activate topvine
  ```

- Create then activate the environment:
  ```bash
  conda env create -f environment.yml
  conda activate topvine
  ```

- (for contributors) Install the development dependencies: 
  ```bash
  pip install -r requirements-dev.txt
  ```

- Test your installation
  ```bash
  python -m unittest discover -s test -p "*.py"
  ```

# Run the model with a qt-enabled console
cd example

ipython --gui=qt

%run tutorial.py

main()

_

# Citation

Gaëtan Louarn, Jérémie Lecoeur, Eric Lebon, A Three-dimensional Statistical Reconstruction Model of Grapevine (Vitis vinifera) Simulating Canopy Structure Variability within and between Cultivar/Training System Pairs, Annals of Botany, Volume 101, Issue 8, May 2008, Pages 1167–1184, https://doi.org/10.1093/aob/mcm170

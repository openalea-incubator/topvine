# TopVine

A 3D digital reconstruction model of grapevine simulating canopy structure variability, depending on cultivar and training systems

## Citation

Gaëtan Louarn, Jérémie Lecoeur, Eric Lebon, A Three-dimensional Statistical Reconstruction Model of Grapevine (Vitis vinifera) Simulating Canopy Structure Variability within and between Cultivar/Training System Pairs, Annals of Botany, Volume 101, Issue 8, May 2008, Pages 1167–1184, https://doi.org/10.1093/aob/mcm170

## Instalation (develop mode)

### install conda (miniconda)

Follow instruction at https://docs.conda.io/en/latest/miniconda.html


### Install dependency with conda
conda create -n topvine -c conda-forge -c openalea3 python=3.8 pytest pandas numba openalea.plantgl statsmodels seaborn


conda activate topvine


### Download topvine and install
git clone https://github.com/openalea-incubator/topvine.git

cd topvine

python setup.py develop

### Test your installation
cd test; pytest

### Run the model with a qt-enabled console
cd example

ipython --gui=qt

%run tutorial.py

main()

_


# TopVine

A 3D vine generator 

## Instalation (develop mode)

### install conda (miniconda)

Follow instruction at https://docs.conda.io/en/latest/miniconda.html


### Install dependency with conda
conda create -n topvine -c conda-forge -c openalea3 python=3.8 openalea.plantgl
conda install -c conda-forge pytest six
conda activate topvine

### Load phenomenal and install
git clone https://github.com/openalea-incubator/topvine.git
cd topvine
python setup.py develop

### Test your installation
cd test; pytest
# TopVine

A 3D vine generator 

## Instalation (develop mode)

### install conda (miniconda)

Follow instruction at https://docs.conda.io/en/latest/miniconda.html


### Install dependency with conda
conda create -n topvine -c conda-forge -c openalea3 python=3.8 pytest openalea.plantgl


conda activate topvine


### Download topvine and install
git clone https://github.com/openalea-incubator/topvine.git

cd topvine

python setup.py develop

### Test your installation
cd test; pytest

### Run the model with a qt-enabled console
ipython --gui=qt

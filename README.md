Selected Topics in Audio Signal Processing - Exercises
======================================================

- [static web pages (using nbviewer)](http://nbviewer.ipython.org/github/spatialaudio/selected-topics-in-audio-signal-processing-exercises/blob/master/index.ipynb)
- [interactive web based (using mybinder)](https://mybinder.org/v2/gh/spatialaudio/selected-topics-in-audio-signal-processing-exercises/HEAD?filepath=index.ipynb)

- for local usage create an conda environment (`mystiasp`), clone the git repository
and start jupyter notebook or jupyter lab
  - created with `conda 4.9.2`
  - currently we rely on some older matplotlib version
  - `conda create -n mystiasp python=3.7.8 pip=20.2.4 numpy=1.19.4 scipy=1.5.3 matplotlib=3.1.3 jupyter=1.0.0 notebook=6.1.5 jupyterlab=2.2.9 pydocstyle=5.1.1 pycodestyle=2.6.0 autopep8=1.5.4 flake8=3.8.4 ipykernel=5.3.4 nb_conda=2.2.1 jupyter_nbextensions_configurator=0.4.1 jupyter_contrib_nbextensions=0.5.1`
  - `conda activate mystiasp`
  - we need to install pip packages since conda does not have them:
  - `pip install soundfile==0.10.3.post1`
  - `pip install sounddevice==0.4.1`
  - `python3 -m pip install sfs==0.5.0 --user`
  - make sure that the kernel is accesible for the notebooks:
  - `python -m ipykernel install --user --name mystiasp --display-name "mystiasp"`
  - now clone the repo:
  - `cd git` or whatever is a good root folder
  - `git clone https://github.com/spatialaudio/selected-topics-in-audio-signal-processing-exercises.git`
  - `cd selected-topics-in-audio-signal-processing-exercises/`
  - `jupyter notebook index.ipynb` or `jupyter lab index.ipynb`
  - make sure that `mystiasp` kernel is used for the notebooks
  - have fun with the playgrounds

Copyright
---------

The authors waive copyright and related rights in the work through the
[CC0 1.0 Universal public domain dedication](http://creativecommons.org/publicdomain/zero/1.0/).

This is supposed to be an [Open Educational Resource](https://en.wikipedia.org/wiki/Open_educational_resources) (OER).

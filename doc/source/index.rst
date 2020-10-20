rp2Paths's Documentation
==========================

Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Introduction
############

.. _rp2Paths: https://github.com/brsynth/rp2paths

Welcome to rp2Paths's documentation. This project wraps the rp2Paths_ into a docker that may be called locally. 

First build the docker using the following command:

.. code-block:: bash

   docker build -t brsynth/rp2paths-standalone .

To call the docker locally you can use the following command:

.. code-block:: bash

   python run.py -rp_pathways test/rp_pathways.csv -rp2paths_pathways test/out_paths.csv -rp2paths_compounds test/out_compounds.csv

API
###

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. currentmodule:: rpTool

.. autoclass:: run_rp2paths
    :show-inheritance:
    :members:
    :inherited-members:

.. currentmodule:: run

.. autoclass:: main
    :show-inheritance:
    :members:
    :inherited-members:


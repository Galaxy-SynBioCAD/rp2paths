rp2Paths's Redis Documentation
================================

Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Introduction
############

.. _rp2Paths: https://github.com/brsynth/rp2paths

Welcome to rp2Paths's redis documentation. This project wraps the rp2Paths_ into a Redis and Flask docker that may be called locally. 

The Redis service is used as a queuing service that allows for a number of users to wait for the x number of rp2Paths instances. This is controlled by modifying the supervisor.conf file at the following line: numprocs=2.

The limit of RAM usage can also be defined by changing the following line of rpTool.py: MAX_VIRTUAL_MEMORY = 30000*1024*1024 # 30 GB. 

In both cases the docker must be rebuild if changed, using the following command:

.. code-block:: bash

   docker build -t brsynth/rp2paths-redis .

The service must be ran, and can be done using the following command:

.. code-block:: bash

   docker run -p 8887:8888 brsynth/rp2paths-redis

Where the public port number can be changed by the first instance of the 8888 number above. 

To call the rest service, the easiest way is to use the galaxy/code/tool_rp2paths.py file in the following fashion:

.. code-block:: bash

   python tool_rp2paths.py -sinkfile test/sink.csv -sourcefile test/source.csv -rulesfile test/rules.tar -rulesfile_format tar -max_steps 3 -scope_csv test_scope.csv

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

.. currentmodule:: rpToolServe

.. autoclass:: RestQuery
    :show-inheritance:
    :members:
    :inherited-members:


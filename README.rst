Digital Ocean API Python Wrapper
================================

Inspired by [dop](https://github.com/ahmontero/dop).

Installation
============

.. code-block:: bash
    
    # pip install dopy

Getting Started
===============

To interact with Digital Ocean, you first need .. a digital ocean account with 
valid API keys.

Keys can be set either as Env variables, or within the code.

.. code-block:: bash
    
    # export DO_CLIENT_ID='client_id'
    # export DO_API_KEY='long_api_key'

.. code-block:: pycon

    >>> from dopy.manager import DoManager
    >>> do = DoManager('client_id', 'long_api_key')

Methods
=======

The methods of the DoManager are self explanatory; ex.

.. code-block:: pycon

    >>> do.all_active_droplets()
    >>> do.show_droplet('12345')
    >>> do.destroy_droplet('12345')
    >>> do.all_regions()
    >>> do.all_images()
    >>> do.all_ssh_keys()
    >>> do.sizes()
    >>> do.all_domains()
    >>> do.new_droplet('new_droplet', 66, 1601, 1)

TODO
====

See github issue list - post if any needed

https://github.com/devo-ps/dopy/issues
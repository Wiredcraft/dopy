DigitalOcean API Python Client
================================

Inspired by [dop](https://github.com/ahmontero/dop).

Installation
============

.. code-block:: bash

    # pip install dopy

Getting Started
===============

To interact with DigitalOcean, first you will need a DigitalOcean account with 
a valid API keys.

Keys can be set either as Env variables, or within the code.

Supports DigitalOcean API v2.

.. code-block:: bash

    # export DO_API_TOKEN='api_token'

.. code-block:: pycon

    >>> from dopy.manager import DoManager
    >>> do = DoManager(api_token='api_token')


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
    >>> do.show_domain('example.com')
    >>> do.new_droplet('new_droplet', '512mb', 'lamp', 'ams2')


Methods for Floating IPs are:

.. code-block:: pycon

    >>> do.all_floating_ips()
    >>> do.new_floating_ip(droplet_id, region)
    >>> do.destroy_floating_ip(ip_addr)
    >>> do.assign_floating_ip(ip_addr)
    >>> do.unassign_floating_ip(ip_addr)
    >>> do.list_floating_ip_actions(ip_addr)
    >>> do.get_floating_ip_action(ip_addr, action_id)

Tests
====

[Responses](https://github.com/getsentry/responses) and [Nose](https://github.com/nose-devs/nose) are needed for testing.

Run tests with command: nosetests

The idea is that use Responses library to mock requests.
The response requests library get are fake and
defined in text files in test_samples folder.

TODO
====

See github issue list - post if any needed

https://github.com/devo-ps/dopy/issues

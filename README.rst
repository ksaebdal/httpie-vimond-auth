httpie-api-auth
===============

Vimond API auth plugin for `HTTPie <https://httpie.org/>`_.

Installation
------------

.. code-block:: bash

    $ pip install httpie-vimond-auth

You should now see ``vimond`` under ``--auth-type`` in ``$ http --help`` output.

Usage
-----

.. code-block:: bash

    $ http --auth-type=vimond --auth='user:secret' my-api-host.net

Dev setup
---------

.. code-block:: bash

    $ virtualenv --no-site-packages env
    $ source env/bin/activate
    $ pip install -r requirements.dev.txt
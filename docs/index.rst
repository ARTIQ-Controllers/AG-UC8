Welcome to AGUC8's documentation!
=================================

General Instructions
--------------------

This software provides ARTIQ support for the Newport Agilis AGUC8 piezo motor controllers.

.. note::
    The software is configured for RS232 communication. If using some other form of communication, change the baud rate setting in :class:`agPort` .

Installation
++++++++++++

Install the AGUC8 package to your environment using pip with git::

    $ python -m pip install git+https://github.com/ARTIQ-Controllers/AGUC8


AG-UC8 Controller Usage Example
+++++++++++++++++++++++++++++++

First, run the AGUC8 controller::

    $ aqctl_AGUC8 --bind ::1 -p 3251 -s COM1

.. note::
    Anything compatible with `serial_for_url <https://pyserial.readthedocs.io/en/latest/pyserial_api.html#serial.serial_for_url>`_
    can be given as a serial port in ``-s`` argument.

    For instance, if you want to specify a host IP address and its port:

    ``-s "socket://<host>:<port>"``.
    for instance:

    ``-d "socket://192.168.1.220:10001"``

Then, send commands via the ``artiq_rpctool`` utility::

    $ sipyco_rpctool ::1 3251 list-targets
    Target(s):   AGUC8
    $ sipyco_rpctool ::1 3251 call move(15,15) # will move 15 steps in the positive direction along each axis
    $ sipyco_rpctool ::1 3251 call move(-15,-15) # will move 15 steps in the negative direction along each axis
    $ sipyco_rpctool ::1 3251 call moveUpUp() # will move to the upper limit of each axis, if device has a limit switch
    $ sipyco_rpctool ::1 3251 call goToZero # will go to zero position
    $ sipyco_rpctool ::1 3251 call close # close the device

API
---

.. automodule:: AGUC8.driver
    :members:

.. automodule:: AGUC8.agPort
    :members:

ARTIQ Controller
----------------

.. argparse::
    :ref: AGUC8.aqctl_AGUC8.get_argparser
    :prog: aqctl_AGUC8

Acknowledgements
----------------

The driver files for the AGUC8 controller were taken from: `https://github.com/dschick/pyagilis <https://github.com/dschick/pyagilis>`_ .

This was adapted from an original respository: `https://github.com/elandini/pyagilis <https://github.com/elandini/pyagilis>`_ .

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

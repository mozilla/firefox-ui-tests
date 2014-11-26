.. py:currentmodule:: greenlight.lib

Firefox Puppeteer
=================

Firefox Puppeteer is a library built on top of the `Marionette python client`_.
It aims to make automation of Firefox's browser UI simpler. It does **not**
make sense to use Firefox Puppeteer if:

* You are manipulating something other than Firefox (like Firefox OS)
* You are only manipulating elements in content scope (like a webpage)

Roughly speaking, Firefox Puppeteer provides a library to manipulate each
visual section of Firefox's browser UI. For example, there is one library for
the tab strip, another for the menu panel, a third for the navigation bar, etc.


Installation
------------

Currently Firefox Puppeteer lives in the `firefox-greenlight-tests`_ repository
but there are plans to move it alongside the `Marionette python client`_.

.. _Marionette python client: http://marionette-client.readthedocs.org/en/latest/
.. _firefox-greenlight-tests: https://github.com/mozilla/firefox-greenlight-tests/tree/master/greenlight/lib

Libraries
---------

The following libraries are currently implemented. More will be added in the
future.

.. autoclass:: Puppeteer
   :members:

.. toctree::
   :hidden:

   windows
   ui/menu
   ui/navbar
   ui/tabs
   api/keys
   api/l10n
   api/prefs


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


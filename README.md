firefox-ui-tests
================

[![Build Status](https://travis-ci.org/mozilla/firefox-ui-tests.svg?branch=master)](https://travis-ci.org/mozilla/firefox-ui-tests)

Installation
------------

First make sure you have [pip](http://pip.readthedocs.org/en/latest/installing.html) installed.

It is recommended that [virtualenv](http://virtualenv.readthedocs.org/en/latest/installation.html) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) be used in conjunction with firefox-ui-tests. Start by installing these.

Then:

    git clone https://github.com/mozilla/firefox-ui-tests.git
    cd firefox-ui-tests
    python setup.py develop

If you do not have installed virtualenv and virtualenvwrapper you can also use the create_venv.py script to let it automatically create a virtual environmnet with all the packages installed:

    ./create_venv.py venv
    source venv/bin/activate

Usage
-----

To run all tests:

    firefox-ui-tests --binary <path to firefox binary>

To run the update tests:

    firefox-ui-update --binary <path to firefox binary>

To run a specific test or directory of tests:

    firefox-ui-tests --binary <path to firefox binary> <path to test or directory>

For more options run:

    firefox-ui-tests --help

Documentation
-------------

Documentation for the puppeteer libraries are hosted on [readthedocs](http://firefox-puppeteer.readthedocs.org/en/latest/).
